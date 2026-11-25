---
name: review
description: "Idea to Orbit helper. Get a change checked by a fresh agent that did not write it, and handle the findings well. Three checks: the task check (does the change do exactly what its task card asks), the code check (correctness, edge cases, tests, secrets, cost) and the branch check (a whole milestone together). Use in build after every task and milestone, before merging any change to a product, or when review feedback arrives."
---

# Review: a fresh pair of eyes on every change

Goal: no change reaches main checked only by the agent that wrote it. The writer knows what
the code is meant to do, so they read what they meant, not what they wrote. A reviewer
with no memory of the work reads what is there.

## The three checks

| Check | Asks | When | Brief |
|---|---|---|---|
| Task check | Does the change do everything the task card asks, and nothing it does not? | After each task is built | `task-check.md` |
| Code check | Is the code correct, safe, tested and affordable? | After the task check passes | `code-check.md` |
| Branch check | Do the pieces fit together? | At the end of each milestone, or before a release | `branch-check.md` |

Run them in this order. A code check on a change that does the wrong thing wastes the
review.

## Asking for a check

1. Get the exact range: `git diff <base>...<head>` with the two commit hashes, so the
   reviewer sees every line and nothing else.
2. Start a fresh agent (the Agent tool) with the brief for that check, every `<...>` filled
   in. Paste the task card and the requirement text; do not tell it to go and find them.
3. Do not tell the reviewer what you think is wrong or right, and do not summarise the
   change for it. Let it read.
4. Without the Agent tool: do the check yourself as a separate pass, starting from the card
   and the full diff, and write the findings down before you fix anything.

## Handling the findings

Every finding gets one of three answers, written down:

- **Fixed:** changed, with the test that proves it. Then ask for the check again.
- **Wrong:** the reviewer misread something. Say what, with evidence: the line, the test,
  the requirement. Do not argue from memory.
- **Later:** real but out of scope. Add a task to `tasks.md` and say which one.

Rules:

- Check a finding against the code before acting on it. A confident reviewer can be wrong.
- Never reply "good catch, fixed" without the fix and its test in the same step.
- Do not accept a finding that contradicts the task card or the PRD without asking the
  owner. The card wins over a reviewer's taste.
- "Must fix" findings block the merge. "Should fix" findings are fixed or explained.
  "Note" findings are optional.
- If a check finds nothing on a large or risky change, ask a second fresh agent to look at
  the riskiest file. An empty review is not proof of a clean change.

## Feedback from people

The same answers apply to review comments from the owner or anyone else: fixed, wrong
(with evidence), or later (with a task). Ask when a comment is unclear; do not guess what
was meant and change code on the guess.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "I wrote it carefully, I can review it myself." | You will read what you meant. Use a fresh agent. |
| "I'll tell the reviewer what to focus on." | You will steer it away from what you missed. Give it the brief and the diff. |
| "The reviewer said it's fine, merge." | Read the findings. Check the reviewer saw the full range. |
| "This finding is just style, ignore it." | Answer it: fixed, wrong or later. Silence is not an answer. |
| "The reviewer is surely right." | Check it against the code and the card first. |
