"""Task-level evals for the spec-to-ticket agent.

An agent is only useful in delivery if you can show it works. These checks
answer the questions a delivery lead or risk partner would actually ask:

  coverage     did every requirement become a ticket?
  priority     were priorities preserved?
  format       do stories and acceptance criteria follow the team's standard?
  leakage      did any redacted personal data reach the output?
  grounding    are spec acceptance criteria reflected in the tickets?

Usage: python evals.py examples/payo-split-bill-spec.md out/tickets.json
"""
import json
import re
import sys
from pathlib import Path

from guardrails import PATTERNS, redact, validate_ticket
from spec_to_tickets import parse_spec


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 3}


def run(spec_path: str, tickets_path: str) -> dict:
    spec = parse_spec(redact(Path(spec_path).read_text())[0])
    tickets = json.loads(Path(tickets_path).read_text())
    reqs = spec["requirements"]

    covered = [r for r in reqs if any(r["text"] == t.get("source_requirement") or len(_words(r["text"]) & _words(t.get("source_requirement", ""))) >= 3 for t in tickets)]
    prio_ok = [t for t in tickets if any(r["priority"] == t.get("priority") and len(_words(r["text"]) & _words(t.get("source_requirement", ""))) >= 3 for r in reqs)]
    fmt_ok = [t for t in tickets if not [p for p in validate_ticket(t) if "form" in p or "missing" in p]]
    blob = json.dumps(tickets)
    leaks = [label for label, p in PATTERNS.items() if p.search(blob)]
    all_ac = " ".join(a for t in tickets for a in t.get("acceptance_criteria", []))
    grounded = [a for a in spec["acceptance"] if len(_words(a) & _words(all_ac)) >= 3]

    # Structural checks are not enough: a story can be perfectly formatted and still unreadable.
    # Cheap heuristic for the most common failure: the words after "I want to" are not a base verb.
    def reads_badly(story: str) -> bool:
        m = re.search(r"(?i)i want to (\w+)", story)
        if not m:
            return True
        w = m.group(1).lower()
        return w in {"each", "the", "a", "an", "all", "every"} or (w.endswith("s") and not w.endswith("ss"))
    readable = [t for t in tickets if not reads_badly(t.get("user_story", ""))]

    def pct(a, b):
        return round(100 * len(a) / b) if b else 0

    return {
        "coverage_pct": pct(covered, len(reqs)),
        "priority_preserved_pct": pct(prio_ok, len(tickets)),
        "format_pass_pct": pct(fmt_ok, len(tickets)),
        "pii_leaks": leaks,
        "spec_acceptance_grounded_pct": pct(grounded, len(spec["acceptance"])),
        "story_readability_pct": pct(readable, len(tickets)),
        "tickets": len(tickets),
        "requirements": len(reqs),
    }


if __name__ == "__main__":
    result = run(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
    ok = result["coverage_pct"] == 100 and not result["pii_leaks"] and result["format_pass_pct"] == 100
    sys.exit(0 if ok else 1)
