---
name: assemble
description: "Idea to Orbit stage 3. Break an approved architecture into small, ordered, testable tasks, each traced to requirements, with a test and a done check, and create them as GitHub issues. Use after blueprint is approved, or when the owner asks for a task breakdown or a build plan."
---

# Assemble: the task breakdown

Goal: a build plan where every task is small enough to finish and verify in one sitting, and
nothing in the PRD is left without a task.

## Inputs

The approved `docs/orbit/architecture.md` and `docs/orbit/prd.md`. Blueprint must be
`approved` in `STATE.md`.

## Steps

1. Split the work into **milestones** that each leave the product working, for example:
   skeleton deployed, first real flow, all must-have requirements, hardening.
2. Inside each milestone, write **tasks** using `templates/tasks.md`. Each task has:
   - an ID (T1, T2, ...) and a short title
   - the requirement IDs it serves
   - the test that proves it (written before the code, in the build stage)
   - a done check anyone can run
   - its dependencies (task IDs)
   - a size: S (under an hour), M (a few hours). Split anything bigger.
3. Put the first tasks in this order: repository and CI, budget guard and `.env.example`,
   a walking skeleton deployed end to end, then features. Operations tasks (health check,
   alerts, backup tag, rollback) belong in the plan, not after it.
4. Write a **task card** for every task in the first milestone (see below). Cards for later
   milestones are written when each milestone starts, using what the earlier ones taught.
5. Check coverage: every requirement ID maps to at least one task. List any gaps.
6. Write `docs/orbit/tasks.md`.
7. After the gate passes, create one GitHub issue per task (`gh issue create`), labelled
   with its milestone, with the test and done check in the body. Record the issue numbers
   in `tasks.md`. Ask before creating issues in a repository the owner has not named.

## Task cards

A task card is what a builder needs to do the task without guessing, and without having seen
the conversation. Write it as if for a capable developer who has never seen this product.

Each card has:

- **Files:** every file to create or change, with its full path, and the test file.
- **Steps:** small steps of a few minutes each, in order. Each step says what to write, the
  exact command to run, and the expected output: the failing test first, then the pass.
- **Interfaces:** the exact names, arguments and return values the task adds or uses, so
  tasks built by different agents fit together.
- **Done check:** the command that proves the task is done, and what it prints.
- **Watch out:** the edge cases and failure paths from `architecture.md` that apply here.

Use real names, never placeholders such as "add error handling" or "write tests for the
above". If a step cannot be written precisely, the design is not finished: go back to the
blueprint for that part, or ask the owner.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "This task is big but it's all one thing." | Bigger than M means split it. A task you cannot check in one sitting hides problems. |
| "The builder will work out the details." | The card names the files, the steps, the commands and the expected output. |
| "Tests can be a task at the end." | Every task carries its own test, written first. |
| "Monitoring and rollback come after launch." | Health check, alerts, backup tag and rollback are tasks in the plan. |
| "The first milestone can just be setup." | The first milestone ends with something deployed and working end to end. |
| "I'll write cards for every task now." | Cards for the next milestone only. Later cards are written when that milestone starts, using what was learned. |

## Gate

Exit list:
- [ ] Every requirement ID has at least one task.
- [ ] Every task has a test, a done check, dependencies and a size of S or M.
- [ ] Every task in the first milestone has a card with files, steps, commands and expected
  output.
- [ ] The first milestone ends with something deployed and working end to end.
- [ ] Budget guard, CI and operations tasks are in the plan.

Show the owner the milestones, the task count per milestone and any coverage gaps, and ask
for approval. Record an explicit yes in `STATE.md`, create the issues, and say that
**build** is next.
