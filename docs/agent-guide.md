# Agent Team Guide

## Architecture Overview

```
User
  │
  ▼
orchestrator          ← Lead agent. Always start here.
  │
  ├──► market-analyst     ← Runs first (or in parallel with due-diligence)
  │
  ├──► due-diligence      ← Runs first (or in parallel with market-analyst)
  │
  ├──► listing-agent      ← Runs after market-analyst (needs pricing context)
  │
  ├──► deal-advisor       ← Runs after BOTH market-analyst + due-diligence
  │
  └──► report-writer      ← Runs last. Needs ALL other agents complete.
```

## Communication Flow

```
data/progress/SHARED_STATE.md   ← All agents read/write here
data/progress/TASK_QUEUE.md     ← Orchestrator assigns tasks; agents claim them
data/progress/*.md              ← Individual agent output files
data/reports/*.md               ← Final client-ready reports
data/listings/*.json            ← Property input data
```

## Starting a Full Analysis Pipeline

```bash
# In your terminal, start Claude Code
claude

# Tell the orchestrator what to do:
"Analyze the property at data/listings/456_elm_st.json as a potential
investment purchase. Run a full pipeline: market analysis, due diligence,
deal advice, and a final report."
```

The orchestrator will:
1. Spawn market-analyst and due-diligence in parallel
2. Once both are done, spawn deal-advisor and listing-agent
3. Once all three are done, spawn report-writer
4. Deliver the final report path to you

## Running Individual Agents

You can invoke any agent directly by name:

```
"Use the market-analyst agent to analyze 456_elm_st"
"Run due-diligence on 456_elm_st only"
```

## Using the ROI Calculator

```bash
python3 src/tools/calc_roi.py data/listings/456_elm_st.json
```

Output prints to console and saves JSON to `data/progress/roi_[property_id].json`.

## Adding a New Agent

1. Create `.claude/agents/your-agent-name.md`

Required frontmatter:
```yaml
---
name: your-agent-name
description: >
  [What the agent does and when to invoke it — be specific]
tools: Read, Write, Bash
model: sonnet
---
```

2. Add the agent to `CLAUDE.md` roster table
3. Update the orchestrator agent to know when to call it
4. Reload: restart session or run `/agents` in Claude Code

## Token Cost Awareness

Each agent team member is a separate Claude instance — costs add up fast.

| Pipeline Stage | Approx. Token Usage |
|---------------|---------------------|
| Single agent | ~5k–20k tokens |
| Full 5-agent pipeline | ~50k–150k tokens |
| Multiple properties | Multiplies linearly |

Use subagents (single session) for quick tasks.
Use agent teams only when cross-agent coordination is genuinely needed.

## Troubleshooting

**Agent says it's blocked:**
→ Check `data/progress/SHARED_STATE.md` for which dependency is missing.
→ Run the missing upstream agent first.

**Agent team not spawning:**
→ Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is in `.claude/settings.json`
→ Confirm you're on Claude Code v2.1.32+

**Agent ignoring CLAUDE.md:**
→ Agents receive only their own system prompt by default. Key instructions
   must be in their individual `.md` file, not just in CLAUDE.md. CLAUDE.md
   is read via the `Read` tool — the agent must be instructed to read it.
