# Troubleshooting

## `/orbit` is not recognised

The plugin is not installed or not enabled. Run `/plugin`, check that `idea-to-orbit` is in
the list and enabled, then restart Claude Code. If it is missing, install it again (see
[Getting started](getting-started.md)).

## Claude doesn't mention the product's stage at the start

The session-start hook did not run or found no `STATE.md`. Check:

- Claude Code was started in the repository's root folder, where `docs/orbit/STATE.md` is.
- On Windows, Git for Windows is installed (the hook runs with Git Bash). Without it, the
  hook stays silent and everything else still works; run `/orbit status` instead.
- Run the hook by hand from the repository root. It should print one line of JSON:
  `bash "<plugin folder>/hooks/run.cmd" session-start`

## Claude refuses to skip the tests

That is the build stage's rule. If you really want to skip a test for one change, say so
plainly ("skip the test for this change, I accept the risk"). Claude will say what the test
would protect, do it your way and record the decision in `STATE.md`.

## It started Ignite on a product that already has docs

`/orbit` looks for `docs/orbit/STATE.md` in the folder Claude Code was started in. Start
Claude Code from the repository's root folder, or move the file there.

## "Blueprint can't start: Ignite is not approved"

The stage before is not marked `approved` in `STATE.md`. Run `/orbit status` to see what is
waiting, then answer that gate. If you approved it in an earlier session that did not record
it, say so and Claude will record it.

## A gate keeps asking again

Only an explicit yes passes. "Looks fine" plus a question counts as feedback. Answer the
question, then say "approved".

## The docs and the code disagree

Say which one is right. If the code is right, Claude updates the docs and marks dependent
stages `needs review`. If the docs are right, it adds a task to bring the code in line.

## Issues were not created after Assemble

Claude needs the GitHub CLI signed in (`gh auth status`) and a repository with issues turned
on. It asks before creating issues in a repository you have not named.

## A deploy step asks for something I don't want to give

Launch asks before anything that spends money, needs a payment method or touches a live
product. Say no, and it records the step as blocked in `STATE.md` with what is needed.
