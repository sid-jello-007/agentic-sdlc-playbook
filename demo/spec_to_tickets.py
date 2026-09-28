"""Spec-to-ticket agent: turns a markdown feature spec into backlog-ready tickets.

Two modes:
  baseline  deterministic rules, no API key needed. Used as the comparison point in evals.
  llm       calls Claude with the redacted spec, validates the output, and retries once
            with the validation errors as feedback (a simple self-correction loop).

Usage:
  python spec_to_tickets.py examples/payo-split-bill-spec.md            # baseline
  python spec_to_tickets.py examples/payo-split-bill-spec.md --mode llm # needs ANTHROPIC_API_KEY
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from guardrails import redact, validate_ticket

SYSTEM_PROMPT = """You are a senior product owner turning a feature spec into backlog tickets.
Rules:
- One ticket per requirement bullet. Keep the requirement's priority (P0, P1, P2).
- user_story must read: "As a <user>, I want <capability>, so that <outcome>".
- 2 to 4 acceptance_criteria per ticket, each in "Given ... when ... then ..." form.
- Use acceptance criteria and constraints from the spec where they apply. Do not invent scope.
- Never reproduce anything shown as [REDACTED_...].
Return only JSON: {"tickets": [{"id","title","user_story","acceptance_criteria","priority","source_requirement"}]}"""


def parse_spec(md: str) -> dict:
    """Split the spec into sections keyed by lowercase heading."""
    sections, current = {}, "_preamble"
    for line in md.splitlines():
        h = re.match(r"^##\s+(.*)", line)
        if h:
            current = h.group(1).strip().lower()
            sections[current] = []
        elif line.strip():
            sections.setdefault(current, []).append(line.strip())
    reqs = []
    for line in sections.get("requirements", []):
        m = re.match(r"^-\s*\[(P\d)\]\s*(.+)", line)
        if m:
            reqs.append({"priority": m.group(1), "text": m.group(2)})
    users = [re.sub(r"^-\s*", "", u).split(":")[0].strip() for u in sections.get("users", [])]
    acs = [re.sub(r"^-\s*", "", a) for a in sections.get("acceptance criteria", [])]
    return {"requirements": reqs, "users": users, "acceptance": acs, "sections": sections}


# ---------- baseline mode ----------
def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 3}


def baseline(spec: dict) -> list[dict]:
    tickets = []
    for i, req in enumerate(spec["requirements"], 1):
        text = req["text"]
        actor = next((u for u in spec["users"] if text.lower().startswith(u.lower())), spec["users"][0] if spec["users"] else "user")
        capability = re.sub(rf"^{re.escape(actor)}\s+(can\s+)?", "", text, flags=re.I)
        capability = capability[0].lower() + capability[1:]
        related = [a for a in spec["acceptance"] if len(_words(a) & _words(text)) >= 2]
        acs = [f"Given the {actor.lower()} is in the flow, when they {capability}, then the action completes and is reflected in the UI"]
        acs += [f"Given the feature is live, when this rule is tested, then {a[0].lower() + a[1:]}" for a in related]
        tickets.append({
            "id": f"SPLIT-{i}",
            "title": text if len(text) <= 70 else text[:67].rsplit(" ", 1)[0] + "...",
            "user_story": f"As a {actor.lower()}, I want to {capability}, so that the bill is settled inside the app",
            "acceptance_criteria": acs,
            "priority": req["priority"],
            "source_requirement": text,
        })
    return tickets


# ---------- llm mode ----------
def llm(redacted_md: str, max_attempts: int = 2) -> list[dict]:
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic to use --mode llm")
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    messages = [{"role": "user", "content": f"Spec:\n\n{redacted_md}"}]
    tickets: list[dict] = []
    for attempt in range(1, max_attempts + 1):
        resp = client.messages.create(model=model, max_tokens=4000, system=SYSTEM_PROMPT, messages=messages)
        raw = resp.content[0].text
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
        tickets = json.loads(raw)["tickets"]
        problems = {t.get("id", "?"): validate_ticket(t) for t in tickets}
        problems = {k: v for k, v in problems.items() if v}
        if not problems:
            break
        print(f"attempt {attempt}: {len(problems)} ticket(s) failed validation, retrying with feedback", file=sys.stderr)
        messages += [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": "Fix these validation errors and return the full JSON again:\n" + json.dumps(problems, indent=2)},
        ]
    return tickets


def to_markdown(tickets: list[dict]) -> str:
    out = []
    for t in tickets:
        out.append(f"### {t['id']} [{t['priority']}] {t['title']}\n\n{t['user_story']}\n")
        out += [f"- {a}" for a in t["acceptance_criteria"]]
        out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--mode", choices=["baseline", "llm"], default="baseline")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    md = Path(args.spec).read_text()
    redacted, counts = redact(md)
    if counts:
        print(f"guardrail: redacted {counts} before processing", file=sys.stderr)

    spec = parse_spec(redacted)
    tickets = baseline(spec) if args.mode == "baseline" else llm(redacted)

    failures = {t["id"]: p for t in tickets if (p := validate_ticket(t))}
    out = Path(args.out)
    out.mkdir(exist_ok=True)
    (out / "tickets.json").write_text(json.dumps(tickets, indent=2))
    (out / "tickets.md").write_text(to_markdown(tickets))
    print(f"{len(tickets)} tickets written to {out}/ ({len(tickets) - len(failures)} passed validation)")
    for tid, probs in failures.items():
        print(f"  {tid}: {'; '.join(probs)}")


if __name__ == "__main__":
    main()
