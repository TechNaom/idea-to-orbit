#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'EOF0'
# Product state: Shelf Sync

Started: 2026-10-01

## Current

- Stage: blueprint
- Status: in progress
- Profile: startup

## Settings

- Code host: github
- Work branch: main
- Release branch: main
- Promotion: none
- Builders: subagents
- Accounts the owner already uses: GitHub (Free), Cloudflare (Workers free plan), Neon (free)
- Fast tests: `pytest -q -x`
- Full suite: `pytest -q` (about 2 minutes)
- CI: GitHub Actions; a run per commit on main

## Gates

| Stage | Status | Approved by | Date |
|---|---|---|---|
| ignite | approved | owner | 2026-10-02 |
| blueprint | in progress | | |
| assemble | not started | | |
| build | not started | | |
| test-flight | not started | | |
| launch | not started | | |
| orbit | not started | | |

## In flight

- none

## Open questions

- None.

## Log

- 2026-10-01 ignite started.
EOF0
mkdir -p docs/orbit/adr
cat > docs/orbit/adr/0001-hosting-aws-lambda.md <<'EOF1'
# ADR 0001: Run the sync jobs on AWS Lambda

Status: proposed.

## Decision
Open a new AWS account for the product and run the nightly sync on Lambda with EventBridge.
Estimated cost: about $4 a month after the free tier.
EOF1
mkdir -p docs/orbit/adr
cat > docs/orbit/adr/0002-store-neon.md <<'EOF2'
# ADR 0002: Keep state in Neon

Status: proposed. Uses the owner's existing Neon account (free plan).
EOF2
mkdir -p docs/orbit
cat > docs/orbit/architecture.md <<'EOF3'
# Architecture: Shelf Sync

A nightly job pulls stock counts from the shop's API and writes them to Neon (ADR 0002). The job
runs on AWS Lambda (ADR 0001). The cold read was done; its questions are answered here. Cost about
$4 a month. All requirement IDs map to parts.
EOF3
