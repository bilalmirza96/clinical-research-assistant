#!/usr/bin/env python3
"""RED/GREEN tests for the study-design tools (run: python3 tests/test_study_design_tools.py).

Each fixture replays a defect that reached the REPEAT DISPARITIES project (esophageal cancer,
NCDB + SEER, 2026) or a value registered there. Synthetic data only; nothing here feeds a
deliverable.

  dictionary_audit  code 3 mapped to "Refused" (NAACCR 1340 has no code 3); code 1 labelled
                    "Not recommended"; the 2023 alphanumeric surgery field parsed as numeric so
                    every 2023 patient read as unoperated; surgery flag contradicting reason 0.
  cohort_flow       differential exclusion by group (missing stage); the 119-patient mismatch
                    between the KM display cohort and the Cox cohort.
  ladder_table      E-values reproduce the registry (OR 0.487 -> 2.221; HR 1.14 -> 1.418); an OR
                    without a stated outcome frequency is refused (the circulating 3.41 was the
                    RR formula applied to a common-outcome OR); N drift across rungs, rungs
                    skipped without a reason, out-of-order rungs and sign flips are flagged.
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import numpy as np
import pandas as pd

import cohort_flow as CF
import dictionary_audit as DA
import ladder_table as LT

FAILS = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ---------------------------------------------------------------- dictionary_audit
REASON_CODES = {
    "0": "Surgery of the primary site was performed",
    "1": "Surgery was not performed because it was not part of the planned first-course treatment",
    "2": "Surgery was not recommended/performed because it was contraindicated due to patient risk factors",
    "5": "Surgery was not performed because the patient died prior to planned or recommended surgery",
    "6": "Surgery was recommended but not performed; no reason was noted",
    "7": "Surgery was recommended but refused by the patient, family member or guardian",
    "8": "Surgery was recommended, unknown if performed",
    "9": "Unknown if surgery was recommended or performed",
}

DOSSIER = {
    "source": "SYNTHETIC test dossier modelled on NCDB PUF 2023",
    "year_column": "YEAR",
    "variables": {
        "REASON_FOR_NO_SURGERY": {
            "item": "NAACCR 1340",
            "ref": "NCDB PUF Data Dictionary (test fixture)",
            "storage": "numeric",
            "codes": REASON_CODES,
            "missing_codes": ["9"],
            "years": [2004, 2023],
            "forbidden_labels": {
                "1": ["not recommended", "not offered", "never offered", "denied"],
                "5": ["not recommended"],
                "6": ["not recommended"],
                "7": ["not recommended"],
            },
        },
        "SURG_2023": {
            "item": "NAACCR 1291",
            "storage": "alphanumeric",
            "pattern": r"^A\d{3}$",
            "years": [2023, 2023],
        },
        "surgery": {
            "item": "derived: any primary-site surgery",
            "storage": "numeric",
            "codes": {"0": "no surgery", "1": "surgery"},
            "years": [2004, 2023],
            "derived_from": ["RX_SUMM_SURG_PRIM_SITE", "SURG_2023"],
        },
    },
    "consistency": [
        {
            "name": "reason code 0 (surgery performed) implies surgery flag 1",
            "expr": "~((REASON_FOR_NO_SURGERY == 0) & (surgery == 0))",
        }
    ],
}

OLD_MAP = {0: "Surgery performed", 1: "Not recommended", 2: "Not recommended", 3: "Refused",
           5: "Not recommended", 6: "Not recommended", 7: "Not recommended",
           8: "Recommended, unknown if performed", 9: "Unknown"}
NEW_MAP = {0: "Surgery performed", 1: "Not part of planned first course",
           2: "Contraindicated by patient risk factors", 5: "Died before planned surgery",
           6: "Recommended, not performed, reason not stated", 7: "Refused by patient or family",
           8: "Recommended, unknown if performed", 9: "Unknown whether recommended"}

res = DA.check_recode_map("REASON_FOR_NO_SURGERY", OLD_MAP, DOSSIER)
fails = " | ".join(res["fail"]).lower()
check("code 3" in fails and "not an allowable" in fails, "recode map: nonexistent code 3 is a hard failure")
check("code 1" in fails and "not recommended" in fails, "recode map: code 1 labelled 'Not recommended' is a hard failure")
check("code 7" in fails, "recode map: refusal (code 7) labelled 'Not recommended' is a hard failure")
check(any("merged" in s.lower() for s in res["info"]), "recode map: merged codes are listed for review")
res_ok = DA.check_recode_map("REASON_FOR_NO_SURGERY", NEW_MAP, DOSSIER)
check(not res_ok["fail"], "recode map: the corrected NAACCR 1340 map passes")
res_gap = DA.check_recode_map("REASON_FOR_NO_SURGERY", {k: v for k, v in NEW_MAP.items() if k != 7}, DOSSIER)
check(any("code 7" in s.lower() and "not mapped" in s.lower() for s in res_gap["fail"]),
      "recode map: an allowable code left unmapped is a hard failure")

rng = np.random.default_rng(42)
n = 4000
years = rng.integers(2004, 2024, n)
surg = rng.random(n) < 0.45
reason = np.where(surg, 0, rng.choice([1, 2, 5, 6, 7, 8, 9], n))
df = pd.DataFrame({
    "YEAR": years,
    "REASON_FOR_NO_SURGERY": reason,
    "surgery": surg.astype(int),
    "SURG_2023": np.where((years == 2023) & surg, "A200", np.where(years == 2023, "A000", None)),
})
clean = DA.audit_frame(df, DOSSIER)
check(not clean["fail"], "audit: a correctly parsed frame has no hard failures")

# Replay the 2023 parse defect: pd.to_numeric('A200') -> NaN, so every 2023 patient became 'no surgery'.
bad = df.copy()
bad.loc[bad.YEAR == 2023, "surgery"] = 0
bad["SURG_2023"] = pd.to_numeric(bad["SURG_2023"], errors="coerce")
bad.loc[bad.index[:3], "REASON_FOR_NO_SURGERY"] = 4  # a code NAACCR 1340 does not allow
out = DA.audit_frame(bad, DOSSIER)
f = " | ".join(out["fail"]).lower()
check("surg_2023" in f and "alphanumeric" in f, "audit: alphanumeric field held as numeric is a hard failure")
check("reason code 0" in f, "audit: surgery flag contradicting reason code 0 is a hard failure")
check("surgery" in f and "2023" in f and "break" in f, "audit: a code that vanishes in one diagnosis year is flagged as a coding break")
check("reason_for_no_surgery" in f and "4" in f, "audit: a value outside the allowable codes is a hard failure")

# ---------------------------------------------------------------- cohort_flow
g = np.array(["White"] * 3000 + ["Black"] * 1000)
frame = pd.DataFrame({"id": np.arange(4000), "race": g, "months": rng.integers(0, 60, 4000)})
stage_missing = np.zeros(4000, bool)
stage_missing[:450] = True            # 15% of White
stage_missing[3000:3200] = True       # 20% of Black
frame["stage_missing"] = stage_missing
frame["site_ok"] = True
flow = CF.CohortFlow(frame, id_col="id", group_col="race", source="synthetic")
cur = flow.include("Esophagus primary site", frame["site_ok"], rationale="study site", ref="ICD-O-3 C15")
cur = flow.exclude("Missing clinical stage", lambda d: d["stage_missing"], rationale="stage needed", ref="TNM_CLIN_STAGE_GROUP")
check(len(cur) == 4000 - 650, "cohort_flow: exclusion applied exactly")
check(any("Missing clinical stage" in fl for fl in flow.flags), "cohort_flow: 15% vs 20% exclusion by group is flagged as differential")
check(not any("Esophagus" in fl for fl in flow.flags), "cohort_flow: a step removing nobody is not flagged")
surv = flow.endpoint("Overall survival", lambda d: d["months"] > 0, rationale="0-month follow-up has no person-time")
check(len(flow.current) == 3350 and len(surv) < 3350, "cohort_flow: endpoint sub-cohort leaves the parent cohort intact")
tmp = tempfile.mkdtemp()
flow.write(tmp)
ops = json.load(open(os.path.join(tmp, "filter_operations.json")))
check(ops["steps"][1]["n_in"] == 4000 and ops["steps"][1]["n_out"] == 3350, "cohort_flow: filter_operations.json records n_in/n_out")
check("Black" in ops["steps"][1]["by_group"], "cohort_flow: counts are recorded by exposure group")
log = open(os.path.join(tmp, "filter_log.md")).read()
check("Overall survival" in log and "Differential" in log, "cohort_flow: filter_log.md carries endpoint cohorts and flags")
try:
    CF.assert_same_cohort(set(range(114633)), set(range(114752)), "KM display vs Cox")
    check(False, "cohort_flow: a 119-patient mismatch raises")
except AssertionError as e:
    check("119" in str(e), "cohort_flow: a 119-patient mismatch raises and names the count")
try:
    CF.assert_n(114633, 114633, "Cox cohort")
    check(True, "cohort_flow: exact N match passes")
except AssertionError:
    check(False, "cohort_flow: exact N match passes")

# ---------------------------------------------------------------- ladder_table / E-values
e, ci = LT.evalue(0.487, 0.451, 0.525, measure="OR", common=True)
check(round(e, 3) == 2.221 and round(ci, 3) == 2.104, f"evalue: surgery OR 0.487 (common) = 2.221 / CI 2.104 (got {e:.3f}/{ci:.3f})")
e, ci = LT.evalue(1.14, 1.11, 1.171, measure="HR", common=True)
check(round(e, 3) == 1.418 and round(ci, 3) == 1.359, f"evalue: OS HR 1.14 (common) = 1.418 / CI 1.359 (got {e:.3f}/{ci:.3f})")
e, _ = LT.evalue(0.50, measure="RR")
check(round(e, 3) == 3.414, "evalue: RR 0.50 = 3.414 (correct only for a risk ratio)")
try:
    LT.evalue(0.50, measure="OR")
    check(False, "evalue: an OR without a stated outcome frequency is refused")
except ValueError:
    check(True, "evalue: an OR without a stated outcome frequency is refused")
e, ci = LT.evalue(1.08, 0.99, 1.17, measure="HR", common=True)
check(ci == 1.0, "evalue: a CI that crosses the null has CI E-value 1")

rungs = [
    dict(rung="crude", est=1.304, lo=1.273, hi=1.336, n=1000),
    dict(rung="modelA", est=1.14, lo=1.11, hi=1.171, n=1000),
    dict(rung="modelB", est=1.091, lo=1.063, hi=1.121, n=900),
]
md, flags = LT.ladder_table(rungs, measure="HR", common=True)
check(any("'iptw'" in fl and "skipped" in fl.lower() for fl in flags), "ladder: a required rung (IPTW) missing without a reason is flagged")
check(any("N changes" in fl for fl in flags), "ladder: N drift between unadjusted, Model A and Model B is flagged")
check("50.6" in md, "ladder: log-scale attenuation unadjusted 1.304 -> Model A 1.14 = 50.6%")
_, flags2 = LT.ladder_table(rungs, measure="HR", common=True,
                            skipped={"iptw": "run in a separate script",
                                     "mediation": "no why-question for this objective", "ml": "no question beyond rungs 1-7"})
check(not any("skipped" in fl.lower() for fl in flags2), "ladder: a stated reason clears the skipped-rung flag")
check(any("mediation" in fl for fl in flags) and any("'ml'" in fl for fl in flags), "ladder: mediation and ML need an explicit run-or-skip decision")
_, flags3 = LT.ladder_table([rungs[0], dict(rung="iptw", est=1.2, lo=1.1, hi=1.3, n=1000), rungs[1]], measure="HR", common=True,
                            skipped={"modelB": "x"})
check(any("order" in fl.lower() for fl in flags3), "ladder: rungs out of canonical order are flagged")
_, flags4 = LT.ladder_table([dict(rung="crude", est=1.2, lo=1.1, hi=1.3, n=10),
                             dict(rung="modelA", est=0.95, lo=0.9, hi=1.0, n=10)], measure="HR", common=True,
                            skipped={"modelB": "x", "iptw": "x"})
check(any("direction" in fl.lower() for fl in flags4), "ladder: an estimate that crosses the null is flagged")
_, flags5 = LT.ladder_table([dict(rung="crude", est=1.3, lo=1.2, hi=1.4, n=10), dict(rung="ses", est=1.2, lo=1.1, hi=1.3, n=10)],
                            measure="HR", common=True)
check(any("Unknown rung 'ses'" in fl for fl in flags5), "ladder: a third adjusted model (e.g. SES-only) is flagged; two adjusted models only")

print()
print(f"{len(FAILS)} failure(s)")
sys.exit(1 if FAILS else 0)
