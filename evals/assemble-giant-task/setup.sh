#!/usr/bin/env bash
# A product for this case, for the session-start hook and the skills to read.
set -e
mkdir -p docs/orbit
cat > docs/orbit/STATE.md <<'STATE'
# Product state: Ledger Lite

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
STATE
cat > docs/orbit/prd.md <<'PRD'
# PRD: Ledger Lite

Small firms import invoices from CSV, approve them, and export the approved ones to accounting.

| ID | Requirement | Acceptance check |
|---|---|---|
| R1 | Import invoices from a CSV file | 3 valid rows give 3 invoices; a bad row is reported with its line number |
| R2 | An approver approves or rejects each invoice | The decision and the approver are stored; a rejected invoice cannot be exported |
| R3 | Export approved invoices as CSV for the accounting tool | The export holds every approved invoice once, in the tool's column order |
| N1 | Costs under $20 a month at 1,000 invoices | The cost estimate in architecture.md |
PRD
cat > docs/orbit/architecture.md <<'ARCH'
# Architecture: Ledger Lite

A web API (Python, FastAPI) on AWS Lambda, a PostgreSQL database (Aurora Serverless v2,
scales to zero), and S3 for uploaded and exported files.

| Part | Responsibility | Requirements |
|---|---|---|
| Importer | Parse and validate the CSV, store invoices | R1 |
| Approvals | Approve or reject, with the approver | R2 |
| Exporter | Write approved invoices as CSV to S3 | R3 |

Failure modes: a malformed CSV row is reported and skipped; an export that fails is retried
once, then reported.
ARCH
