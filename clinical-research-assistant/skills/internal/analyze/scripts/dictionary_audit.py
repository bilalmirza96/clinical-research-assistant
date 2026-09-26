#!/usr/bin/env python3
"""dictionary_audit.py - check a dataset, and the recode maps applied to it, against the
project's data-dictionary dossier (analyze/references/data-dictionary-dossier.md, L089).

The dossier JSON is the machine half of specs/data_dictionary_dossier.md: one entry per variable
the study uses, written from the official dictionary for the exact data vintage (item number,
storage type, allowable codes with their definitions, years available, labels a code must never
carry, cross-field consistency rules).

Hard failures (exit 1)
  D1  a dossier variable is absent from the data
  D2  a value outside the allowable codes, pattern or range
  D3  an alphanumeric field held as a numeric dtype, or a numeric field whose values do not parse
  D4  a variable with no values at all in a year inside its declared availability window
  D5  a coding break: a common code that vanishes in one year, or missingness that jumps
  D6  a cross-field consistency rule violated
  M1  a recode map keyed on a code the dictionary does not allow
  M2  an allowable code left unmapped (pass it in `excluded` if dropping it is deliberate)
  M3  a label that contradicts the code's definition (dossier "forbidden_labels")
Info (exit 0): allowable codes never observed; several codes merged into one label.

Usage
  python3 dictionary_audit.py --dossier specs/data_dictionary_dossier.json --data data/working/cohort.parquet
  python3 dictionary_audit.py --dossier specs/data_dictionary_dossier.json --map recode.json --var REASON_FOR_NO_SURGERY
  In a cohort builder, after loading raw data:
      from dictionary_audit import audit_frame
      rep = audit_frame(raw, dossier); assert not rep["fail"], rep["fail"]
Fixed-width files (NCDB .dat) are read by the project's own loader; call audit_frame() on the frame.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

MIN_YEAR_N = 50          # a year needs this many rows before a coding break is judged
MIN_EXPECTED = 10        # ...and this many expected rows of the code that vanished
BREAK_SHARE = 0.05       # a code must hold >= 5% of rows in the median other year


def _key(v, storage="numeric"):
    """Normalise one code for comparison: 7, 7.0, '7', '07' -> '7' for numeric storage;
    stripped text for alphanumeric storage; None for missing or blank."""
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    if s == "":
        return None
    if storage == "numeric":
        try:
            f = float(s)
            if f.is_integer():
                return str(int(f))
        except ValueError:
            pass
    return s


def _allowed(spec):
    storage = spec.get("storage", "numeric")
    codes = spec.get("codes") or {}
    miss = spec.get("missing_codes") or []
    if not codes and not miss:
        return None
    return {_key(c, storage) for c in list(codes) + list(miss)}


def _definition(spec, code):
    storage = spec.get("storage", "numeric")
    for c, d in (spec.get("codes") or {}).items():
        if _key(c, storage) == code:
            return d
    return "missing/unknown code" if code in {_key(c, storage) for c in spec.get("missing_codes") or []} else ""


def _outside(values, spec):
    """Distinct normalised values that the dossier does not allow, with counts."""
    storage = spec.get("storage", "numeric")
    allowed = _allowed(spec)
    pattern = re.compile(spec["pattern"]) if spec.get("pattern") else None
    rng = spec.get("range")
    bad = {}
    for raw, cnt in values.items():
        k = _key(raw, storage)
        if k is None:
            continue
        ok = True
        if allowed is not None and k not in allowed:
            ok = False
        if ok and pattern is not None and not pattern.match(k):
            ok = False
        if ok and rng is not None:
            try:
                f = float(k)
                ok = rng.get("min", float("-inf")) <= f <= rng.get("max", float("inf"))
            except ValueError:
                ok = False
        if not ok:
            bad[k] = bad.get(k, 0) + int(cnt)
    return bad


def audit_frame(df, dossier):
    """Audit a DataFrame against a dossier dict. Returns {"fail": [...], "info": [...], "by_year": DataFrame|None}."""
    fail, info = [], []
    ycol = dossier.get("year_column")
    has_year = bool(ycol) and ycol in df.columns
    by_year_cols = {}
    for var, spec in dossier.get("variables", {}).items():
        storage = spec.get("storage", "numeric")
        item = spec.get("item", "")
        tag = f"{var} ({item})" if item else var
        if var not in df.columns:
            fail.append(f"D1 {tag}: listed in the dossier but absent from the data")
            continue
        col = df[var]

        # D3 storage type
        if storage == "alphanumeric" and pd.api.types.is_numeric_dtype(col):
            fail.append(f"D3 {tag}: declared alphanumeric but held as numeric dtype {col.dtype}; "
                        f"codes such as 'A200' cannot survive numeric parsing (read it as text)")
        if storage == "numeric" and not pd.api.types.is_numeric_dtype(col):
            nonnull = col.dropna().astype(str).str.strip()
            nonnull = nonnull[nonnull != ""]
            bad = nonnull[pd.to_numeric(nonnull, errors="coerce").isna()]
            if len(bad):
                fail.append(f"D3 {tag}: declared numeric but {len(bad)} value(s) do not parse, "
                            f"e.g. {sorted(bad.unique())[:5]}")

        # D2 allowable values
        bad = _outside(col.value_counts(dropna=True), spec)
        if bad:
            top = sorted(bad.items(), key=lambda kv: -kv[1])[:10]
            fail.append(f"D2 {tag}: {sum(bad.values())} value(s) outside the dictionary's allowable set: "
                        + ", ".join(f"{k} (n={v})" for k, v in top))
        allowed = _allowed(spec)
        if allowed:
            seen = {_key(v, storage) for v in col.dropna().unique()}
            never = sorted(a for a in allowed if a not in seen)
            if never:
                info.append(f"{tag}: allowable code(s) never observed: {never}")

        if not has_year:
            continue
        years = spec.get("years")
        norm = col.map(lambda v: _key(v, storage))
        by_year_cols[var] = norm.notna().groupby(df[ycol]).mean().mul(100).round(1)
        if not years:
            continue
        lo, hi = years
        window = df[ycol].between(lo, hi)
        sub = norm[window]
        yr = df.loc[window, ycol]
        present = sub.notna().groupby(yr).sum()
        # D4 fully missing year inside the window
        for y, k in present.items():
            if k == 0:
                fail.append(f"D4 {tag}: no values at all in {int(y)}, inside its declared availability "
                            f"window {lo}-{hi} (field renamed, split or dropped in that vintage?)")
        # D5 coding breaks (only for coded variables with >= 3 years in the window)
        counts = yr.value_counts()
        if allowed is None or counts.size < 3:
            continue
        shares = pd.crosstab(yr, sub.fillna("<missing>"), normalize="index")
        for code in shares.columns:
            for y in shares.index:
                if counts.get(y, 0) < MIN_YEAR_N or present.get(y, 0) == 0:
                    continue
                others = shares[code].drop(index=y)
                others = others[[counts.get(o, 0) >= MIN_YEAR_N for o in others.index]]
                if others.empty:
                    continue
                med = float(others.median())
                s = float(shares.at[y, code])
                if code == "<missing>":
                    if s >= 0.95 and med <= 0.5:
                        fail.append(f"D5 {tag}: coding break in {int(y)}: {s:.0%} missing vs a median "
                                    f"{med:.0%} in other years")
                elif s == 0 and med >= BREAK_SHARE and counts[y] * med >= MIN_EXPECTED:
                    fail.append(f"D5 {tag}: coding break in {int(y)}: code {code} "
                                f"('{_definition(spec, code)}') is absent that year vs a median {med:.0%} "
                                f"of rows in other years")

    # D6 cross-field consistency
    for rule in dossier.get("consistency", []):
        rows = df
        if rule.get("years") and has_year:
            rows = df[df[ycol].between(*rule["years"])]
        try:
            ok = rows.eval(rule["expr"], engine="python")
        except Exception as e:  # a rule that cannot run is itself a failure
            fail.append(f"D6 rule '{rule['name']}' could not be evaluated: {e}")
            continue
        ok = pd.Series(ok, index=rows.index).fillna(False).astype(bool)
        nbad = int((~ok).sum())
        if nbad:
            example = list(rows.index[~ok][:5])
            msg = f"D6 rule '{rule['name']}' violated by {nbad} row(s), e.g. index {example}"
            if rule.get("severity") == "warn":
                info.append(msg)
            else:
                fail.append(msg)

    by_year = pd.DataFrame(by_year_cols) if by_year_cols else None
    return {"fail": fail, "info": info, "by_year": by_year}


def check_recode_map(var, mapping, dossier, excluded=()):
    """Check a {code: label} recode map against the dossier entry for `var`."""
    spec = dossier["variables"][var]
    storage = spec.get("storage", "numeric")
    item = spec.get("item", var)
    allowed = _allowed(spec) or set()
    excluded = {_key(c, storage) for c in excluded}
    fail, info = [], []
    mapped = {}
    for code, label in mapping.items():
        k = _key(code, storage)
        mapped[k] = label
        if allowed and k not in allowed:
            fail.append(f"M1 {var}: code {k} is not an allowable value of {item}; "
                        f"a map keyed on it counts nothing (allowable: {sorted(allowed, key=str)})")
    for a in sorted(allowed, key=str):
        if a not in mapped and a not in excluded:
            fail.append(f"M2 {var}: code {a} is not mapped ('{_definition(spec, a)}'); map it or pass it in excluded=")
    forbidden = {_key(c, storage): terms for c, terms in (spec.get("forbidden_labels") or {}).items()}
    for k, label in mapped.items():
        for term in forbidden.get(k, []):
            if term.lower() in str(label).lower():
                fail.append(f"M3 {var}: code {k} labelled '{label}' contradicts its definition "
                            f"'{_definition(spec, k)}' (forbidden term '{term}')")
    groups = {}
    for k, label in mapped.items():
        groups.setdefault(label, []).append(k)
    for label, codes in groups.items():
        if len(codes) > 1:
            info.append(f"{var}: codes {', '.join(sorted(codes, key=str))} merged into '{label}'; confirm every "
                        f"definition belongs under that label: "
                        + "; ".join(f"{c} = {_definition(spec, c)}" for c in sorted(codes, key=str)))
    return {"fail": fail, "info": info}


def _read(path, dossier):
    p = Path(path)
    alnum = [v for v, s in dossier.get("variables", {}).items() if s.get("storage") == "alphanumeric"]
    if p.suffix in (".parquet", ".pq"):
        return pd.read_parquet(p)
    if p.suffix == ".feather":
        return pd.read_feather(p)
    if p.suffix in (".pkl", ".pickle"):
        return pd.read_pickle(p)
    sep = "\t" if p.suffix in (".tsv", ".txt") else ","
    return pd.read_csv(p, sep=sep, dtype={v: str for v in alnum}, low_memory=False)


def main():
    ap = argparse.ArgumentParser(description="Audit data and recode maps against a data-dictionary dossier (L089).")
    ap.add_argument("--dossier", required=True, help="specs/data_dictionary_dossier.json")
    ap.add_argument("--data", help="csv / tsv / parquet / feather / pickle")
    ap.add_argument("--map", help="JSON recode map {code: label}")
    ap.add_argument("--var", help="dossier variable the map recodes")
    ap.add_argument("--excluded", default="", help="comma-separated codes the map drops on purpose")
    ap.add_argument("--out", help="write the markdown report here too")
    a = ap.parse_args()
    dossier = json.loads(Path(a.dossier).read_text())
    lines, fails = [f"# Data-dictionary audit ({dossier.get('source', a.dossier)})", ""], 0
    if a.data:
        rep = audit_frame(_read(a.data, dossier), dossier)
        fails += len(rep["fail"])
        lines += ["## Data: " + a.data, ""] + [f"- FAIL {m}" for m in rep["fail"]] + [f"- info {m}" for m in rep["info"]]
        if rep["by_year"] is not None:
            try:
                table = rep["by_year"].to_markdown()
            except ImportError:  # tabulate not installed
                table = rep["by_year"].to_string()
            lines += ["", "### Non-missing % by year", "", table]
    if a.map:
        if not a.var:
            ap.error("--map needs --var")
        mp = json.loads(Path(a.map).read_text())
        rep = check_recode_map(a.var, mp, dossier, excluded=[c for c in a.excluded.split(",") if c])
        fails += len(rep["fail"])
        lines += ["", f"## Recode map: {a.map} ({a.var})", ""] + [f"- FAIL {m}" for m in rep["fail"]] + [f"- info {m}" for m in rep["info"]]
    lines += ["", f"**{fails} hard failure(s)**"]
    text = "\n".join(lines)
    print(text)
    if a.out:
        Path(a.out).write_text(text + "\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
