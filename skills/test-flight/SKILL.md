---
name: test-flight
description: "Idea to Orbit stage 5. The release gate: verify a built product before launch with tests against every requirement, failure and burst tests, a security and secrets check, a cost estimate and a rehearsed rollback, and record a go or no-go. Use after build is approved, or when the owner asks if a product is ready to release."
---

# Test flight: the release gate

Goal: an honest go or no-go before anything reaches real users, with evidence for every
claim and a list of what could not be tested.

## Inputs

The built product on the **Release branch** (`STATE.md` Settings), `prd.md`,
`architecture.md` and `tasks.md`. Build must be `approved` in `STATE.md`. If the work branch
is not the release branch, merge it into the release branch through a pull or merge request
first; the release commit is that merge.

## Steps

Fill in `docs/orbit/release.md` from `templates/release-checklist.md` as you go. Every line
needs evidence: a command and its output, a link to a CI run, or a screenshot.

1. **Requirements:** for each requirement ID, run its acceptance check. Pass or fail, with
   evidence.
2. **Tests:** the full suite and CI are green on the release commit.
   **CI that cannot fail:** list every CI job that is allowed to fail (`allow_failure`,
   `continue-on-error`, a manual job that nothing waits for). Each one either blocks the
   release, or has a written reason and an owner. A check that cannot fail the pipeline is
   not evidence; a security scan that is "reported only" is not a security check.
3. **End to end:** run the main flows against a production-like environment (a shadow or
   staging deploy that sends nothing to real users).
4. **Failure and load:** kill or block each outside dependency in turn and confirm the
   failure path in `architecture.md` really happens. Send a burst of requests and confirm
   limits, retries and timeouts hold.
5. **Security:** no secrets in the repository or its history; least-privilege keys;
   every credential's expiry date known, with a warning set before it; inputs validated;
   dependencies scanned, with the scan blocking. In the enterprise profile, also: the
   control mapping in `architecture.md` checked against what is built, no personal data or
   secrets in logs, and a passive security scan of the deployed staging site.
6. **AI** (when the product calls a model): the eval suite runs on the release commit
   against the live model and meets every bar in the PRD; guardrail checks are tested; AI
   spend is metered and inside its budget at the expected load.
7. **Screens** (when the product has a UI): the browser tests cover every screen in the
   screen list for every role, plus accessibility and phone width. Give the owner a
   screen-by-screen checklist from the same list (each screen, each role, what to do, what
   they should see), and record what they found. A person finds what tests were never
   told to look for.
8. **Cost:** estimate the monthly cost at the expected load and at ten times that load.
   Both must fit the PRD's budget, or the owner must accept the risk in writing.
9. **Rollback:** rehearse it. Deploy the release to staging, roll back to the previous
   version, and confirm it works.
10. **Not tested:** list what could not be tested and why. Never leave this empty without
   saying "nothing".
11. Decide: **go** only if every must-have requirement passes and nothing in the list above
   is red. Otherwise **no-go**, with what must change.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "All the tests pass, so it's a go." | Tests are one line of the gate. Run every check on the list. |
| "We can't test failure paths without production." | Block the dependency in staging, or in a test, and watch what happens. |
| "Rollback is just redeploying the old version." | Rehearse it. An untested rollback fails when you need it. |
| "Nothing was left untested." | Write 'nothing' only after looking. Most releases have something. |
| "The owner needs this live tomorrow, mark it go." | Give the honest decision. The owner may accept a risk in writing; you never hide one. |
| "It's a small release, skip the cost check." | Small releases still add loops, retries and calls. Check the estimate. |
| "That scan is reported only, but it's green." | Green by luck is not a gate. Make it block, or write why it may not. |
| "The evals passed last week." | Run them on the release commit, against the live model. Models and prompts drift. |

## Gate

Exit list:
- [ ] Every requirement's acceptance check was run on the release commit, with evidence.
- [ ] The full suite and CI are green on the release commit; every CI job allowed to fail is
  blocking, or has a written reason and an owner.
- [ ] Each outside dependency was failed in turn, and a burst was sent; the failure paths held.
- [ ] No secrets in the repository or its history; credential expiry dates and warnings set;
  dependency scan blocking. Enterprise: the control mapping checked against what is built.
- [ ] If the product calls a model: the evals passed every bar on the release commit.
- [ ] If the product has a UI: browser tests for every screen and role, and the owner's
  screen checklist done, with what they found recorded.
- [ ] The cost at the expected load and at ten times it fits the budget, or the owner
  accepted the risk in writing.
- [ ] Rollback rehearsed on staging.
- [ ] The not-tested list is filled in ("nothing" only after looking).

Show the owner the decision, the failures if any, the cost estimate and the not-tested list,
and ask for approval to launch. Record an explicit yes in `STATE.md` and say that **launch**
is next. A no-go sends the product back to build with new tasks in `tasks.md`.
