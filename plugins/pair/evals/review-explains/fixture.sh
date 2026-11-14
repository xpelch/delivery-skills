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

cat > change.diff <<'EOF'
diff --git a/pricing/fees.py b/pricing/fees.py
--- a/pricing/fees.py
+++ b/pricing/fees.py
@@ -1,6 +1,7 @@
 from pricing import settings


 def fee_for(base):
     """The processing fee charged on an amount."""
-    return round(base * settings.FEE_RATE, 2)
+    fee = round(base * settings.FEE_RATE, 2)
+    return min(fee, settings.FEE_FLOOR)
diff --git a/pricing/invoices.py b/pricing/invoices.py
--- a/pricing/invoices.py
+++ b/pricing/invoices.py
@@ -1,9 +1,9 @@
 from pricing.fees import fee_for


-def total(base):
+def total(base, currency):
     """What the customer pays: the amount plus its fee."""
-    return round(base + fee_for(base), 2)
+    return round(base + fee_for(base), 2) if currency else base
EOF
