# Re-check brief

Send this to a fresh agent after a fix round (see the build skill's `fix-loop.md`), with every
`<...>` filled in. It checks only whether the findings were fixed, so the loop ends.

---

You are checking a fix you did not write. An earlier check found the problems below; a builder
has tried to fix them. Your only questions: is each finding fixed, and did the fix break
anything? Do not review the rest of the task; another check did that.

## The findings

<each open finding, word for word, with its file and line>

## The fix

Repository: <path>. Range: `<commit the last check saw>...<head>`. Read it with
`git diff <commit the last check saw>...<head>`. The builder's fix report: <paste it: what
changed, the tests run, the command and the output>.

## What to check

1. Each finding: is it fixed? Point to the line and the test that shows it.
2. The tests in the fix report: would each fail if the fix were undone?
3. The fix diff only: anything it breaks that is a must fix (a wrong result, a failure, a leak,
   a cost overrun).

## Report

```
Findings:
- <finding>: addressed | not addressed, <file:line and test>
New must fix in the fix diff: <file:line problem>, or "none"
Notes: <anything else, which will not start another round>, or "none"
```
