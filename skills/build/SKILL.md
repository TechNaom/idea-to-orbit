---
name: build
description: "Idea to Orbit stage 4. Build an approved task list one task at a time under one rule: no production code without a failing test first. Each task goes to a fresh builder agent, then a task check and a code check by two more fresh agents, then a commit, a push and a pull request; the whole branch gets a final review. Use after assemble is approved, or when the owner asks to build the next task or fix a bug in a product."
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
protect, then follow their decision and record it in `STATE.md`.

## Inputs

The approved `docs/orbit/tasks.md`, with a task card for every task in the milestone being
built. Assemble must be `approved` in `STATE.md`. If a card is missing or vague, stop and
write it (see the assemble skill) before building that task.

## Set up, once per milestone

1. Pull and rebase: other sessions may be working in the same repository.
2. Run the full test suite on main and record the count. If it is not green, fix that first:
   you cannot tell a new failure from an old one on a red baseline.
3. Decide how tasks will run:
   - **Delegated** (the default, when the Agent tool is available): a fresh builder agent per
     task, with no memory of this conversation, briefed from `builder-brief.md`.
   - **Solo**: you build each task yourself, in this session, following the same loop.
   - **Parallel**: tasks with no dependency on each other and no shared files run at the
     same time, each in its own worktree. See `parallel.md`.

## The loop, for each task

1. **Pick** the next task whose dependencies are done. Say which one and why.
2. **Branch:** `t<id>-<slug>` from an up-to-date main, in its own worktree when running in
   parallel.
3. **Brief** the builder from `builder-brief.md`, pasting in the full task card, the
   requirement text it serves and the relevant part of `architecture.md`. Never tell it to
   "read the plan": give it what it needs.
4. **Build:** the builder follows the card step by step:
   - **Red:** write the test from the card. Run it. Show it fails, and why.
   - **Green:** write the smallest code that passes. Run the whole suite.
   - **Clean:** tidy names and duplication with the suite still green. No new behaviour.
   - **Commit** each green step with a clear message.
   - **Report** using the report form in the brief: status, what was built, test output, and
     any doubts.
5. **Handle the report:**
   - `done`: go to the checks.
   - `done with doubts`: read the doubts. Fix anything about correctness or scope before the
     checks; note the rest for the code check.
   - `needs context`: give the missing context and send the task back.
   - `blocked`: find out why. Give more context, split the task, or bring a design question
     to the owner. Never send the same task back unchanged.
6. **Task check:** a second fresh agent compares the diff with the task card, line by line:
   does it do everything the card asks, and nothing it does not? Use the review skill's
   `task-check.md`. Fix every gap it finds, then check again. Do not start the code check
   until the task check passes.
7. **Code check:** a third fresh agent reviews the diff for correctness, edge cases, error
   handling, tests, secrets and cost. Use the review skill's `code-check.md`. Fix every
   "must fix" finding; fix or explain every "should fix". Check again after fixes.
8. **Verify:** run the card's done check and the full suite yourself, and read the output.
   A report saying "tests pass" is a claim, not evidence. See the verify skill.
9. **Push and pull request:** push the branch and open a pull request that names the task,
   its requirement IDs, the test count before and after, and both check results. Merge only
   when CI is green and the repository's merge rules allow it. Close the task's issue with a
   link to the pull request.
10. **Record:** mark the task done in `tasks.md` and add a line to the log in `STATE.md`.

Solo mode uses the same loop: you build, then the two checks still run as separate fresh
agents. Without the Agent tool, do each check as its own pass: re-read the card and the full
diff from the start, as if someone else wrote it, and write the findings down before fixing.

## At the end of each milestone

1. **Branch review:** one fresh agent reviews everything merged in the milestone together,
   using the review skill's `branch-check.md`: how the pieces fit, duplication across tasks,
   and anything the per-task checks could not see.
2. Show the owner what works now, with real output, before the next milestone starts.
3. Write or refresh the task cards for the next milestone using what this one taught.

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
| "The task check is enough, skip the code check." | They look for different things. Run both. |
| "The review found nothing, that was quick." | Ask for a second look at the riskiest file, or check the reviewer had the full diff. |
| "This is urgent, the owner wants it now." | Urgent work is where shortcuts hurt most. Do the loop; it is minutes, not hours. |
| "I'll fix this unrelated thing while I'm here." | Out of scope. Note it as a new task. |
| "Let me just try another fix." | Two failed fixes means you do not know the cause. Use the debug skill. |
| "I'll disable this flaky test for now." | Flaky means a real race or a bad test. Debug it; do not silence it. |
| "Mock everything, then it's easy to test." | A test of mocks tests nothing. Mock only what crosses the product's edge. |

## Gate

Exit list:
- [ ] Every task in `tasks.md` is done, with a merged pull request and a closed issue.
- [ ] Every task had a test seen failing before its code, a task check and a code check.
- [ ] Every milestone had a branch review, and its findings are fixed or recorded as tasks.
- [ ] The full test suite and CI are green on main, and you ran it yourself.
- [ ] No open TODOs that block a requirement.

Show the owner the milestones delivered, the test count, the checks' findings and how they
were resolved, and anything deferred. Ask for approval. Record an explicit yes in `STATE.md`
and say that **test-flight** is next.
