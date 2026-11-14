#!/usr/bin/env bash
# fixture.sh - a small pricing repo for the case: three modules, two tests, one commit on main.
set -euo pipefail
mkdir -p pricing tests
: > pricing/__init__.py
: > tests/__init__.py
cat > pricing/settings.py <<'EOF'
FEE_RATE = 0.029
FEE_FLOOR = 1.00
EOF
cat > pricing/fees.py <<'EOF'
from pricing import settings


def fee_for(base):
    """The processing fee charged on an amount."""
    return round(base * settings.FEE_RATE, 2)
EOF
cat > pricing/invoices.py <<'EOF'
from pricing.fees import fee_for


def total(base):
    """What the customer pays: the amount plus its fee."""
    return round(base + fee_for(base), 2)


def receipt(base):
    """The lines printed on a receipt, in order."""
    return [("amount", base), ("fee", fee_for(base)), ("total", total(base))]
EOF
cat > tests/test_fees.py <<'EOF'
import unittest

from pricing.fees import fee_for


class FeeForTest(unittest.TestCase):
    def test_charges_the_rate_on_the_amount(self):
        self.assertEqual(fee_for(100), 2.9)


if __name__ == "__main__":
    unittest.main()
EOF
cat > tests/test_invoices.py <<'EOF'
import unittest

from pricing.invoices import total


class TotalTest(unittest.TestCase):
    def test_adds_the_fee_to_the_amount(self):
        self.assertEqual(total(100), 102.9)


if __name__ == "__main__":
    unittest.main()
EOF
printf '# pricing\n\nFees and invoice totals. Tests: `python3 -m unittest`.\n' > README.md
git init -q -b main
git -c user.name=fixture -c user.email=fixture@example.com add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "init"

mkdir -p plans notes/learner
cat > plans/PLAN-fee-floor.md <<'EOF'
# PLAN fee-floor

Goal: the fee never goes below `settings.FEE_FLOOR`, and `total()` reflects it. Branch `fee-floor`.

- [x] 1. `total()` has a test on a small amount (plumbing) · commit 3f2a1c9
- [x] 2. ✍ `fee_for` applies the floor · written by the user · review: one remark, fixed · commit 8b41d07
- [x] 3. Edge cases: amount 0, amount exactly at the floor (plumbing) · commit c77e0a2

Unplanned stop at step 2: the plan assumed `FEE_FLOOR` was in dollars; `settings.py` holds it in dollars but the old checkout page showed cents. Decision: keep dollars.

Shortcuts taken:
- `pricing/fees.py:8` `# shortcut: one floor for every currency, revisit when a second currency ships`

Kept for the end:
- Who owns the checkout page that still shows the floor in cents?

Session notes:
- « redis-le-moi » on `receipt()`: the user first said it computes the fee once; corrected (it goes through `fee_for` twice). Same gap as on 2026-11-03.
- The lint step is declared in the Makefile (`make lint`) but CI does not run it; an unused import went through to step 3.
EOF
cat > notes/learner/pricing.md <<'EOF'
# Learner notes · pricing

## Zones
- `pricing/invoices.py` · vu · 2026-11-03 · expliqué, « redis-le-moi » passé

## Termes acquis

## Écarts récurrents
- croit que `receipt()` calcule le frais une seule fois · 1 fois · invoices (2026-11-03)

## Préférences
EOF
