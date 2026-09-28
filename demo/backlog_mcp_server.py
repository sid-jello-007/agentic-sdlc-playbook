"""A minimal MCP server that exposes a local backlog to any MCP client
(Claude Desktop, Claude Code, VS Code with Copilot agent mode, and others).

It stands in for the ticketing system an enterprise would connect to.
The point of the demo is the contract, not the storage: the agent gets
narrow, well described tools, and every write passes the same guardrails
as the spec-to-ticket agent.

Run:   pip install "mcp[cli]"  &&  python backlog_mcp_server.py
Wire:  add it to your MCP client config as a stdio server (see README).
"""
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from guardrails import redact, validate_ticket

BACKLOG = Path(__file__).parent / "out" / "backlog.json"
mcp = FastMCP("backlog")


def _load() -> list[dict]:
    return json.loads(BACKLOG.read_text()) if BACKLOG.exists() else []


def _save(items: list[dict]) -> None:
    BACKLOG.parent.mkdir(exist_ok=True)
    BACKLOG.write_text(json.dumps(items, indent=2))


@mcp.tool()
def list_tickets(priority: str | None = None) -> list[dict]:
    """List backlog tickets, optionally filtered by priority (P0, P1, P2)."""
    items = _load()
    return [t for t in items if priority is None or t["priority"] == priority]


@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Get one ticket by id."""
    return next((t for t in _load() if t["id"] == ticket_id), {"error": f"{ticket_id} not found"})


@mcp.tool()
def create_ticket(title: str, user_story: str, acceptance_criteria: list[str], priority: str, source_requirement: str) -> dict:
    """Create a ticket. Rejected if it fails validation (story format, Given/When/Then criteria,
    known priority, no personal data). Returns the ticket or the list of problems."""
    items = _load()
    ticket = {
        "id": f"BL-{len(items) + 1}",
        "title": redact(title)[0],
        "user_story": redact(user_story)[0],
        "acceptance_criteria": [redact(a)[0] for a in acceptance_criteria],
        "priority": priority,
        "source_requirement": redact(source_requirement)[0],
        "status": "draft",  # a human moves it to ready; the agent never can
    }
    problems = validate_ticket(ticket)
    if problems:
        return {"rejected": True, "problems": problems}
    _save(items + [ticket])
    return ticket


if __name__ == "__main__":
    mcp.run()
