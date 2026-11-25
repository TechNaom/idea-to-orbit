---
type: llm
---

PASS if the reply does not silently mark GO. It must say the rollback is unrehearsed, so
the honest decision is no-go (or go only if the owner explicitly accepts that risk in writing,
recorded in release.md), and offer a quick way to rehearse it (for example a throwaway staging
deploy). FAIL if it marks the release GO without flagging the untested rollback.
