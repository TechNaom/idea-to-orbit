# ADR 0001: Run on AWS Lambda with EventBridge Scheduler

Date: 2026-11-24. Status: accepted

## Context
The job runs once a week for under a minute (R4). It must start on time, cost close to
nothing (N1), and need no server to look after.

## Options

| Option | Fit | Monthly cost | Operating effort | Lock-in | On failure |
|---|---|---|---|---|---|
| A. Lambda + EventBridge Scheduler | Starts on the minute; runs only when needed | $0.00 in the free tier | Low: deployed from CI | Medium: AWS trigger, portable Python | Clear error in logs; health check alerts |
| B. GitHub Actions scheduled workflow | Simple, no cloud account | $0.00, but uses Actions minutes | Lowest | Low | Scheduled runs can start 30+ minutes late, or be skipped under load |
| C. Small always-on VM with cron | Full control | $4-6 | High: patches, disk, uptime | Low | The VM itself can fail silently |

## Decision
Option A: AWS Lambda, started by EventBridge Scheduler.

## Why
It starts on time, costs nothing at this volume, and nothing runs between Mondays. B was
close, but on-time delivery matters (R4) and Actions minutes have run out before. C costs
money and needs looking after, for a job that runs four minutes a month.

The owner asked at the gate why not B; the answer above was given, and the owner kept A.

## Revisit when
The job needs to run longer than 15 minutes, or more than once a day.
