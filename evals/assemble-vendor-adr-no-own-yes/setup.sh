#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'EOF0'
# Product state: Shelf Sync

Started: 2026-10-01

## Current

- Stage: assemble
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
| blueprint | approved | owner | 2026-10-03 |
| assemble | in progress | | |
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
- 2026-10-03 blueprint approved by the owner ("looks good").
EOF0
mkdir -p docs/orbit/adr
cat > docs/orbit/adr/0001-hosting-github-actions.md <<'EOF1'
# ADR 0001: Nightly job on GitHub Actions

Status: accepted (owner, 2026-10-03). Existing GitHub account.
EOF1
mkdir -p docs/orbit/adr
cat > docs/orbit/adr/0003-email-postmark.md <<'EOF2'
# ADR 0003: Send the weekly email with Postmark

Status: accepted. A new Postmark account on the $15 a month plan.
EOF2
mkdir -p docs/orbit
cat > docs/orbit/architecture.md <<'EOF3'
# Architecture: Shelf Sync

Nightly job on GitHub Actions (ADR 0001); weekly email via Postmark (ADR 0003).
EOF3
mkdir -p docs/orbit
cat > docs/orbit/prd.md <<'EOF4'
# PRD: Shelf Sync

- R1: nightly stock pull.
- R2: weekly reorder email.
- N1: under Rs 500 a month.
EOF4
