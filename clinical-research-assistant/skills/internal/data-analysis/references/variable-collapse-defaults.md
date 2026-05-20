# Variable Collapse Defaults

When `/analyze` Phase 1 INTAKE encounters a multi-category variable without a user-specified collapse rule, apply these defaults and **flag the auto-collapse in the Phase 3 critique panel** (Lessons-applier surfaces it). User can override at HALT 1 via section-by-section revise.

Every auto-collapse decision is recorded in `variable_spec.json` with an `auto_collapsed_from: "<original_column>"` field for full audit traceability.

---

## Default rules

| Variable | Default collapse | Reference category | Rationale |
|---|---|---|---|
| **Race / ethnicity** (≥3 categories) | NIH 5-category: NHW / NHB / Hispanic / Asian-NHPI / Other-Unknown | NHW | Standard for federal grant reporting; matches NCDB / NSQIP convention |
| **Insurance** | Private / Medicare / Medicaid / Uninsured / Other | Private | Captures the access-disparity gradient most studies care about |
| **Age (continuous → categorical, if requested)** | 10-year bands ≥18 (18-27 / 28-37 / 38-47 / 48-57 / 58-67 / 68-77 / 78+) | band containing cohort median | Standard demographic banding |
| **ASA class** | I-II / III / IV+ | I-II | Captures the meaningful risk gradient; avoids ASA I sparsity |
| **AJCC Stage (8th ed.)** | I / II / III / IV (numerical Roman preserved) | I | Preserves prognostic ordering; no collapse needed in most cases |
| **Tumor grade** | Well / Moderately / Poorly / Undifferentiated | Well | Standard pathology grading |
| **BMI** | <25 / 25-<30 / 30-<35 / ≥35 | <25 | WHO obesity classes I-III collapsed; under-25 as reference |
| **Smoking status** | Never / Former / Current | Never | Standard exposure stratification |
| **Charlson Comorbidity Index** | 0 / 1 / 2 / 3+ | 0 | Standard comorbidity banding for risk-adjustment |
| **Income quartile (registry-specific)** | Q1-lowest / Q2 / Q3 / Q4-highest | Q4-highest | Preserves gradient; highest as reference for "exposed to disadvantage" framing |
| **Education quartile (registry-specific)** | Q1-lowest / Q2 / Q3 / Q4-highest | Q4-highest | Same logic as income |
| **Procedure approach** | Open / Lap / Robotic | Open | Open as historical reference; collapse other minimally invasive into Lap if necessary |
| **Procedure year (if not the exposure)** | 5-year bands | first band | Captures temporal trend without overfitting |
| **Hospital volume (annual cases)** | Low (<25th pct) / Mid / High (>75th pct) of cohort | High | Captures volume-outcome gradient |
| **Tumor size (continuous → categorical, if requested)** | ≤2cm / 2-5cm / >5cm | ≤2cm | Standard surgical oncology bands |

---

## Variables that should NOT be auto-collapsed

Always halt for user input on these — collapsing destroys signal:

- **Outcome variables** (CR-POPF grade should not be silently collapsed; LET THE USER state the binary definition explicitly)
- **The primary exposure** if it's a multi-level construct under study (e.g., comparing surgical vs medical vs radiation therapy — never auto-collapse)
- **Time-to-event variables** (always preserve as time + event, not as categorical)
- **Tumor mutation / genetic variant fields** (binary or multi-allelic specifics needed)

If INTAKE encounters one of these without user specification → halt mid-Phase 1 with explicit prompt.

---

## Override mechanism

User can override any default by:

1. **In `study_spec.json`** at project setup: declare `variable_collapse_overrides: {variable: rule}`
2. **At HALT 1** via section-by-section revise on the variable_spec
3. **Post-HALT-1** via the soft-lock amendment protocol (creates `variable_spec_amendments.json` entry)

---

## Documentation in the analysis report

Section 5 (Variables) of the master analysis_report.md lists every auto-collapsed variable with its rule, surfacing the decisions transparently for reviewers.

---

## Lesson references

- **L020** — Race terminology must match what was actually measured; use source dataset labels (TCGA / NSQIP / NCDB conventions)
- **L038** — Comparator-aligned reporting: reference category must be stated in every table footnote + figure caption
