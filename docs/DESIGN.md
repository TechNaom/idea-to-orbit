# Design

Version 0.1, 2026-11-25.

## Goal

One repeatable way to take any product from an idea to a running product that stays up, so
that every product is planned, designed, built, tested, deployed and operated to the same
standard, and the owner stays in control at every step.

The first user is the owner, building TechNaom products. Anyone else can use it as is.

## How it works

Idea to Orbit is a Claude Code plugin:

- **Seven skills**, one per stage, in `skills/<stage>/SKILL.md`. Each skill says what the
  stage needs as input, what it does, what it writes, and what its gate checks.
- **Templates** for every document a stage writes, in `skills/<stage>/templates/`.
- **One command**, `/orbit`, in `commands/orbit.md`. It reads the product's state and starts
  or continues the right stage.

All output goes into the product's own repository under `docs/orbit/`, so the plan, the
decisions and the history travel with the code.

## State

`docs/orbit/STATE.md` is the single source of truth for where a product is:

- the current stage and its status (`in progress`, `waiting for approval`, `approved`)
- each gate's approval: who said yes and when
- open questions that block a stage
- a dated log of stage changes

A stage may start only when the stage before it is `approved`. The owner can send a product
back to an earlier stage at any time; later stages are then marked `needs review`.

## Gates

Every stage ends with a gate:

1. Claude checks the stage's exit list (in its skill).
2. Claude shows the owner a short summary: what was made, what was decided, what is open.
3. The owner answers. Only an explicit yes ("approved", "go", "yes, proceed") passes the gate.
   Anything else is feedback, and the stage continues.
4. Claude records the approval in `STATE.md` with the date.

## The stages

| Stage | Input | Output | Gate checks |
|---|---|---|---|
| Ignite | The idea, in any form | brief, PRD | Problem, users, scope and success measures are clear; out of scope is written down |
| Blueprint | Approved PRD | architecture, ADRs, diagrams | At least two options weighed for each big decision; data model, interfaces, security, cost and failure modes covered |
| Assemble | Approved architecture | tasks, issues | Every requirement maps to tasks; every task has a test and a done check; order and dependencies are clear |
| Build | Approved tasks | code, tests | Each task: test written first, test passes, reviewed, committed and pushed |
| Test flight | Built product | release gate result | Tests green, risks listed, secrets safe, cost estimated, rollback tested |
| Launch | Passed release gate | deploy plan, live product | Budget cap and alerts set first, backup tag taken, smoke test passes on the live product |
| Orbit | Live product | runbook, incident records | Health check on its own clock, alerts reach the owner, healing has limits, every incident gets a root cause |

## Defaults

These hold unless the owner chooses otherwise for a product:

- Serverless hosting that scales to zero, on the free tier where possible.
- A monthly spending cap with alerts at 25, 50, 80 and 100 percent, set before the first
  deploy.
- Secrets in a gitignored `.env`, with a committed `.env.example`.
- GitHub for code, CI, issues and alerts.
- Diagrams in Mermaid, so they render on GitHub with nothing to install.

## Next

- A product dashboard that reads every product's `STATE.md`.
- Ready-made deploy templates for the common targets (AWS Lambda with EventBridge,
  Cloudflare Workers, Cloud Run).
- An evaluation: build one real product end to end with the plugin and record the time,
  cost and number of fixes after launch.
