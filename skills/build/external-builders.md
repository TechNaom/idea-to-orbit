# Outside builders

When **Builders** in `STATE.md` names an outside agent (Cursor's CLI, Kiro, Codex, another
coding agent) instead of Claude's subagents, the loop is the same: one task, one fresh
builder, test first, then the task check and the code check. What changes is how the builder
gets its brief, what it may run, and how you know it is working.

## Before the first task

1. **A launcher script** that for each task does the steps below. Keep machine paths (where
   the agent is installed, where worktrees live) out of the repository: read them from the
   environment, or keep the launcher outside the repository. For each task it:
   - puts the brief in the task's worktree as a file (for example `.cursor-task.md`), so the
     builder reads the same text every time and the brief is on disk for the checks;
   - copies the builder's **allow-list** into the worktree (for Cursor, `.cursor/cli.json`)
     before the builder starts. Without it most CLIs fall back to the user's own settings,
     which usually allow almost nothing, and the builder spends the task being refused;
   - starts the builder with a short prompt: "Read <brief file> in this folder and do
     exactly what it says. Run shell commands from this folder exactly as written.";
   - writes a status line per task (started, exit code) to a file you can watch.
2. **The allow-list** names exactly what the builder may run: the test runner, the linter,
   the formatter and the build, each as the brief will write it (relative paths, the
   project's own virtual environment). It refuses git, package installs, network tools and
   cloud CLIs: the builder changes files; you commit, push and deploy. If a card names a new
   dependency, install it in the worktree yourself before starting the builder.
3. **The shell.** Find out which shell the builder's commands run in, and write every
   command in the brief for that shell. On Windows many agents run Git Bash, which eats
   backslashes: write `.venv/Scripts/python.exe -m pytest`, not
   `.venv\Scripts\python.exe -m pytest`.
   Some agents put `cd "<folder>" &&` before each command; allow `cd`, or tell the builder
   not to change folder.
4. **A probe.** Run the launcher once on a throwaway worktree with a one-line brief ("run the
   fast tests and paste the summary line"). If it is refused, fix the allow-list now, not in
   the middle of a milestone.
5. **Keep the builder's files out of commits.** Add the brief file, the report file and the
   allow-list (for example `.cursor-task.md`, `BUILDER_REPORT.md`, `.cursor/`) to
   `.git/info/exclude`, or to `.gitignore` if the whole team uses outside builders.

## For each task

1. Brief from `builder-brief.md`, written to the worktree as the brief file. Paste the whole
   card in; an outside builder cannot read this conversation either.
2. Ask for the report as a file in the worktree (for example `BUILDER_REPORT.md`), in the
   brief's report form, starting with the status line. The **Red** line must hold the
   failing run itself (the command and its failing output), pasted, not described: you will
   not have commits to show the test came first.
3. **Check the first command within a minute or two.** Read the builder's log: did its first
   shell command run, or was it refused? A refused builder often keeps going for a long time
   and reports `blocked` at the end. A started process is not a working builder.
4. When it finishes, read the report, then the diff (`git diff` in the worktree; the builder
   does not commit). The report is a claim; the diff and your own runs are the evidence.
5. **Check that the test came first.** Read the report's Red output against the diff: the
   failure must be the one the card predicts, for the test now in the diff. If it is
   missing or does not match, the test was not seen failing; ask for it, or revert the code
   change, run the test, watch it fail, and restore the code.
6. Commit the builder's work on the task branch yourself, the test and the code as separate
   commits when you can, with the task ID in each message. Check that none of the builder's
   own files (brief, report, allow-list) are staged. Then run the task check and the code
   check as usual.
7. When the task is merged, remove its worktree and branch unless the owner wants them kept.

## Red flags: stop if you think

| Thought | What to do instead |
|---|---|
| "The builder is running, I'll look when it's done." | Check its first command now. Refusals waste whole runs. |
| "It worked in my shell, so the brief's commands are fine." | The builder's shell may differ. Write commands for its shell, and probe once. |
| "Give it git so it can commit as it goes." | The builder changes files. You commit, so every commit is checked. |
| "The report says done, start the checks." | Read the diff first. A report can be wrong about its own work. |
