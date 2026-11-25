---
name: build
description: "Idea to Orbit stage 4. Build an approved task list one task at a time, test-first: write the failing test, make it pass, review, commit and push in small steps, and close the task's issue. Use after assemble is approved, or when the owner asks to build the next task."
---

# Build: test-first, one task at a time

Goal: working code where every task is proven by a test that was written before the code.

## Inputs

The approved `docs/orbit/tasks.md`. Assemble must be `approved` in `STATE.md`.

## The loop, for each task

1. **Pick** the next task whose dependencies are done. Say which one and why.
2. **Branch:** one branch per task, named `t<id>-<slug>`. Pull and rebase first, since other
   sessions may be working in the same repository.
3. **Red:** write the test from the task's test column. Run it and show that it fails for
   the right reason.
4. **Green:** write the smallest code that makes it pass. Run the whole test suite.
5. **Clean:** tidy names and duplication with the tests still green. No new behaviour.
6. **Review:** read the full diff as a reviewer would: correctness, edge cases, error
   handling, secrets, cost. For larger tasks, use a separate review pass or a subagent
   with no context from writing the code. Fix what it finds.
7. **Commit and push:** small commits with clear messages, pushed as soon as they work.
   Open a pull request that names the task and its requirement IDs.
8. **Done check:** run the task's done check. Merge only when CI is green and the owner's
   merge rules for the repository allow it. Close the issue with a link to the pull request.
9. **Update** `tasks.md` (mark the task done) and the log in `STATE.md`.

## Rules

- Never weaken or delete a test to make it pass. If the test is wrong, say so and fix it as
  its own change.
- Never commit secrets. New settings go in `.env.example` with a placeholder.
- If a task turns out bigger than M, stop and split it in `tasks.md`.
- If the design must change, stop, write or update the ADR, and ask the owner. Mark the
  blueprint `needs review` until they answer.
- At the end of each milestone, show the owner what works now, with output, before the
  next milestone.

## Gate

Exit list:
- [ ] Every task in `tasks.md` is done, with a merged pull request and a closed issue.
- [ ] The full test suite and CI are green on main.
- [ ] No open TODOs that block a requirement.

Show the owner the milestones delivered, the test count and anything deferred, and ask for
approval. Record an explicit yes in `STATE.md` and say that **test-flight** is next.
