# Guardrails for agentic delivery in a regulated organisation

A checklist to agree with engineering, security and risk before any agent touches a real workflow. The demo implements the items marked ✅.

## Data in
- ✅ Redact personal data and secrets before text leaves the developer's machine (emails, card numbers, sort codes, IBANs, API keys)
- ☐ Use only models and endpoints approved by the organisation, with no training on inputs
- ☐ Keep production data out of prompts entirely; use synthetic or masked data for examples
- ☐ Log what was sent, redacted, to support audit

## Actions
- ✅ Agents get narrow, named tools (for example `create_ticket`), never broad API access
- ✅ Every agent write lands as a draft; only a human can promote it
- ☐ Allowlist repositories and projects each agent may touch
- ☐ No agent can merge, deploy or change permissions

## Output
- ✅ Validate structure against the team's standard (story format, Given/When/Then, priority)
- ✅ Block output that contains anything that was redacted on the way in
- ✅ Retry with validation feedback; report failures instead of hiding them
- ☐ Scan generated code with the same SAST and licence checks as human code

## Proof
- ✅ Task level evals run on every change to prompts or tools
- ☐ Quality sample reviewed by a human each sprint
- ☐ Eval results and incidents reviewed with risk on a fixed cadence

## Questions a risk partner will ask (and should)
1. Where does the data go, and who can see it?
2. What can the agent change without a person agreeing?
3. How do you know it is working, and how would you know if it stopped?
4. What happens when the model or vendor changes?
