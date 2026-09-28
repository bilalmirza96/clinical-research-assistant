#!/usr/bin/env python3
"""
gates.py - between-rung invariants for the analysis ladder (Study-Design Standard, L087-L090,
L092, L098), generalized from the REPEAT DISPARITIES project's ad hoc per-project checks.

Each check is a plain function returning (ok: bool, message: str). A failing gate means the
chain stops - do not proceed to the next rung, table, or manuscript render until it is fixed or
explicitly, visibly skipped with a reason (mirroring ladder_table.py's `skipped=` convention).

Checks
  cohort_n(registry, expected_by_group, keys_by_group=None)
      Exact-N reconciliation across every constant-N rung (crude/modelA/modelB) and every
      exposure group: the reported N must be identical across those rungs and must equal the
      pre-registered, curated cohort size for that group (L088, L090). No "close enough".
  denominator_named(registry)
      Every current result carries a stated population/denominator: an explicit n (or N), a
      "n/N" or "n of N" value, or a label naming an explicit N= count (L090: one denominator,
      named on every artifact).
  dictionary_labels(registry, dossier)
      Every categorical level used to slice a registry result (a dict-valued `current.value`,
      keyed by category) is a level the data-dictionary dossier actually defines - reuses
      dictionary_audit.py's code/definition lookup rather than reimplementing it (L089).
  two_adjusted_models(registry)
      No more than Model A and Model B: reuses ladder_table.py's canonical rung vocabulary
      (RUNG_ORDER) to flag any registry key implying a third adjusted covariate model, e.g. a
      "modelC" (L087).
  no_penalizer(script_paths)
      Grep for a nonzero lifelines `penalizer=` in Cox fits (L092: penalizer biases an exposure
      HR; fit unpenalized and fix sparse levels instead).
  run_time_dates(paths)
      Grep record-writer scripts for a hardcoded module-level `DATE = "YYYY-MM-DD"` constant
      instead of stamping at run time (L098).

CLI
    python3 gates.py cohort-n --registry REG.json --expected '{"NHB": 12345, "NHW": 67890}' \
        [--keys keys_by_group.json]
    python3 gates.py denominator-named --registry REG.json
    python3 gates.py dictionary-labels --registry REG.json --dossier DOSSIER.json
    python3 gates.py two-adjusted-models --registry REG.json
    python3 gates.py no-penalizer FILE [FILE ...]
    python3 gates.py run-time-dates FILE [FILE ...]

Every subcommand prints its message and exits 1 on failure, 0 on pass - wire it into any workflow
step between analysis rungs. Stdlib-only except dictionary-labels/dictionary_labels, which needs
pandas transitively through dictionary_audit.py (only if you actually import that path).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ladder_table as LT  # noqa: E402  (reused for the canonical rung vocabulary, L087)

try:
    import dictionary_audit as DA  # noqa: E402  (reused for code/definition lookup, L089)
except ImportError:  # pandas not installed in this environment; dictionary_labels() will say so
    DA = None


# --------------------------------------------------------------------------------- helpers

def _results(registry) -> dict:
    return registry.get("results", registry) if isinstance(registry, dict) else registry


def _norm_token(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


# --------------------------------------------------------------------------------- cohort_n

def cohort_n(registry, expected_by_group: dict, keys_by_group: dict | None = None):
    """Exact-N reconciliation across every constant-N rung (crude, modelA, modelB) and every
    exposure group (L088, L090: one denominator, named and reconciled exactly - no "close
    enough" Ns).

    `expected_by_group`: {group_name: expected_N} - the curated, PI-reconciled cohort size for
    each group, built once elsewhere (e.g. cohort_flow.py).
    `keys_by_group`: optional {group_name: {rung_name: registry_key}} telling this function
    exactly which registry key carries the N for a given group at a given rung. `rung_name` is
    one of ladder_table.CONSTANT_N ("crude", "modelA", "modelB"). When omitted, the registry is
    searched for a key containing both the rung token and the group token as delimited
    components (the same substring convention tools/registry_lint.py uses for arm parity);
    exactly one match per (group, rung) is required, or the gate fails rather than guess.
    """
    R = _results(registry)
    problems: list[str] = []
    rungs = LT.CONSTANT_N  # ["crude", "modelA", "modelB"]

    def _auto_key(group: str, rung: str):
        gt, rt = _norm_token(group), _norm_token(rung)
        hits = [k for k in R if rt in _norm_token(k) and gt in _norm_token(k)]
        return hits

    for group, expected in expected_by_group.items():
        seen: dict[str, int] = {}
        for rung in rungs:
            key = None
            if keys_by_group and group in keys_by_group and rung in keys_by_group[group]:
                key = keys_by_group[group][rung]
                if key not in R:
                    problems.append(f"{group}/{rung}: registry key '{key}' not found")
                    continue
            else:
                hits = _auto_key(group, rung)
                if len(hits) == 1:
                    key = hits[0]
                elif len(hits) == 0:
                    continue  # rung not reported for this group; nothing to reconcile against
                else:
                    problems.append(f"{group}/{rung}: ambiguous - {len(hits)} registry keys match "
                                    f"({sorted(hits)}); pass keys_by_group to disambiguate")
                    continue
            n = (R[key].get("current") or {}).get("n")
            if n is None:
                problems.append(f"{group}/{rung}: registry key '{key}' carries no n")
                continue
            seen[rung] = int(n)
        if len(set(seen.values())) > 1:
            problems.append(f"{group}: N differs across rungs {seen} - unadjusted, Model A and "
                            f"Model B must share one N (refit every compared rung on one cohort)")
        for rung, n in seen.items():
            if n != int(expected):
                problems.append(f"{group}/{rung}: registry N={n:,} but the curated cohort N="
                                f"{int(expected):,} (difference {n - int(expected):+,})")
    ok = not problems
    msg = "; ".join(problems) if problems else "cohort N reconciles exactly across every rung and group"
    return ok, msg


# --------------------------------------------------------------------------------- denominator_named

_DENOM_PATTERNS = [re.compile(r"\d[\d,]*\s*/\s*\d[\d,]*"), re.compile(r"\d[\d,]*\s+of\s+\d[\d,]*", re.I),
                   re.compile(r"\bn\s*=\s*[\d,]+", re.I)]


def _has_denominator(cur: dict, label: str) -> bool:
    if cur.get("n") not in (None, ""):
        return True
    if cur.get("N") not in (None, ""):
        return True
    val = cur.get("value")
    if isinstance(val, dict) and "n" in val and "N" in val:
        return True
    blob = str(val) if val is not None else ""
    text = f"{blob} {label}"
    return any(p.search(text) for p in _DENOM_PATTERNS)


def denominator_named(registry):
    """Every current result names its population/denominator (L090): an explicit n (or N), a
    value shaped "n/N" or {"n":..,"N":..}, or a label/value stating an "n of N" or "N=" count.
    A result with no `current` block (UNSOURCED) is not judged here - that is registry_lint's
    job."""
    R = _results(registry)
    missing = []
    for key, entry in R.items():
        cur = entry.get("current") or {}
        if not cur:
            continue
        if not _has_denominator(cur, entry.get("label") or ""):
            missing.append(key)
    ok = not missing
    msg = ("every result names a population/denominator" if ok else
           f"{len(missing)} result(s) with no stated denominator: {sorted(missing)}")
    return ok, msg


# --------------------------------------------------------------------------------- dictionary_labels

def _dossier_labels(dossier: dict) -> set:
    labels = set()
    for spec in dossier.get("variables", {}).values():
        for cat in spec.get("categories") or []:
            labels.add(str(cat).strip().lower())
        for defn in (spec.get("codes") or {}).values():
            labels.add(str(defn).strip().lower())
    for lab in dossier.get("labels") or []:
        labels.add(str(lab).strip().lower())
    return labels


def dictionary_labels(registry, dossier):
    """Every categorical level used to slice a registry result is a level the data-dictionary
    dossier actually defines (L089: study every variable in the official dossier before use;
    labels stay inside the dossier's definitions). Reuses dictionary_audit.py's dossier reading
    rather than reimplementing a second parser.

    A registry result is treated as "sliced by category" when its `current.value` is a dict
    whose string keys are category names (e.g. {"Adenocarcinoma": ..., "Squamous": ...} or a
    per-stage breakdown) - every such key must match a declared `categories` entry or a code
    definition somewhere in the dossier (case-insensitive), or be listed in the dossier's
    top-level `labels`.
    """
    if DA is None:
        return False, "dictionary_audit.py could not be imported (pandas missing); cannot run this gate"
    allowed = _dossier_labels(dossier)
    if not allowed:
        return False, "dossier has no categories, code definitions, or labels to check against"
    R = _results(registry)
    problems = []
    for key, entry in R.items():
        val = (entry.get("current") or {}).get("value")
        if not isinstance(val, dict):
            continue
        for level in val:
            if not isinstance(level, str):
                continue
            if level.strip().lower() not in allowed:
                problems.append(f"{key}: level '{level}' does not appear in the data-dictionary dossier")
    ok = not problems
    msg = "every categorical level appears in the data-dictionary dossier" if ok else "; ".join(problems)
    return ok, msg


# --------------------------------------------------------------------------------- two_adjusted_models

_MODEL_TAG_RE = re.compile(r"(?:^|[_.])model([A-Za-z0-9]+)(?:$|[_.])", re.I)


def two_adjusted_models(registry):
    """No more than Model A and Model B (L087): reuses ladder_table.py's canonical rung
    vocabulary (RUNG_ORDER only ever has "modelA" and "modelB" as adjusted-covariate rungs) to
    flag any registry key implying a third one, e.g. "..._modelC_..." or "..._model3"."""
    R = _results(registry)
    bad = []
    for key in R:
        for m in _MODEL_TAG_RE.finditer(key):
            tag = m.group(1).upper()
            if tag not in ("A", "B"):
                bad.append(f"{key}: rung 'model{m.group(1)}' implies a third adjusted model; "
                          f"the analysis ladder allows only {LT.LABELS['modelA']} and "
                          f"{LT.LABELS['modelB']}")
    ok = not bad
    msg = "two adjusted models only (Model A / Model B); no extra rung found" if ok else "; ".join(bad)
    return ok, msg


# --------------------------------------------------------------------------------- no_penalizer

_PENALIZER_RE = re.compile(r"penalizer\s*=\s*([^,\)\n]+)")


def no_penalizer(script_paths):
    """Grep for a nonzero lifelines `penalizer=` (L092: a nonzero penalizer scales with the
    mean log-likelihood and can bias an exposure HR; fit unpenalized and fix sparse levels in
    the covariate set instead)."""
    bad = []
    for p in script_paths:
        path = Path(p)
        if not path.exists():
            continue
        text = path.read_text(errors="ignore")
        for i, line in enumerate(text.splitlines(), 1):
            for m in _PENALIZER_RE.finditer(line):
                val = m.group(1).strip()
                if val not in ("0", "0.0", "0.00"):
                    bad.append(f"{p}:{i}: penalizer={val}")
    ok = not bad
    msg = "no nonzero penalizer= found in lifelines fits" if ok else "; ".join(bad)
    return ok, msg


# --------------------------------------------------------------------------------- run_time_dates

_HARDCODED_DATE_RE = re.compile(r'^\s*DATE\s*=\s*["\']\d{4}-\d{2}-\d{2}["\']', re.M)


def run_time_dates(paths):
    """Grep record-writer scripts for a hardcoded module-level `DATE = "YYYY-MM-DD"` constant
    (L098: a fixed DATE constant stamped a registry entry with the wrong day when the script ran
    just after midnight). Record writers should take the date, and preferably the time, at call
    time (see number_format.now_stamp)."""
    bad = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        text = path.read_text(errors="ignore")
        for m in _HARDCODED_DATE_RE.finditer(text):
            line_no = text[:m.start()].count("\n") + 1
            bad.append(f"{p}:{line_no}: hardcoded DATE constant; stamp at run time instead "
                      f"(number_format.now_stamp())")
    ok = not bad
    msg = "no hardcoded DATE constants found" if ok else "; ".join(bad)
    return ok, msg


# --------------------------------------------------------------------------------- CLI

def _load(path):
    return json.loads(Path(path).read_text())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Analysis-ladder gates (L087-L090, L092, L098). "
                                             "A failed gate means the chain stops.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("cohort-n")
    pc.add_argument("--registry", required=True)
    pc.add_argument("--expected", required=True, help='JSON, e.g. \'{"NHB": 12345, "NHW": 67890}\'')
    pc.add_argument("--keys", help="JSON file: {group: {rung: registry_key}}")

    pd_ = sub.add_parser("denominator-named")
    pd_.add_argument("--registry", required=True)

    pl = sub.add_parser("dictionary-labels")
    pl.add_argument("--registry", required=True)
    pl.add_argument("--dossier", required=True)

    pm = sub.add_parser("two-adjusted-models")
    pm.add_argument("--registry", required=True)

    pp = sub.add_parser("no-penalizer")
    pp.add_argument("paths", nargs="+")

    pr = sub.add_parser("run-time-dates")
    pr.add_argument("paths", nargs="+")

    a = ap.parse_args(argv)

    if a.cmd == "cohort-n":
        keys = _load(a.keys) if a.keys else None
        ok, msg = cohort_n(_load(a.registry), json.loads(a.expected), keys)
    elif a.cmd == "denominator-named":
        ok, msg = denominator_named(_load(a.registry))
    elif a.cmd == "dictionary-labels":
        ok, msg = dictionary_labels(_load(a.registry), _load(a.dossier))
    elif a.cmd == "two-adjusted-models":
        ok, msg = two_adjusted_models(_load(a.registry))
    elif a.cmd == "no-penalizer":
        ok, msg = no_penalizer(a.paths)
    elif a.cmd == "run-time-dates":
        ok, msg = run_time_dates(a.paths)
    else:  # pragma: no cover - argparse enforces `required=True`
        ap.error("unknown command")
        return 2

    print(("PASS " if ok else "FAIL ") + msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
