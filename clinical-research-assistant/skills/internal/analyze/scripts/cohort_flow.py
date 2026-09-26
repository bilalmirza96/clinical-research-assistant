#!/usr/bin/env python3
"""cohort_flow.py - build the analytic cohort as a recorded sequence of inclusion and exclusion
steps (analyze/references/cohort-curation.md, L088).

Every step keeps its counts overall and by exposure group, and a step that removes a clearly
different share of one group is flagged as differential exclusion. Endpoint cohorts (for example
"overall survival: follow-up > 0 months") are named subsets of the parent cohort, so a Kaplan-Meier
export and a Cox model can never quietly use different patients. assert_n / assert_same_cohort
give exact, not approximate, reconciliation before a number leaves the project.

    flow = CohortFlow(raw, id_col="PUF_CASE_ID", group_col="race", source="NCDB PUF 2023", source_sha256=sha)
    df = flow.include("Esophagus, ICD-O-3 C15.0-C15.9", raw["PRIMARY_SITE"].str.startswith("C15"),
                      rationale="study site", ref="NAACCR 400")
    df = flow.exclude("Unknown clinical stage", lambda d: d["stage"].isna(),
                      rationale="stage is a Model A confounder", ref="TNM_CLIN_STAGE_GROUP")
    os_df = flow.endpoint("Overall survival", lambda d: d["months"] > 0,
                          rationale="0-month follow-up contributes no person-time")
    flow.write("data/working")                 # filter_operations.json + filter_log.md
    assert_n(REGISTERED_OS_N, len(os_df), "OS cohort")

Masks are boolean Series aligned to the current frame, or callables taking the current frame.
A mask containing missing values raises: decide explicitly whether unknowns are in or out.
"""
import json
from pathlib import Path

import pandas as pd

try:
    from scipy.stats import chi2_contingency
except ImportError:  # the flag still fires on the percentage-point rule alone
    chi2_contingency = None


class CohortFlow:
    def __init__(self, frame, id_col, group_col=None, source="", source_sha256=None,
                 diff_pp=2.0, alpha=0.05):
        if frame[id_col].duplicated().any():
            raise ValueError(f"{id_col} is not unique ({int(frame[id_col].duplicated().sum())} duplicates); "
                             f"define the cohort unit (patient, tumour, admission) before filtering")
        self.current = frame
        self.id_col, self.group_col = id_col, group_col
        self.source, self.source_sha256 = source, source_sha256
        self.n_source = len(frame)
        self.diff_pp, self.alpha = diff_pp, alpha
        self.steps, self.endpoints, self.flags = [], [], []

    # ------------------------------------------------------------------ internals
    def _groups(self, d):
        if not self.group_col:
            return {}
        return d[self.group_col].astype(str).value_counts().to_dict()

    def _mask(self, mask, d, name):
        m = mask(d) if callable(mask) else mask
        if not isinstance(m, pd.Series):
            m = pd.Series(m, index=d.index)
        m = m.reindex(d.index)
        if m.isna().any():
            raise ValueError(f"step '{name}': mask has {int(m.isna().sum())} missing value(s); "
                             f"state whether unknowns are included or excluded")
        return m.astype(bool)

    def _by_group(self, before, after):
        g_in, g_out = self._groups(before), self._groups(after)
        out = {}
        for g, n_in in g_in.items():
            n_out = g_out.get(g, 0)
            out[g] = {"n_in": int(n_in), "n_out": int(n_out), "removed": int(n_in - n_out),
                      "pct_removed": round(100.0 * (n_in - n_out) / n_in, 2) if n_in else 0.0}
        return out

    def _differential(self, by_group):
        if len(by_group) < 2 or sum(v["removed"] for v in by_group.values()) == 0:
            return None
        pct = {g: v["pct_removed"] for g, v in by_group.items()}
        hi, lo = max(pct, key=pct.get), min(pct, key=pct.get)
        gap = pct[hi] - pct[lo]
        if gap < self.diff_pp:
            return None
        p = None
        if chi2_contingency is not None:
            table = [[v["removed"], v["n_out"]] for v in by_group.values()]
            try:
                p = float(chi2_contingency(table)[1])
            except ValueError:
                p = None
            if p is not None and p >= self.alpha:
                return None
        ptxt = f", chi2 P={p:.2g}" if p is not None else ""
        return (f"removed {pct[hi]:.1f}% of {hi} vs {pct[lo]:.1f}% of {lo} "
                f"({gap:.1f} points{ptxt}); run a selection sensitivity analysis")

    def _record(self, bucket, op, name, before, after, rationale, ref, expr):
        by_group = self._by_group(before, after)
        rec = {"step": len(self.steps) + 1 if bucket is self.steps else len(self.endpoints) + 1,
               "op": op, "name": name, "expr": expr or name, "rationale": rationale, "ref": ref,
               "n_in": int(len(before)), "n_out": int(len(after)), "removed": int(len(before) - len(after)),
               "by_group": by_group}
        diff = self._differential(by_group)
        if diff:
            rec["differential"] = diff
            label = "Step" if bucket is self.steps else "Endpoint"
            self.flags.append(f"{label} {rec['step']} '{name}': {diff}")
        bucket.append(rec)

    # ------------------------------------------------------------------ public API
    def include(self, name, mask, rationale, ref="", expr=None):
        """Keep rows where mask is True."""
        m = self._mask(mask, self.current, name)
        after = self.current[m]
        self._record(self.steps, "include", name, self.current, after, rationale, ref, expr)
        self.current = after
        return after

    def exclude(self, name, mask, rationale, ref="", expr=None):
        """Drop rows where mask is True."""
        m = self._mask(mask, self.current, name)
        after = self.current[~m]
        self._record(self.steps, "exclude", name, self.current, after, rationale, ref, expr)
        self.current = after
        return after

    def endpoint(self, name, mask, rationale, ref="", expr=None):
        """A named endpoint sub-cohort of the current cohort; the parent is left unchanged."""
        m = self._mask(mask, self.current, name)
        sub = self.current[m]
        self._record(self.endpoints, "endpoint", name, self.current, sub, rationale, ref, expr)
        return sub

    def write(self, outdir):
        """Write filter_operations.json (machine) and filter_log.md (CONSORT by group)."""
        out = Path(outdir)
        out.mkdir(parents=True, exist_ok=True)
        ops = {"source": self.source, "source_sha256": self.source_sha256, "n_source": self.n_source,
               "id_col": self.id_col, "group_col": self.group_col, "steps": self.steps,
               "endpoints": self.endpoints, "final_n": int(len(self.current)), "flags": self.flags}
        (out / "filter_operations.json").write_text(json.dumps(ops, indent=2) + "\n")
        groups = sorted({g for s in self.steps + self.endpoints for g in s["by_group"]})
        head = "| # | Step | n in | n out | Removed | " + " | ".join(f"{g} removed (%)" for g in groups) + " | Rationale | Dictionary ref |"
        rule = "|" + "---|" * (6 + len(groups) + 1)

        def row(s):
            cells = [f"{s['by_group'].get(g, {}).get('removed', 0):,} ({s['by_group'].get(g, {}).get('pct_removed', 0):.1f})"
                     for g in groups]
            return (f"| {s['step']} | {s['op']}: {s['name']} | {s['n_in']:,} | {s['n_out']:,} | {s['removed']:,} | "
                    + " | ".join(cells) + f" | {s['rationale']} | {s['ref']} |")

        lines = [f"# Cohort flow: {self.source}", "",
                 f"Source N = {self.n_source:,}" + (f"; sha256 {self.source_sha256}" if self.source_sha256 else ""),
                 f"Analytic cohort N = {len(self.current):,}", "", "## Inclusion and exclusion steps", "", head, rule]
        lines += [row(s) for s in self.steps]
        lines += ["", "## Endpoint cohorts (subsets of the analytic cohort)", ""]
        if self.endpoints:
            lines += [head.replace("| # | Step |", "| # | Endpoint |"), rule] + [row(s) for s in self.endpoints]
        else:
            lines.append("None defined.")
        lines += ["", "## Differential exclusion flags", ""]
        lines += [f"- {f}" for f in self.flags] if self.flags else ["None."]
        (out / "filter_log.md").write_text("\n".join(lines) + "\n")
        return out


def assert_n(expected, observed, label=""):
    """Exact N reconciliation: close is not equal."""
    if int(expected) != int(observed):
        raise AssertionError(f"{label}: N={int(observed):,} but the registered cohort has N={int(expected):,} "
                             f"(difference {int(observed) - int(expected):+,}); rebuild from the cohort artifact")


def assert_same_cohort(expected_ids, observed_ids, label=""):
    """Exact patient-level reconciliation between two artifacts that claim the same cohort."""
    a, b = set(expected_ids), set(observed_ids)
    if a != b:
        raise AssertionError(f"{label}: cohorts differ - {len(a - b):,} expected id(s) missing, "
                             f"{len(b - a):,} unexpected id(s) present (expected N={len(a):,}, "
                             f"observed N={len(b):,})")
