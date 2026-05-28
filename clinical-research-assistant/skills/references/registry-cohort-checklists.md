# Registry-Specific Cohort Inclusion/Exclusion Checklists

**Purpose:** Hard-gate enforcement at `/analyze` Phase 1.1 dataset_spec generation. Per L050 (added 2026-05-24): no `dataset_spec.json` can be locked without explicit PI decision on every item in the registry-appropriate checklist below.

**Origin:** Esophageal Organ-Preservation HTE — NCDB Phase 1 silently defaulted "all primaries" (no sequence-number filter); SEER Phase 1 silently defaulted "first primary only." The two cohorts were not methodologically comparable until the PI caught it. The root cause was that no structured checklist forced explicit review of each conventional filter at design lock.

**Enforcement contract:**

1. At Phase 1.1, BEFORE writing any filter to `dataset_spec.json`, the assistant must present the registry-appropriate checklist below as a structured table.
2. Each row in the table must show: (a) the filter name, (b) common defaults in the literature, (c) the **proposed value for this study with rationale**, (d) an explicit `[ ]` for PI checkbox.
3. The PI selects yes/no/custom for each row. Custom values require free-text rationale.
4. The PI must explicitly tick `[ ] I have reviewed every item in the checklist; no filter is silently defaulted` before `dataset_spec.json` is written.
5. If the same study uses multiple registries (e.g., NCDB + SEER for cross-registry replication), the assistant must explicitly compare filter choices across registries and surface any deviation as a §HALT/AMBIGUITY note in the Phase 1 report.

The checklist is **non-exhaustive but should be comprehensive enough that no commonly-applied filter is silently skipped**. When in doubt, ADD a row rather than skip it.

---

## 1 · NCDB (National Cancer Database)

For any analysis using NCDB PUF data.

| # | Filter | Common defaults in NCDB literature | Decision required |
|---|---|---|---|
| 1 | **Diagnosis year range** | varies by SAP | start year, end year |
| 2 | **Primary site** | site-specific (per ICD-O-3 C-code) | which C-codes, inclusive of subsites? |
| 3 | **Sequence number / first primary** | Some studies restrict to "single primary only" (PUF_SEQ_NUM = 1 alone); others include "1 of N or more"; many include ALL primaries. | EXPLICIT — must justify per study question |
| 4 | **Histology (ICD-O-3 morphology codes)** | site-specific (e.g., SCC 8050-89 + adeno 8140-389 for esophagus) | inclusive code ranges + exclusion of rare types |
| 5 | **Behavior code** | malignant only (behavior=3) standard; some include in-situ (2) | malignant only? |
| 6 | **Age at diagnosis** | Many studies use 18-89 (NCDB tops at 90+); some use ≥18 only | min, max, pediatric handling |
| 7 | **Sex** | usually no restriction | restriction if any? |
| 8 | **Race / ethnicity** | usually no restriction; some studies restrict to disparities-relevant categories | restriction if any? |
| 9 | **Clinical M-stage** | M0 only standard for non-metastatic studies; M1 included for advanced-disease studies | M0 only? include MX? |
| 10 | **Clinical T-stage** | varies; locally-advanced typically cT2-4 | inclusive set |
| 11 | **Clinical N-stage** | varies; some require nodal involvement (cN+), some include cN0, some include cNX | inclusive set; handle cNX |
| 12 | **AJCC stage group** | varies | inclusive group set, era-specific (6th/7th/8th) |
| 13 | **AJCC edition harmonization** | some studies restrict to single edition; others pool across editions with sensitivity | which edition(s); harmonization strategy |
| 14 | **Treatment combinations** | study-specific | which combinations define each arm; exclusions |
| 15 | **Surgical class boundary** | per NAACCR/STORE manual; site-specific | which codes = "esophagectomy"; how to handle code 80 NOS; manual verification per L046 |
| 16 | **Chemotherapy receipt** | "yes" vs include "unknown"; some studies treat unknown as no | restrictive (yes only) or inclusive |
| 17 | **Radiation receipt** | "yes" + correct sequence to surgery | restrictive (yes only) or inclusive |
| 18 | **Treatment sequence** (RX_SUMM_SURG_RAD_SEQ, RX_SUMM_SYSTEMIC_SUR_SEQ) | neoadjuvant (CRT before surgery) is study-specific | which sequence codes count |
| 19 | **Days from diagnosis to treatment start** | sometimes restricted (e.g., must start within 6 months) to exclude no-treatment misclassification | min/max if any |
| 20 | **Reason for no surgery** | sometimes used as cohort restrictor (exclude "patient refused") | use as restrictor or covariate |
| 21 | **Vital status / follow-up** | exclude unknown vital status; minimum follow-up requirement | follow-up cutoff if any |
| 22 | **Facility type (CoC accreditation level)** | usually no restriction; some studies stratify | restriction if any? |
| 23 | **Charlson/Deyo comorbidity** | usually included as covariate not filter | restriction if any? |
| 24 | **Missing data handling for key covariates** | complete-case on outcome; missing-as-category for categoricals (per L004) | follow L004 default? |
| 25 | **SSDI completeness** (site-specific data items) | per L046 — verify before use | which SSDIs critical; documented per L046 |
| 26 | **PUF year vintage** | most recent PUF preferred; sometimes restricted to pre-pandemic | which vintage; pandemic handling |

**Default-changes-must-be-flagged warning:** If this study uses a registry that another study in the same lab uses, ANY deviation from that prior study's filters MUST be explicitly justified in `decision_log.md` and surfaced in `manuscript_methods` to enable apples-to-apples comparison.

---

## 2 · SEER (Surveillance, Epidemiology, and End Results)

For any analysis using SEER Research Data (any registry release: 9/13/17/22 registries).

| # | Filter | Common defaults in SEER literature | Decision required |
|---|---|---|---|
| 1 | **Diagnosis year range** | varies; align with NCDB if cross-registry | start year, end year |
| 2 | **SEER registry version** | SEER 9 / 13 / 17 / 22 — choice affects coverage | which release; document coverage % |
| 3 | **Primary site** | ICD-O-3 site code(s) | inclusive set |
| 4 | **Sequence number / first primary** | **SEER convention often "first primary only" (Seq=00 OR 01)** — DIFFERENT from NCDB convention | EXPLICIT — must align with NCDB choice if cross-registry |
| 5 | **Histology (ICD-O-3 morphology)** | same as NCDB approach | inclusive code ranges |
| 6 | **Behavior code (ICD-O-3)** | malignant only (3) standard | malignant only? |
| 7 | **Diagnostic confirmation** | microscopically confirmed often required; "death certificate only" excluded | exclude DCO/autopsy only? |
| 8 | **Age at diagnosis** | recode is grouped 5-year bins; "<1 year" and "90+ years" separate | min, max |
| 9 | **Stage M-component** | era-dependent (CS 2004-2015, AJCC 7 2010-2017, EOD 2018+) | inclusive set |
| 10 | **Stage T-component** | era-dependent | inclusive set |
| 11 | **Stage N-component** | era-dependent | inclusive set |
| 12 | **Stage group** | era-dependent harmonization | inclusive groups, era-specific |
| 13 | **Treatment — surgery** (RX Summ--Surg Prim Site) | site-specific code table | which codes = primary surgery |
| 14 | **Treatment — radiation** (Radiation recode) | "yes" vs "yes/no/unk" handling | restrictive or inclusive |
| 15 | **Treatment — chemotherapy** (Chemotherapy recode) | **SEER chemo flag is known to under-capture (yes/no/unk only)** — handle explicitly | restrictive or inclusive; declare under-capture limitation |
| 16 | **Treatment sequence (Surg/Rad Seq, Systemic/Sur Seq)** | neoadjuvant identification | which sequence codes |
| 17 | **Reason for no surgery** | unique to SEER; useful as operability proxy | use as restrictor or covariate |
| 18 | **Vital status** | exclude unknown | restriction |
| 19 | **Survival months** | exclude missing/flag-invalid | restriction; flag handling |
| 20 | **Cause-specific death classification** | SEER-unique; for competing-risks analyses | use for primary endpoint? competing risk? |
| 21 | **Race / Hispanic origin** | varies; restrict only if disparities-focused | restriction if any |
| 22 | **County-level attributes** | rural-urban, income — usually included as covariates | restriction if any |
| 23 | **Multiple primary handling** | overlaps with sequence number; some studies use unique person ID | how to define cohort unit |
| 24 | **Time from diagnosis to treatment days** | available as categorical recode | use as covariate? restriction? |
| 25 | **PRCDA designation** | Purchased/Referred Care Delivery Area | restriction if relevant to AI/AN focus |
| 26 | **Response to neoadjuvant therapy (2010+)** | new SEER variable; populated depending on site | check site-specific completeness per L046 |

---

## 3 · NSQIP (National Surgical Quality Improvement Program)

For any analysis using NSQIP PUF data.

| # | Filter | Common defaults | Decision required |
|---|---|---|---|
| 1 | Year range | per study | start, end |
| 2 | CPT code(s) defining the procedure | site-specific | inclusive CPT set |
| 3 | Wound classification | clean/clean-contaminated/contaminated/dirty | inclusive set |
| 4 | Elective vs emergency status | study-specific | restriction |
| 5 | ASA class | sometimes restrict to ASA I-III | restriction |
| 6 | Age | per study | min, max |
| 7 | Postoperative outcome window | 30-day, sometimes 90-day | window |
| 8 | Trainee involvement | rarely restricted | restriction |
| 9 | Functional status | sometimes restricted | restriction |
| 10 | Pre-operative SIRS/sepsis | sometimes excluded | restriction |

---

## 4 · UNOS / SRTR (transplant registries)

| # | Filter | Common defaults | Decision required |
|---|---|---|---|
| 1 | Era (often restricted to align with allocation policy changes) | per organ + era | start, end |
| 2 | Organ type | per study | which organ(s) |
| 3 | Recipient age | per study | min, max |
| 4 | Donor age | per study | min, max |
| 5 | Living vs deceased donor | per study | restriction |
| 6 | Re-transplants | sometimes excluded | restriction |
| 7 | Multi-organ transplants | sometimes excluded | restriction |
| 8 | Cause of organ failure | per study | restriction |
| 9 | MELD/PELD restrictions | sometimes (e.g., MELD > 15 for liver) | restriction |
| 10 | Follow-up window | varies | minimum |

---

## 5 · TriNetX / cohort-of-cohorts platforms

| # | Filter | Common defaults | Decision required |
|---|---|---|---|
| 1 | Network selection | per study | which network |
| 2 | Time window | per study | start, end |
| 3 | Index event definition | ICD/CPT/RxNorm | code set + first-occurrence rule |
| 4 | Lookback for prior conditions | typically 1-2 years | lookback window |
| 5 | Follow-up window | per outcome | min/max |
| 6 | Encounter requirement | minimum visit count to be "in cohort" | requirement |
| 7 | Death capture method | network-specific | declare limitation |

---

## 6 · Generic (single-institution EHR / prospective registry)

| # | Filter | Common defaults | Decision required |
|---|---|---|---|
| 1 | Time period | per study | start, end |
| 2 | Inclusion event(s) | per study | event(s) + temporal anchor |
| 3 | Exclusion criteria | per study | explicit list |
| 4 | Missing data thresholds | per L004 (>5% missingness for covariates) | threshold |
| 5 | Loss-to-follow-up handling | per study | competing-risks / censoring |

---

## Cross-registry consistency rule

When a study uses multiple registries (e.g., NCDB + SEER, NCDB + TriNetX), the assistant must:

1. Build the checklist for EACH registry separately
2. Present a **side-by-side comparison table** showing each filter's value in each registry
3. Highlight EVERY deviation in red/bold/§HALT notation
4. Require PI to either (a) justify the deviation as methodologically appropriate or (b) align filters across registries

A registry replication is not a replication if the filter choices differ; this rule prevents that silent failure.

---

## Failure modes this gate prevents

1. **NCDB-vs-SEER first-primary mismatch** (Esophageal Organ-Preservation HTE, 2026-05-24) — NCDB defaulted to "all primaries", SEER to "first primary only" without explicit decision; produced 16k N difference between cohorts that was not methodologically driven.
2. Silent application of restrictive defaults (e.g., excluding cNX, excluding unknown grade) that the PI would have caught if shown the checklist.
3. Silent omission of known-important filters (e.g., diagnostic confirmation in SEER, ASA in NSQIP) that the assistant didn't think of.
4. Cross-registry replications that are not actually replications because filters silently diverged.

---

## How to invoke this checklist in /analyze

At Phase 1.1, the assistant must:

```python
# Pseudo-code for Phase 1.1
1. Identify the registry from study_spec.json::dataset_type
2. Load the registry-appropriate checklist from references/registry-cohort-checklists.md
3. Pre-populate "proposed value" column with study-specific recommendations + rationale
4. Present as structured table to PI
5. Require explicit yes/no/custom per item
6. Require PI sign-off on the "I have reviewed every item; no filter is silently defaulted" attestation
7. ONLY THEN write dataset_spec.json with the locked filter set
```

The checklist is appended to `Reports/phase1_consort_<date>.md` as a permanent record of WHICH filters were considered (including those rejected) — not just the ones that survived.
