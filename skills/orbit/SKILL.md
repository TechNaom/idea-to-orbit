---
name: orbit
description: "Idea to Orbit stage 7. Keep a live product running: a health check on its own clock, alerts that reach the owner, self-healing retries within limits, a cost report, and a root cause analysis with a fix for every incident. Use after launch is approved, when a live product fails, or when the owner asks how a product is doing."
---

# Orbit: keep it running

Goal: the owner hears about problems before users do, small failures fix themselves within
safe limits, and every real incident leaves the product stronger.

## Inputs

The live product, `docs/orbit/deploy-plan.md` and `architecture.md`. Launch must be
`approved` in `STATE.md`.

## Set up (once)

Write `docs/orbit/runbook.md` from `templates/runbook.md` and build these as tasks:

1. **Health check on its own clock.** A scheduled check, on a different trigger from the
   product itself, that asks "did it do its job?", not only "is it up?". A job that never
   started cannot report itself, so the watcher must not share its trigger.
2. **Alerts** go to the owner as GitHub issues (or the owner's chosen channel), one per
   problem per day, never a flood. Each alert says what failed, since when, and the first
   thing to check.
3. **Self-healing within limits.** When a run fails, retry it automatically, with a
   different input or a fallback provider where the failure calls for it, but with a hard
   cap on attempts and on spend. It must never do the same job twice (check before acting),
   and it stops and alerts the owner when the cap is reached.
4. **Cost report** on a schedule: spend so far this month against the cap, and anything
   unusual.
5. **Last known good.** After every healthy release, tag it, so a rollback always has a
   target.

## When something fails

1. Stabilise first: if users are affected and a fix is not quick, roll back to the last
   known good tag.
2. Open `docs/orbit/rca/<YYYY-MM-DD>-<slug>.md` from `templates/rca.md`.
3. Find the root cause with the debug skill: reproduce it, read the evidence (logs, runs,
   traces, metrics), and test one idea at a time. Ask "why" until the answer is something
   you can change.
4. Fix it test-first, through the build loop with both checks: a test that reproduces the failure, then the
   fix. Add a check so the same failure is caught earlier next time.
5. Tell the owner: what happened, the impact, the root cause, the fix, and what now
   prevents it.

Ask the owner before any fix to a part of a live product that is working.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "The product can report its own failures." | A job that never started reports nothing. The watcher runs on its own clock. |
| "Retry until it works." | Every retry has a cap on attempts and on spend, then it alerts the owner. |
| "Just run it again, it was a blip." | Check first that it did not already do the job, so nothing happens twice. |
| "It's fixed, no need for a root cause." | Every incident gets an RCA, a test that reproduces it, and a check that catches it earlier. |
| "The run was green, so it worked." | Green that delivered nothing is a failure. Check the result where the user sees it. |
| "I'll quickly patch the live product." | Ask the owner first. Fixes go through the build loop, test first. |

## Gate

Orbit has no final gate: it runs for as long as the product is live. Its setup is done when:
- [ ] The health check, alerts, self-healing, cost report and last-known-good tag work, each
  proven by a deliberate test failure.
- [ ] `runbook.md` says how to check, heal, roll back and pause the product.

Show the owner the runbook and the results of the test failures, and ask for approval.
Record an explicit yes in `STATE.md`. Afterwards, whenever the owner asks how the product is
doing, report its health, incidents and spend since the last report.
