# The fix loop

What happens after a task check or a code check finds something, so that findings are fixed,
re-checked and closed, and a task that will not settle stops instead of looping forever.

## Before the loop

Sort the findings first:

- **Note** findings never enter the loop. Write each as a Change row in `JOURNAL.md` marked
  "open note" (or a task in `tasks.md`); the branch check reads them and decides which matter
  before release.
- A finding that **contradicts the task card or the PRD** is yours to rule on before anything
  is fixed: the card and the PRD win over a reviewer's taste, and a real conflict goes to the
  owner. Write the ruling down.
- Every **must fix**, every **should fix** you are not explaining away with evidence, and every
  task-check gap enters the loop. A should fix you explain away gets a Decision row in
  `JOURNAL.md` with the evidence.

A round closes review findings. It is not a second try at a bug: if a fix fails because the
cause is unknown (a test still fails for a reason nobody predicted, the behaviour is still
wrong), that is the debug skill's rule (find the cause; after two failed fixes, stop and
question the design), not another round.

## A round

One round is one fix by the builder plus one **scoped** re-check:

1. Send the builder the open findings word for word, with the file and line of each.
2. The builder fixes them test first (a finding about missing behaviour gets a failing test
   before the fix), runs the tests that cover the changed code, and adds a fix report to the
   same report: what changed, the tests run, the command, and the output.
3. Before the re-check, confirm the fix report has all three: the covering tests, the command
   and the output. If not, send it back; that is not a round.
4. The re-check is a fresh agent with the review skill's `re-check.md`: the findings list and
   only the diff of the fix (`git diff <commit the last check saw>...<now>`). For each finding
   it answers **addressed** or **not addressed**, and it reports any new must-fix breakage in
   the fix diff. Anything else it notices becomes a note, not a new round.
5. Add a Change row to `JOURNAL.md`: `T<id> fix round <n>/4: <addressed>, <open>`.

## How many rounds

- **Rounds 1 and 2:** the same builder, which still knows the task and its own choices. An
  outside builder gets the findings in a new brief with its earlier report attached.
- **Rounds 3 and 4:** a fresh builder, on a stronger model if one is available, told "an
  earlier builder tried this <n> times; you own it now; read its report". Two failed rounds
  usually mean the first builder cannot see its own problem.
- **After round 4,** stop sending fixes. Rule on each open finding yourself, and write each
  ruling as a Decision row in `JOURNAL.md`:
  - **The reviewer is wrong:** say why, with the line, the test or the requirement.
  - **Real, but nothing depends on it:** a new task in `tasks.md`.
  - **Real, and it must be fixed before this merges** (a wrong result, lost data, a leak): the
    findings were probably unclear to the builder. Write a new, narrow card yourself, with the
    failing test that shows the problem; give it to a fresh builder as a new task (not a fifth
    round), and tell the owner the task is held until it lands.
  - **Real, and later tasks depend on it, or it shows the design is wrong:** stop the
    milestone and bring it to the owner as a design question, as the debug skill does when
    fixes keep failing. Do not build on it.

Rule only at the cap, never earlier to end a loop sooner. A finding dropped without a ruling
is the one that comes back in production.

## Two shortcuts that are not allowed

- **Fixing it yourself to save a round.** If you do fix something, it gets the same scoped
  re-check, and a **Fix in review** row says what the builder missed and why.
- **Re-running the full check instead of the scoped one.** A full re-review finds new
  opinions, and the loop never ends. Scope it to the findings and the fix diff.

## Items the checker could not verify

A check may report requirements it cannot see from the diff: behaviour in code that did not
change, or something that spans tasks. Resolve each one yourself before the task is done:
read the code, run the test, or ask the owner. If it turns out to be a real gap, it joins the
open findings and enters the loop.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "Round 5 will get it." | Four rounds is the cap. Rule on each open finding and record it. |
| "I'll just fix the last finding myself." | Then it gets the scoped re-check and a Fix in review row, like any fix. |
| "Re-review the whole task, to be safe." | Scope the re-check to the findings and the fix diff, or the loop never ends. |
| "It's only a note, I'll drop it." | Write it down. The branch check decides what notes matter. |
