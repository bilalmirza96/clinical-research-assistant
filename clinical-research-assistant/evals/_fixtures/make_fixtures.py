#!/usr/bin/env python3
"""
make_fixtures.py — generates SYNTHETIC-ONLY fixture data for the CRA plugin
eval suite (clinical-research-assistant/evals/).

No real patient data. All values are seeded (random_state=42) and fabricated
for the sole purpose of exercising the plugin's lesson-enforcement logic
(see clinical-research-assistant/evals/README.md). Do not use these files for
anything other than eval scaffolding.

Outputs (written next to this script):
  cohort_50.csv        50-row synthetic clinical cohort
  tmb_mixed.csv         mixed-platform (WES vs targeted panel) mutation/TMB data
  registry_mock.json    a MASTER_ANALYSIS_REGISTRY-shaped mock registry
  abstract_draft.md     a short disparities abstract draft with known style issues
  project_CLAUDE.md     a minimal project brief naming Reports/ as the registry home

Run: python3 make_fixtures.py
"""
import json
import os
import random

import numpy as np

SEED = 42
random.seed(SEED)
rng = np.random.default_rng(SEED)

HERE = os.path.dirname(os.path.abspath(__file__))


def w(name, content):
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path} ({len(content)} bytes)")


# ---------------------------------------------------------------------------
# 1. cohort_50.csv
# ---------------------------------------------------------------------------
def make_cohort_csv():
    n = 50
    ids = [f"SYN{str(i + 1).zfill(3)}" for i in range(n)]
    age = rng.normal(64, 11, n).round(0).clip(28, 92).astype(int)
    sex = rng.choice(["M", "F"], size=n, p=[0.55, 0.45])
    race_ethnicity = rng.choice(
        [
            "Non-Hispanic White",
            "Non-Hispanic Black",
            "Hispanic",
            "Non-Hispanic Asian/Pacific Islander",
            "Other/Unknown",
        ],
        size=n,
        p=[0.55, 0.20, 0.12, 0.09, 0.04],
    )
    stage = rng.choice(["I", "II", "III", "IV"], size=n, p=[0.30, 0.30, 0.25, 0.15])
    treatment = rng.choice([0, 1], size=n, p=[0.38, 0.62])  # 1 = definitive treatment received
    exposure = rng.choice([0, 1], size=n, p=[0.5, 0.5])  # 1 = exposure of interest (e.g., delayed care >90d)

    # time_months / event: exposure=1 given a mild hazard bump for face validity
    base_hazard = 0.018
    hr_true = 1.35
    lam = base_hazard * np.where(exposure == 1, hr_true, 1.0)
    time_months = rng.exponential(1.0 / lam, n)
    censor_time = rng.uniform(6, 60, n)
    event = (time_months <= censor_time).astype(int)
    time_months = np.minimum(time_months, censor_time).round(1)

    # covariate with ~8% missing (4/50 rows)
    comorbidity_index = rng.integers(0, 5, n).astype(float)
    missing_idx = rng.choice(n, size=4, replace=False)  # 4/50 = 8%
    comorbidity_index[missing_idx] = np.nan

    # one categorical with a single-patient level
    insurance_type = rng.choice(
        ["Private", "Medicare", "Medicaid", "Uninsured"], size=n, p=[0.4, 0.35, 0.2, 0.05]
    ).astype(object)
    insurance_type[0] = "Other-TribalHealth"  # sparse level, n=1 patient

    header = [
        "id", "age", "sex", "race_ethnicity", "stage", "treatment", "exposure",
        "time_months", "event", "comorbidity_index", "insurance_type",
    ]
    rows = []
    for i in range(n):
        com = "" if np.isnan(comorbidity_index[i]) else str(int(comorbidity_index[i]))
        rows.append([
            ids[i], str(age[i]), sex[i], race_ethnicity[i], stage[i],
            str(int(treatment[i])), str(int(exposure[i])), f"{time_months[i]:.1f}",
            str(int(event[i])), com, insurance_type[i],
        ])

    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(r))
    w("cohort_50.csv", "\n".join(lines) + "\n")

    # Handed to make_registry_mock() below so the registry's stageIV entry is
    # DERIVED from the same array that produced the CSV, not a second
    # hand-typed literal (that mismatch -- label says "of the 50-patient
    # cohort" while n was hardcoded "5/8" -- was the L091 fixture-contradiction
    # bug this function now prevents by construction). No new RNG draws here,
    # so downstream fixtures (tmb_mixed.csv etc.) are unaffected.
    return {"n": n, "stageIV_n": int((stage == "IV").sum())}


# ---------------------------------------------------------------------------
# 2. tmb_mixed.csv — mixed WES vs targeted-panel mutation/TMB data
# ---------------------------------------------------------------------------
def make_tmb_csv():
    # panel gene coverage (the trap: PANEL_B does not test APC or SMAD4)
    panel_genes = {
        "PANEL_A_71gene": ["TP53", "KRAS", "PIK3CA", "APC", "SMAD4", "EGFR"],
        "PANEL_B_50gene": ["TP53", "KRAS", "PIK3CA", "EGFR"],  # omits APC, SMAD4
    }
    all_genes = ["TP53", "KRAS", "PIK3CA", "APC", "SMAD4", "EGFR"]

    n_patients = 30
    patient_ids = [f"TMB{str(i + 1).zfill(3)}" for i in range(n_patients)]
    platforms = rng.choice(["WES", "panel"], size=n_patients, p=[0.4, 0.6])

    rows = []
    header = [
        "patient_id", "platform", "panel_name", "gene", "gene_mutated",
        "tmb_value_mut_per_mb", "tmb_category",
    ]
    for pid, platform in zip(patient_ids, platforms):
        if platform == "WES":
            panel_name = "NA"
            genes_tested = all_genes  # WES covers everything
            tmb_value = ""  # WES rows in this cohort only report the binary category (per fixture spec)
            tmb_category = rng.choice(["High", "Low"], p=[0.3, 0.7])
        else:
            panel_name = rng.choice(list(panel_genes.keys()))
            genes_tested = panel_genes[panel_name]
            tmb_value = round(float(rng.uniform(0.5, 12.0)), 2)  # mutations/Mb, panel-derived
            tmb_category = ""  # panels in this cohort report per-base TMB, not the binary category

        for gene in genes_tested:
            mutated = int(rng.random() < 0.22)
            rows.append([
                pid, platform, panel_name, gene, str(mutated),
                str(tmb_value) if platform == "panel" else "",
                tmb_category if platform == "WES" else "",
            ])
        # NOTE: genes NOT in genes_tested simply have no row for this patient.
        # This mirrors real AACR GENIE-style panel data: a gene absent from a
        # patient's panel is NOT-TESTED, not wild-type. A downstream pivot to a
        # wide patient-by-gene matrix must fill missing combinations with NaN
        # (not-tested), never 0 (wild-type) -- see lessons-log L061.

    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(r))
    w("tmb_mixed.csv", "\n".join(lines) + "\n")

    # small side-car documenting panel coverage explicitly (so the "ground truth"
    # of which genes are off-panel for which platform is auditable, without
    # solving the coding problem for the agent)
    w("tmb_panel_coverage.json", json.dumps(panel_genes, indent=2) + "\n")


# ---------------------------------------------------------------------------
# 3. registry_mock.json — mirrors analysis_registry.py's schema
# ---------------------------------------------------------------------------
def make_registry_mock(cohort_stats):
    stageIV_n = cohort_stats["stageIV_n"]
    cohort_n = cohort_stats["n"]
    stageIV_value = stageIV_n / cohort_n
    registry = {
        "registry_meta": {
            "project": "EVAL-SYNTHETIC-DISPARITIES",
            "schema_version": "1.0",
            "standard": (
                "Single Consolidated Analysis Registry (SCAR). One file per "
                "project; update in place; prior valid results carried forward "
                "in each entry's history[]. Rule: 00_Context/working-rules.md."
            ),
            "created": "2026-09-01",
            "last_updated": "2026-09-15",
            "current_analysis_vintages": {"cohort_50": "EVAL-V2"},
            "update_log": [
                {
                    "date": "2026-09-01",
                    "analysis_id": "EVAL-V1",
                    "action": "initial_load",
                    "note": "synthetic cohort_50.csv unadjusted pass",
                },
                {
                    "date": "2026-09-15",
                    "analysis_id": "EVAL-V2",
                    "action": "adjusted_model_added",
                    "note": "Model B (fully adjusted) added; superseded EVAL-V1 unadjusted-only entries where re-estimated",
                },
            ],
        },
        "results": {
            "cohort_50.exposure.unadjusted_HR": {
                "domain": "cohort_50",
                "label": "Synthetic cohort unadjusted HR, exposure (delayed care) vs outcome",
                "current": {
                    "value": 1.243,
                    "ci": [0.671, 2.302],
                    "p": "0.49",
                    "n": "50",
                    "analysis_id": "EVAL-V1",
                    "script": "eval_fixture_analysis.py",
                    "source_file": "Reports/EVAL-V1_results.json",
                    "source_key": "unadjusted.hr",
                    "date": "2026-09-01",
                    "status": "current",
                },
                "history": [],
            },
            "cohort_50.exposure.adjusted_HR_modelB": {
                "domain": "cohort_50",
                "label": "Synthetic cohort Model B (fully adjusted) HR, exposure (delayed care) vs outcome",
                "current": {
                    "value": 1.275,
                    "ci": [0.685, 2.373],
                    "p": "0.44",
                    "n": "50",
                    "analysis_id": "EVAL-V2",
                    "script": "eval_fixture_analysis.py",
                    "source_file": "Reports/EVAL-V2_results.json",
                    "source_key": "modelB.hr",
                    "date": "2026-09-15",
                    "status": "current",
                },
                "history": [
                    {
                        "value": 1.081,
                        "ci": [0.611, 1.912],
                        "p": "0.51",
                        "n": "50",
                        "analysis_id": "EVAL-V1-penalized",
                        "script": "eval_fixture_analysis.py",
                        "source_file": "Reports/EVAL-V1_results.json",
                        "source_key": "modelB_penalized.hr",
                        "date": "2026-09-01",
                        "status": "superseded",
                        "superseded_reason": "penalizer=0.05 inflated/attenuated the exposure HR; refit unpenalized per L092",
                    }
                ],
            },
            "cohort_50.comorbidity_index.proportion_missing": {
                "domain": "cohort_50",
                "label": "Proportion of cohort_50 with missing comorbidity_index",
                "current": {
                    "value": 0.08,
                    "ci": None,
                    "p": "NA",
                    "n": "4/50",
                    "analysis_id": "EVAL-V1",
                    "script": "eval_fixture_analysis.py",
                    "source_file": "Reports/EVAL-V1_results.json",
                    "source_key": "missingness.comorbidity_index",
                    "date": "2026-09-01",
                    "status": "current",
                },
                "history": [],
            },
            "cohort_50.stageIV.proportion_of_cohort": {
                "domain": "cohort_50",
                "label": "Proportion of cohort_50 diagnosed at stage IV",
                "current": {
                    "value": stageIV_value,
                    "ci": None,
                    "p": "NA",
                    "n": f"{stageIV_n}/{cohort_n}",
                    "analysis_id": "EVAL-V1",
                    "script": "eval_fixture_analysis.py",
                    "source_file": "Reports/EVAL-V1_results.json",
                    "source_key": "descriptive.stageIV_proportion_of_cohort",
                    "date": "2026-09-01",
                    "status": "current",
                },
                "history": [],
            },
        },
        "flags": [
            {
                "id": "cohort_50.bmi_at_diagnosis",
                "note": "BMI at diagnosis is not captured in cohort_50.csv; UNSOURCED, never guessed.",
                "date": "2026-09-01",
            }
        ],
        "archived_sources": [],
    }
    w("registry_mock.json", json.dumps(registry, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 4. abstract_draft.md — short disparities abstract with known style issues
# ---------------------------------------------------------------------------
ABSTRACT_DRAFT = """# Draft Abstract (synthetic, for eval fixture use only)

## Background
Racial disparities in access to definitive treatment remain a major concern.
Caucasian patients have been reported to receive definitive treatment at
higher rates than other groups, but the drivers among Oriental and other
minority populations are less well characterized.

## Methods
We analyzed a synthetic cohort of 50 patients (cohort_50.csv). Race was
categorized as European American, Black, Hispanic, and Asian based on
self-report. Logistic regression estimated the association between exposure
(delayed care >90 days) and receipt of definitive treatment, adjusting for
age, stage, and comorbidity index.

## Results
Of the 50 patients, 31 (62%) received definitive treatment. The unadjusted
odds ratio for treatment among European American patients versus all others
was 1.243 (95% CI 0.671-2.302). After full adjustment the odds ratio was
1.28 (95% CI 0.69-2.37). Missingness in comorbidity index was 8.0%. Overall
survival at 12 months was 74.5%.

## Conclusion
European American patients in this synthetic cohort experienced modestly
higher rates of definitive treatment; the difference did not reach
significance in this small sample.
"""


def make_abstract_draft():
    w("abstract_draft.md", ABSTRACT_DRAFT)


# ---------------------------------------------------------------------------
# 5. project_CLAUDE.md — minimal project brief naming Reports/ as registry home
# ---------------------------------------------------------------------------
PROJECT_CLAUDE = """# EVAL-SYNTHETIC-DISPARITIES (fixture project)

## What This Is
A synthetic, seeded (random_state=42) disparities cohort used ONLY to exercise
the clinical-research-assistant plugin's eval suite. No real patient data.
Question: is a synthetic "delayed care" exposure associated with receipt of
definitive treatment and overall survival in a 50-patient synthetic cohort.

## Key Paths
- Raw data: `data/cohort_50.csv`, `data/tmb_mixed.csv`
- Registry: `Reports/MASTER_ANALYSIS_REGISTRY.json` (mirrors
  `registry_mock.json` seeded into this workspace)
- Outputs: `Reports/`

## Conventions
- Every analysis result is upserted into `Reports/MASTER_ANALYSIS_REGISTRY.json`
  (see `skills/internal/analyze/scripts/analysis_registry.py`).
- Quantities no analysis computes are flagged UNSOURCED, never guessed.

## Rules
- Never modify `data/` in place.
- random_state=42 on every stochastic call.

## Current Status
- Last completed: cohort assembled, unadjusted pass registered (EVAL-V1).
- Next: adjusted analysis, sensitivity battery, abstract draft.
"""


def make_project_claude():
    w("project_CLAUDE.md", PROJECT_CLAUDE)


if __name__ == "__main__":
    cohort_stats = make_cohort_csv()
    make_tmb_csv()
    make_registry_mock(cohort_stats)
    make_abstract_draft()
    make_project_claude()
    print("done.")
