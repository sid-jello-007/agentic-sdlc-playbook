"""Guardrails applied before and after the model call.

Inbound:  redact personal data and secrets before any text leaves the machine.
Outbound: reject tickets that are incomplete or that leak redacted content.

These are deliberately simple regex and schema checks. In a regulated setting
they sit alongside, not instead of, the organisation's own DLP and review controls.
"""
import re

PATTERNS = {
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "UK_SORT_CODE": re.compile(r"\b\d{2}-\d{2}-\d{2}\b"),
    "CARD_NUMBER": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    "API_KEY": re.compile(r"\b(?:sk|pk|api|key)[-_][A-Za-z0-9_-]{16,}\b", re.I),
}

REQUIRED_FIELDS = ("id", "title", "user_story", "acceptance_criteria", "priority", "source_requirement")
PRIORITIES = {"P0", "P1", "P2"}


def redact(text: str) -> tuple[str, dict[str, int]]:
    """Replace sensitive values with typed placeholders. Returns text and counts per type."""
    counts: dict[str, int] = {}
    for label, pattern in PATTERNS.items():
        text, n = pattern.subn(f"[REDACTED_{label}]", text)
        if n:
            counts[label] = n
    return text, counts


def validate_ticket(ticket: dict) -> list[str]:
    """Return a list of problems. Empty list means the ticket passes."""
    problems = [f"missing field: {f}" for f in REQUIRED_FIELDS if not ticket.get(f)]
    if ticket.get("priority") and ticket["priority"] not in PRIORITIES:
        problems.append(f"unknown priority: {ticket['priority']}")
    story = ticket.get("user_story", "")
    if story and not re.match(r"(?i)^as an? .+, i want .+ so that .+", story):
        problems.append("user story not in 'As a..., I want..., so that...' form")
    for ac in ticket.get("acceptance_criteria", []):
        if not re.match(r"(?i)^given .+ when .+ then .+", ac):
            problems.append(f"acceptance criterion not in Given/When/Then form: {ac[:50]}")
    blob = " ".join(str(v) for v in ticket.values())
    for label, pattern in PATTERNS.items():
        if pattern.search(blob):
            problems.append(f"output contains unredacted {label}")
    return problems
