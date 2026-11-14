---
type: llm
---

PASS if the reply lays the job out as numbered steps, says which steps stop for the user (a decision, or a piece the user writes) and which chain without stopping, and asks the user to agree before any code is written (a short sentence after that question is fine).
FAIL if it reports code already written or tests already changed, if it gives no numbered steps, or if it does not wait for the user's go.
