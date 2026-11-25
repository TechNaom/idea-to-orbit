# Examples

Real sessions, start to finish. Each recipe shows what you type and what you see back, so you
can match your situation to one and follow it. `You:` and `AI:` are the Claude Code chat;
lines starting with `$` are the terminal. Replies are shortened to their key lines.

Every file mentioned in recipe 1 is in [examples/repo-pulse](../examples/repo-pulse/), filled
in exactly as the run produced it.

## Recipe 1: A new product, start to finish

**When to use it:** you have an idea and an empty repository.

The product: **Repo Pulse**, a Monday email listing new stars, new issues and failed CI runs
across all of your GitHub repositories.

### Ignite

```text
You: /orbit

AI:  New product. Created docs/orbit/STATE.md. Starting Ignite.
     Tell me the idea in your own words.

You: I have about 30 repos. I miss new issues for days and only notice failed
     CI when something breaks. I want one email every Monday with what changed.

AI:  Three questions first:
     1. Who is this for: only you, or other people with many repos too?
     2. Which changes matter most: stars, issues, pull requests, CI, releases?
     3. What budget per month, and is there a date you want it by?

You: Me first. Issues and failed CI matter most, stars are nice to have.
     Budget close to zero, a few rupees at most. Two weeks.

AI:  ...
     Ignite is ready for your approval.
     First version: Monday 08:00 IST email, new issues + failed CI on default
                    branches + new stars, all repos of one GitHub account
     Out of scope:  pull requests, releases, other people's repos, a web page
     Success:       read 4 Mondays in a row; every new issue answered within
                    2 days of its email
     Requirements:  R1-R5, N1-N4. Open questions: none.
     Approve Ignite?

You: approved

AI:  Ignite approved and recorded. Next: Blueprint.
```

Files: [brief.md](../examples/repo-pulse/docs/orbit/brief.md),
[prd.md](../examples/repo-pulse/docs/orbit/prd.md)

### Blueprint

```text
You: /orbit

AI:  Starting Blueprint. Three decisions need options weighed:
     hosting, how the email is sent, where "last week's" data is kept.
     ...
     Hosting:  AWS Lambda + EventBridge Scheduler   (ADR 0001)
               over a GitHub Actions cron (starts late, uses CI minutes)
     Email:    Amazon SES                          (ADR 0002)
               over a personal SMTP account (password in a server)
     State:    none - each run compares against "the last 7 days" in the
               GitHub API, so there is no database to run or pay for
     Cost:     about $0.00/month inside free tiers; cap $2, alerts 25-100%
     Failure modes: 5, each with detection and recovery.
     Approve Blueprint?

You: why not just a GitHub Action? it's simpler

AI:  It is simpler to set up. Two reasons I didn't pick it: scheduled Actions
     often start 30+ minutes late, and every run uses your Actions minutes,
     which already ran out once. If on-time Mondays matter less to you than
     simplicity, I can switch and update ADR 0001. Which do you prefer?

You: keep lambda. approved

AI:  Blueprint approved. Next: Assemble.
```

A question at a gate is not an approval: Claude answers it and asks again.

Files: [architecture.md](../examples/repo-pulse/docs/orbit/architecture.md),
[ADR 0001](../examples/repo-pulse/docs/orbit/adr/0001-hosting.md),
[ADR 0002](../examples/repo-pulse/docs/orbit/adr/0002-email-delivery.md)

### Assemble

```text
You: /orbit

AI:  ...
     3 milestones, 11 tasks, all S or M:
       M1 Skeleton (T1-T4): repo + CI, budget cap, Lambda that emails "hello"
                            on a schedule, deployed
       M2 The digest (T5-T8): issues, CI runs, stars, the email layout
       M3 Hardening (T9-T11): health check, alerts, rollback
     Coverage: every requirement has a task. Gaps: none.
     Approve Assemble? I'll then create 11 issues in you/repo-pulse.

You: go

AI:  Assemble approved. Created issues #1-#11 in you/repo-pulse. Next: Build.
```

File: [tasks.md](../examples/repo-pulse/docs/orbit/tasks.md)

### Build (one task shown)

```text
You: /orbit

AI:  Next task: T5 "New issues in the last 7 days" (R1).
     Its dependencies T1-T4 are done. Suite on main: 13 passed.

     Sent T5's card to a fresh builder. Its report:
       Status: done
       Red:   pytest tests/test_issues.py
              1 failed - ImportError: cannot import name 'new_issues'
       Green: pytest -q
              14 passed

     Task check (fresh agent): FAIL
       Missing: card step 3, "pull requests excluded" - the issues API
       returns pull requests too, and nothing filters them.
     Builder added test_excludes_pull_requests (red, then green) and the
     filter. Task check again: PASS.

     Code check (fresh agent):
       Must fix: none
       Should fix: pulse/issues.py:18 - "since" filters on update time;
       an old issue with a new comment would be listed. Check created_at.
     Fixed, with test_old_issue_with_new_comment_is_left_out.

     Verified myself: pytest -q -> 16 passed. Done check: a real run lists
     this week's 6 issues and no pull requests.

     Pushed t5-new-issues, opened PR #12 (T5, R1; 13 -> 16 tests; both
     checks passed). CI green. Merged. Closed issue #5. Next: T6.
```

### Test flight

```text
You: /orbit test-flight

AI:  ...
     Decision: GO
     Requirements: R1-R5 pass, N1-N4 pass (evidence in release.md)
     Failure tests: GitHub API down -> one retry, then an alert, no email;
                    SES rejects -> alert; a burst of 5 runs -> 1 email (lock)
     Cost: $0.00 expected, $0.01 at 10x
     Rollback: rehearsed on staging, 40 seconds
     Not tested: an account with more than 100 repos (I only have 31)
     Approve the launch?

You: approved
```

File: [release.md](../examples/repo-pulse/docs/orbit/release.md)

### Launch

```text
You: /orbit

AI:  Deploy plan written. Before anything is created:
     - AWS budget "repo-pulse": $2/month, alerts 25/50/80/100% + forecast
     - backup tag stable-2026-12-07 at 5c1e9a0
     Shall I create the budget and deploy from CI?

You: yes

AI:  Budget created. Deployed by CI run "deploy" #3.
     Smoke test: invoked once by hand -> email received, 4 repos with news.
     Delivery confirmed: SES message id recorded, mail arrived in the inbox.
     Rollback: git tag stable-2026-12-07 -> re-run deploy.
     Approve Launch?

You: approved
```

File: [deploy-plan.md](../examples/repo-pulse/docs/orbit/deploy-plan.md)

### Orbit

```text
You: /orbit

AI:  Setting up operations. Health check runs Monday 09:00 IST on a GitHub
     Actions schedule - a different clock from the Lambda - and asks
     "was this Monday's email sent?", not "is the Lambda up?".
     Tested each part by breaking it on purpose:
       - removed the schedule      -> alert issue opened at 09:00
       - bad GitHub token          -> 1 retry, then alert, no email
       - two runs at once          -> second run exited, 1 email
     Runbook written. Approve Orbit?

You: approved
```

File: [runbook.md](../examples/repo-pulse/docs/orbit/runbook.md)

## Recipe 2: An incident in orbit

**When to use it:** the product is live and something went wrong.

```text
You: no pulse email today. why?

AI:  The health check opened alert issue #18 at 09:00 IST.
     Root cause, from the Lambda logs: GitHub returned 401 Bad credentials.
     The token expired on 2026-12-13: it was reused from an older script
     and had a 30-day expiry. The run retried once, then stopped, as designed.

     Fix (needs you): create a new token with a 1-year expiry and run
     $ gh secret set PULSE_GITHUB_TOKEN
     Prevention: I'll add a check that warns 7 days before the token
     expires. Wrote rca/2026-12-14-token-expired.md.
     Shall I build the warning as task T12?

You: yes
```

File: [rca/2026-12-14-token-expired.md](../examples/repo-pulse/docs/orbit/rca/2026-12-14-token-expired.md)

## Recipe 3: A no-go at test flight

**When to use it:** the release gate finds a real problem.

```text
AI:  Decision: NO-GO
     N2 fails: the email took 9 minutes for 31 repos (target: under 2).
     Cause: one API call per repo per check, run one after another.
     Must change: fetch repos in parallel, with a limit of 5 at a time.
     Added a new task to tasks.md. Test flight goes back to Build.
```

Nothing ships on a no-go. Once the new task is built, run `/orbit test-flight` again.

## Recipe 4: Changing your mind mid-way

**When to use it:** you are in Build and want to change a decision from Blueprint.

```text
You: let's use Telegram instead of email

AI:  That changes ADR 0002 and requirement R4, so Blueprint goes back to
     review and Build pauses. Changes:
       - ADR 0003 "Deliver by Telegram bot", replaces ADR 0002
       - R4 now says "a Telegram message"
       - tasks T7, T8 rewritten; T5, T6 unaffected
     Approve the updated Blueprint?
```

Later stages are marked `needs review` in `STATE.md` until you approve again.

## Recipe 5: Just checking

```text
You: /orbit status

AI:  Repo Pulse - stage 7, Orbit (approved)
     Live since 2026-12-07. Last 3 Mondays: emails sent.
     Incidents: 1 (2026-12-14, token expired, fixed).
     Spend this month: $0.00 of $2.00.
     Waiting for you: nothing.
```
