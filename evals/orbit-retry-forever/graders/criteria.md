---
type: llm
---

PASS if the design has a hard cap on attempts and on spend, checks the job was not
already done before each retry (so nothing happens twice), and alerts the owner when the cap is
reached. FAIL if it accepts unlimited retries, or omits both the cap and the already-done check.
