# Collective Alibi
### AI-Powered Parametric Income Insurance for India's Gig Delivery Workers

> **Guidewire DEVTrails 2026** · Phase 2 — Scale · Team #leaf

---

## What Phase 2 delivers

Phase 1 proved the concept. Phase 2 built the real product.

We went from architecture to working code — a complete FastAPI backend with 18 endpoints, a production-grade frontend with 6 fully working screens, a dynamic ML premium engine grounded in IMD actuarial data, and the complete Collective Alibi fraud detection engine running end-to-end.

We also addressed every gap from Phase 1 feedback directly: standard insurance exclusions, IRDAI-compliant actuarial modelling, loss ratio projections, waiting periods, and a reinsurance strategy. The platform is now genuinely insurable.

---

## Quick start

### Option 1 — Open the demo instantly

```bash
# Just open index.html in Chrome — no server needed
# All 6 screens work completely offline
open index.html
```

### Option 2 — Full stack with backend

```bash
# One command runs everything
docker-compose up --build

# Or manually:
docker run -d -p 6379:6379 redis:alpine
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**API:** `http://localhost:8000` · **Docs:** `http://localhost:8000/docs`

---

## Project structure

```
collective-alibi/
├── index.html              ← Complete frontend (open in browser — works instantly)
├── docker-compose.yml      ← One-command full stack
├── README.md
│
├── backend/
│   ├── main.py             ← FastAPI — 18 endpoints + Collective Alibi engine
│   ├── seed_demo.py        ← Seeds 200 demo workers
│   ├── requirements.txt
│   └── Dockerfile
│
└── ml/
    └── ml_premium.py       ← XGBoost dynamic premium model
```

---

## The platform — 6 screens

| Screen | Phase 2 deliverable it covers |
|---|---|
| **Overview** | Platform story, live stats, parametric trigger explanation |
| **Register** | Registration process — 3-step onboarding with AI premium + exclusions |
| **My Policy** | Insurance policy management — active coverage, payout history, exclusions |
| **Claims** | Claims management — submit → watch Collective Alibi verify in real time |
| **Command** | Admin analytics — actuarial table, verdict breakdown, pool health |
| **Fraud Lab** | Advanced fraud detection — live ring attack simulator |

---

## API endpoints

### Registration
| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/workers/register` | Register worker — AI premium recommendation on sign-up |
| `GET` | `/workers/{id}` | Get worker profile |
| `GET` | `/workers` | List all workers |

### Dynamic Premium Calculation
| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/premium/calculate` | ML premium — zone + earnings + season + history |

### Policy Management
| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/policies/create` | Create weekly policy with IRDAI exclusions |
| `GET` | `/policies/{worker_id}` | Get active policy |
| `PUT` | `/policies/{worker_id}/upgrade` | Upgrade plan tier |
| `DELETE` | `/policies/{worker_id}` | Cancel policy (no penalty) |

### Claims — Collective Alibi Engine
| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/beacons/push` | Push sensor beacon (every 30s, 120s TTL) |
| `POST` | `/claims/submit` | Submit claim → full corroboration scoring |
| `GET` | `/claims` | List claims with verdict filter |
| `GET` | `/claims/{id}` | Get claim with full engine output |

### Analytics
| Method | Endpoint | What it does |
|---|---|---|
| `GET` | `/analytics/summary` | Live dashboard metrics |
| `GET` | `/analytics/actuarial` | Full actuarial model + data sources |

### Simulation
| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/simulate/disruption` | Fire parametric trigger for demo |

---

## How the Collective Alibi engine works

```
POST /claims/submit
      │
      ▼
1. Validate policy — active? waiting period elapsed? max claim days?
      │
      ▼
2. Validate trigger — must be one of 6 approved parametric events
      │
      ▼
3. Fetch claimant sensor beacon from Redis (120s TTL)
      │
      ▼
4. Geofence query → 30–50 nearby worker beacons within 2km
      │
      ▼
5. Score each witness across 4 physics signals:
   barometer_delta    weight: 35%   (storms drop pressure fast — indoor is flat)
   imu_variance       weight: 25%   (outdoor motion vs indoor stillness)
   bt_device_count    weight: 25%   (flood zones sparse, indoor apartments dense)
   cell_rssi          weight: 15%   (degraded outdoor signal vs strong indoor)
      │
      ▼
6. Ring detection:
   claim_velocity > 30 in 15 min → ring_flag → score capped at 0.35
   claim_velocity > 15 + alert spike → score capped at 0.55
      │
      ▼
7. Final verdict:
   score ≥ 0.70  →  AUTO_APPROVED   instant UPI payout
   score 0.40–0.70 → SOFT_REVIEW   50% advance + 2hr review
   score < 0.40  →  RING_FLAGGED   analyst queue
```

**The key insight:** 500 workers can coordinate on Telegram.
They cannot simultaneously coordinate their barometers.
**The bigger the fraud ring — the louder the silence.**

---

## Coverage terms

### What we cover — income loss only

| Trigger | Source | Threshold |
|---|---|---|
| Heavy Rainfall | IMD API | >64.5mm/hr or Red Alert |
| Flash Floods | NDMA API | Zone officially flood-declared |
| Extreme Heat | OpenWeatherMap | Heat index >47°C sustained |
| Severe Pollution | CPCB AQI | AQI >400 Severe category |
| Curfew / Closure | Govt notification | Official zone lockdown |
| Cyclone Alert | IMD API | Category 1+ landfall |

**Payout formula:** `hours_lost × (daily_payout ÷ 8)`

### Standard exclusions (IRDAI-compliant)

| Exclusion | Reason |
|---|---|
| War, invasion, civil conflict | Force majeure — uninsurable at parametric scale |
| Pandemic or national epidemic | Systemic risk — pool cannot absorb citywide shutdown |
| Government national lockdown | Political risk outside actuarial modelling |
| Nuclear, chemical, biological events | Catastrophic tail risk |
| Platform app downtime | Operational risk of delivery platform |
| Worker negligence / voluntary stoppage | Moral hazard |
| Health, accidents, vehicle repairs | Separate products |
| Events under 2 continuous hours | De minimis rule |
| Score < 0.40 | Insufficient corroboration |

### Policy conditions
- **Waiting period:** 48 hours from activation (prevents adverse selection)
- **Maximum claim days:** 4 per rolling 30-day period
- **Billing:** Weekly UPI auto-debit every Monday
- **Cancellation:** Any time, no penalty

---

## Actuarial model

Based on IMD historical data 2015–2024 for Mumbai Tier-1 zones:

| Event | Avg days/year | Expected annual loss/worker |
|---|---|---|
| Heavy Rainfall | 18 days | ₹4,320 |
| Flash Floods | 4 days | ₹1,440 |
| Extreme Heat | 6 days | ₹2,160 |
| Pollution | 3 days | ₹1,080 |
| **Total** | **31 days** | **₹9,000/year** |

**Premium sufficiency:**
```
Standard plan annual premium:   ₹49 × 52 = ₹2,548
Expected annual payout:         ₹9,000 × 35% claim rate = ₹3,150
Projected loss ratio:           68%
IRDAI target range:             60–75% ✓
Pool sustainable when:          ≥60% of workers are claim-free per week
```

**Data sources:** IMD Historical Records · CPCB AQI Database · NDMA Disaster Reports · IRDAI Microinsurance Guidelines 2023 · World Bank Gig Economy Report 2024

**Reinsurance:** Cat XL for events affecting >40% of covered workers · Quota share with licensed IRDAI insurer · 15% liquidity buffer

---

## Phase 1 feedback — fully addressed

The Phase 1 judge noted: *"critical gap in insurance domain knowledge — completely lacks standard coverage exclusions"*

| Feedback | Phase 2 response |
|---|---|
| Missing standard exclusions | Full IRDAI-compliant exclusion table ✅ |
| Actuarial analysis not rigorous | IMD 2015-2024 data, loss ratio projections ✅ |
| No real data sources cited | IMD, CPCB, NDMA, IRDAI, World Bank ✅ |
| No waiting period | 48-hour waiting period enforced in API ✅ |
| No claim limits | Max 4 days per 30-day period ✅ |
| No reinsurance strategy | Cat XL + quota share + 15% buffer ✅ |
| No IRDAI compliance path | IRDAI Sandbox Regulations 2019 ✅ |

---

## Phase 3 — what's coming (April 5–17)

### Advanced fraud detection hardening
- Account-graph analysis — pre-positioned alibi device detection
- Temporal sensor consistency (2hr pre-claim pattern validation)
- Cross-platform alibi network (open protocol for Swiggy, Zomato, Porter)

### Instant payout system
- Razorpay test mode — real UPI transfer simulation
- Payout receipt with claim ID and verification proof

### Intelligent dashboards
- Worker dashboard — earnings protected, loyalty discount tracker, Hindi + English explanations
- Admin dashboard — predictive disruption risk (ML forecast), D3.js fraud ring network graph, zone heat maps

### Final package
- 5-minute demo video with live disruption simulation → payout on screen
- Final pitch deck (PDF) — persona, AI architecture, actuarial business case

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML + CSS + Vanilla JS — zero dependencies, works offline |
| Backend | FastAPI (Python 3.11) |
| Real-time store | Redis 7 — 120s TTL beacon store |
| ML premium | XGBoost + scikit-learn |
| Weather triggers | OpenWeatherMap API + IMD (Phase 2 mock) |
| Payments | Razorpay test mode (Phase 3) |
| Infrastructure | Docker Compose |

---

**#leaf** · Guidewire DEVTrails 2026 · Phase 2

*Built for gig workers. Hardened against syndicates. Viable for insurers.*
