# Real Estate Agent Team

A multi-agent Claude Code repository for real estate analysis.
Specialized AI agents collaborate to analyze properties, assess risk,
structure deals, write listings, and produce client reports.

## Agents

| Agent | Role |
|-------|------|
| `guide` | ⭐ Start here — plain-English onboarding, collects property info, sets everything up |
| `orchestrator` | Lead — assigns tasks, tracks progress, synthesizes results |
| `market-analyst` | Comps, pricing strategy, rental yield |
| `due-diligence` | Risk, zoning, title flags, inspection profile |
| `listing-agent` | MLS copy, marketing descriptions, buyer targeting |
| `deal-advisor` | ROI, offer strategy, negotiation tactics |
| `report-writer` | Final client-ready report compilation |

## Output

Final reports land in `data/reports/[property_id]_report.md`.

## Docs

See `docs/agent-guide.md` for full usage, adding agents, and troubleshooting.

## Quick Start

```bash
# Start Claude Code
claude

# Then just say:
"help"
```

The **guide agent** will walk you through everything — no setup knowledge needed.
It'll ask you a few simple questions about the property and kick off the full pipeline for you.

---

## Agents
