# Branch check brief

Send this to a fresh agent at the end of a milestone, or before test flight, with every
`<...>` filled in.

---

You are reviewing a whole milestone of work, merged from several tasks that were each
checked on their own. Look for what per-task checks cannot see: how the pieces fit.

## Context

- Product: <one line from brief.md>
- Milestone: <name>, which should leave the product able to: <the milestone's goal>
- Tasks in it: <IDs and titles>
- Architecture: `docs/orbit/architecture.md`. Requirements: `docs/orbit/prd.md`.
- Repository: <path>. Range: `<sha before the milestone>...<sha now>`. Run tests with
  `<command>`.

## Check

1. **The goal:** can the product now do what the milestone promised? Run it, or the closest
   thing to it, and report what happened.
2. **Fit:** do the tasks use the same names, types, error handling and config for the same
   things? Is there duplicated logic that two tasks wrote separately?
3. **Design drift:** does the code still match `architecture.md`? List every difference.
4. **Gaps between tasks:** an input one task produces that the next does not handle; an
   error raised in one place and never caught.
5. **The suite:** does it run cleanly, in a sensible time, with no skipped or flaky tests?
6. **Operations:** are logs, health checks and alerts in place for what this milestone added?

## Report

```
Goal met: yes | no | partly, with what you ran and saw
Must fix:
- <problem> <where> <fix>
Should fix:
- <problem> <where> <fix>
Design drift: <each difference from architecture.md, or "none">
Suite: <command, count, time, skipped or flaky tests>
```
