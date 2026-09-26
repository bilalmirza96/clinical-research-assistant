#!/usr/bin/env python3
"""ladder_table.py - the analysis-ladder comparison table and E-values
(analyze/references/analysis-ladder.md, L087).

    rungs = [dict(rung="crude",  est=1.304, lo=1.273, hi=1.336, n=106266),
             dict(rung="modelA", est=1.140, lo=1.110, hi=1.171, n=106266),
             dict(rung="modelB", est=1.091, lo=1.063, hi=1.121, n=106266),
             ...]
    md, flags = ladder_table(rungs, measure="HR", common=True, survival=True,
                             skipped={"mediation": "no why-question for this objective"})
    e_point, e_ci = evalue(0.487, 0.451, 0.525, measure="OR", common=True)   # 2.221, 2.104

Rung names, in the order they are computed and compared:
    crude, modelA (clinical), modelB (fully adjusted), adjsurv, iptw, psm, mediation, ml
Two adjusted models only. E-values (rung 6) are a column of the table, computed for every adjusted ratio estimate.
A rung carries its own `measure` when it differs from the table's (adjusted survival in
percentage points, proportion mediated in %); attenuation is computed only on the table's measure.
"""
import math

RUNG_ORDER = ["crude", "modelA", "modelB", "adjsurv", "iptw", "psm", "mediation", "ml"]
LABELS = {
    "crude": "1. Unadjusted",
    "modelA": "2. Model A (clinical)",
    "modelB": "3. Model B (fully adjusted)",
    "adjsurv": "4. Adjusted survival",
    "iptw": "5. IPTW",
    "psm": "5b. Propensity-matched",
    "mediation": "7. Causal mediation",
    "ml": "8. ML / novel method",
}
CONSTANT_N = ["crude", "modelA", "modelB"]
RATIO = {"HR", "OR", "RR"}


def _to_rr(x, measure, common):
    m = measure.upper()
    if m == "RR":
        return x
    if m not in ("OR", "HR"):
        raise ValueError(f"E-value: measure {measure!r} not supported (use RR, OR or HR)")
    if common is None:
        raise ValueError(f"E-value for an {m}: state whether the outcome is common (>15% in the reference "
                         f"group). The RR formula applied to a common-outcome {m} overstates robustness.")
    if not common:
        return x
    if m == "OR":
        return math.sqrt(x)
    return (1 - 0.5 ** math.sqrt(x)) / (1 - 0.5 ** math.sqrt(1 / x))


def _e(rr):
    rr = 1 / rr if rr < 1 else rr
    return rr + math.sqrt(rr * (rr - 1))


def evalue(est, lo=None, hi=None, measure="RR", common=None):
    """VanderWeele-Ding E-value for the point estimate and for the CI limit nearer the null.
    OR and HR need `common` (True when the outcome exceeds ~15% in the reference group).
    Returns (point, ci); ci is 1.0 when the interval crosses the null, None without a CI."""
    point = _e(_to_rr(est, measure, common))
    if lo is None or hi is None:
        return point, None
    if lo <= 1 <= hi:
        return point, 1.0
    limit = lo if est > 1 else hi
    return point, _e(_to_rr(limit, measure, common))


def _fmt(x, d=3):
    return "" if x is None else f"{x:.{d}f}".rstrip("0").rstrip(".") if d else f"{x}"


def ladder_table(rungs, measure="HR", common=None, skipped=None, survival=False):
    """Return (markdown table, flags). Flags are problems to fix or explain before the ladder is reported."""
    skipped = dict(skipped or {})
    flags = []
    names = [r["rung"] for r in rungs]
    for nm in names:
        if nm not in RUNG_ORDER:
            flags.append(f"Unknown rung '{nm}'; use one of {RUNG_ORDER}")
    idx = [RUNG_ORDER.index(nm) for nm in names if nm in RUNG_ORDER]
    if idx != sorted(idx):
        flags.append("Rung order: compute and present rungs in the canonical order "
                     + " -> ".join(RUNG_ORDER) + f"; got {' -> '.join(names)}")
    # Every rung is decided: run, or skipped with a reason ("not relevant because ..." is a reason).
    required = ["crude", "modelA", "modelB", "iptw", "mediation", "ml"] + (["adjsurv"] if survival else [])
    for r in required:
        if r not in names and r not in skipped:
            flags.append(f"Rung '{r}' missing: not computed and not skipped with a stated reason")
    ns = {r["rung"]: r.get("n") for r in rungs if r["rung"] in CONSTANT_N and r.get("n") is not None}
    if len(set(ns.values())) > 1:
        flags.append("N changes across rungs 1-3 (" + ", ".join(f"{k} {v:,}" for k, v in ns.items())
                     + "); refit every compared rung on one cohort, or register why they differ")

    crude = next((r for r in rungs if r["rung"] == "crude"), None)
    base = math.log(crude["est"]) if crude and measure.upper() in RATIO and crude["est"] > 0 else None
    header = ["Rung", f"Estimate (95% CI)", "N", "Change from unadjusted, % (log scale)", "E-value (CI limit)"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rungs:
        m = r.get("measure", measure)
        est, lo, hi = r["est"], r.get("lo"), r.get("hi")
        ci = f" ({_fmt(lo)}-{_fmt(hi)})" if lo is not None and hi is not None else ""
        change, ev = "", ""
        same_scale = m.upper() == measure.upper() and m.upper() in RATIO
        if same_scale and r["rung"] != "crude" and base:
            change = f"{100 * (base - math.log(est)) / base:.1f}"
            if crude and (crude["est"] - 1) * (est - 1) < 0:
                flags.append(f"Direction: '{r['rung']}' estimate {est} is on the other side of the null "
                             f"from the unadjusted {crude['est']}; investigate before reporting")
        if same_scale and r["rung"] != "crude" and common is not None:
            p, c = evalue(est, lo, hi, measure=m, common=common)
            ev = f"{p:.2f}" + (f" ({c:.2f})" if c is not None else "")
        label = LABELS.get(r["rung"], r["rung"]) + ("" if m == measure else f" [{m}]")
        n = f"{r['n']:,}" if r.get("n") is not None else ""
        lines.append(f"| {label} | {_fmt(est)}{ci} | {n} | {change} | {ev} |")
    for r, why in skipped.items():
        lines.append(f"| {LABELS.get(r, r)} | not run: {why} |  |  |  |")
    return "\n".join(lines), flags


if __name__ == "__main__":
    demo = [dict(rung="crude", est=1.304, lo=1.273, hi=1.336, n=106266),
            dict(rung="modelA", est=1.14, lo=1.11, hi=1.171, n=106266)]
    md, fl = ladder_table(demo, measure="HR", common=True,
                          skipped={r: "demo" for r in ("modelB", "iptw", "mediation", "ml")})
    print(md)
    print("\n".join(fl) or "no flags")
