# Collective Alibi
### AI-Powered Parametric Income Insurance for India's Gig Delivery Workers

> **Guidewire DEVTrails 2026** · Phase 1 Submission · Team #leaf

---

## The Problem

Every morning, thousands of delivery riders across Mumbai, Delhi, 
and Bengaluru strap on their helmets, fire up Zomato or Swiggy, 
and head out to earn their day. They are the invisible backbone 
of India's digital economy.

And then it rains.

Not just any rain — a red-alert, IMD-declared, city-shutting 
monsoon downpour. In a single day, a Zomato rider in Andheri 
can lose ₹800 to ₹1,200. In a single week, that's a month's 
worth of grocery money gone. No refund. No safety net. 
No one to call.

India's 15 million platform delivery workers lose 20–30% of 
their monthly income every time an extreme weather event 
shuts down their city. They bear that loss entirely alone.

Our team sat with that number for a while. Then we decided 
to do something about it.

But as we started designing the platform, we ran into a second 
problem — one nobody was talking about openly.

A real fraud syndicate had already exploited a beta parametric 
insurance platform. 500 workers. One Telegram group. One GPS 
spoofing app. They faked their locations inside a red-alert 
weather zone and drained the entire liquidity pool in hours.

So our team made a decision: we wouldn't just build the 
insurance. We'd build it fraud-proof from day one.

That decision became **Collective Alibi**.

---

## Our Persona

We chose to focus on **food delivery partners — Zomato and 
Swiggy riders in Tier-1 Indian cities.** Here's who we're 
actually building for:

| Attribute | Detail |
|---|---|
| Target cities | Mumbai, Delhi, Bengaluru, Chennai, Hyderabad |
| Avg. daily earnings | ₹700 – ₹1,400 |
| Avg. working hours | 8–12 hrs/day, 6 days/week |
| Income at risk | 20–30% monthly during disruption events |
| Primary disruptions | Heavy rain, floods, extreme heat, red-alert weather |
| Device | Android smartphone (primary) |
| Payment preference | UPI — GPay, PhonePe |
| What we cover | Lost income during external disruptions only |
| What we don't cover | Health, life, accidents, vehicle repairs ✗ |

### Meet Ramesh

> Ramesh has been riding for Swiggy in Andheri, Mumbai for 
> three years. He earns around ₹900 a day — good days, bad 
> days averaged out. But every monsoon season, he loses roughly 
> 18 working days to red-alert shutdowns. That's about ₹16,200 
> a year disappearing into the rain with nothing to show for it.
>
> With Collective Alibi, Ramesh pays ₹49 a week. When IMD 
> issues a red alert for his zone, his payout triggers 
> automatically. No claim. No form. No waiting.
> The money arrives before the rain even stops.

---

## What We Built

Collective Alibi is a passive, zero-friction parametric income 
insurance platform built specifically for food delivery workers.

The core idea is simple: **we pay workers automatically when 
a verified disruption stops them from working — and we make 
sure no one can fake that disruption.**

Here's how the full journey works for a worker:
```
Ramesh downloads the app and onboards in 3 minutes
                    │
                    ▼
         Picks a weekly coverage plan
         (₹29 / ₹49 / ₹79 per week, charged every Monday)
                    │
                    ▼
     App runs silently in the background — no action needed
     Every 30 seconds it reads: barometer · motion · 
     Bluetooth density · cell signal strength
                    │
                    ▼
        IMD issues a red alert for Andheri, Mumbai
                    │
                    ▼
     Our system queries 30–50 nearby active workers:
     "Does the environment around Ramesh match a storm?"
                    │
         ┌──────────┴──────────┐
    70%+ corroborate        Less than 40% corroborate
         │                         │
         ▼                         ▼
  Payout sent to UPI         Fraud flag raised
  in under 800ms ✓           Analyst reviews ✗
```

No claim filed. No office visited. No proof uploaded.
The platform handles everything.

---

## Our Weekly Premium Model

Our team structured the entire financial model on a weekly 
basis — because that's how delivery workers actually live. 
Week to week. Order to order.

### Plans

| Plan | Weekly Premium | Daily coverage | Max weekly payout |
|---|---|---|---|
| Basic | ₹29 / week | ₹400 / disruption day | ₹800 (2 days) |
| Standard | ₹49 / week | ₹600 / disruption day | ₹1,800 (3 days) |
| Pro | ₹79 / week | ₹900 / disruption day | ₹3,600 (4 days) |

### How it works in practice

- Premium auto-debits every Monday via UPI
- Coverage is live for exactly 7 days from payment
- Miss a week? Coverage lapses — no penalty, no lock-in, 
  no fine print
- Payout = covered hours × estimated hourly rate, based on 
  the worker's own 30-day earnings average captured at 
  onboarding

### How AI makes it smarter

Our team plans to use machine learning to make premiums 
genuinely personal — not just a flat rate for everyone:

- **Zone flood history** — riders in historically flood-prone 
  areas like Kurla or Sion pay a little more because their 
  risk is genuinely higher
- **Seasonal adjustment** — premiums rise during monsoon 
  (June–September) and come down in winter
- **Loyalty discount** — workers with zero claims in 6 months 
  earn back ₹5–10 off their weekly rate
- **Predictive weather modelling** — if a high-probability 
  storm is forecast for next week, the system proactively 
  offers increased coverage to workers in the projected zone 
  before the event even happens

---

## Our Parametric Triggers

Our team defined six automated triggers — when any of these 
fire for a worker's zone, their payout initiates automatically. 
They never need to file a claim.

| Trigger | Where the data comes from | When it fires |
|---|---|---|
| IMD Red / Orange Alert | India Meteorological Department API | Alert issued for worker's pin code zone |
| Heavy rainfall | OpenWeatherMap API | Rainfall > 64.5mm/hr (IMD heavy rain threshold) |
| Flood zone activation | NDMA / State disaster API (mock) | Worker's area officially declared flood-affected |
| Extreme heat | OpenWeatherMap API | Heat index > 47°C sustained for 3+ hours |
| Severe pollution | CPCB AQI API | AQI > 400 (Severe category) in worker's zone |
| Curfew / zone closure | Government notification API (mock) | Official curfew declared in active delivery zone |

> We cover **lost income only.** Vehicle repair, health 
> expenses, accidents, and medical bills are completely 
> outside our scope — by design and by the rules of the 
> challenge.

---

## Our AI/ML Plan

### 1. Dynamic premium engine
We plan to train a Gradient Boosted Tree model (XGBoost) on:
- Zone-level flood and weather history from IMD
- Seasonal risk patterns across Tier-1 cities
- Worker earnings baseline from onboarding
- Individual claim history over time

The model outputs a personalised weekly premium for each 
worker — not a one-size-fits-all rate.

### 2. Fraud detection — the Collective Alibi engine

This is the part our team is most proud of, and the thing 
we believe no other team will have.

When a claim arrives, instead of trusting the worker's GPS, 
our system silently queries the 30–50 nearest active workers 
in the same zone. It asks their phones — not them — one 
question: *does your environment actually match a storm?*

Five physics signals get fused into a single corroboration 
score:

| Signal | What it's really measuring |
|---|---|
| Barometer delta | Storms drop pressure fast. A home reading stays flat. |
| IMU motion variance | A stranded rider has motion. Someone at home is still. |
| Bluetooth device density | Flooded streets are empty. Indoor apartments aren't. |
| Cell tower handoff rate | Stranded = no handoffs. Moving around at home = handoffs. |
| Collective absence pattern | If all 30 nearby witnesses show indoor readings together, the ring betrays itself. |

The insight that drove this: **500 workers can coordinate on 
Telegram. They cannot coordinate their barometers.**

### 3. Anomaly and ring detection
- A spike of 30+ claims in one zone within 15 minutes = 
  coordinated ring signal
- Claims filed within seconds of a public IMD alert, from 
  accounts with no zone history = temporal anomaly flag
- New accounts get lower trust weight than workers with 
  6+ months of verified activity in the zone

---

## Adversarial Defense & Anti-Spoofing Strategy

Our team read the threat brief and made a deliberate choice: 
we wouldn't patch the GPS problem — we'd make GPS irrelevant.

### 1. How we tell a genuine worker from a bad actor

A genuine delivery partner stranded in a flood has a phone 
that tells a physically coherent story: dropping barometric 
pressure, outdoor motion patterns, sparse Bluetooth 
environment, degraded cell signal. A fraudster at home has 
a phone that tells a completely different story — even if 
their GPS has been spoofed.

We don't catch the lie. We notice that the physics don't match.

### 2. What data we look at beyond GPS

- Barometer, IMU, Bluetooth density, and cell RSSI from the 
  claimant's own device
- The same four signals from 30–50 nearby workers — because 
  a genuine storm affects everyone in the zone, not just 
  one person
- Claim velocity — how many claims arrived in the last 
  15 minutes from this zone
- Account age and zone history — has this worker ever 
  delivered in this area before?

### 3. How we handle flagged claims fairly

Our team held one rule firm throughout the design: **the 
system must be harder on fraud than it is on workers.**

- **Score ≥ 0.70** — Auto-approved. Instant UPI payout. 
  The worker never even knows a check ran.
- **Score 0.40–0.70** — Soft review. 50% of the payout 
  lands immediately. An optional 15-second ambient video 
  offers fast-track clearance — framed as a safety check, 
  never an accusation.
- **Score < 0.40** — Analyst queue. Payout held. 2-hour 
  SLA. Plain-language explanation available on request. 
  Workers with a clean 6-month history get fast-tracked.

A real worker with a bad network connection in a storm is 
protected by their neighbours' corroboration — their 
colleagues' phones testify on their behalf even when their 
own signal drops.

---

## Why Mobile, Not Web

Our team chose mobile-first for reasons that go beyond 
preference:

- Delivery workers live on their phones — a web platform 
  would never get opened
- Our fraud detection depends on passive native sensor 
  access (barometer, IMU, Bluetooth) — impossible on web
- UPI payouts are natively integrated on Android
- Onboarding needs to work in 3 minutes on a mid-range 
  Android with patchy connectivity

---

## Tech Stack

| Layer | What we're using | Why |
|---|---|---|
| Mobile app | React Native + Expo | Native sensor access, cross-platform |
| Sensor beacon | expo-sensors + expo-bluetooth | Barometer, IMU, BT density — passive background |
| Backend | FastAPI (Python) | Fast, async, built for real-time scoring |
| Fraud engine | Python + Redis | Sub-800ms corroboration via geospatial query |
| Database | PostgreSQL | Worker profiles, policies, claim history |
| Weather triggers | OpenWeatherMap + IMD mock | Live parametric event detection |
| Payments | Razorpay test mode / UPI simulator | Simulated instant payout |
| Dashboard | React + Vite + Leaflet.js | Live claim map, risk scores, analyst view |
| Infrastructure | Docker Compose | One command, runs locally, no cloud needed |

---

## Our Development Plan

### Phase 1 — Ideation & Foundation (March 4–20) ✓
- [x] Chose our persona — Zomato/Swiggy food delivery riders
- [x] Designed the weekly premium model and pricing tiers
- [x] Defined 6 parametric income-loss triggers
- [x] Architected the Collective Alibi fraud engine
- [x] Chose mobile platform and justified the decision
- [x] README submitted to GitHub

### Phase 2 — Automation & Protection (March 21 – April 4)
- [ ] 3-minute mobile onboarding flow
- [ ] Weekly policy creation and UPI auto-debit
- [ ] Dynamic premium calculation (ML model v1)
- [ ] 5 automated parametric triggers wired to live/mock APIs
- [ ] Zero-touch claim processing
- [ ] Claims management dashboard

### Phase 3 — Scale & Optimise (April 5 – 17)
- [ ] Full Collective Alibi fraud detection engine
- [ ] Instant UPI payout via Razorpay test mode
- [ ] Worker dashboard — earnings protected, weekly coverage
- [ ] Admin dashboard — loss ratios, predictive disruption 
      analytics
- [ ] 5-minute demo video
- [ ] Final pitch deck

---

## Why We Believe This Wins

Every other team will build a parametric insurance platform 
that trusts GPS and adds a fraud layer on top.

We built one that assumes GPS is already compromised — and 
designed the entire fraud architecture around that reality 
from hour one.

The insight our team kept coming back to:

> *A fraud ring's greatest weakness is its own size.*
> *500 people can lie about where they are.*
> *They cannot all be outdoors in a storm at the same time 
> if they're actually sitting at home.*

Collective Alibi makes parametric insurance for India's gig 
workers actually viable at scale — because right now, fraud 
risk is the single biggest reason insurers won't underwrite it.

We're not just building a product. We're building the trust 
layer that makes the whole category possible.

---

**#leaf** · Guidewire DEVTrails 2026

*Built for gig workers. Hardened against syndicates.*
