# Agent Questioning Protocol

This file defines how every agent in this system asks questions.
All agents must read and follow this protocol before taking any action.

---

## Core Principle

Every agent is responsible for gathering the data it needs.
No agent may assume, guess, or invent missing information.
If data is missing, incomplete, or ambiguous — ask before acting.

---

## Rule 1 — Identify gaps before starting work

Before beginning any analysis or writing, every agent must:
1. Read all available data files for the property
2. List every field that is UNKNOWN, MISSING, or AMBIGUOUS
3. Determine: can I do my job without this? If no — ask. If yes — proceed and flag.

---

## Rule 2 — Ask questions in batches, not one at a time

Group all missing data into a single, organized question block.
Do not ask one question, wait, then ask another. Batch by category.

Bad pattern:
  "What year was the roof replaced?"
  [waits]
  "What is the HOA monthly dues?"
  [waits]
  "Is there any unpermitted work?"

Good pattern:
  "Before I run your analysis, I need a few things confirmed:

  About the property condition:
  - What year was the roof last replaced or inspected?
  - Is there any unpermitted work or open permits you're aware of?

  About the HOA:
  - What are the monthly dues?
  - Are there any pending special assessments?

  Please answer what you can — if you don't know, just say so."

---

## Rule 3 — Who to ask

Each agent has a defined audience for questions:

| Agent | Ask human | Ask other agents |
|-------|-----------|-----------------|
| guide | buyer or seller (whoever is present) | none |
| orchestrator | buyer or seller | any agent that is BLOCKED or has gaps |
| listing-agent | seller | market-analyst, due-diligence, deal-advisor |
| market-analyst | seller (if data gaps in listing file) | listing-agent (for property specs) |
| due-diligence | seller | listing-agent (for improvement history) |
| deal-advisor | buyer or investor | market-analyst (for comp freshness), due-diligence (for risk details) |
| buyer-agent | buyer | none |
| report-writer | human (buyer or seller, whoever commissioned) | any agent with incomplete output |

To ask another agent a question, write to data/progress/SHARED_STATE.md:
  [your-agent] — QUESTION FOR [target-agent] — [timestamp]
  - Question: [specific question]
  - Context: [why you need it]
  - Blocking: yes / no

---

## Rule 4 — Mark what is still unknown after asking

If the human or agent cannot answer a question, mark the field explicitly:
  field_name: UNKNOWN — not provided by seller
  field_name: UNCONFIRMED — seller said X but could not verify

Never leave a field blank. Never fill it with a guess.
Include all UNKNOWN fields in your output's data gaps section.

---

## Rule 5 — Never proceed past a blocking gap

Some missing data is blocking — the agent cannot do its job without it.
Some missing data is non-blocking — the agent can proceed and flag it.

Blocking gaps — agent must stop and ask:
- Property address (all agents)
- Property type (all agents)
- Square footage (market-analyst, deal-advisor)
- Intended use: primary / investment (deal-advisor)
- Down payment / financing (deal-advisor, if buyer context)
- Asking price (all agents)

Non-blocking gaps — agent continues and flags in output:
- School district
- HOA reserve fund status
- Exact plumbing material
- Permit history beyond last 5 years
- Virtual tour / floor plan availability

---

## Rule 6 — Confirm before publishing or handing off

Before any agent marks itself DONE and hands off:
- Re-read your output
- Flag any claim that could not be confirmed
- Write a DATA GAPS section in your output listing everything still unknown
- If a blocking gap was never resolved, do not mark DONE — mark BLOCKED

---

## Question Templates by Agent

### guide — asking the human
"Hi! Before I get started, I have a few quick questions to make sure
I point you to the right agents.

[Question 1]
[Question 2]
[Question 3]

Take your time — the more you tell me, the better the team can help."

### market-analyst — asking the seller (via listing file gaps)
"I'm pulling comps and market data for your property. To get the most
accurate analysis, I need to confirm a few specs:

[List of missing fields needed for accurate comp matching]

If you don't have exact figures, approximate answers are fine — I'll
note them as estimates in my report."

### due-diligence — asking the seller
"I'm running the risk and compliance check on your property. A few
questions about the property's history will help me flag anything
that buyers will likely ask about:

[List of condition, permit, and disclosure questions]

Being upfront about these now helps avoid surprises during escrow."

### deal-advisor — asking the buyer or investor
"To build the right deal strategy for you, I need to understand
your financial position and goals:

[List of financing, hold period, and risk tolerance questions]

These numbers stay in your profile — they help me tailor the
offer strategy to what actually works for you."

### buyer-agent — asking the buyer
"To find properties that match what you're looking for, I need
to understand your search in more detail:

[List of criteria, must-haves, deal-breakers, timeline questions]

The more specific you are, the fewer mismatches you'll see."

### report-writer — asking the human
"Before I finalize the report, I want to make sure it's formatted
for your needs:

- Who is the primary audience? (you as buyer / seller / your investor group)
- Do you need a short executive summary, or the full detail?
- Are there any sections you want me to emphasize or cut?
- Any conflicting information I should clarify before finalizing?"

### orchestrator — asking agents
"[Agent name] — I see you're BLOCKED / have gaps on [property_id].
Before I can move the pipeline forward, I need:

[Specific question or missing output]

Please respond in SHARED_STATE when resolved."
