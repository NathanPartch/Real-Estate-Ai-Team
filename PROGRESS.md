# Project Progress

Human-readable status tracker. Updated by the orchestrator after each pipeline run.

---

## Active Pipelines

| Property | Started | Status | Report |
|----------|---------|--------|--------|
| _(none)_ | — | IDLE | — |

---

## Completed Pipelines

_(None yet)_

---

## How to Start a Pipeline

1. Drop a property JSON into `data/listings/[property_id].json`
2. In Claude Code, run: `claude`
3. Tell the orchestrator: _"Analyze 456_elm_st as an investment property and produce a full report."_
4. The orchestrator will spawn the agent team automatically.

## How to Add a New Agent

1. Create `.claude/agents/[agent-name].md` with YAML frontmatter
2. Add the agent to the roster table in `CLAUDE.md`
3. Update the orchestrator's task assignment logic in its agent file
4. Restart your Claude Code session or run `/agents` to reload
