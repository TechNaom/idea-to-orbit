---
name: ignite
description: "Idea to Orbit stage 1. Turn a rough product idea into an approved brief and PRD by asking the owner questions until the problem, users, scope and success measures are clear. Use when starting a new product, when the owner shares an idea to build, or when /orbit starts a product."
---

# Ignite: from idea to an approved PRD

Goal: the owner and Claude agree on exactly what to build and why, in writing, before any
design or code.

## Inputs

The idea in any form: a sentence, a voice note transcript, a list, an existing doc.

## Steps

1. Set up the workspace if it is missing: create `docs/orbit/`, copy `templates/state.md`
   to `docs/orbit/STATE.md` and `templates/journal.md` to `docs/orbit/JOURNAL.md`. Fill in
   the product name and today's date.
2. Read everything the owner gave. Note what is known and what is missing.
3. Ask questions, a few at a time, most important first. Cover:
   - **Problem:** what hurts today, for whom, how often, how they cope now.
   - **Users:** who uses it, who pays, who decides.
   - **Outcome:** what changes for the user when it works.
   - **Scope:** the smallest version worth shipping; what is explicitly out.
   - **Success:** measurable signs it works (numbers and dates where possible).
   - **Constraints:** budget per month, deadline, platforms, data and privacy, must-use or
     must-avoid tools.
   - **Risks:** what could make this fail or not worth it.
   - **How it is built:** the code host (GitHub, GitLab), the branches (one `main`, or a
     work branch such as `dev` that releases to `main`), who builds (Claude's subagents, or
     an outside agent such as Cursor or Kiro), and the profile: **startup** (scale to zero,
     free tier) or **enterprise** (a secret store, compliance, audit). These fill the
     **Settings** in `STATE.md`; every later stage reads them. The test commands and the
     suite's time are unknown before there is code: leave them for Assemble's first task.
   - **AI and screens:** does the product call a model, and does it have screens people
     use? If it calls a model, ask what it must get right and how well (for example "every
     figure matches the source; at most 1 answer in 20 not grounded"): those become eval bars,
     as requirements with IDs.
   Do not invent answers. Mark anything unanswered as an open question in `STATE.md`.
4. Write `docs/orbit/brief.md` from `templates/brief.md`: one page, plain words.
5. Write `docs/orbit/prd.md` from `templates/prd.md`. Every requirement gets an ID
   (R1, R2, ...) and an acceptance check, so later stages can trace it.
6. Run the gate.

## Existing product

When the repository already has code, catch the documents up from what exists instead of
asking from a blank page:

1. Pull first (other sessions may be working), then read the code, tests, README, history,
   CI and any design notes. Run the tests now and note the result, and how long they took.
2. **Fill the Settings** in `STATE.md` from what is there: the code host (the CI file and the
   remote), the branches and how they promote, who builds, the fast test command and the
   full suite with its time, and the profile. Mark each one you inferred.
3. **Map, don't copy.** If the product already keeps its own plan, task list, decision
   records or journal, point to them from `STATE.md` (for example "tasks: `docs/TASKS.md`")
   and use them as they are. Write an orbit document only where nothing covers it; if the
   product keeps no journal, copy `templates/journal.md` to `docs/orbit/JOURNAL.md`. Two
   copies of the same plan drift apart within a week.
4. Where step 3 found nothing, write `brief.md`, `prd.md` and `architecture.md` from what is built, each marked
   **reconstructed** with the date. Give every requirement a state (built, not built, or
   built but its acceptance check not met). Mark every line you inferred rather than read as
   *(inferred)*, so the owner can correct it.
5. **ADRs:** where the decisions and their options are already written down (a design doc,
   a README section), cite that source in `architecture.md` and list the decisions there;
   writing them as ADRs is an open question for the owner at the Blueprint gate. Where a
   decision has no written reason, write the ADR with "why" as a question for the owner.
6. **Work in flight:** anything half-done when the product joins (a running job, an
   unfinished branch, a stopped run) is recorded in `STATE.md` under **In flight**, with
   what is known about it, and paused until it is a task or a lane. Do not continue it.
7. Record gaps you found (no alerts, no spending cap, no rollback) as open questions.
8. Show the owner a short summary and ask whether this is an accurate picture of the product.
   Only an explicit yes records Ignite and Blueprint as `approved`. Then go on by where the
   product is: code but not deployed → Assemble; live without monitoring → Orbit setup
   (skill **keep-running**); live with a new feature → a feature lane (`/orbit`, Lanes).

Do not rewrite or redo code that works.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "The idea is clear enough, let's start building." | If the problem, the users and success are not written down, it is not clear. Ask. |
| "I'll fill in the details myself." | Your guess becomes the owner's product. Ask the question; mark it open if they don't know yet. |
| "Everything is a must-have." | Ask what the first version can ship without. A list with no out-of-scope section is not finished. |
| "Success means it works." | Success is a number the owner can check: users, time saved, money, errors. |
| "It's on GitHub and main, like most products." | Ask. The code host, the branches and the builders change every later stage. |
| "Let me sketch the architecture while we talk." | Design comes in blueprint, after the PRD is approved. |
| "The owner said 'sounds good', that's approval." | Only an explicit yes passes a gate. Ask for it. |

## Gate

Exit list:
- [ ] The problem and the users are specific (a real person could be named as an example).
- [ ] The first version's scope fits on one screen, and out of scope is written down.
- [ ] Every requirement has an ID and an acceptance check.
- [ ] Success measures are measurable.
- [ ] Budget and deadline are stated, or recorded as open questions.
- [ ] The Settings in `STATE.md` are filled in, except the test commands, or each gap is an
  open question.
- [ ] If the product calls a model, its eval bars are requirements with IDs.

Show the owner a short summary (problem, users, first-version scope, success measures, open
questions) and ask for approval. Only an explicit yes passes. Record it in `STATE.md` with
the date, set the stage to `approved`, and say that **blueprint** is next.
