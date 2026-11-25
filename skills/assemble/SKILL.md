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
4. Check coverage: every requirement ID maps to at least one task. List any gaps.
5. Write `docs/orbit/tasks.md`.
6. After the gate passes, create one GitHub issue per task (`gh issue create`), labelled
   with its milestone, with the test and done check in the body. Record the issue numbers
   in `tasks.md`. Ask before creating issues in a repository the owner has not named.

## Gate

Exit list:
- [ ] Every requirement ID has at least one task.
- [ ] Every task has a test, a done check, dependencies and a size of S or M.
- [ ] The first milestone ends with something deployed and working end to end.
- [ ] Budget guard, CI and operations tasks are in the plan.

Show the owner the milestones, the task count per milestone and any coverage gaps, and ask
for approval. Record an explicit yes in `STATE.md`, create the issues, and say that
**build** is next.
