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

1. Set up the workspace if it is missing: create `docs/orbit/` and copy
   `templates/state.md` to `docs/orbit/STATE.md`. Fill in the product name and today's date.
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
   Do not invent answers. Mark anything unanswered as an open question in `STATE.md`.
4. Write `docs/orbit/brief.md` from `templates/brief.md`: one page, plain words.
5. Write `docs/orbit/prd.md` from `templates/prd.md`. Every requirement gets an ID
   (R1, R2, ...) and an acceptance check, so later stages can trace it.
6. Run the gate.

## Gate

Exit list:
- [ ] The problem and the users are specific (a real person could be named as an example).
- [ ] The first version's scope fits on one screen, and out of scope is written down.
- [ ] Every requirement has an ID and an acceptance check.
- [ ] Success measures are measurable.
- [ ] Budget and deadline are stated, or recorded as open questions.

Show the owner a short summary (problem, users, first-version scope, success measures, open
questions) and ask for approval. Only an explicit yes passes. Record it in `STATE.md` with
the date, set the stage to `approved`, and say that **blueprint** is next.
