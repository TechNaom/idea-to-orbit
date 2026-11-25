---
name: debug
description: "Idea to Orbit helper. Find the root cause of a bug, a failing test, a broken build or a production incident before changing any code: reproduce it, read the evidence, test one idea at a time, prove the cause with a failing test, then fix it once. Use whenever something does not work as expected, a fix did not work, or a test fails for a reason nobody predicted."
---

# Debug: find the cause before the fix

Goal: every fix addresses the real cause, is proven by a test that failed before it, and is
made once. A fix that works by luck hides the bug until the worst moment.

## The rule

**No fix without a known cause.** Until you can say "it fails because X, and here is the
evidence", you are still investigating, and you change no production code.

## Steps

1. **Stop changing things.** Note what was changed since it last worked. If you have already
   tried fixes, list them and undo the ones that did not help.
2. **Reproduce it.** Find the smallest command that shows the failure every time. If it only
   fails sometimes, find what differs between a good run and a bad one: timing, order, data,
   environment. Write down the command and its output.
3. **Read the evidence, all of it.** The full error and stack trace, the logs around it, the
   inputs. Read the first error, not the last; later errors are often caused by the first.
4. **Trace it back.** Start where it fails and walk back towards where the bad value or
   state came from. At each step, check the value; do not assume it. Add a log line or a
   breakpoint to see it when reading the code is not enough.
5. **Compare with something that works.** A passing test, an earlier commit, the same call
   in another place. List every difference. `git bisect` finds the commit that broke it when
   there is a known good one.
6. **One idea at a time.** State a hypothesis: "it fails because X". Predict what you will
   see if it is true. Run one check that tells you. If it is wrong, cross it out and form the
   next one. Never change two things at once.
7. **Prove it with a test.** Write a test that fails because of the cause you found. Run it
   and watch it fail. This test is the start of the fix; it goes into the build loop.
8. **Fix the cause, once.** The smallest change at the place the problem starts, not where it
   shows. Run the new test and the whole suite.
9. **Look for siblings.** Search for the same mistake elsewhere: the same call, the same
   pattern, the same assumption. Each one found gets its own test.
10. **Record it.** In a live product, write the incident in `docs/orbit/rca/` (see the orbit
    skill). In build, put the cause and the test in the pull request description.

## When the third fix fails

If two fixes have failed and you are about to try a third, stop. Repeated failures mean the
cause is not where you are looking, or the design itself is wrong: a shared state that two
parts both change, a timing assumption, a missing boundary. Write down what you know, what
you tried and what each attempt showed, and bring it to the owner with a question about the
design. This is a finding, not a failure.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "I can see the problem, let me just fix it." | Then proving it costs one test. Write the test first. |
| "Let me try this and see if it helps." | That is a guess. State the hypothesis and what it predicts. |
| "I'll change these three things at once to save time." | You will not know which one mattered. One at a time. |
| "Wrap it in a try/except so it stops failing." | That hides the bug. Find why it fails. |
| "Add a retry, it's probably flaky." | Flaky has a cause: a race, an order, a limit. Find it. |
| "It works on my machine." | Then the difference is the cause. List the differences. |
| "The error message is misleading, ignore it." | Read it again, slowly. Then read the one before it. |
| "It's fixed, the error went away." | Did the test that reproduced it go from red to green? If there was none, there is no proof. |
| "One more fix and it will work." | After two failed fixes, stop and question the design. |
