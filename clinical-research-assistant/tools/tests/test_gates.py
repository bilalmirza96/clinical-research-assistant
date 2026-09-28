#!/usr/bin/env python3
"""RED/GREEN tests for skills/internal/analyze/scripts/gates.py
(run: python3 tools/tests/test_gates.py).

Same dependency-free style as skills/internal/analyze/tests/test_study_design_tools.py and
tools/tests/test_linters.py: print PASS/FAIL per assertion, exit 1 if anything failed. Each gate
gets one failing and one passing fixture, replaying the Study-Design Standard invariants
(L087-L090) and the L092/L098 reporting lessons.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # .../clinical-research-assistant/tools
SCRIPTS = os.path.join(os.path.dirname(ROOT), "skills", "internal", "analyze", "scripts")
sys.path.insert(0, SCRIPTS)

import gates as G  # noqa: E402

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ================================================================== cohort_n
REG_COHORT_OK = {"results": {
    "os_nhb_crude": {"current": {"value": "1.30", "n": 5000}},
    "os_nhb_modelA": {"current": {"value": "1.14", "n": 5000}},
    "os_nhb_modelB": {"current": {"value": "1.09", "n": 5000}},
    "os_nhw_crude": {"current": {"value": "1.0", "n": 20000}},
    "os_nhw_modelA": {"current": {"value": "1.0", "n": 20000}},
    "os_nhw_modelB": {"current": {"value": "1.0", "n": 20000}},
}}
ok, msg = G.cohort_n(REG_COHORT_OK, {"nhb": 5000, "nhw": 20000})
check(ok, f"cohort_n: matching N across every rung and group passes (msg: {msg})")

REG_COHORT_DRIFT = {"results": {
    "os_nhb_crude": {"current": {"value": "1.30", "n": 5000}},
    "os_nhb_modelA": {"current": {"value": "1.14", "n": 4950}},   # N drifted between rungs
    "os_nhb_modelB": {"current": {"value": "1.09", "n": 4950}},
}}
ok, msg = G.cohort_n(REG_COHORT_DRIFT, {"nhb": 5000})
check(not ok and "differs across rungs" in msg, f"cohort_n: N drift between crude and Model A/B fails (msg: {msg})")

REG_COHORT_WRONG_EXPECTED = {"results": {
    "os_nhb_crude": {"current": {"value": "1.30", "n": 5000}},
    "os_nhb_modelA": {"current": {"value": "1.14", "n": 5000}},
    "os_nhb_modelB": {"current": {"value": "1.09", "n": 5000}},
}}
ok, msg = G.cohort_n(REG_COHORT_WRONG_EXPECTED, {"nhb": 5001})
check(not ok and "curated cohort N" in msg, f"cohort_n: N reconciled across rungs but not to the curated cohort fails (msg: {msg})")

# explicit keys_by_group disambiguates when auto-detection would be ambiguous
REG_COHORT_AMBIGUOUS = {"results": {
    "surgery_nhb_crude": {"current": {"value": "0.5", "n": 111}},
    "os_nhb_crude": {"current": {"value": "1.3", "n": 5000}},
}}
ok, msg = G.cohort_n(REG_COHORT_AMBIGUOUS, {"nhb": 5000},
                     keys_by_group={"nhb": {"crude": "os_nhb_crude"}})
check(ok, f"cohort_n: an explicit keys_by_group mapping resolves an otherwise-ambiguous match (msg: {msg})")

# ================================================================== denominator_named
REG_DENOM_OK = {"results": {
    "surg_nhb": {"label": "NCDB surgery receipt (NHB)", "current": {"value": "0.487 (0.451-0.525)", "n": 5000}},
    "npct_ici": {"label": "Stage IV ICI receipt", "current": {"value": "233/1197"}},
    "npct_dict": {"label": "Stage IV ICI receipt (dict form)", "current": {"value": {"n": 233, "N": 1197}}},
    "labeled_n": {"label": "Charlson >=3, n=812 of the NCDB cohort", "current": {"value": 0.234}},
}}
ok, msg = G.denominator_named(REG_DENOM_OK)
check(ok, f"denominator_named: n, n/N, {{n,N}} and an 'n=' label all count as a stated denominator (msg: {msg})")

REG_DENOM_MISSING = {"results": {
    "surg_nhb": {"label": "NCDB surgery receipt (NHB)", "current": {"value": "0.487 (0.451-0.525)"}},  # no n, no N in label/value
}}
ok, msg = G.denominator_named(REG_DENOM_MISSING)
check(not ok and "surg_nhb" in msg, f"denominator_named: a result with no n/N/label count fails (msg: {msg})")

# an UNSOURCED entry (no current block) is not this gate's concern
REG_DENOM_UNSOURCED = {"results": {"flagged": {"label": "not yet computed", "current": {}}}}
ok, msg = G.denominator_named(REG_DENOM_UNSOURCED)
check(ok, "denominator_named: an entry with no current block (UNSOURCED) is skipped, not failed")

# ================================================================== dictionary_labels
DOSSIER = {"variables": {
    "histology": {"item": "NAACCR 522", "storage": "alphanumeric", "categories": ["Adenocarcinoma", "Squamous"]},
    "stage": {"item": "derived AJCC", "storage": "numeric",
              "codes": {"1": "Stage I", "2": "Stage II", "3": "Stage III", "4": "Stage IV"}},
}}
REG_DICT_OK = {"results": {
    "chemo_by_histology": {"current": {"value": {"Adenocarcinoma": {"OR": 1.1}, "Squamous": {"OR": 0.9}}}},
    "surg_by_stage": {"current": {"value": {"Stage I": 0.6, "Stage III": 0.3}}},
    "scalar": {"current": {"value": "1.30 (1.27-1.34)"}},   # not dict-valued: not judged by this gate
}}
ok, msg = G.dictionary_labels(REG_DICT_OK, DOSSIER)
check(ok, f"dictionary_labels: categories and code definitions declared in the dossier all pass (msg: {msg})")

REG_DICT_BAD = {"results": {
    "chemo_by_histology": {"current": {"value": {"Adenocarcinoma": {"OR": 1.1}, "Other": {"OR": 0.9}}}},
}}
ok, msg = G.dictionary_labels(REG_DICT_BAD, DOSSIER)
check(not ok and "Other" in msg, f"dictionary_labels: a level ('Other') absent from the dossier fails (msg: {msg})")

# ================================================================== two_adjusted_models
REG_LADDER_OK = {"results": {
    "os_nhb_crude": {"current": {"value": "1.30"}},
    "os_nhb_modelA": {"current": {"value": "1.14"}},
    "os_nhb_modelB": {"current": {"value": "1.09"}},
    "os_nhb_iptw": {"current": {"value": "1.21"}},
}}
ok, msg = G.two_adjusted_models(REG_LADDER_OK)
check(ok, f"two_adjusted_models: only modelA/modelB rungs present passes (msg: {msg})")

REG_LADDER_BAD = {"results": {
    "os_nhb_crude": {"current": {"value": "1.30"}},
    "os_nhb_modelA": {"current": {"value": "1.14"}},
    "os_nhb_modelB": {"current": {"value": "1.09"}},
    "os_nhb_modelC": {"current": {"value": "1.05"}},   # a third adjusted model
}}
ok, msg = G.two_adjusted_models(REG_LADDER_BAD)
check(not ok and "modelC" in msg, f"two_adjusted_models: a third adjusted model (modelC) fails (msg: {msg})")

# ================================================================== no_penalizer
tmp = tempfile.mkdtemp()
good_script = Path(tmp) / "run_cox_ok.py"
good_script.write_text("from lifelines import CoxPHFitter\n"
                      "cph = CoxPHFitter(penalizer=0.0)\n"
                      "cph.fit(df, 'T', 'E')\n")
bad_script = Path(tmp) / "run_cox_bad.py"
bad_script.write_text("from lifelines import CoxPHFitter\n"
                     "cph = CoxPHFitter(penalizer=0.05)\n"
                     "cph.fit(df, 'T', 'E')\n")

ok, msg = G.no_penalizer([str(good_script)])
check(ok, f"no_penalizer: penalizer=0.0 passes (msg: {msg})")
ok, msg = G.no_penalizer([str(bad_script)])
check(not ok and "0.05" in msg, f"no_penalizer: a nonzero penalizer=0.05 fails and names the value (msg: {msg})")

# ================================================================== run_time_dates
good_writer = Path(tmp) / "upsert_ok.py"
good_writer.write_text("import number_format as NF\n"
                      "DATE = NF.now_stamp()\n"
                      "print(DATE)\n")
bad_writer = Path(tmp) / "upsert_bad.py"
bad_writer.write_text('DATE = "2026-09-26"\n'
                     "print(DATE)\n")

ok, msg = G.run_time_dates([str(good_writer)])
check(ok, f"run_time_dates: a DATE computed via now_stamp() passes (msg: {msg})")
ok, msg = G.run_time_dates([str(bad_writer)])
check(not ok and "hardcoded DATE" in msg, f"run_time_dates: a hardcoded DATE constant fails (msg: {msg})")

print()
print(f"{len(FAILS)} failure(s)")
sys.exit(1 if FAILS else 0)
