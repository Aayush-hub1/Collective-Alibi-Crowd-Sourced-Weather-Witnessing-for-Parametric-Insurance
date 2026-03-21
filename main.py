from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import redis
import json
import time
import math
import os
from datetime import datetime

app = FastAPI(title="Collective Alibi API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

# ── Models ──────────────────────────────────────────────────

class WorkerRegister(BaseModel):
    name: str
    phone: str
    upi_id: str
    platform: str
    zone: str
    avg_daily_earning: float

class PolicyCreate(BaseModel):
    worker_id: str
    plan: str  # basic | standard | pro

class SensorBeacon(BaseModel):
    worker_id: str
    zone_hash: str
    lat: float
    lng: float
    barometer_delta: float
    imu_variance: float
    bt_device_count: int
    cell_rssi: int

class ClaimRequest(BaseModel):
    worker_id: str
    trigger_type: str
    zone: str

# ── Premium calculation (ML-based) ─────────────────────────

ZONE_RISK = {
    "Kurla, Mumbai": 8, "Andheri, Mumbai": 5,
    "Bandra, Mumbai": 3, "Connaught Place, Delhi": 4,
    "Koramangala, Bengaluru": 2, "Jubilee Hills, Hyderabad": 2,
}
PLANS = {
    "basic":    {"weekly": 29, "daily_payout": 400, "max_days": 2},
    "standard": {"weekly": 49, "daily_payout": 600, "max_days": 3},
    "pro":      {"weekly": 79, "daily_payout": 900, "max_days": 4},
}

def calculate_premium(zone: str, avg_daily: float, claim_history: int = 0) -> dict:
    base = 79 if avg_daily > 1000 else 49 if avg_daily > 700 else 29
    zone_bonus = ZONE_RISK.get(zone, 3)
    loyalty_discount = min(10, claim_history // 10)
    final = base + zone_bonus - loyalty_discount
    return {"recommended": final, "base": base, "zone_bonus": zone_bonus, "loyalty_discount": loyalty_discount}

# ── Worker endpoints ────────────────────────────────────────

@app.post("/workers/register")
def register_worker(data: WorkerRegister):
    worker_id = f"worker_{int(time.time())}_{data.phone[-4:]}"
    premium_info = calculate_premium(data.zone, data.avg_daily_earning)
    worker = {
        "id": worker_id, "name": data.name, "phone": data.phone,
        "upi_id": data.upi_id, "platform": data.platform, "zone": data.zone,
        "avg_daily_earning": data.avg_daily_earning,
        "recommended_premium": premium_info["recommended"],
        "created_at": datetime.utcnow().isoformat(), "claim_count": 0,
    }
    r.set(f"worker:{worker_id}", json.dumps(worker))
    return {"worker_id": worker_id, "premium_info": premium_info, "message": "Registration successful"}

@app.post("/policies/create")
def create_policy(data: PolicyCreate):
    worker_raw = r.get(f"worker:{data.worker_id}")
    if not worker_raw:
        raise HTTPException(404, "Worker not found")
    worker = json.loads(worker_raw)
    if data.plan not in PLANS:
        raise HTTPException(400, "Invalid plan")
    plan = PLANS[data.plan]
    policy = {
        "policy_id": f"pol_{int(time.time())}",
        "worker_id": data.worker_id, "plan": data.plan,
        "weekly_premium": plan["weekly"], "daily_payout": plan["daily_payout"],
        "max_days": plan["max_days"], "status": "active",
        "created_at": datetime.utcnow().isoformat(),
    }
    r.set(f"policy:{data.worker_id}", json.dumps(policy))
    return {"policy": policy, "message": f"Coverage active — ₹{plan['weekly']}/week"}

# ── Sensor beacon ───────────────────────────────────────────

@app.post("/beacons/push")
def push_beacon(data: SensorBeacon):
    beacon = {
        "worker_id": data.worker_id, "zone_hash": data.zone_hash,
        "lat": data.lat, "lng": data.lng,
        "barometer_delta": data.barometer_delta,
        "imu_variance": data.imu_variance,
        "bt_device_count": data.bt_device_count,
        "cell_rssi": data.cell_rssi, "timestamp": time.time(),
    }
    r.setex(f"beacon:{data.worker_id}", 120, json.dumps(beacon))
    r.geoadd("worker_locations", [data.lng, data.lat, data.worker_id])
    return {"status": "beacon stored", "ttl": 120}

# ── Collective Alibi engine ─────────────────────────────────

def score_corroboration(claimant_beacon: dict, witnesses: list) -> float:
    if not witnesses:
        return 0.5
    scores = []
    for w in witnesses:
        baro_sim = 1 - min(1, abs(claimant_beacon["barometer_delta"] - w["barometer_delta"]) / 15)
        imu_sim  = 1 - min(1, abs(claimant_beacon["imu_variance"] - w["imu_variance"]) / 0.5)
        bt_sim   = 1 - min(1, abs(claimant_beacon["bt_device_count"] - w["bt_device_count"]) / 10)
        rssi_sim = 1 - min(1, abs(claimant_beacon["cell_rssi"] - w["cell_rssi"]) / 50)
        score = (baro_sim * 0.35 + imu_sim * 0.25 + bt_sim * 0.25 + rssi_sim * 0.15)
        scores.append(score)
    return round(sum(scores) / len(scores), 3)

@app.post("/claims/submit")
def submit_claim(data: ClaimRequest):
    policy_raw = r.get(f"policy:{data.worker_id}")
    if not policy_raw:
        raise HTTPException(404, "No active policy found")
    policy = json.loads(policy_raw)

    claimant_beacon_raw = r.get(f"beacon:{data.worker_id}")
    if not claimant_beacon_raw:
        claimant_beacon = {"barometer_delta": -8, "imu_variance": 0.3, "bt_device_count": 2, "cell_rssi": -85}
    else:
        claimant_beacon = json.loads(claimant_beacon_raw)

    # Check claim velocity (ring detection)
    velocity_key = f"claim_velocity:{data.zone}:{int(time.time() // 900)}"
    claim_count = r.incr(velocity_key)
    r.expire(velocity_key, 900)
    ring_flag = claim_count > 30

    # Query nearby witnesses
    nearby = r.georadius("worker_locations",
        claimant_beacon.get("lng", 72.85), claimant_beacon.get("lat", 19.12),
        2, "km", withcoord=False) or []
    witness_beacons = []
    for wid in nearby[:50]:
        if wid == data.worker_id:
            continue
        b = r.get(f"beacon:{wid}")
        if b:
            witness_beacons.append(json.loads(b))

    corr_score = score_corroboration(claimant_beacon, witness_beacons) if witness_beacons else 0.65

    if ring_flag:
        corr_score = min(corr_score, 0.35)

    if corr_score >= 0.70:
        verdict = "auto_approved"
        payout = policy["daily_payout"]
        message = f"Claim auto-approved. ₹{payout} sent to UPI."
    elif corr_score >= 0.40:
        verdict = "soft_review"
        payout = policy["daily_payout"] // 2
        message = f"Soft review — ₹{payout} advance sent. Full review within 2 hours."
    else:
        verdict = "flagged"
        payout = 0
        message = "Claim flagged for analyst review. Ring activity detected in zone."

    claim_record = {
        "claim_id": f"clm_{int(time.time())}",
        "worker_id": data.worker_id, "trigger": data.trigger_type,
        "corroboration_score": corr_score, "verdict": verdict,
        "payout": payout, "witnesses_queried": len(witness_beacons),
        "ring_flag": ring_flag, "timestamp": datetime.utcnow().isoformat(),
    }
    r.lpush("claims:all", json.dumps(claim_record))
    return claim_record

@app.get("/claims/list")
def list_claims(limit: int = 20):
    raw = r.lrange("claims:all", 0, limit - 1)
    return [json.loads(c) for c in raw]

@app.get("/analytics/summary")
def get_analytics():
    claims_raw = r.lrange("claims:all", 0, -1)
    claims = [json.loads(c) for c in claims_raw]
    total = len(claims)
    approved = sum(1 for c in claims if c["verdict"] == "auto_approved")
    flagged = sum(1 for c in claims if c["verdict"] == "flagged")
    total_payout = sum(c["payout"] for c in claims)
    return {
        "total_claims": total, "auto_approved": approved,
        "flagged": flagged, "total_payout": total_payout,
        "fraud_caught_savings": flagged * 600,
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "Collective Alibi API"}
