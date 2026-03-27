# Real Estate AI Agent Team — Project Instructions

## Overview

This repository houses a coordinated team of specialized real estate AI agents.
Each agent has a defined role and communicates with the others via shared files in `data/progress/`.

**Always read `data/progress/SHARED_STATE.md` before starting any task.**
**Always update it when you complete work or hand off to another agent.**

---

## Agent Roster

> 👋 **New here? Start with the `guide` agent.** Just say "help" or "guide me."

| Agent | File | Role |
|---|---|---|
| `guide` | `.claude/agents/guide.md` | ⭐ Start here — walks users through everything step by step |
| `orchestrator` | `.claude/agents/orchestrator.md` | Lead agent — assigns tasks, synthesizes results |
| `market-analyst` | `.claude/agents/market-analyst.md` | Analyzes market trends, comps, pricing |
| `listing-agent` | `.claude/agents/listing-agent.md` | Writes and reviews property listings |
| `due-diligence` | `.claude/agents/due-diligence.md` | Runs property risk and compliance checks |
| `deal-advisor` | `.claude/agents/deal-advisor.md` | Evaluates deal structure, ROI, negotiation |
| `buyer-agent` | `.claude/agents/buyer-agent.md` | Manages buyer profiles, matches buyers to listings |
| `report-writer` | `.claude/agents/report-writer.md` | Compiles agent outputs into final client reports |

---

## Communication Protocol

Agents communicate by **reading and writing Markdown files** in `data/progress/`.

### Shared State File
- Path: `data/progress/SHARED_STATE.md`
- Every agent reads this on start
- Every agent writes an update when their task finishes

### Handoff Pattern
When your task is done, write to `data/progress/SHARED_STATE.md`:

```
## [YourAgentName] — DONE — [timestamp]
- Summary of what you completed
- Files you wrote: data/...
- Next recommended agent: [agent-name]
- Blockers (if any): none
```

### Task Queue
Pending tasks live in `data/progress/TASK_QUEUE.md`.
If you finish early, check the queue for unassigned work.

---

## Directory Structure

```
realestate-agents/
├── CLAUDE.md                  ← You are here. All agents read this.
├── PROGRESS.md                ← High-level project status (human-readable)
├── .claude/
│   ├── settings.json          ← Agent teams config
│   └── agents/                ← All agent definition files
│       ├── orchestrator.md
│       ├── market-analyst.md
│       ├── listing-agent.md
│       ├── due-diligence.md
│       ├── deal-advisor.md
│       └── report-writer.md
├── src/
│   ├── tools/                 ← Shared scripts agents can run
│   │   ├── fetch_comps.py
│   │   ├── calc_roi.py
│   │   └── format_report.py
│   └── utils/
│       └── shared_helpers.py
├── data/
│   ├── listings/              ← Raw listing inputs (JSON/CSV)
│   ├── reports/               ← Final output reports
│   └── progress/              ← Agent communication hub
│       ├── SHARED_STATE.md    ← Cross-agent state (read/write)
│       └── TASK_QUEUE.md      ← Pending tasks
└── docs/
    ├── agent-guide.md
    └── workflow-diagrams.md
```

---

## General Rules for All Agents

1. **Never overwrite another agent's output** — append or create new files only
2. **Log every action** in `data/progress/SHARED_STATE.md`
3. **Check TASK_QUEUE.md** before declaring yourself idle
4. **Keep file output clean** — other agents will parse your outputs
5. **Be explicit about assumptions** — write them to the shared state
6. **Use ISO timestamps** when logging: `2026-03-27T14:00:00Z`

---

## Tech Stack

- Claude Code v2.1.32+
- Agent Teams: enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Python 3.11+ for tooling scripts
- Markdown for all inter-agent communication
- JSON for structured listing data

---

## Questioning Protocol

All agents follow a shared questioning protocol defined in:
`docs/questioning-protocol.md`

Every agent must read this file before beginning any task. Key rules:
- Ask questions in batches, not one at a time
- Never assume, guess, or invent missing data — ask first
- Mark unresolved fields as UNKNOWN, never blank
- Do not mark DONE if a blocking gap was never resolved
