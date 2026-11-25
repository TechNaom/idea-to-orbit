#!/usr/bin/env bash
# A product half-way through build, for the session-start hook to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Shop Reminders

Started: 2026-11-20

## Current

- Stage: build
- Status: in progress

## Open questions

- Which SMS provider? (blocks: launch)

## Log

- 2026-11-20 ignite started.
STATE
