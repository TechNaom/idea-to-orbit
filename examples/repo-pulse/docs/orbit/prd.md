# PRD: Repo Pulse

Version 1, 2026-11-23. Brief: [brief.md](brief.md)

## Users and their jobs

| User | Wants to | So that |
|---|---|---|
| Repository owner | See last week's changes across all repositories in one place | Nothing waits for days without them knowing |

## Requirements

| ID | Requirement | Priority | Acceptance check |
|---|---|---|---|
| R1 | List every issue opened in the last 7 days in each repository, with title and link; pull requests are not counted as issues | must | Test fixture with 3 issues and 1 pull request in the window lists exactly the 3 issues |
| R2 | List every failed CI run on each repository's default branch in the last 7 days, with workflow name and link | must | Fixture with 2 failed runs on main and 1 on a feature branch lists only the 2 |
| R3 | Show the number of new stars per repository in the last 7 days | should | Fixture with 5 stars, 2 of them older than 7 days, shows 3 |
| R4 | Send one email every Monday at 08:00 IST; repositories with nothing new are left out | must | Email received on a Monday between 08:00 and 08:05 IST; a repository with no news does not appear |
| R5 | In a week with no news at all, send a one-line "quiet week" email instead | should | Fixture with no news produces the one-line email |

## Non-functional requirements

| ID | Area | Requirement | Acceptance check |
|---|---|---|---|
| N1 | Cost | Runs within the free tiers; hard cap $2 per month | AWS budget exists with alerts at 25/50/80/100%; month-to-date cost $0.00 after the first run |
| N2 | Performance | A run finishes in under 2 minutes for up to 100 repositories | Timed run against 31 real repositories plus a 100-repository fixture |
| N3 | Security | The GitHub token is read-only and lives only in the cloud secret store and CI secrets | Token scopes checked; secret scan of the repository and history is clean |
| N4 | Reliability | Exactly one email per Monday; a missing email raises an alert within 1 hour | Two runs started together send one email; a disabled schedule raises an alert by 09:00 IST |

## Out of scope
Pull requests, releases, other accounts' repositories, a web page, more than one recipient.

## Success measures

| Measure | Target | By |
|---|---|---|
| Emails opened | 4 Mondays in a row | 2026-12-28 |
| New issues answered | Within 2 days of the email | 2026-12-28 |

## Risks and assumptions

| Risk or assumption | Impact | How we check or reduce it |
|---|---|---|
| GitHub API rate limit with many repositories | Run fails | 31 repositories need about 100 calls; the limit is 5,000 an hour |
| Email lands in spam | Not read | Verified sender domain on SES; check the first email arrives in the inbox |
| The token expires | No email | Alert on failure (N4); reminder before expiry |

## Open questions
- None.
