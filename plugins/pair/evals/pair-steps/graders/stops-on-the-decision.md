---
type: llm
---

PASS if the reply stops on step 2 and waits for the user: it says step 1 is committed, explains what it did for step 2 and why, names where the decision to validate is (a file and line), says the step is not committed, and ends by asking for « ok » or a remark.
FAIL if it reports all three steps done, if it committed step 2, or if it does not ask the user to validate the decision.
