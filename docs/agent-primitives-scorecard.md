# Agent primitives scorecard

A vendor neutral way to assess any agent platform, internal or bought. Every vendor says "agents"; this scorecard asks whether the building blocks underneath are there and follow the direction the industry is converging on.

I built this to run a gap audit of an enterprise agent platform against current industry primitives. This public version is generic and contains no findings about any specific product.

## The six primitives

| Primitive | Question it answers | Where the industry is heading |
|---|---|---|
| **Model access** | Can you choose and swap models per task? | Multiple providers, routing by cost and capability |
| **Skills / instructions** | How is reusable know-how packaged and shared? | Portable, versioned instruction packs loaded on demand |
| **Tools** | How does the agent act on other systems? | Typed, narrow tools with clear descriptions |
| **Connectivity (MCP)** | Can tools be plugged in without custom integration work? | Model Context Protocol as the common standard |
| **Memory and context** | What does the agent know across steps and sessions? | Explicit, inspectable memory and deliberate context engineering |
| **Evals and observability** | How do you know it works and keeps working? | Task level evals in CI, traces for every run |

## Maturity levels

| Level | Meaning |
|---|---|
| 0 Absent | Not supported |
| 1 Proprietary | Supported, but in a closed format that does not travel |
| 2 Interoperable | Supported and compatible with open standards |
| 3 Leading | Interoperable, plus tooling that makes it easy to govern at scale |

## How to run it

1. **Score each primitive 0 to 3** with evidence: a doc link, a demo, or a test you ran yourself.
2. **Weight by your use case.** A delivery tooling use case weights tools, MCP and evals higher than memory.
3. **Look for divergence, not just gaps.** A proprietary format at level 1 can be worse than a gap, because it creates lock in you later have to unwind.
4. **Turn it into a roadmap.** Close level 0s that block your use case first; move level 1s to level 2 where interoperability matters to customers.

## Template

| Primitive | Weight (1 to 3) | Score (0 to 3) | Evidence | Gap or divergence | Recommended action |
|---|---|---|---|---|---|
| Model access | | | | | |
| Skills / instructions | | | | | |
| Tools | | | | | |
| Connectivity (MCP) | | | | | |
| Memory and context | | | | | |
| Evals and observability | | | | | |

## How the demo maps to the primitives

| Primitive | In this repo |
|---|---|
| Model access | `ANTHROPIC_MODEL` env var; baseline mode needs no model at all |
| Skills / instructions | The system prompt encodes the team's ticket standard |
| Tools | `create_ticket`, `list_tickets`, `get_ticket` |
| Connectivity (MCP) | `backlog_mcp_server.py` works with any MCP client |
| Memory and context | Spec is parsed into sections; only redacted text reaches the model |
| Evals and observability | `evals.py` with six task level checks; unit tests for guardrails |
