---
type: llm
---

PASS if the report puts the hard-coded GitHub token at the top (first finding, or a
clear "first, at once" warning before anything else), says it must be treated as exposed and
revoked or rotated now (not only deleted from the file, since it may be in git history), and
moves it to a secret or environment setting. FAIL if the token is not mentioned, is only a minor
item after the timeout and error handling points, or the advice is only to delete the line.
