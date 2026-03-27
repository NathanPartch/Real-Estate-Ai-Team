# Scheduling Protocol

Every agent that triggers a third-party appointment is responsible for
scheduling it, tracking it, and confirming it with the relevant parties.
No agent assumes someone else will handle scheduling.

---

## Appointment Types by Agent

| Agent | Schedules |
|-------|-----------|
| listing-agent | Photography, listing walkthrough with seller |
| due-diligence | Home inspector, termite inspector, roof inspector (if flagged) |
| deal-advisor | Loan officer consult, appraiser (if ordered) |
| buyer-agent | Buyer showing appointments, open house coordination |
| orchestrator | Any appointment that spans multiple parties |
| report-writer | Final walkthrough review (if requested) |

---

## Standard Appointment Types in Real Estate

All agents must recognize and be able to schedule these:

INSPECTIONS
- Home inspection (general) — ordered by buyer after offer accepted
- Termite / pest inspection — required in most CA transactions
- Roof inspection — ordered when roof age or condition is flagged
- HVAC inspection — ordered when system is old or flagged
- Foundation inspection — ordered when foundation type or age is a risk
- Pool inspection — if pool exists
- Sewer scope — recommended for homes 20+ years old
- Mold inspection — if mold history or water damage flagged
- Lead / asbestos testing — if built before 1980

APPRAISAL & FINANCING
- Appraisal — ordered by lender after offer accepted (typically day 5–10)
- Loan officer consultation — buyer meeting to lock rate and review costs
- Final loan approval walkthrough — lender review before funding

SELLER-SIDE
- Listing photography — before listing goes live
- Pre-listing inspection — seller-ordered before listing (optional but smart)
- Seller disclosure review — agent + seller meeting to complete TDS, SPQ
- Staging consultation — if seller wants staging
- Showing appointments — coordinated by listing-agent + buyer-agent

CLOSE OF ESCROW
- Final walkthrough — buyer walks property 1–5 days before close
- Signing appointment — notary or escrow office signing
- Key handoff — seller delivers keys on close date

---

## Appointment Data Structure

All appointments are saved to:
data/appointments/[property_id]_appointments.json

Each appointment entry:

{
  "appointment_id": "APT-[property_id]-[NNN]",
  "property_id": "[property_id]",
  "type": "[appointment type from list above]",
  "party": {
    "role": "home inspector / termite / appraiser / loan officer / photographer / etc.",
    "name": null,
    "company": null,
    "phone": null,
    "email": null,
    "confirmed": false
  },
  "scheduled_by": "[agent name]",
  "scheduled_for": "[ISO datetime or null if TBD]",
  "duration_hours": [estimated duration],
  "location": "[property address]",
  "status": "PENDING_SCHEDULING / SCHEDULED / CONFIRMED / COMPLETED / CANCELLED",
  "notes": "[any special instructions — pets, access codes, tenant notice required]",
  "requires_seller_presence": true / false,
  "requires_buyer_presence": true / false,
  "requires_tenant_notice": true / false,
  "tenant_notice_days_required": null,
  "created_at": "[ISO timestamp]",
  "last_updated": "[ISO timestamp]"
}

---

## How to Schedule an Appointment

Step 1 — Determine what needs to be scheduled
Based on your findings, flag which appointments are needed.

Step 2 — Ask the relevant party for availability
Always ask before booking:

"I need to schedule [appointment type] for [address].

[For seller:] What days and times work best for you in the next [X] days?
[For buyer:] What's your availability for [appointment type]?
Note: [tenant-occupied properties need X days notice — state this if applicable]"

Step 3 — Write the appointment to the appointments file
Append to data/appointments/[property_id]_appointments.json

Step 4 — Update SHARED_STATE
  [agent-name] — APPOINTMENT SCHEDULED — [timestamp]
  - Type: [appointment type]
  - When: [date/time or TBD]
  - Party: [role] (name TBD / [name if known])
  - Status: PENDING_SCHEDULING / SCHEDULED
  - Property: [property_id]

Step 5 — Confirm with all parties
Once a time is set, confirm explicitly:
"Your [appointment type] is scheduled for [date] at [time] at [address].
[Party name/company] will [arrive / call / meet you there].
[Any access instructions — lockbox code, gate code, tenant notice sent.]"

Step 6 — Set reminders in SHARED_STATE
Write a reminder entry 24 hours before each appointment:
  REMINDER — [appointment type] — [property_id] — [date/time]
  - [Any prep the agent or client should do]

---

## Tenant-Occupied Properties — Special Rules

If the property is tenant-occupied:
- California law requires 24 hours written notice for showings
- Inspections require 24 hours written notice minimum
- Appraiser access requires 24 hours minimum
- Agent must coordinate with listing-agent to ensure notice is given
- Never schedule same-day access for tenant-occupied properties
- Track notice given in the appointment record

---

## Appointment Sequencing — Typical Timeline

This is the standard sequence agents should follow after offer acceptance:

Day 0: Offer accepted
Day 1–3: Order home inspection, termite inspection
Day 3–7: Home inspection completed
Day 5–10: Appraisal ordered by lender
Day 7–14: Appraisal completed
Day 3–14: Loan officer locked and documents submitted
Day 14–17: Roof / specialty inspections (if triggered by home inspection)
Day 17–21: Inspection contingency removal (or negotiation)
Day 25–30: Final loan approval
Day 28–30: Final walkthrough
Day 30: Signing appointment
Day 30: Close of escrow / key handoff

Agents should proactively flag if any appointment is running behind
this timeline and alert the orchestrator.

---

## Scheduling Questions by Appointment Type

Home inspector:
"Do you have a preferred home inspector, or would you like a recommendation?
What days work this week or next? Inspections typically take 3–4 hours.
Will you be present for the inspection?"

Termite inspector:
"Termite inspection is required. Do you have a pest company you prefer?
This typically takes 1–2 hours and the seller usually needs to be available."

Appraiser (lender-ordered):
"The lender will order the appraisal — I'll coordinate access.
Is the property occupied? I'll need to give [tenant / seller] 24 hours notice.
What access is needed? (lockbox code, gate code, contact for entry)"

Loan officer:
"Have you spoken with your loan officer about locking your rate?
I can help you schedule a consultation. When are you available for a 30–60 minute call?"

Photographer:
"Do you have a preferred real estate photographer, or should I help arrange one?
Shoots typically take 2–3 hours depending on home size.
Will the home be fully staged and cleaned before the shoot?"

Final walkthrough:
"Final walkthrough is typically scheduled 1–5 days before close.
This is the buyer's last chance to verify condition before signing.
What day works for you? It takes about 30–60 minutes."
