---
type: llm
---

Judge only the testing of behaviour the product changes on its own.

PASS if the reply names that the product changes behaviour on its own at run time (the frame-rate
fallback, the WebGL fallback, the retries) and says how a test pins or observes each one (for
example a test mode or flag that fixes the quality level, state a test can read, forcing WebGL off
on purpose), noting that headless CI browsers would otherwise hit the fallback.

FAIL if it writes the summary without addressing how tests control or observe the fallbacks.
