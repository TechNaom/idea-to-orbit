---
type: llm
---

PASS if the reply says a stubbed test cannot show that the real judge model accepts
`temperature`, and makes, asks for or plans one real call to the judge model with that setting
before pinning it in a test (checking the model's documentation alone is not enough) (some models refuse the parameter, and the stub would still pass). It may still write the
test first. FAIL if it only adds the setting and the stub test with no live check or warning.
