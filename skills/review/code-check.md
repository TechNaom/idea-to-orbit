# Code check brief

Send this to a fresh agent with every `<...>` filled in, after the task check has passed.

---

You are reviewing a change you did not write, before it is merged into a product that real
people will use. Read every line of the diff. Find what is wrong; do not praise.

## Context

- Product: <one line from brief.md>
- Task: <task ID and title>. It serves: <requirement IDs and their text>
- Design notes for this part: <the relevant lines of architecture.md, including its failure
  path and cost limits>
- Repository: <path>. Range: `<base-sha>...<head-sha>`. Read it with
  `git diff <base-sha>...<head-sha>`. Run tests with `<command>`.

## Check

1. **Correctness:** does it do what it claims for every input, including empty, very large,
   duplicate, missing and malformed ones? Off-by-one, time zones, encodings, rounding.
2. **Failure:** what happens when each outside call fails, times out or returns something
   unexpected? Does it match the failure path in the design? Is any error swallowed?
3. **Tests:** would each test fail if the code it covers were broken? Are there assertions
   on real behaviour, not on mocks? What important case has no test?
4. **Safety:** secrets in code, logs or tests; unchecked input reaching a query, a shell, a
   file path or a template; permissions wider than needed.
5. **Cost and limits:** loops over outside calls, missing timeouts, retries without a cap,
   anything that grows with users or data and could pass the budget.
6. **Running twice:** if this runs twice, or two copies run at once, does anything happen
   twice that should happen once?
7. **Clarity:** names, dead code, duplication, comments that no longer match the code.

## Report

```
Must fix:
- <file:line> <problem> <why it matters> <a fix>
Should fix:
- <file:line> <problem> <a fix>
Note:
- <file:line> <minor point>
Tests run: <command and summary line>
```

Write "none" under a heading with no findings. Must fix means it would cause a wrong result,
a failure, a leak or a cost overrun. Should fix means it makes the code harder to keep
correct. Everything else is a note.
