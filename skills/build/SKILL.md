---
name: build
description: "Idea to Orbit stage 4. Use for ANY change to a product's code, tests, config or prompts, however small or urgent: \"just do it\", \"a two-minute change\", \"only a test\", \"one line\", a task card to carry out, the next task, or a bug fix. Builds one task at a time under one rule: no production code without a failing test first; a model setting (temperature, tools, a model ID) gets one real call before a test pins it. Each task goes to a fresh builder (a subagent or an outside agent such as Cursor), then a task check and a code check by two more fresh agents, then a commit, a push and a pull request; each milestone gets a branch review."
---

# Build: test-first, one task at a time

Goal: working code where every task is proven by a test that was written, run and seen to fail
before the code existed, and where every change was checked by someone who did not write it.

## The iron rule

**No production code without a failing test first.**

Write the test. Run it. Watch it fail, for the reason you expect. Only then write the code.
Code written before its test is deleted and written again after the test, not kept "as a
reference". This holds for features, bug fixes, refactors and one-line changes, in every
stage, however urgent the request. If the owner asks to skip it, say what the test would
protect, then follow their decision and record it as a Skipped rule row in `JOURNAL.md`, with a
line in the `STATE.md` log.

## Inputs

The approved `docs/orbit/tasks.md`, with a task card for every task in the milestone being
built. Assemble must be `approved` in `STATE.md`. If a card is missing or vague, stop and
write it (see the assemble skill) before building that task.

## Set up, once per milestone

1. Read the **Settings** in `STATE.md`: the code host, the work branch, who builds, and the
   test commands. Below, "the work branch" is that branch (`main` unless it says otherwise),
   and "pull request" means a merge request on GitLab.
2. Pull and rebase: other sessions may be working in the same repository.
3. Run the full test suite on the work branch and record the count. If it is not green, fix
   that first: you cannot tell a new failure from an old one on a red baseline.
4. Decide how tasks will run:
   - **Delegated** (the default, when the Agent tool is available): a fresh builder agent per
     task, with no memory of this conversation, briefed from `builder-brief.md`.
   - **Outside builders**, when **Builders** names Cursor, Kiro or another CLI agent: the
     same loop, with a launcher, an allow-list and a check on the first command. Read
     `external-builders.md` before the first task. While an outside builder runs, read its
     log within a minute or two of the start, and again whenever you are about to do other
     work: did its shell commands run, or were they refused? A running process is not a
     working builder.
   - **Solo**: you build each task yourself, in this session, following the same loop.
   - **Parallel**: tasks with no dependency on each other and no shared files run at the
     same time, each in its own worktree. See `parallel.md`.

## Token guard: the builders are an AI system too

Agents cost tokens, and the owner's plan or API budget is finite. Even a product that calls no
model is built by one, so the build has its own guards (N7 to N10 in the PRD):

- **Ledger:** every agent run is a row in `docs/orbit/token-ledger.md` (from
  `templates/token-ledger.md`): stage, task, role, model, tokens as the harness reports them,
  result. Per task: tokens against its budget, first-pass task check, fixes in review.
- **Estimate first:** before each milestone, write its expected tokens from the task sizes
  (defaults: S 60k, M 150k, all agents together) and compare with what the plan has left.
- **Lean by default:** an S task with pure code and no CI, security or UI change may be built
  solo and gets **one combined check** (task and code, in one fresh agent on a smaller model);
  M tasks and any CI, security, money or UI change keep the two separate checks. Briefs point to
  the card file instead of pasting documents; checkers get the diff and the card only.
- **At the limit:** stop cleanly with the work saved (uncommitted is fine, recorded in
  `STATE.md`), and resume the same agent after the reset rather than starting a new one.
- Over budget: record why in the ledger; the learn skill looks at those rows first.

## The loop, for each task

1. **Pick** the next task whose dependencies are done. Say which one and why.
2. **A model setting?** If the task adds or changes a setting sent to a model (temperature,
   top_p, tools, a response format, a model ID), make one real call to that model with the
   setting before anything pins it in a test or a config, and quote the reply. If this
   session cannot make the call, stop: tell the owner the exact call to run and do not write
   the test or the change until its result is known. A test against a stub passes even when
   the real model refuses the setting.
3. **Branch:** `t<id>-<slug>` from an up-to-date work branch, in its own worktree when
   running in parallel or with outside builders.
4. **Brief** the builder from `builder-brief.md`, pasting in the full task card, the
   requirement text it serves and the relevant part of `architecture.md`. Never tell it to
   "read the plan": give it what it needs.
5. **Build:** the builder follows the card step by step:
   - **Red:** write the test from the card. Run it. Show it fails, and why.
   - **Green:** write the smallest code that passes. Run the whole suite.
   - **Clean:** tidy names and duplication with the suite still green. No new behaviour.
   - **Commit** each green step with a clear message. An outside builder does not commit:
     it leaves its changes in the worktree, and you commit them (see
     `external-builders.md`).
   - **Report** using the report form in the brief: status, what was built, test output, and
     any doubts.
6. **Handle the report:**
   - `done`: go to the checks.
   - `done with doubts`: read the doubts. Fix anything about correctness or scope before the
     checks; note the rest for the code check.
   - `needs context`: give the missing context and send the task back.
   - `blocked`: find out why. Give more context, split the task, or bring a design question
     to the owner. Never send the same task back unchanged.
   - **Tests the builder could not run** (no shell, a missing service, a refused command):
     the task is not done. Run them yourself now and read the output. Until they have run,
     everything in the report about them is a claim.
7. **Task check:** a second fresh agent compares the diff with the task card, line by line:
   does it do everything the card asks, and nothing it does not? Use the review skill's
   `task-check.md`. Every gap goes through the fix loop (`fix-loop.md`): the builder fixes
   it, a scoped re-check confirms it, four rounds at most. Do not start the code check until
   the task check passes.
8. **Code check:** a third fresh agent reviews the diff for correctness, edge cases, error
   handling, tests, secrets and cost. Use the review skill's `code-check.md`. Every "must
   fix", and every "should fix" you cannot explain away with evidence, goes through the fix
   loop. Items a check could not verify from the diff are yours to resolve before the task
   is done (see `fix-loop.md`).
9. **Verify:** run the card's done check and the full suite yourself, and read the output.
   A report saying "tests pass" is a claim, not evidence. When the full suite is slow, the
   verify skill says what counts instead.
10. **Push and pull request:** push the branch and open a pull request (`gh pr create`, or
   `glab mr create`) into the work branch that names the task, its requirement IDs, the test
   count before and after, and both check results. Merge only when CI is green for that
   exact commit and the repository's merge rules allow it. Close the task's issue with a
   link to the pull request.
11. **Record:** mark the task done in `tasks.md`, add a line to the log in `STATE.md` and a
    row to `JOURNAL.md`. If you or a check fixed something the builder missed, record it as
    **Fix in review**: what was missed, by whom, and why. Those rows show where the cards or
    the checks need to improve.

**Batch small changes of the same shape.** When several tasks are each the same small edit
(one constant, one field, the same one-line fix in many files), give them to one builder in
one brief that lists every file and its change, with one test that covers them all, and
check the diff as one unit. Keep one builder per task for work that needs its own judgment,
its own tests or its own review.

Solo mode uses the same loop: you build, then the two checks still run as separate fresh
agents. Without the Agent tool, do each check as its own pass: re-read the card and the full
diff from the start, as if someone else wrote it, and write the findings down before fixing.

## At the end of each milestone

1. **Branch review:** one fresh agent reviews everything merged in the milestone together,
   using the review skill's `branch-check.md`: how the pieces fit, duplication across tasks,
   and anything the per-task checks could not see.
2. Show the owner what works now, with real output, before the next milestone starts.
3. Write or refresh the task cards for the next milestone using what this one taught, and
   run a cold read on them (the review skill's `cold-read.md`).
4. Run the learn skill on this milestone's journal rows.

## When something goes wrong

- A test fails in a way you did not expect, a bug appears, or a fix did not work: stop and
  use the debug skill. No more changes until the cause is known.
- A task turns out bigger than M: stop and split it in `tasks.md`.
- The design must change: stop, write or update the ADR, mark the blueprint `needs review`
  in `STATE.md`, and ask the owner.
- Never weaken, skip or delete a test to make it pass. If the test is wrong, say so and fix
  it as its own change, with its own reason.
- Never commit secrets. New settings go in `.env.example` with a placeholder.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "It's a one-line change, it doesn't need a test." | One-line changes break production too. Write the test. |
| "I'll write the tests after, it's faster." | Tests written after code pass by design and prove nothing. Delete the code, write the test. |
| "I already know it works, I tested it by hand." | A manual check is gone the moment you close the terminal. Turn it into a test. |
| "The test passed the first time I ran it." | Then it never failed. Make sure it can fail: break the code on purpose, watch it go red. |
| "The builder said the tests pass." | Run them yourself and read the output. |
| "The outside builder is running; I'll check when it's done." | Read its log now: a refused builder can run for an hour and end blocked. |
| "The task check is enough, skip the code check." | They look for different things. Run both. |
| "The review found nothing, that was quick." | Ask for a second look at the riskiest file, or check the reviewer had the full diff. |
| "This is urgent, the owner wants it now." | Urgent work is where shortcuts hurt most. Do the loop; it is minutes, not hours. |
| "I'll fix this unrelated thing while I'm here." | Out of scope. Note it as a new task. |
| "Let me just try another fix." | Two failed fixes means you do not know the cause. Use the debug skill. |
| "I'll plan it from the comparison and ask which step to build." | A new feature needs its lane's ignite first: requirements with checks, out of scope, the owner's yes. |
| "One more fix round will settle it." | Four rounds is the cap. Then rule on each open finding and record it. |
| "The builder couldn't run the tests, but the code looks right." | Run them yourself. Until then the task is not done. |
| "I'll disable this flaky test for now." | Flaky means a real race or a bad test. Debug it; do not silence it. |
| "Mock everything, then it's easy to test." | A test of mocks tests nothing. Mock only what crosses the product's edge. |
| "Pin the model setting in a test, it's obviously supported." | Make one real call with it first. Models refuse settings (temperature, top_p, tools), and a test against a stub passes anyway. |
| "I fixed the builder's miss myself, no need to note it." | Record it as Fix in review in `JOURNAL.md`. Unrecorded fixes hide which cards and checks fail. |

## Gate

Exit list:
- [ ] Every task in `tasks.md` is done, with a merged pull request and a closed issue.
- [ ] Every task had a test seen failing before its code, a task check and a code check.
- [ ] Every milestone had a branch review, and its findings are fixed or recorded as tasks.
- [ ] The full test suite and CI are green on the work branch, and you ran it yourself (or,
  for a slow suite, as the verify skill says).
- [ ] Every fix made in review is a row in `JOURNAL.md`.
- [ ] No open TODOs that block a requirement.

Show the owner the milestones delivered, the test count, the checks' findings and how they
were resolved, and anything deferred. Ask for approval. Record an explicit yes in `STATE.md`
and say that **test-flight** is next.
