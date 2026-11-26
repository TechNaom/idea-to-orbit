---
name: learn
description: "Idea to Orbit helper. Learn from the product's own history: group the roadblocks, review fixes, incidents and skipped rules in JOURNAL.md, STATE.md and rca/ by cause, find the patterns that keep costing time, and turn each top pattern into a check, a red flag, a card or brief change, or an eval case. Use at the end of a milestone, after an incident, when the same kind of problem has happened twice, or when the owner asks what is slowing the work down."
---

# Learn: turn repeated trouble into checks

Goal: the same kind of problem does not cost time three times. Every pattern the history
shows becomes something that catches it earlier: a check in code or CI, a red flag in a
skill, a line on a card or brief template, or an eval case.

## Inputs

`docs/orbit/JOURNAL.md` (or the product's own journal, if `STATE.md` points to one), its
Skipped rule rows, the log in `STATE.md`, and `docs/orbit/rca/`. If the product keeps no
journal yet, start one from the ignite skill's `templates/journal.md` and say that there is little to learn
from until it has rows.

## Steps

1. **Collect.** Every Roadblock, Fix in review, Skipped rule and incident since the last
   learn run (or all of them, the first time). Note each one's date, cost (time lost, failed
   pipelines, rework) and stated cause.
2. **Check the causes.** A cause written as "flaky", "a blip" or "fixed it" is not a cause.
   Where a row names a symptom, read its evidence (the commit, the CI run, the RCA) and write
   the real cause, or mark it unknown.
3. **Group by cause, not by symptom.** For example: a builder's shell refused its commands;
   a test in an unexpected folder broke; a model refused a setting; a deploy rolled back for
   a config value; a check that could not fail. One group per cause, with a count and the
   total cost.
4. **Rank** the groups by count times cost. The top three to five are the patterns.
5. **For each pattern, choose the cheapest thing that would have caught it earliest.** Most
   lessons belong to the product:
   - a check in the product's code or CI (a test, a lint rule, a pre-push step): best,
     because it runs every time without anyone remembering;
   - a line on the product's cards in `tasks.md`, or in its own brief or card notes, so every
     future task carries it;
   - a line in the product's `CLAUDE.md` (or the file its agents read first).
   Write each as a task or a fix lane (see `/orbit`), test first like any other change.
   Some lessons are about Idea to Orbit itself: a skill missed a step, a red flag was
   missing, a template had no field for it. Do not edit the installed plugin (an update
   overwrites it); propose the change to the plugin's maintainers as an issue or pull request,
   with the journal rows as evidence and, for a behaviour under pressure, a draft eval case.
6. **Report** to the owner: the patterns, their counts and cost, and the change proposed for
   each. Add a Decision row to the journal for what the owner picks.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "Each of these was a one-off." | Group by cause. Three one-offs with the same cause are a pattern. |
| "The lesson is to be more careful." | Careful does not scale. Find the check that catches it without anyone remembering. |
| "I'll add a red flag for every row." | Rank first. A skill with forty red flags gets none of them read. |
| "The journal says the cause was a flaky test." | Flaky has a cause. Read the evidence and write the real one, or mark it unknown. |
| "This history is too short to learn from." | Say so, and keep the journal. Two rows with the same cause are already worth a check. |
