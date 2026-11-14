---
type: llm
---

The change replaces the fee with `min(fee, FEE_FLOOR)`, which caps every fee at the floor instead of never going below it (it should be `max`).
PASS if the reply reports this as a problem to fix and gives a concrete case or number showing the wrong result (for example a large amount now charged only the floor).
FAIL if it does not flag the min/max mistake, or flags it with no concrete case.
