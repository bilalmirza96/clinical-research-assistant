# EVAL-SYNTHETIC-DISPARITIES (fixture project)

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
