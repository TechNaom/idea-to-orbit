# Free worker router (optional)

An MCP server that lets Claude Code (or Cursor) hand self-contained sub-tasks to other models
through any OpenAI-compatible endpoint, with failover. Claude stays the supervisor and the quality
gate: read [the rules for workers](../../skills/build/workers.md) before using it.

## What it does

- Two tools: `delegate_to_worker(task_prompt, tier, preferred_model)` and `fanout_workers(task_prompt, tier)`
  (two workers in parallel, to compare drafts).
- Tiers `heavy_code`, `context` and `fast`, each an ordered list of providers in
  [providers.json](providers.json). A provider without a key is skipped; a 429, a timeout or an
  error moves to the next one.
- **Size guard:** a `fast` prompt over about 3,000 tokens moves up a tier; a prompt over about
  60,000 tokens is cut with a warning unless the tier is `context`.
- **Secret guard:** a prompt that looks like it holds a key is refused before it leaves the machine,
  and key values are redacted from error messages.
- **Log:** one line per call in `router.log` (time, tier, worker, token estimates), never the prompt
  or the answer. Every answer starts with `[WORKER: <provider>/<model> | ~<tokens> tok]`.

## Install

```
python tools/free-router/install.py            # copies to ~/.claude/mcp, prints the register command
python tools/free-router/install.py --register # also runs `claude mcp add --scope user free-router ...`
```

It never overwrites your `.env` or your own `providers.json`, and it writes a Cursor snippet
(`cursor_mcp_snippet.json`) with this machine's paths. Needs [uv](https://docs.astral.sh/uv/).
Then put your keys in `~/.claude/mcp/.env` and start a new session.

## Models

Every model in `providers.json` is marked `"status": "to verify"`: free tiers and model names change
often. Change it to `"verified"` once a real call has worked, and replace any that keep failing
(the log shows which). Any OpenAI-compatible endpoint can be added, including a local one.

## Token savers that see agent traffic

These are not installed by this tool; each needs its own yes, because it reads what the agent
sees or sends. Check each one live (activity, licence, network calls) before installing, and
measure its saving with `skills/build/token_meter.py`:

| Tool | What it compresses |
|---|---|
| RTK (`rtk-ai/rtk`) | Shell output before it enters the context (a Bash hook); telemetry is opt-in |
| Headroom (`headroomlabs-ai/headroom`) | Tool outputs, logs and files, as a proxy or MCP server |
| mcp-compressor (`atlassian-labs/mcp-compressor`) | MCP tool schemas, loaded only when called |
| token-optimizer-mcp (`ooples/token-optimizer-mcp`) | Tool outputs, with a cache across sessions |

## Tests

`pytest -q tools/free-router` (needs `mcp`, `openai`, `python-dotenv`, `pytest`). Fakes only, no
network; the tests never write a real `router.log`.
