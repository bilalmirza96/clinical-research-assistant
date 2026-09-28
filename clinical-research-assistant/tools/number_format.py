#!/usr/bin/env python3
"""
number_format.py - one Decimal half-up formatter for every manuscript/table/figure surface,
generalized from the REPEAT DISPARITIES project's Scripts/manuscript_format.py (L091, L097, L098).

Why this exists
---------------
L091. Registry values stored at 3 decimals and printed at 2 were wrong whenever the stored digit
was a boundary 5 (0.275 may really be 0.27498...): ~19 manuscript values were off by 0.01, and
separate ad hoc rounding helpers in text/tables/figures disagreed with each other.
L097. Supplement tables printed a point estimate and its CI limits at different decimals because
each was rounded from its own stored precision (mixed-precision cells like "0.972 (0.911-1.04)").
L098. A record writer with a fixed DATE constant stamped a registry entry with yesterday's date
after running just after midnight.

Rules enforced here
  * Round once, half-up (decimal.ROUND_HALF_UP), at one target precision.
  * A registry entry's `current` block may carry a full-precision companion `current["fp"]`
    (a value, or a dict mapping a dotted sub-path -> full-precision replacement, exactly as
    written by the project's registry upsert scripts). The resolver always prefers it.
  * Boundary guard: a value is ambiguous to round when it was STORED already rounded and its
    stored digits end exactly at the target precision + 1 with a final 5 (e.g. "0.275" printed
    to 2 decimals) - the true full-precision value could round either way. Printing it needs
    either a registered full-precision companion or an explicit acknowledgement; otherwise raise.
  * One precision per estimate: a point estimate and its CI limits print at ONE number of
    decimals - the fewest held by any of the three, but never below the main-text default.
  * Record writers take the date (and preferably the time) at call time, never a hardcoded
    constant.

CLI
    python3 number_format.py --check REGISTRY.json --dp 2

    Lists every `current` value in the registry that would trip the boundary guard at --dp
    decimals and carries no full-precision companion. This is an audit aid (a listing), not a
    hard gate; wire skills/internal/analyze/scripts/gates.py into a build for a pass/fail gate.

Everything here is stdlib-only and importable (`import number_format as NF`) as well as
runnable as a CLI.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

DEFAULT_DP = 2  # main-text default precision for ratios/E-values (manuscript_format.py convention)

_NUM_RE = re.compile(r"-?\d+\.\d+")


class BoundaryError(ValueError):
    """A value was printed from a stored, already-rounded number sitting exactly on a
    half-rounding boundary at the target precision, with no full-precision companion to
    disambiguate it (L091)."""


# --------------------------------------------------------------------------------- formatting

def _digits_after_point(x) -> int:
    """How many decimal digits `x` was written/stored with. Scientific notation is treated as
    full precision (never a boundary case) by returning a large sentinel."""
    s = x if isinstance(x, str) else repr(float(x))
    if "e" in s.lower():
        return 99
    return len(s.split(".", 1)[1]) if "." in s else 0


def fmt(value, dp: int) -> str:
    """Half-up round `value` to `dp` decimals (decimal.ROUND_HALF_UP) and format it as a fixed-
    point string. Accepts a number or a numeric string (a string is honored digit-for-digit,
    which is what makes the boundary guard meaningful - a float has already lost the ambiguity).
    Never prints "-0.00"."""
    q = Decimal(1).scaleb(-dp)
    d = Decimal(value if isinstance(value, str) else repr(float(value))).quantize(q, rounding=ROUND_HALF_UP)
    if d == 0:
        d = abs(d)
    return f"{d:.{dp}f}"


def fmt_estimate(point, lo, hi, dp: int | None = None, default_dp: int = DEFAULT_DP) -> dict:
    """Format a point estimate and its two CI limits at ONE shared precision (L097): the fewest
    decimals held by any of the three stored values, but never below `default_dp` (the main-text
    default). Pass `dp` to force a specific precision instead of the L097 rule.

    Returns {"point": str, "lo": str, "hi": str, "dp": int}.
    """
    if dp is None:
        held = [_digits_after_point(v) for v in (point, lo, hi)]
        dp = max(default_dp, min(held))
    return {"point": fmt(point, dp), "lo": fmt(lo, dp), "hi": fmt(hi, dp), "dp": dp}


# --------------------------------------------------------------------------------- registry access

def from_registry(entry, path: str = ""):
    """Resolve a value out of one registry result entry (the dict at `results[key]`, or the
    `current` block itself), preferring the full-precision companion `current["fp"]` over the
    stored `current["value"]` (L091) - mirrors manuscript_format.py's Registry.resolve, scoped to
    a single already-loaded entry so this module never has to read a whole registry file itself.

    `path` is an optional dotted sub-path into a nested value ("" resolves the whole value).
    `fp`, when present, maps a dotted sub-path ("" = top level) to its full-precision
    replacement; the longest matching prefix of `path` is used and the remaining sub-path is
    walked inside it, exactly as the project's manuscript_format.py does.
    """
    cur = entry.get("current", entry) if isinstance(entry, dict) else entry
    v = cur.get("value")
    fp = cur.get("fp") or {}
    if isinstance(v, str) and v.strip().startswith("{"):
        try:
            v = json.loads(v.replace("'", '"'))
        except (json.JSONDecodeError, ValueError):
            pass
    subs = [s for s in path.split(".") if s] if path else []
    for s in subs:
        v = v[int(s)] if isinstance(v, list) else v[s]
    for k in range(len(subs), -1, -1):
        pre = ".".join(subs[:k])
        if pre in fp:
            w = fp[pre]
            try:
                for s in subs[k:]:
                    w = w[int(s)] if isinstance(w, list) else w[s]
                return w
            except (KeyError, IndexError, ValueError, TypeError):
                break  # companion does not cover this sub-path: keep the stored value
    return v


# --------------------------------------------------------------------------------- boundary guard

def check_boundary(stored_value, dp: int) -> bool:
    """True if `stored_value` sits exactly on a half-rounding boundary at `dp` decimals (its
    stored digits end at dp + 1 places with a final 5)."""
    s = stored_value if isinstance(stored_value, str) else repr(float(stored_value))
    if "e" in s.lower():
        return False
    frac = s.split(".", 1)[1] if "." in s else ""
    return len(frac) == dp + 1 and frac.endswith("5")


def boundary_guard(stored_value, dp: int, fp=None) -> bool:
    """Raise BoundaryError when `stored_value` sits on a rounding boundary at `dp` decimals and no
    full-precision companion `fp` is supplied to disambiguate it (L091). Returns True otherwise
    (including when `stored_value` is not a boundary case at all). This function only judges the
    boundary; when `fp` is given, callers should format `fp` itself (via `fmt`), not
    `stored_value` - the whole point of the companion is that it may round the other way."""
    if check_boundary(stored_value, dp) and fp is None:
        raise BoundaryError(
            f"stored value {stored_value!r} sits on a rounding boundary at {dp} decimal place(s) "
            f"(the digit after the target precision is 5); register a full-precision companion "
            f"(current['fp']) before printing it, or pass fp= explicitly once one is known")
    return True


# --------------------------------------------------------------------------------- run-time stamps

def now_stamp(clock=None, fmt_str: str = "%Y-%m-%d") -> str:
    """Timestamp for record writers, taken at call time (L098) - never a hardcoded DATE constant.
    Pass `clock` (a zero-argument callable returning a datetime) to inject a fake clock in tests;
    it defaults to `datetime.datetime.now`."""
    clock = clock or datetime.datetime.now
    return clock().strftime(fmt_str)


# --------------------------------------------------------------------------------- CLI

def _scan_registry(registry: dict, dp: int) -> list[str]:
    """List every `current` value with no full-precision companion whose stringified value
    contains a decimal number sitting on a rounding boundary at `dp` decimals. This is an audit
    listing (informational), not the hard per-value gate `boundary_guard` performs when a
    specific sub-path and its companion (if any) are known."""
    results = registry.get("results", registry)
    hits = []
    for key, entry in results.items():
        cur = entry.get("current") or {}
        if "value" not in cur:
            continue
        has_fp = bool(cur.get("fp"))
        blob = json.dumps(cur["value"]) if not isinstance(cur["value"], str) else cur["value"]
        for m in _NUM_RE.finditer(blob):
            if check_boundary(m.group(0), dp) and not has_fp:
                hits.append(f"{key}: stored {m.group(0)} would round ambiguously to {dp} dp "
                            f"(no full-precision companion registered)")
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", metavar="REGISTRY.json", help="registry JSON to scan")
    ap.add_argument("--dp", type=int, default=DEFAULT_DP, help=f"target precision (default {DEFAULT_DP})")
    a = ap.parse_args(argv)
    if not a.check:
        ap.error("--check REGISTRY.json is required")
    reg = json.loads(Path(a.check).read_text())
    hits = _scan_registry(reg, a.dp)
    for h in hits:
        print(h)
    print(f"\n{len(hits)} value(s) at {a.dp} dp would trip the boundary guard")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
