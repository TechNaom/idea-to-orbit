# ADR 0002: Send the email with Amazon SES

Date: 2026-11-24. Status: accepted

## Context
One email a week to one recipient (R4), arriving in the inbox rather than spam, without
storing a mailbox password anywhere (N3).

## Options

| Option | Fit | Monthly cost | Operating effort | Lock-in | On failure |
|---|---|---|---|---|---|
| A. Amazon SES | Same cloud as the function; role-based, no password | $0.00 at 5 emails | Verify a sender once | Low: plain email | Error returned on send |
| B. Personal SMTP account with an app password | Works anywhere | $0.00 | Low | Low | Password kept as a secret; account limits change without notice |
| C. Third-party email API | Good deliverability | $0.00 on a free plan | Another account and key | Medium | Depends on the provider's free plan |

## Decision
Option A: Amazon SES, from a verified sender.

## Why
No password to store, the function's role already controls what it may do, and it costs
nothing at this volume. B means keeping a mailbox password as a secret. C adds another
account and key for no gain at one email a week.

## Revisit when
There is more than one recipient, or emails start landing in spam.
