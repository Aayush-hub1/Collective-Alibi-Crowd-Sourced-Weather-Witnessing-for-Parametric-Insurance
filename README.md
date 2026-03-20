# Collective Alibi
### Crowd-Sourced Weather Witnessing for Parametric Insurance

> **DEVTrails 2026** · Team #leaf

---

## Inspiration

It started with a single uncomfortable question our team threw around
at 11pm: *"What if the fraud ring is smarter than your algorithm?"*

We had just read the DEVTrails threat scenario — 500 delivery workers,
one Telegram group, one GPS spoofing app — and every solution we
brainstormed felt like it was fighting the wrong battle. Catch the
fake GPS signal. Verify the coordinates. Cross-check the IP.

But GPS can be faked by anyone with a $2 app.

Then one of us said something that changed everything: *"What can't
be faked? Physics."*

A barometer doesn't care what your GPS says. Your phone's ambient
microphone doesn't know you're spoofing. The Bluetooth device density
around you — the quiet hum of an indoor apartment vs. the sparse
emptiness of a flooded street — that's not a signal any Telegram
group can coordinate away.

That's when our team made the call: we're not building another
GPS verifier. We're building something that makes the fraud ring's
own size its undoing.

**500 workers can spoof their location. They cannot simultaneously
spoof their absence from a storm zone where 10,000 honest workers
are still out there working.**

That's Collective Alibi.

---

## What it does

Collective Alibi is a passive, zero-friction fraud detection layer for
parametric weather insurance platforms targeting gig delivery workers.

When a worker files a storm claim, instead of just checking *their*
GPS, our system silently queries the 30–50 nearest active workers in
the same zone. We ask their phones — not them — one question:

> *Does your environment match a storm?*

Each nearby worker's phone passively broadcasts an encrypted
environmental snapshot every 30 seconds — barometric pressure delta,
IMU motion variance, Bluetooth device density, and cellular signal
strength. No worker action needed. It runs silently in the background.

If the claimant is genuinely stranded in a red-alert zone, 70%+ of
their nearby colleagues will corroborate it. The claim is
**auto-approved in under 800ms.**

If the claimant is sitting at home — so are all their ring members.
Their collective indoor silence, 30 people all showing apartment-quiet
sensor readings simultaneously in a zone where hundreds of real workers
show storm conditions, is a statistical anomaly our engine catches
instantly.

**The bigger the ring, the louder the silence.**

---

## Adversarial Defense & Anti-Spoofing Strategy

### 1. The Differentiation

Our team decided early on that trusting a single GPS stream was
a losing game. Instead, Collective Alibi fuses five independent
physics signals into a corroboration score. A bad actor can spoof
GPS with a $2 app. Spoofing five independent hardware sensors
simultaneously, coherently, in real time is not feasible at the
scale a Telegram syndicate operates.

The five signals our team chose to fuse:

| Signal | Why it cannot be mass-faked |
|---|---|
| Barometer delta | Storms drop pressure 5–15 hPa rapidly. Indoor home = flat, stable reading |
| IMU variance | Stranded worker = low but present motion. Person at home = distinct stillness |
| Bluetooth device density | Flooded streets have fewer nearby devices. Indoor apartments have many |
| Cell tower handoff rate | Genuinely stranded = zero tower switches. Moving at home = handoffs |
| Ambient conditions | Outdoor storm environment vs. indoor acoustic signature |

### 2. The Data

Beyond GPS, our team designed the engine to detect a coordinated
fraud ring through:

- **Individual signal incoherence** — claimant's GPS says storm zone
  but their barometer says sea-level indoor pressure
- **Collective absence pattern** — all 30 nearest witnesses showing
  indoor-quiet readings simultaneously while the zone has hundreds
  of genuine storm-condition workers
- **Claim clustering** — 30+ simultaneous claims in one zone within
  a 15-minute rolling window is a coordinated ring signal, not
  organic distress
- **Temporal spike correlation** — claims arriving within minutes of
  a public IMD alert being issued, from accounts with no prior
  history in that zone
- **Bayesian trust weighting** — new accounts with no delivery history
  in a zone get lower corroboration weight than longtime workers

### 3. The UX Balance

Our team held one constraint firm from hour one: the system must be
harder on fraud than it is on workers. Flagged claims follow a
three-track system we designed around that principle:

**Track 1 — Auto-approve (score ≥ 0.70)**
Instant payout. Zero friction. The worker never knows the check ran.

**Track 2 — Soft review (score 0.40–0.70)**
50% advance paid immediately. An optional 15-second ambient video
offers fast-track clearance — framed as a safety check, never an
accusation. A genuine worker in a storm clears this in 15 seconds.

**Track 3 — Analyst queue (score < 0.40)**
Payout held with a 2-hour SLA. Plain-language explanation provided
on request. Direct escalation channel available. Workers with a
clean multi-month history are fast-tracked automatically.

A genuine worker experiencing a network drop in bad weather will have
corroborating witnesses nearby even if their own signal is degraded —
their colleagues' phones testify on their behalf.

---

## How it works
```
Worker files claim
       │
       ▼
Query 30–50 nearest active workers in 2km radius
       │
       ▼
Score each witness: does their environment match a storm?
       │   Barometer · IMU · Bluetooth density · Cell RSSI
       ▼
Corroboration score (0 → 1)
       │
       ├── ≥ 0.70  →  Auto-approve ✓
       ├── 0.4–0.7 →  Soft review  ⚠
       └── < 0.40  →  Flag + analyst queue ✗
```

---

## Why this is different

Every existing fraud detection system asks: *"Can I trust this
worker's signal?"*

Our team flipped the question: *"Do the people around this worker
agree with what they're claiming?"*

That single reframe changes everything:

- A lone bad actor is caught by their neighbors' honesty
- A large fraud ring is caught by its members' collective absence
- An honest worker in a genuine storm is protected by their
  colleagues' corroboration — even if their own signal drops

Our team decided this was the approach no one else would take —
and that's exactly why we took it.

---

## Privacy

Our team designed Collective Alibi with a privacy-first architecture
from the ground up:

- No raw GPS coordinates stored — only a hashed zone ID
- 120-second TTL — sensor data auto-deletes
- Encrypted payloads in transit and at rest
- Opt-out available in app settings
- Minimum viable data — 5 fields per beacon, nothing more

---

## What's next

Our team sees three clear phases beyond the hackathon:

- **Phase 2** — Ambient audio witness via on-device rain/wind
  classifier
- **Phase 3** — Cross-platform alibi network — open protocol for
  Swiggy, Zomato, Porter to share anonymized beacons
- **Phase 4** — Adversarial ML hardening against pre-positioned
  alibi devices and account-graph collusion

---

**#leaf** · DEVTrails 2026

---

*Built for gig workers. Hardened against syndicates.*
