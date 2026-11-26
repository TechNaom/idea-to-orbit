#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Ledger Lite

Started: 2026-10-01

## Current

- Stage: build
- Status: in progress
- Profile: startup

## Settings

- Code host: github
- Work branch: main
- Release branch: main
- Promotion: none
- Builders: subagents
- Fast tests: `pytest -q -x`
- Full suite: `pytest -q` (about 2 minutes)
- CI: GitHub Actions; a run per commit on main

## Gates

| Stage | Status | Approved by | Date |
|---|---|---|---|
| ignite | approved | owner | 2026-10-02 |
| blueprint | approved | owner | 2026-10-03 |
| assemble | approved | owner | 2026-10-04 |
| build | in progress | | |
| test-flight | not started | | |
| launch | not started | | |
| orbit | not started | | |

## In flight

- none

## Open questions

- None.

## Log

- 2026-10-01 ignite started.
STATE
mkdir -p evals
cat > evals/judge.py <<'PY'
import boto3

client = boto3.client("bedrock-runtime")


def judge(answer: str, source: str) -> bool:
    reply = client.converse(
        modelId="example-judge-model",
        messages=[{"role": "user", "content": [{"text": f"Is this grounded? {answer} / {source}"}]}],
        inferenceConfig={"maxTokens": 300},
    )
    return "yes" in reply["output"]["message"]["content"][0]["text"].lower()
PY
