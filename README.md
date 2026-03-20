# 🛡️ Collective Alibi
### Parametric Income Insurance for India's Gig Delivery Workers
### *Because when it rains, someone should have their back.*

> **Guidewire DEVTrails 2026** · Phase 1 Submission · Team #leaf

---

## The Human Problem Behind the Tech Problem

Picture this.

It's 7am on a Tuesday in Mumbai. Ramesh, a Swiggy delivery partner from Andheri, wakes up, checks his phone, and sees the IMD notification he dreads every monsoon season:

**"Red Alert — Heavy Rainfall Warning. Mumbai City District."**

He knows what this means. Not just wet roads. Not just slow orders. It means today he earns nothing. Tomorrow maybe nothing. And unlike the restaurants that close their shutters or the offices that declare work-from-home — Ramesh has no safety net. No paid leave. No insurance. No one to call.

He will lose ₹900 today. Possibly ₹900 tomorrow. By the end of monsoon season, he will have lost roughly ₹16,200 — just to the rain.

**India has 15 million delivery workers like Ramesh.**
They power every food order, every grocery delivery, every same-day package that urban India takes for granted. And every single one of them faces this same silent financial bleeding — with zero protection.

Our team decided that was unacceptable.

But as we started building the solution, we uncovered a second crisis hiding underneath the first one — a real fraud syndicate had already exploited a beta parametric insurance platform. 500 workers. One Telegram group. One GPS spoofing app. They faked their locations inside a red-alert weather zone and drained the entire liquidity pool within hours.

Simple GPS verification is dead.

So our team made a decision that changed everything about our architecture:

**We wouldn't just build the insurance.**
**We'd build it impossible to drain.**

That decision became Collective Alibi.

---

## The Insight That Drives Everything

> *500 workers can coordinate on Telegram.*
> *They cannot coordinate their barometers.*
> *They cannot coordinate the Bluetooth device density*
> *of a flooded street versus an indoor apartment.*
> *They cannot coordinate their collective absence*
> *from a storm zone where 10,000 honest workers*
> *are still out there riding in the rain.*

When a worker files a claim, instead of trusting their GPS — 
which can be faked — our system silently queries the 30 to 50 
nearest active workers in the same zone. We ask their phones, 
not them, one question:

***Does your environment actually match a storm?***

If yes → payout in under 800 milliseconds.
If the ring is fake → their collective indoor silence 
betrays them.

**The bigger the fraud ring, the louder the silence.**

This is Collective Alibi. The crowd becomes the witness. 
The fraud ring becomes its own evidence.

---

## Our Persona — Who We Are Building For

We chose to focus exclusively on **food delivery partners — 
Zomato and Swiggy riders in Tier-1 Indian cities.** Not 
because it was the easiest persona — but because they are 
the most exposed, the most numerous, and the most ignored 
when it comes to financial protection.

| Attribute | Reality |
|---|---|
| Target cities | Mumbai, Delhi, Bengaluru, Chennai, Hyderabad |
| Average daily earnings | ₹700 – ₹1,400 |
| Working hours | 8–12 hrs/day, 6 days/week |
| Income lost to disruptions | 20–30% every monsoon season |
| Primary threat | Heavy rain, floods, extreme heat, red alerts |
| Device | Android smartphone — their entire work life lives here |
| Payment preference | UPI — GPay, PhonePe |
| What we cover | Lost income during verified external disruptions |
| What we never cover | Health, life, accidents, vehicle repairs ✗ |

### Ramesh's Story — Our North Star

> Ramesh, 31, has been riding for Swiggy in Andheri for three 
> years. He earns around ₹900 a day — averaging good days and 
> bad. Every monsoon, he loses roughly 18 working days to 
> red-alert shutdowns. That's ₹16,200 vanishing into the rain 
> every year, with nothing to show for it.
>
> With Collective Alibi, Ramesh pays ₹49 a week — less than 
> a single order's delivery fee. When IMD issues a red alert 
> for Andheri, his payout triggers automatically. No claim 
> form. No office visit. No proof needed.
>
> The money arrives in his GPay before the rain even stops.
>
> He never knew the system ran. He just knew someone 
> finally had his back.

---

## How It Works — The Full Journey
```
Ramesh downloads Collective Alibi
              │
              ▼
    3-minute onboarding
    Name · Phone · UPI ID · Delivery platform
    30-day earnings average captured for payout calculation
              │
              ▼
    Picks a weekly plan (auto-debits every Monday via UPI)
    ₹29 Basic · ₹49 Standard · ₹79 Pro
              │
              ▼
    App runs silently in background — Ramesh does nothing
    Every 30 seconds: barometer · IMU · Bluetooth · cell signal
    Encrypted beacon pushed to our Redis store (120s TTL)
              │
              ▼
    IMD issues Red Alert for Andheri, Mumbai
    OpenWeatherMap confirms: rainfall > 64.5mm/hr
              │
              ▼
    Collective Alibi engine activates
    Queries 30–50 nearest active worker beacons in 2km radius
    "Does the environment around Ramesh match a storm?"
              │
        ┌─────┴─────┐
    70%+ confirm    Ring members all show
    storm conditions    indoor readings
        │                   │
        ▼                   ▼
  Payout sent to        Fraud flagged
  Ramesh's GPay         Analyst reviews
  in < 800ms ✓          Ring exposed ✗
```

---

## Our Weekly Premium Model

Our team built the financial model around one truth: 
**gig workers think week to week, not month to month.**

A monthly premium feels like a bill. A weekly premium feels 
like a choice. At ₹49 a week, the decision is easy. At ₹196 
a month, it feels like a commitment they can't afford.

### The Plans

| Plan | Weekly Premium | Daily payout | Max weekly payout |
|---|---|---|---|
| Basic | ₹29 / week | ₹400 / disruption day | ₹800 — up to 2 days |
| Standard | ₹49 / week | ₹600 / disruption day | ₹1,800 — up to 3 days |
| Pro | ₹79 / week | ₹900 / disruption day | ₹3,600 — up to 4 days |

### The Mechanics

- Premium auto-debits every Monday via UPI
- Coverage is live for exactly 7 days from payment
- Miss a week? Coverage lapses — no penalty, no lock-in, 
  no fine print, no guilt
- Payout formula: `disrupted hours × estimated hourly rate`
  based on the worker's own 30-day earnings average from 
  onboarding — so Ramesh gets paid what *he* actually earns, 
  not what some actuary thinks he should

### AI-Powered Dynamic Pricing

Our team plans to use a machine learning model to make 
premiums genuinely fair — not just a flat rate that 
overcharges safe-zone workers and undercharges risky ones:

- **Zone flood history** — riders in historically flood-prone 
  areas like Kurla or Dharavi pay ₹5–8 more per week because 
  their real risk is higher. Riders in elevated, historically 
  dry zones pay less.
- **Seasonal adjustment** — premiums rise during peak monsoon 
  (June–September) and come back down in winter, reflecting 
  actual risk in real time
- **Loyalty discount** — workers with zero claims in 6 months 
  earn back ₹5–10 off their weekly rate. Honest workers get 
  rewarded.
- **Predictive weather modelling** — if a high-probability 
  storm is forecast for next week, our system proactively 
  offers increased coverage to workers in the projected zone 
  before the event happens. They can upgrade their plan 
  before it's too late.

---

## Our Parametric Triggers

No worker ever files a claim on our platform. 
These six triggers fire automatically — and when they do, 
the payout process begins without a single tap from the worker.

| Trigger | Data Source | Threshold | What happens |
|---|---|---|---|
| IMD Red / Orange Alert | India Meteorological Dept. API | Alert issued for worker's pin code | Payout auto-initiated |
| Heavy rainfall | OpenWeatherMap API | > 64.5mm/hr — IMD heavy rain definition | Payout auto-initiated |
| Flood zone activation | NDMA / State disaster API | Worker's area officially flood-declared | Payout auto-initiated |
| Extreme heat | OpenWeatherMap API | Heat index > 47°C for 3+ hours | Payout auto-initiated |
| Severe pollution | CPCB AQI API | AQI > 400 Severe category | Payout auto-initiated |
| Curfew / zone closure | Government notification API | Official curfew in active delivery zone | Payout auto-initiated |

> We insure **lost income only.** Always. Vehicle repairs, 
> health costs, accident bills — completely out of scope, 
> by design and by the rules of this challenge.

---

## Our AI/ML Architecture

### 1. Dynamic premium engine
We will train a Gradient Boosted Tree model on:
- Zone-level weather and flood history from IMD records
- Seasonal disruption patterns across Tier-1 cities
- Worker earnings baselines captured at onboarding
- Individual claim history building over time

Output: a personalised weekly premium per worker — 
not a one-size-fits-all rate that punishes safe-zone 
riders for risks they don't face.

### 2. The Collective Alibi fraud engine

This is the heart of what makes our platform different 
from every other solution in this space.

When a claim arrives, our engine executes a geofence 
query against our Redis beacon store — finding every 
active worker within 2km of the claimant. It pulls 
their last 60 seconds of passive sensor data and scores 
each witness's environmental similarity against the 
claimant's reported conditions.

Five physics signals fused into one corroboration score:

| Signal | The fraud-detection logic |
|---|---|
| **Barometer delta** | A genuine storm drops atmospheric pressure 5–15 hPa rapidly. An indoor home reading stays flat and stable. |
| **IMU motion variance** | A delivery partner stranded in a flooded street has motion — tension, repositioning, the physics of being outside. A person sitting at home is still. |
| **Bluetooth device density** | A flooded street is sparse — people have gone home. An indoor apartment building is dense with devices. |
| **Cell tower handoff rate** | A genuinely stranded worker triggers zero tower switches. Someone walking around their apartment triggers handoffs. |
| **Collective absence pattern** | If 30 ring members all show indoor-quiet sensor readings simultaneously in a zone where hundreds of real workers show storm conditions — the ring betrays itself statistically. |

The Bayesian trust weighting layer adds: workers with 
6+ months of verified activity in a zone carry more 
corroboration weight than newly created accounts.

### 3. Ring detection and anomaly scoring
- **Claim velocity** — 30+ claims in one zone within 
  15 minutes = coordinated ring signal
- **Temporal correlation** — claims arriving seconds 
  after a public IMD alert from accounts with no zone 
  history = pre-meditated fraud pattern
- **Collective silence** — when the claimant's nearest 
  witnesses all show indoor readings simultaneously 
  while the broader zone shows genuine storm conditions, 
  the math tells the story

---

## Adversarial Defense & Anti-Spoofing Strategy

Our team read the threat brief carefully. Then we made 
a deliberate architectural decision: we wouldn't try 
to verify GPS — we'd make GPS irrelevant.

### 1. How we tell a genuine worker from a bad actor

A genuine delivery partner stranded in a Mumbai flood 
has a phone telling a physically coherent story: dropping 
barometric pressure, outdoor motion patterns, sparse 
Bluetooth environment, degraded cell signal, and dozens 
of nearby colleagues showing the exact same conditions.

A fraudster at home has a phone telling a completely 
different story — even if their GPS coordinate has been 
perfectly spoofed.

We don't catch the lie. We notice that the physics 
don't add up.

### 2. The data we look at beyond GPS

- Four passive sensor streams from the claimant's device
- The same four streams from 30–50 nearby workers — 
  because a real storm affects everyone in the zone, 
  not just one person
- Claim velocity in the zone over the last 15 minutes
- Account age and delivery history in that specific area
- The statistical distribution of indoor vs. outdoor 
  sensor readings across all active workers in the zone

### 3. How we protect honest workers from being penalised

Our team held one design principle firm from hour one:

**The system must be harder on fraud than it is on workers.**

A flagged claim is never a dead end. It follows a 
three-track system:

**Track 1 — Auto-approve (score ≥ 0.70)**
Instant UPI payout. The worker never knows a check ran. 
This is the experience for the vast majority of genuine 
claims.

**Track 2 — Soft review (score 0.40–0.70)**
50% of the payout lands in the worker's UPI immediately. 
An optional 15-second ambient video offers fast-track 
clearance — framed as a safety check ("help us confirm 
you're safe"), never as an accusation. A genuine worker 
in a real storm clears this in 15 seconds.

**Track 3 — Analyst queue (score < 0.40)**
Payout held. 2-hour resolution SLA. Plain-language 
explanation available on request — not jargon, not 
legalese, just "here's what our system noticed and 
here's how to resolve it." Workers with a clean 
6-month history are fast-tracked automatically.

A real worker experiencing a network drop in a genuine 
storm is protected by their neighbours' corroboration — 
their colleagues' phones testify on their behalf even 
when their own signal degrades.

---

## Why Mobile — Not Web

Our team chose mobile-first. Not as a default — as a 
deliberate decision with four reasons behind it:

1. **Delivery workers live on their phones.** A web 
   platform would never get opened. The app needs to 
   exist where Ramesh already is — between orders, 
   on his lock screen, in his notification tray.

2. **Our fraud engine requires native sensor access.** 
   Barometer, IMU, and Bluetooth passive scanning are 
   only accessible through a native mobile SDK. The 
   entire Collective Alibi architecture depends on this.

3. **UPI is natively Android.** Instant payouts to GPay 
   or PhonePe are frictionless on mobile. On web, 
   they're not.

4. **Onboarding must work on a mid-range Android with 
   patchy connectivity.** We designed for a ₹8,000 
   phone with intermittent 4G — not a MacBook on WiFi.

---

## Tech Stack

| Layer | Technology | Why we chose it |
|---|---|---|
| Mobile app | React Native + Expo | Native sensor access, single codebase for Android |
| Sensor beacon | expo-sensors + expo-bluetooth | Barometer, IMU, BT density — passive, battery-efficient |
| Backend API | FastAPI (Python) | Async, fast, purpose-built for real-time claim scoring |
| Fraud engine store | Redis | Sub-800ms geospatial beacon query — speed is the point |
| Database | PostgreSQL | Worker profiles, policies, claim history, audit trail |
| Weather triggers | OpenWeatherMap + IMD API | Live parametric event detection |
| Payment simulation | Razorpay test mode / UPI sandbox | Realistic instant payout demonstration |
| Analyst dashboard | React + Vite + Leaflet.js | Live claim map, corroboration scores, ring visualisation |
| Infrastructure | Docker Compose | One command to run everything locally — no cloud needed for demo |

---

## Development Plan

### Phase 1 — Ideation & Foundation (March 4–20) ✓
- [x] Chose persona — Zomato/Swiggy food delivery riders
- [x] Designed weekly premium model and pricing tiers
- [x] Defined 6 parametric income-loss triggers
- [x] Architected the Collective Alibi fraud engine
- [x] Justified mobile platform choice
- [x] Wrote this README

### Phase 2 — Automation & Protection (March 21 – April 4)
- [ ] 3-minute mobile onboarding flow
- [ ] Weekly policy creation with UPI auto-debit
- [ ] Dynamic premium ML model v1
- [ ] 5 automated parametric triggers connected to 
      live and mock APIs
- [ ] Zero-touch claim processing engine
- [ ] Claims management system

### Phase 3 — Scale & Optimise (April 5 – 17)
- [ ] Full Collective Alibi fraud detection engine
- [ ] Instant UPI payout via Razorpay test mode
- [ ] Worker dashboard — weekly coverage, earnings 
      protected, claim history
- [ ] Admin dashboard — loss ratios, predictive 
      disruption analytics, ring detection alerts
- [ ] 5-minute demo video
- [ ] Final pitch deck

---

## The Bigger Picture

Right now, parametric insurance for gig workers in India is largely theoretical. Insurers know the market 
exists. They know the need is real. But they won't underwrite it at scale because the fraud risk is too high and the verification infrastructure doesn't exist.

Collective Alibi is that infrastructure.

We're not just building a product for this hackathon. 
We're building the trust layer that makes the entire 
category viable — a system where honest workers get 
paid automatically and fraud rings collapse under the 
weight of their own deception.

Every Ramesh in every flooded street in every monsoon 
season deserves better than bearing that loss alone.

We built this for him.

Collective Alibi is your project name that we came up with together. Here's what it means:

Collective — the system queries a crowd of nearby workers together, not just one person in isolation.

Alibi — those nearby workers act as each other's alibi. Their phones passively confirm "yes, there really is a storm here" — or expose the fraud ring by their collective silence.

---

**#leaf** · Guidewire DEVTrails 2026

*Built for gig workers. Hardened against syndicates.*
