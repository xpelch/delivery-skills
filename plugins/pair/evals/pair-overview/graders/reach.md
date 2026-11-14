---
type: llm
---

The goal is to make the fee never go below a floor. `fee_for` is called by `total` and, through it and directly, by `receipt`; both have or need tests.
PASS if the reply says, before any code, which existing code the change reaches beyond `fee_for` itself: at least one of the callers (`total`, `receipt`) or the existing tests that the change affects.
FAIL if it plans only the edit to `fee_for` with no mention of a caller or an existing test it affects.
