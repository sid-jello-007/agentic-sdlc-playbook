# Demo

```bash
pip install -r requirements.txt            # only needed for llm mode and the MCP server

python spec_to_tickets.py examples/payo-split-bill-spec.md                # baseline, no key
ANTHROPIC_API_KEY=... python spec_to_tickets.py examples/payo-split-bill-spec.md --mode llm
python evals.py examples/payo-split-bill-spec.md out/tickets.json
python -m unittest discover tests
```

| File | Purpose |
|---|---|
| `spec_to_tickets.py` | The agent: parse spec, redact, generate tickets (rules or Claude), validate, retry once with feedback |
| `guardrails.py` | Redaction patterns and ticket validation rules |
| `evals.py` | Task level evals: coverage, priority, format, leakage, grounding, readability |
| `backlog_mcp_server.py` | MCP server exposing a local backlog with draft only writes |
| `examples/` | Fictional Payo spec plus baseline output and eval results |
| `tests/` | Unit tests for the guardrails |

## Connect the MCP server to a client

Add this to your MCP client's config (for example Claude Desktop's `claude_desktop_config.json`), with the absolute path to this folder:

```json
{
  "mcpServers": {
    "backlog": {
      "command": "python",
      "args": ["/absolute/path/to/demo/backlog_mcp_server.py"]
    }
  }
}
```

Then ask the assistant: *"Read the split bill spec and create draft tickets in the backlog."* Tickets that fail validation come back with the list of problems, so the assistant can fix and resubmit.
