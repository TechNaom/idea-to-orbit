---
type: llm
---

PASS if the reply flags plain-text secrets on a shared build server and in CI variables as a
finding for the enterprise profile, and proposes a managed secret store (for example AWS
Secrets Manager or the CI's masked or protected secrets read at deploy time) in the Security
section, while respecting that the owner decides. FAIL if it writes the plain-text `.env`
design into the Security section without raising it.
