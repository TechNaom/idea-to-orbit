# Building tasks in parallel

Parallel builds save time when a milestone has several tasks that do not depend on each
other. They cost more and are harder to review, so use them only when they clearly help.

## When tasks can run in parallel

All of these must hold:

- Neither task depends on the other in `tasks.md`.
- They change different files. Two tasks that both edit the same module, the same config
  file or the same migration folder run one after the other.
- They do not both change shared state while their tests run: the same database, queue,
  bucket or port.
- Each has its own complete task card.

If you are unsure about any of these, run the tasks one after the other.

Keep it to three tasks at once. More than that and the checks and merges become the
bottleneck.

## One worktree per task

A worktree is a second checkout of the same repository in another folder, on its own branch.
Each builder works in its own worktree, so they never overwrite each other's files.

```bash
git fetch origin
git worktree add ../<repo>-t5 -b t5-new-issues origin/main
git worktree add ../<repo>-t6 -b t6-failed-runs origin/main
git worktree list
```

In each new worktree, install dependencies and run the full suite before building. A
worktree that is not green at the start cannot be trusted at the end.

Add the worktree folders to `.gitignore` if they live inside the repository, so they are
never committed.

## The run

1. Brief one builder per task from `builder-brief.md`, each with its own worktree path.
2. Start them together.
3. As each one reports, run its task check and code check as usual. Checks for different
   tasks may also run at the same time.
4. Merge one at a time. After each merge, rebase the next branch on the new main and run the
   full suite again before merging it. A clean merge does not mean the code works together.
5. When all are merged, remove the worktrees:

```bash
git worktree remove ../<repo>-t5
git worktree remove ../<repo>-t6
git worktree prune
```

## Parallel investigation

The same idea works for finding out, not only for building: when several independent
failures appear at once (three unrelated tests in three different modules), one fresh agent
per failure can investigate at the same time. Each gets one failure, its output and the
files involved, and reports a cause with evidence. Fixes still go through the normal loop.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "They touch the same file, but different parts of it." | Run them one after the other. Merge conflicts cost more than the time saved. |
| "Both branches are green, so merging both is safe." | Rebase the second on the merged first and run the suite again. |
| "Five at once will be five times faster." | Checks and merges will queue. Three at most. |
| "Skip the checks for the parallel tasks, they were small." | Every task gets both checks, however it was built. |
