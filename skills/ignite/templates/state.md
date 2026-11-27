# Product state: <product name>

Started: <YYYY-MM-DD>

## Current

- Stage: ignite
- Status: in progress   <!-- in progress | waiting for approval | approved | needs review -->
- Profile: startup   <!-- startup | enterprise: see the blueprint skill, Profiles -->

## Settings

How this product is built and shipped. Every stage reads these instead of assuming GitHub,
`main` or Claude's own subagents. Change them here, not in a stage's output.

- Code host: github   <!-- github (gh, pull requests) | gitlab (glab, merge requests) | other: <name and CLI> -->
- Work branch: main   <!-- where task branches merge, e.g. main, or dev -->
- Release branch: main   <!-- what test flight and launch release from -->
- Promotion: none   <!-- none | <branch> -> staging -> prod (manual approval) -->
- Builders: subagents   <!-- subagents | external: <tool and launcher>, e.g. cursor-agent via scripts/launch-builder.sh -->
- Fast tests: <command>   <!-- the affected tests a builder and the checks run; filled at Assemble's T1 if there is no code yet -->
- Full suite: <command> (about <n> minutes)   <!-- over 15 minutes: see the verify skill, "A slow suite" -->
- CI: <CI system>; a run per commit on the work branch
- Toolchain: <runtime and minimum version; how to install what is missing without changing lock files>
- Pace: ask at every gate   <!-- ask at every gate | run on: <the owner's words, date>; still stop at: new vendor or bill, a change to the live product, UAT -->

## Gates

| Stage | Status | Approved by | Date |
|---|---|---|---|
| ignite | in progress | | |
| blueprint | not started | | |
| assemble | not started | | |
| build | not started | | |
| test-flight | not started | | |
| launch | not started | | |
| orbit | not started | | |

## In flight

Work that runs beside the product's stage: a feature, a fix or a hotfix (see `/orbit`,
Lanes). One line each, with its lane and step; remove it once merged and
recorded in the journal.

- none

## Open questions

- <question> (blocks: <stage>)

## Log

- <YYYY-MM-DD> ignite started.
