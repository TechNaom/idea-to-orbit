---
name: verify
description: "Idea to Orbit helper. Evidence before claims: before saying anything is done, fixed, passing, deployed, approved or working, run the command that proves it in this session, read its full output, and quote it. Use before every status update, every gate summary, every pull request description and every 'it works' to the owner."
---

# Verify: evidence before claims

Goal: the owner can trust every status line without checking it, because each one comes
with the evidence that proves it.

## The rule

**No claim without fresh evidence.** "Fresh" means from a command run in this session, after
the last change, with its output read in full. Memory, an earlier run, another agent's
report and "it should work" are not evidence.

## Steps, before any claim

1. **Name the claim.** "The tests pass." "The bug is fixed." "The email was delivered."
2. **Name the proof.** The one command or check that would show the claim is false if it
   were. See the table below.
3. **Run it now,** after the last change.
4. **Read all of the output:** the summary line, the exit code, skipped tests, warnings.
5. **Say what it shows,** with the key lines quoted. If it shows less than the claim, make
   the smaller claim: "12 of 13 pass; one is skipped because ...".

| Claim | Proof | Not proof |
|---|---|---|
| Tests pass | The full suite run now, its summary line and exit code | A run before the last edit; one test file; a builder's report |
| Bug fixed | The test that reproduced it, red before and green now | "The error stopped showing" |
| Task done | The card's done check, run now | All the steps were followed |
| Build or CI green | The CI run for this exact commit | Green on the previous commit |
| Deployed | The live version or commit, read from the running product | The deploy command finished |
| Delivered | The result seen where the user sees it: the email in the inbox, the post on the page | The send call returned 200 |
| Requirement met | Its acceptance check from the PRD, run now | The code that should meet it exists |
| Gate approved | The owner's yes, in this conversation | The owner seemed happy |

## Words to avoid without proof

"Should work", "probably", "seems to", "I think it's fixed", "done" (without the done check),
"all good". When you notice one of these in your own reply, run the check or remove the
claim.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "I ran it a minute ago." | Was that before the last change? Run it again. |
| "The agent reported that it passes." | Run it yourself and read the output. |
| "It's a tiny change, it can't have broken anything." | Run the full suite. That is what it is for. |
| "The command succeeded, so it worked." | Succeeded means it exited. Check that it did the job. |
| "I'll say it's done and check after." | Check, then say. |
| "I can't run that check here." | Say exactly that, and what is unproven. Never fill the gap with a guess. |
