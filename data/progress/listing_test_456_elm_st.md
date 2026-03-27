# LISTING AGENT TEST RUN — 456 Elm Street
# Simulating full Phase 1 → Phase 3 flow against real property data
# Date: 2026-03-27

## STARTUP SEQUENCE

### Read: docs/questioning-protocol.md ✅
### Read: data/progress/SHARED_STATE.md ✅ — no prior work
### Read: data/listings/456_elm_st.json ✅

---

## GAP ANALYSIS — What I have vs. what I need

HAVE (from listing file):
- Address: 456 Elm Street, Anaheim CA 92801 ✅
- Type: single-family ✅
- Price: $875,000 ✅
- Beds/baths: 4bd/2.5ba ✅
- Sq ft: 2,100 ✅
- Lot: 6,500 sq ft ✅
- Year built: 1988 ✅
- Garage: 2-car attached ✅
- Pool: no ✅
- HOA: yes, $185/month, Elm Park HOA ✅
- Taxes: $10,200/yr ✅
- Insurance estimate: $2,400/yr ✅
- Last sold: $540,000 on 2016-07-14 ✅
- Zestimate: $862,000 ✅
- Intended use: investment ✅
- Est. rent: $3,800/mo ✅
- Features: kitchen 2022, HVAC 2023, original roof 1988, hardwood, patio ✅
- Notes: motivated seller, price reduction, roof concern ✅

MISSING — blocking:
- None. All blocking fields are present.

MISSING — non-blocking (must ask seller):
- Occupancy status: owner-occupied / tenant / vacant? NOT IN FILE
- Roof material: unknown (age known: 1988)
- Water heater: age/type unknown
- Plumbing material: unknown
- Electrical panel brand: unknown
- Unpermitted work: not disclosed
- Open permits: unknown
- Insurance claims last 5 years: unknown
- Pest/mold history: unknown
- HOA reserve fund status: unknown
- HOA special assessments pending: unknown
- HOA rental restrictions: unknown
- Mello-Roos: unknown
- Photos available: unknown
- Floor plan: unknown
- Virtual tour: unknown
- Seller disclosures prepared: unknown
- Preferred showing windows: unknown
- Items included/excluded: unknown
- Target close date: unknown

HISTORICAL FACTS TO VERIFY WITH SELLER:
- Last sale: $540,000 on July 14, 2016
- Zestimate: $862,000 vs. list price $875,000 (+$13K above Zestimate)
- Days on market: 26 days (with 1 price reduction)
- Roof age: 38 years (1988 — same as build year, likely original)

---

## PHASE 1B — SELLER INTAKE QUESTIONS

The agent would present this to the seller:

"Before I build your listing and dispatch the analysis team, I need to
fill in a few gaps. I'll ask in groups to keep it organized:

**About the property right now:**
- Is the property currently occupied by you, a tenant, or is it vacant?
- If tenant-occupied: when does the lease expire, and is the tenant planning to stay?
- Are there any items you're including or excluding from the sale?
  (appliances, fixtures, furniture, etc.)
- What's your ideal close date?
- What are your preferred showing windows? (e.g. weekdays after 5pm, weekends anytime)

**About the property's condition:**
- The roof appears to be original from 1988. What do you know about its current condition?
  Has it been inspected recently? Any known leaks or repairs?
- What type and age is the water heater?
- Do you know the plumbing material? (copper, PEX, galvanized?)
- What brand is the electrical panel? (e.g. Siemens, Square D, Leviton — or do you know if
  it's a Federal Pacific or Zinsco?)
- Are you aware of any unpermitted additions, conversions, or renovations?
- Are there any open permits currently on the property?

**About the HOA:**
- Do you have a copy of the HOA financials or reserve fund study?
- Are there any pending special assessments from the HOA?
- Are there any HOA rental restrictions (short-term or long-term)?
- Is there any active HOA litigation you're aware of?

**About history:**
- Have there been any insurance claims on this property in the last 5 years?
  (water damage, fire, theft, etc.)
- Any known pest infestations or mold history?
- Have seller disclosures been prepared? If so, can I review them?

**About media:**
- Do you have professional listing photos ready, or do we need to schedule photography?
- Is there a floor plan, virtual tour, or 3D scan available?

---

## PHASE 1C — HISTORICAL FACTS FOR VERIFICATION

The agent would present these to the seller for confirmation:

'Before I write anything, I want to confirm a few things from the public record
so nothing in your listing is inaccurate:

1. Records show this property last sold for $540,000 on July 14, 2016.
   Is that accurate?

2. The current Zestimate is $862,000, and you're listed at $875,000 —
   that's $13,000 above the automated estimate. The market analysis will
   tell us if comps support that gap. Just flagging it.

3. The listing notes mention one prior price reduction. What was the
   original list price, and when was it reduced?

4. The roof appears to be original from 1988 — 38 years old.
   Has it been replaced, repaired, or inspected recently?
   This will be a buyer question and a due diligence flag.

Please confirm, correct, or add context for each.'"

---

## PHASE 2 — DISPATCH TO SPECIALIST AGENTS

Task cards the agent would write:

TASK-001
- Assigned to: market-analyst
- Priority: high
- Property ID: 456_elm_st
- Input: data/listings/456_elm_st.json
- Expected output: data/progress/market_analysis_456_elm_st.md
- Context: Investment property. Est. rent $3,800/mo (seller-provided).
  Need: comps, $/sqft, DOM for 92801 SFR, rental yield validation.
- Status: PENDING

TASK-002
- Assigned to: due-diligence
- Priority: high
- Property ID: 456_elm_st
- Input: data/listings/456_elm_st.json
- Expected output: data/progress/due_diligence_456_elm_st.md
- Context: Year built 1988. HOA exists ($185/mo). Original roof flagged.
  Seller motivated. Ask seller about: unpermitted work, HOA reserve fund,
  insurance claims, electrical panel brand.
- Status: PENDING

TASK-003
- Assigned to: deal-advisor
- Priority: high
- Property ID: 456_elm_st
- Input: data/listings/456_elm_st.json
- Dependencies: TASK-001, TASK-002 must complete first
- Expected output: data/progress/deal_advice_456_elm_st.md
- Context: Investment use. Est. rent $3,800/mo. HOA $185/mo. Taxes $10,200/yr.
  Motivated seller with price reduction — leverage exists.
- Status: PENDING (waiting on TASK-001, TASK-002)

---

## TEST FINDINGS — What passed, what needs fixing

PASS: Agent correctly identified all non-blocking gaps without stopping
PASS: Questions batched by category, not dripped one at a time
PASS: Historical facts (last sale, Zestimate gap, price reduction, roof age) surfaced for verification
PASS: Context passed to each specialist agent in task cards — no re-asking needed
PASS: Agent did not invent occupancy, HOA reserve status, or plumbing material
PASS: Roof flagged as 38 years old — correct and critical

FLAG: The listing file has no field for "occupancy_status" — the agent asked correctly
      but there's nowhere to save the answer. JSON schema needs this field added.

FLAG: No field for "showing_windows" or "close_date" in the listing JSON.
      These need to be added for appointment scheduling.

FLAG: No field for "appointments" — needed for the new scheduling requirement.
      This should live in data/appointments/456_elm_st_appointments.json

FLAG: The agent has no way to schedule the inspector, appraiser, loan officer,
      or termite company. Scheduling system needed before Phase 3 can complete fully.
