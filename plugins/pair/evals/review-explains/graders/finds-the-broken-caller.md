---
type: llm
---

The change adds a required `currency` parameter to `total()`. `receipt()` in the same file still calls `total(base)` with one argument and is not in the diff, and the existing test calls `total(100)`.
PASS if the reply reports that a caller outside the changed lines (receipt, or the existing test) breaks because `total` now needs a second argument.
FAIL if it mentions no caller broken by the new signature.
