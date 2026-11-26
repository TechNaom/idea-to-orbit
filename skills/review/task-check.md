# Task check brief

Send this to a fresh agent with every `<...>` filled in.

---

You are checking one change against the task it was built for. You did not write it. Your
only question: does the change do everything the task card asks, and nothing it does not?
Do not judge code style or quality; another check does that.

## The task card

<the full task card from tasks.md>

## The requirements it serves

<the text of each requirement ID on the card>

## The change

Repository: <path>. Range: `<base-sha>...<head-sha>`. Read it with
`git diff <base-sha>...<head-sha>` and open any file you need for context.

## What to check

1. Every step on the card: is it done? Point to the lines and the test for each.
2. The test written first: does it test what the card says, and would it fail if the
   feature were removed? Read the assertion, not the name.
3. The done check on the card: run it if you can. Report its output.
4. Anything in the change that the card does not ask for: new features, extra options,
   unrelated refactors, changed files the card does not name.
5. Anything the card asks for that is only partly done, stubbed or left as a TODO.

## Report

```
Result: pass | fail
Done: <each card step, with the file:line and test that shows it>
Missing: <card steps not done or only partly done, or "none">
Extra: <changes the card does not ask for, or "none">
Done check: <command and output, or why it could not be run>
Could not verify: <a requirement or behaviour you could not check from the diff, and why>, or "none"
```

Pass only when Missing and Extra are both "none".
