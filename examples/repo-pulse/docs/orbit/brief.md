# Brief: Repo Pulse

**One line:** a Monday email that tells a developer with many repositories what changed
in all of them last week.

## The problem
I have 31 repositories. New issues sit unanswered for days because I only see them when I
happen to open that repository. Failed CI on a default branch goes unnoticed until
something else breaks. GitHub's notifications are too many to read, so I have turned most
of them off.

## Who it is for
- **Users:** me first; then any developer who owns many small repositories.
- **Buyer:** none for now. It is a tool for my own work.

## What changes when it works
Every Monday morning I know, in one minute of reading, which repositories need me this week.

## Why now
The number of repositories has tripled this year, and two issues waited more than a week.

## First version
- One email, Monday 08:00 IST.
- For every repository of one GitHub account: new issues, failed CI runs on the default
  branch, new stars, all from the last 7 days.
- Repositories with nothing new are left out. A quiet week gets a one-line email.

## Not in the first version
- Pull requests and releases.
- Repositories owned by other accounts or organisations.
- A web page or dashboard.
- More than one recipient.

## How we will know it works
- I open the email 4 Mondays in a row.
- Every new issue is answered within 2 days of the email that listed it.

## Constraints
- Budget: close to zero; hard cap $2 per month.
- Deadline: live by 2026-12-07 (two weeks).
- Other: no server to look after; the GitHub token is read-only.
