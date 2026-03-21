"""
Collective Alibi — Demo Data Seeder
Seeds 200 workers: 170 genuine (storm conditions) + 30 fraudulent (indoor)
Run: python seed_demo.py
"""
import redis
import json
import random
import time
from faker import Faker

fake = Faker('en_IN')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

ZONES = [
    {"name": "Andheri, Mumbai", "lat": 19.1136, "lng": 72.8697, "risk": 5},
    {"name": "Kurla, Mumbai",   "lat": 19.0726, "lng": 72.8845, "risk": 8},
    {"name": "Bandra, Mumbai",  "lat": 19.0596, "lng": 72.8295, "risk": 3},
]
PLATFORMS = ["Zomato", "Swiggy", "Zepto", "Blinkit"]
PLANS = ["basic", "standard", "pro"]

def make_genuine_beacon(worker_id, zone):
    return {
        "worker_id": worker_id,
        "zone_hash": zone["name"].replace(" ", "_").lower(),
        "lat": zone["lat"] + random.uniform(-0.01, 0.01),
        "lng": zone["lng"] + random.uniform(-0.01, 0.01),
        "barometer_delta": random.uniform(-12, -5),   # storm = dropping pressure
        "imu_variance": random.uniform(0.25, 0.55),   # outdoor motion
        "bt_device_count": random.randint(1, 4),       # sparse street
        "cell_rssi": random.randint(-95, -75),         # degraded signal
        "timestamp": time.time(),
    }

def make_fraud_beacon(worker_id, zone):
    return {
        "worker_id": worker_id,
        "zone_hash": zone["name"].replace(" ", "_").lower(),
        "lat": zone["lat"] + random.uniform(-0.05, 0.05),  # far from zone
        "lng": zone["lng"] + random.uniform(-0.05, 0.05),
        "barometer_delta": random.uniform(-0.5, 0.5),   # indoor = stable pressure
        "imu_variance": random.uniform(0.01, 0.05),     # very still (sitting)
        "bt_device_count": random.randint(6, 15),        # indoor apartment = many devices
        "cell_rssi": random.randint(-60, -40),           # strong indoor signal
        "timestamp": time.time(),
    }

print("Seeding 200 workers...")
for i in range(200):
    is_fraud = i >= 170
    zone = random.choice(ZONES)
    worker_id = f"worker_demo_{i:03d}"

    worker = {
        "id": worker_id,
        "name": fake.name(),
        "phone": fake.phone_number(),
        "upi_id": f"{fake.first_name().lower()}@gpay",
        "platform": random.choice(PLATFORMS),
        "zone": zone["name"],
        "avg_daily_earning": random.uniform(600, 1400),
        "is_fraud_seed": is_fraud,
        "created_at": "2026-01-15T10:00:00",
        "claim_count": 0,
    }
    r.set(f"worker:{worker_id}", json.dumps(worker))

    plan = random.choice(PLANS)
    plans_data = {"basic": (29,400,2), "standard": (49,600,3), "pro": (79,900,4)}
    wp, dp, md = plans_data[plan]
    policy = {
        "policy_id": f"pol_demo_{i:03d}",
        "worker_id": worker_id, "plan": plan,
        "weekly_premium": wp, "daily_payout": dp,
        "max_days": md, "status": "active",
    }
    r.set(f"policy:{worker_id}", json.dumps(policy))

    beacon = make_fraud_beacon(worker_id, zone) if is_fraud else make_genuine_beacon(worker_id, zone)
    r.setex(f"beacon:{worker_id}", 120, json.dumps(beacon))
    r.geoadd("worker_locations", [beacon["lng"], beacon["lat"], worker_id])

    if (i + 1) % 50 == 0:
        print(f"  {i+1}/200 workers seeded...")

print(f"\nDone! Seeded:")
print(f"  170 genuine workers (storm-condition sensor readings)")
print(f"  30  fraudulent workers (indoor sensor readings)")
print(f"\nRun the fraud simulation to see them get caught.")
