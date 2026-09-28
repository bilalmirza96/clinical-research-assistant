#!/usr/bin/env python3
"""RED/GREEN tests for tools/number_format.py (run: python3 tools/tests/test_number_format.py).

Same dependency-free style as skills/internal/analyze/tests/test_study_design_tools.py: print
PASS/FAIL per assertion, exit 1 if anything failed.

Fixtures replay the defects behind L091 (half-up boundary rounding), L097 (one precision per
estimate) and L098 (run-time date stamps) from the REPEAT DISPARITIES project's audit history
(skills/references/lessons-log.json).
"""
from __future__ import annotations

import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

import number_format as NF  # noqa: E402

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ---------------------------------------------------------------- fmt: half-up rounding (L091)
check(NF.fmt(0.275, 2) == "0.28", f"fmt: 0.275 -> 0.28 at 2dp (got {NF.fmt(0.275, 2)})")
check(NF.fmt(1.275, 2) == "1.28", f"fmt: 1.275 -> 1.28 at 2dp (got {NF.fmt(1.275, 2)})")
check(NF.fmt("0.275", 2) == "0.28", "fmt: a stored string rounds the same as the equivalent float")
check(NF.fmt(-0.001, 2) == "0.00", "fmt: never prints -0.00")
check(NF.fmt(3, 1) == "3.0", "fmt: an integer input still prints at the requested precision")

# ---------------------------------------------------------------- boundary_guard (L091)
# The REPEAT DISPARITIES defect: a value is stored rounded to 3dp as "0.275". Printed naively to
# 2dp that rounds up to 0.28. Its true full-precision value, once refit, was 0.2749 - which
# rounds DOWN to 0.27. The guard must block the naive print and, once the companion is known,
# the caller formats the companion (not the stored value).
try:
    NF.boundary_guard("0.275", 2, fp=None)
    check(False, "boundary_guard: stored 0.275 without a full-precision companion raises BoundaryError")
except NF.BoundaryError as e:
    check("0.275" in str(e), "boundary_guard: stored 0.275 without fp raises BoundaryError naming the value")

ok = NF.boundary_guard("0.275", 2, fp=0.2749)
check(ok is True, "boundary_guard: stored 0.275 WITH a full-precision companion (0.2749) passes")
check(NF.fmt(0.2749, 2) == "0.27",
     f"boundary_guard companion: the full-precision value 0.2749 prints as 0.27, not the naive 0.28 "
     f"(got {NF.fmt(0.2749, 2)})")

# a value that is NOT on a rounding boundary never raises, fp or not
check(NF.boundary_guard(0.271, 2) is True, "boundary_guard: a non-boundary value never raises")
check(NF.check_boundary("0.275", 2) is True, "check_boundary: detects the boundary case directly")
check(NF.check_boundary("0.271", 2) is False, "check_boundary: a non-boundary value is not flagged")

# ---------------------------------------------------------------- fmt_estimate: one precision (L097)
# Supplement v04 defect: point 0.972 (3dp), CI 0.911 (3dp) - 1.04 (2dp, or 3 sig figs) printed at
# their own stored decimals. Fixed: print all three at one precision (fewest held, floor at the
# main-text default of 2).
est = NF.fmt_estimate(0.972, 0.911, 1.04)
check(est["dp"] == 2, f"fmt_estimate: mixed-decimal CI (3,3,2 held) settles on 2dp (got {est['dp']})")
check(est["point"] == "0.97" and est["lo"] == "0.91" and est["hi"] == "1.04",
     f"fmt_estimate: point/lo/hi all rendered at the same 2dp (got {est})")
check(len(est["point"].split(".")[1]) == len(est["lo"].split(".")[1]) == len(est["hi"].split(".")[1]),
     "fmt_estimate: point, lo and hi carry an identical number of decimal digits")

# never below the main-text default: three values all held to 4dp still print at the 2dp default
est2 = NF.fmt_estimate(1.2345, 1.1000, 1.4000)
check(est2["dp"] == 2, f"fmt_estimate: never rounds MORE precisely than the main-text default (got {est2['dp']})")

# an explicit dp overrides the L097 rule entirely
est3 = NF.fmt_estimate(1.2345, 1.1000, 1.4000, dp=3)
check(est3["dp"] == 3 and est3["point"] == "1.235", "fmt_estimate: an explicit dp= is honored as-is")

# ---------------------------------------------------------------- from_registry: fp preference (L091)
entry_no_fp = {"current": {"value": "1.304 (1.273-1.336)", "n": 106266}}
check(NF.from_registry(entry_no_fp) == "1.304 (1.273-1.336)",
     "from_registry: falls back to current.value when there is no fp companion")

entry_fp_top = {"current": {"value": {"OR": 0.487, "ci_low": 0.451, "ci_high": 0.525},
                            "fp": {"": {"OR": 0.48711, "ci_low": 0.45098, "ci_high": 0.52534}}}}
resolved = NF.from_registry(entry_fp_top, path="OR")
check(abs(resolved - 0.48711) < 1e-9,
     f"from_registry: a top-level fp companion is preferred over the stored rounded value (got {resolved})")

entry_fp_sub = {"current": {"value": {"Adenocarcinoma": {"OR": 1.1, "ci_low": 1.0, "ci_high": 1.2},
                                       "Squamous": {"OR": 0.9, "ci_low": 0.8, "ci_high": 1.0}},
                            "fp": {"Adenocarcinoma": {"OR": 1.10234}}}}
check(abs(NF.from_registry(entry_fp_sub, path="Adenocarcinoma.OR") - 1.10234) < 1e-9,
     "from_registry: a sub-path fp companion resolves through nested value keys")
check(NF.from_registry(entry_fp_sub, path="Squamous.OR") == 0.9,
     "from_registry: a value with no fp companion for that sub-path falls back to the stored value")

# ---------------------------------------------------------------- now_stamp (L098): run time, not a constant
calls = iter([datetime.date(2026, 9, 27), datetime.date(2026, 9, 28)])
fake_clock = lambda: datetime.datetime.combine(next(calls), datetime.time())  # noqa: E731
s1 = NF.now_stamp(clock=fake_clock)
s2 = NF.now_stamp(clock=fake_clock)
check(s1 == "2026-09-27" and s2 == "2026-09-28",
     f"now_stamp: reads the injected clock at call time and changes across a date boundary (got {s1}, {s2})")
check(s1 != s2, "now_stamp: two calls straddling midnight never share a stamp")

print()
print(f"{len(FAILS)} failure(s)")
sys.exit(1 if FAILS else 0)
