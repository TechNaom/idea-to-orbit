# Journal: Repo Pulse

Every change and every roadblock, newest first.

| When | Kind | What | Commit |
|---|---|---|---|
| 2026-12-14 09:40 | Roadblock | **The Monday digest did not go out.** Cause: the GitHub token had expired on 2026-12-13; the watcher caught it at 09:30. Cleared: new token, the run repeated once (the check showed no digest had been sent). Lesson: test flight now checks every credential's expiry, with a warning 7 days before. See [the RCA](rca/2026-12-14-token-expired.md). | - |
| 2026-12-02 16:10 | Fix in review | **T8: the code check found the retry had no cap.** Missed by: the builder; the card's Watch out did not mention retries. Fixed with a cap of 3 and a test. Lesson for this product's cards: every outside call names its retry cap. | - |
| 2026-11-24 11:00 | Decision | **Hosting: Lambda with EventBridge Scheduler** over a small VM: scales to zero, about $0 a month at this load. See [ADR 0001](adr/0001-hosting.md). | - |
