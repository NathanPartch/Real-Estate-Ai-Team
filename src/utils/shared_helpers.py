"""
shared_helpers.py — Utilities shared across agent tool scripts
"""

from datetime import datetime, timezone
from pathlib import Path
import json


def iso_now() -> str:
    """Return current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_listing(property_id: str) -> dict:
    """Load a property listing JSON by property_id."""
    path = Path(f"data/listings/{property_id}.json")
    if not path.exists():
        raise FileNotFoundError(f"No listing found for property_id: {property_id}")
    with open(path) as f:
        return json.load(f)


def append_shared_state(agent_name: str, status: str, message: str):
    """Append an update to the shared state file."""
    path = Path("data/progress/SHARED_STATE.md")
    entry = f"\n## {agent_name} — {status} — {iso_now()}\n{message}\n"
    with open(path, "a") as f:
        f.write(entry)
    print(f"[{agent_name}] Shared state updated.")


def update_task_status(task_id: str, new_status: str):
    """Update a task's status in TASK_QUEUE.md."""
    path = Path("data/progress/TASK_QUEUE.md")
    content = path.read_text()
    # Simple find-replace for the status line under the task block
    old = f"- **Status:** PENDING"
    new = f"- **Status:** {new_status}"
    updated = content.replace(old, new, 1)
    path.write_text(updated)


def list_completed_agents() -> list[str]:
    """Return list of agents that have logged DONE in shared state."""
    path = Path("data/progress/SHARED_STATE.md")
    content = path.read_text()
    done_agents = []
    for line in content.splitlines():
        if "— DONE —" in line:
            agent = line.split("##")[1].split("—")[0].strip()
            done_agents.append(agent)
    return done_agents
