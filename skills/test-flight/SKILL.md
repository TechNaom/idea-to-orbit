---
name: test-flight
description: "Idea to Orbit stage 5. The release gate: verify a built product before launch with tests against every requirement, failure and burst tests, a security and secrets check, a cost estimate and a rehearsed rollback, and record a go or no-go. Use after build is approved, or when the owner asks if a product is ready to release."
---

# Test flight: the release gate

Goal: an honest go or no-go before anything reaches real users, with evidence for every
claim and a list of what could not be tested.

## Inputs

The built product on main, `prd.md`, `architecture.md` and `tasks.md`. Build must be
`approved` in `STATE.md`.

## Steps

Fill in `docs/orbit/release.md` from `templates/release-checklist.md` as you go. Every line
needs evidence: a command and its output, a link to a CI run, or a screenshot.

1. **Requirements:** for each requirement ID, run its acceptance check. Pass or fail, with
   evidence.
2. **Tests:** the full suite and CI are green on the release commit.
3. **End to end:** run the main flows against a production-like environment (a shadow or
   staging deploy that sends nothing to real users).
4. **Failure and load:** kill or block each outside dependency in turn and confirm the
   failure path in `architecture.md` really happens. Send a burst of requests and confirm
   limits, retries and timeouts hold.
5. **Security:** no secrets in the repository or its history; least-privilege keys;
   every credential's expiry date known, with a warning set before it; inputs validated;
   dependencies scanned.
6. **Cost:** estimate the monthly cost at the expected load and at ten times that load.
   Both must fit the PRD's budget, or the owner must accept the risk in writing.
7. **Rollback:** rehearse it. Deploy the release to staging, roll back to the previous
   version, and confirm it works.
8. **Not tested:** list what could not be tested and why. Never leave this empty without
   saying "nothing".
9. Decide: **go** only if every must-have requirement passes and nothing in the list above
   is red. Otherwise **no-go**, with what must change.

## Gate

Show the owner the decision, the failures if any, the cost estimate and the not-tested list,
and ask for approval to launch. Record an explicit yes in `STATE.md` and say that **launch**
is next. A no-go sends the product back to build with new tasks in `tasks.md`.
