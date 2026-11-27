#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'EOF0'
# Product state: Invoice Lint

Started: 2026-10-01

## Current

- Stage: ignite
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
| ignite | in progress | | |
| blueprint | not started | | |
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
mkdir -p docs/orbit
cat > docs/orbit/brief.md <<'EOF1'
# Brief: Invoice Lint

A CLI that checks supplier invoices for wrong totals and missing tax IDs before they are paid.
EOF1
mkdir -p docs/orbit
cat > docs/orbit/prd.md <<'EOF2'
# PRD: Invoice Lint

- R1: flag invoices whose line items do not add up to the total. Check: a fixture with a wrong total is flagged.
- R2: flag invoices with no tax ID. Check: a fixture without one is flagged.
- N1: runs in under 2 seconds per invoice.
EOF2
