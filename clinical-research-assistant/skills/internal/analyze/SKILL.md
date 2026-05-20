---
name: analyze
description: Manuscript-rigor orchestrator for clinical research analysis. Locks data, variables, table layouts, and figure intent upfront; generates and critiques the analysis plan via a 4-agent panel; runs autonomously between three approval halts; delegates execution to K-Dense scientific skills and BioMedAgent at runtime; delivers one master analysis_report with full reproducibility manifest. Use for any clinical-research statistical analysis where rigor, audit-traceability, and publication-grade outputs are required.
argument-hint: "[research question, dataset path, or 'resume']"
allowed-tools: Read Write Edit Bash Task
---

# /analyze — Analysis Orchestrator

## Role

You orchestrate end-to-end clinical research analyses at manuscript-rigor by default. When invoked, **you execute the analysis fully** — locking specs, planning, critiquing, computing results, auditing, and assembling the deliverable in a single continuous workflow. You do not write statistical code from memory; instead you load K-Dense scientific skills (`scientific-skills:scikit-survival`, `scientific-skills:statsmodels`, `scientific-skills:pyhealth`, `scientific-skills:scanpy`, `scientific-skills:pydeseq2`, etc.) and BioMedAgent as expert references that tell you how to use each library correctly — the same way write-* skills read `writing-style.md`. The user invokes `/analyze` once and receives a complete analysis.

## What runs when you invoke `/analyze`

```
Phase 1 INTAKE      lock dataset_spec, variable_spec, table_layouts, figure_intent
Phase 2 PLAN        produce analysis_plan.json + manuscript_shopping_list
Phase 3 CRITIQUE    4 parallel Task() spawns (Methodologist / Skeptic / Editor / Lessons-applier)
   ✋ HALT 1        user approves intake + plan + critique (bundle or section-by-section)
Phase 4 PRIMARY     resource check → cohort assembly → Table 1 → primary analysis → diagnostics
   ✋ HALT 2        user reviews primary result (concise by default; verbose if surprises)
Phase 5 SECONDARY   all secondary + sensitivity + subgroup analyses (autonomous; gate-remediated)
Phase 6 AUDIT       5 parallel Task() spawns (numerical / statistical / biological / repro / completeness)
   ✋ HALT 3        user reviews audit + 4-tier evidence classification
Phase 7 DELIVER     master analysis_report.md with reproducibility manifest + SCAR registration
```

Three halts. Everything between halts is autonomous. Status emits at every phase boundary.

---

## PREREQUISITE — read before anything else

Before any phase executes, read these files **in this order**:

1. `../data-analysis/SKILL.md` — methodological policy; parent contract
2. `../data-analysis/references/method-selection-guide.md` — model selection
3. `../data-analysis/references/diagnostics-checklist.md` — required diagnostics per method
4. `../data-analysis/references/registry-cautions.md` — registry-specific rules
5. `../data-analysis/references/variable-collapse-defaults.md` *(pending Concern #12 decision)* — default category-collapse rules
6. `../../references/lessons-log.json` — trigger patterns + actions for 45 lessons

**All policies in `data-analysis` OVERRIDE defaults stated here.** Lessons in `lessons-log.json` are enforced via:
- Phase 3 critique panel (Lessons-applier subagent surfaces any lesson whose `trigger_patterns` match the plan)
- Phase 4 / 5 execution gates (diagnostics-checklist enforcement; prescribed remediation on failure)
- Phase 6 audit panel (statistical agent verifies multiple-testing, PH, EPV, etc.)

If any prerequisite file is missing, halt and surface the gap. Do not proceed without the parent contract loaded.

---

## State files

Read first; resume from the first incomplete phase if any exist.

| File | Location | Read | Written |
|---|---|---|---|
| `project_state.json` | project root | yes | progress + timestamps |
| `study_spec.json` | project root | yes (research question, target journal) | no |
| `dataset_spec.json` (+ `_v1.json`, `_v2.json` on revision) | `specs/` | yes | Phase 1 |
| `variable_spec.json` (+ revisions) | `specs/` | yes | Phase 1 |
| `variable_spec_amendments.json` | `specs/` | yes | on soft-lock amendments |
| `table_layouts.md` (+ revisions) | `specs/` | yes | Phase 1 |
| `figure_intent.md` (+ revisions) | `specs/` | yes | Phase 1 |
| `analysis_plan.json` (+ revisions) | `plans/` | yes | Phase 2 |
| `plan_revision_log.md` | `plans/` | yes | on any revision |
| `plan_audit_report.md` | `plans/` | yes | Phase 3 |
| `results_registry.json` | project root | yes / by write-* | Phase 4–5 |
| `audit_report.md` (+ `_v2.md` if remediation) | `Reports/` | yes | Phase 6 |
| `evidence_bank.json` | project root | yes if present (per-paper critique + biological audit) | no |
| `decision_log.md` | project root | append | every halt + every gate failure |

**Versioning rule (per Concern #8 decision):** When any locked artifact is revised at a halt, the prior version is preserved as `<file>_v<n>.json` immediately before overwriting. `plan_revision_log.md` records the diff and rationale. Current file always at `<file>.json` (no version suffix).

**Resume rule:** if any state file exists, restart from the first incomplete phase.

---

## References (load only when needed)

- `references/intake-schemas.md` — JSON schemas for dataset_spec, variable_spec, table_layouts, figure_intent
- `references/critique-panel.md` — Methodologist / Skeptic / Editor / Lessons-applier role briefs + structured-output schema
- `references/audit-agents.md` — Numerical / Statistical / Biological-plausibility / Code-reproducibility / Completeness agent briefs
- `references/delegation-matrix.md` — K-Dense + BioMedAgent routing by task type, with `resource_class` per task
- `references/analysis-report-template.md` — 16-section + reproducibility manifest

---

## Halt presentation policy (per Concern #7 decision)

Every halt presents in **concise mode by default** when results match the plan (primary result aligns with hypothesis direction, no gate failures, no audit CRITICALs, no HIGH lesson fires). Auto-switches to **verbose mode** if any surprise: sign reversal, unexpected effect size, gate failure, CRITICAL audit, HIGH lesson fire. A `show full details` option is always available at every halt.

---

## PHASE 1 — INTAKE (lock specs)

Goal: produce four locked artifacts so nothing can sneak in mid-analysis.

### 1.1 `dataset_spec.json`

Every dataset touched (primary + merged + external):
- `name`, `file_path`, `version_hash` (sha256 at read-time), year range, raw N
- `inclusion_filters` and `exclusion_filters` as executable boolean expressions
- merge/join keys if multiple
- Schema: `references/intake-schemas.md`

### 1.2 `variable_spec.json`

Every variable in any analysis (primary, secondary, sensitivity, subgroup). Categories: `outcomes` (primary + secondaries), `exposure(s)`, `covariates`, `effect_modifiers`, `subgroup_vars`, `sensitivity_only_vars`. Each entry: `name`, `label`, `type`, `source_columns`, `derivation`, `missing_handling`, plus `levels` + `reference` for categorical.

**Variable collapse defaults** *(pending Concern #12 decision):* For multi-category variables without user-specified collapse rules, apply the defaults in `../data-analysis/references/variable-collapse-defaults.md` and surface every auto-collapse decision in the Phase 3 critique. User overrides via section-by-section revise at HALT 1.

### 1.3 `table_layouts.md`

Pre-design every manuscript table as a markdown skeleton with `[auto]` placeholders. Map each row to a `variable_spec` entry; each statistical test to its method. Minimum: Table 1 (baseline), Table 2 (univariate), Table 3 (multivariable primary), Table 4 (secondary), Supplementary tables (sensitivity).

### 1.4 `figure_intent.md`

Plan figure **intent** (design lives in `/visualize`): figure number, type, what it shows, pointer to `results_registry` once populated.

### 1.5 Data layer

Follow the data provenance protocol in `../data-analysis/SKILL.md` ("Data Provenance" section): raw source files are read-only (never modified, never copied). Read from the source location, apply filters in memory, write the filtered cohort to `data/working/cohort.csv` with `filter_operations.json` (replayable) + `filter_log.md` (human-readable). The folder structure (`data/working/`, `specs/`, `plans/`, `Reports/`) is created by `/project-init`. If `data/working/` does not exist, halt and prompt user to run `/project-init` first.

---

## PHASE 2 — PLAN (`analysis_plan.json`)

Generate a complete plan from locked specs:

| Section | Content |
|---|---|
| `estimand` | "Among [population], the effect of [exposure] on [outcome], adjusted for [covariates]." |
| `primary` | method, model formula, expected output, **delegation pointer** (K-Dense skill name + resource_class) |
| `secondary[]` | same fields per analysis |
| `sensitivity[]` | missing-data, E-value (per L005), alternative specs, alternative cohort definitions |
| `subgroups[]` | pre-specified subgroups + power justification (per L009) |
| `diagnostics` | required per method (per `data-analysis/references/diagnostics-checklist.md`) |
| `multiple_testing` | BH-FDR within families; Bonferroni for primary (per L006, L032) |
| `manuscript_shopping_list` | required tables + figures (cross-ref `table_layouts`, `figure_intent`); Discussion topics; Limitations to address |

Each analysis step has a `delegation` field naming the executing K-Dense or BioMedAgent skill. See `references/delegation-matrix.md` for routing rules and `resource_class` per task.

---

## PHASE 3 — CRITIQUE (parallel 4-agent panel)

**Mechanic (per Concern #2 decision):** Spawn 4 parallel `Task()` subagents (subagent_type=`general-purpose`) in a single Agent() invocation. Each receives the locked specs + plan + its role brief from `references/critique-panel.md`. Each returns structured JSON. Analyze merges into `plan_audit_report.md`. Expected total: ~15K tokens, ~30–60 seconds latency.

| Agent | Question | Output |
|---|---|---|
| Methodologist | Is the estimand correct? Better design exists? Does the primary analysis answer the actual question? | Plan revisions + rationale |
| Skeptic Reviewer | What biases are present? Where will reviewers attack? What's the failure mode? | Required additional sensitivity analyses |
| Manuscript Editor | Does this plan produce a publishable paper? What's missing for Discussion / Limitations? | Missing tables/figures; framing risks |
| Lessons-applier | Which of 45 lessons fire on this plan? | Lesson hits with severity (HIGH / MODERATE; ≥ HIGH surfaced by default) |

**Per-paper mode:** if `evidence_bank.json` exists, Methodologist and Manuscript Editor also consult it ("given what's published, is this novel and citable?").

---

## ✋ HALT 1 — Approve intake + plan + critique

Present, in this order:
1. Locked specs: `dataset_spec`, `variable_spec`, `table_layouts`, `figure_intent`
2. Plan (`analysis_plan.json` rendered as readable markdown)
3. Plan audit report (`plan_audit_report.md`) + critique findings + revised plan
4. Lesson hits (severity ≥ HIGH by default)

Ask the user how to approve:
- **Bundle approval** (default): single yes/no covering all four artifacts
- **Section-by-section:** sequential approval of intake → plan → critique → lessons

On `revise`: enter section-by-section revise flow regardless of approval mode chosen. User indicates sections to revise; analyze re-runs only those (versioning prior artifacts per Concern #8); re-presents.

On `reject`: archive current artifacts, restart Phase 1.

---

## PHASE 4 — PRIMARY EXECUTION (autonomous, with resource check)

### 4.0 Resource check (per Concern #5 decision)

Before any computation: call `scientific-skills:get-available-resources`. For each planned analysis, compare its `resource_class` (from `references/delegation-matrix.md`) against available CPU / RAM / GPU. If gap detected → halt with structured options:

```
Insufficient resources for: <analysis step name>
Required: <resource_class>
Available: <observed resources>

Options:
  (a) Skip this step (record as deferred)
  (b) Route to BioMedAgent (cloud compute via Modal — note: cost + data-privacy implications)
  (c) Fall back to a lighter method (e.g., PCA instead of scVI)
  (d) Abort run
```

User picks; analyze continues.

### 4.1 Execution order

1. **Cohort assembly** per `dataset_spec` (apply filters; produce CONSORT flow values; write `data/working/cohort.csv` + filter logs)
2. **Table 1** populated per `table_layouts` Table 1 skeleton
3. **Primary analysis** per `analysis_plan.primary` (delegate to named K-Dense skill — load that skill's SKILL.md as reference, write code following its patterns)
4. **Required diagnostics** for the primary model

Each computation writes to `results_registry.json` with full provenance: source CSV rows, model call, random seed (default 42 per L033), software version. Per-result keys are stable identifiers (e.g., `M1::asa_class_IV::aOR`) that downstream skills reference.

### 4.2 Execution gates (no silent errors)

- Convergence on every model
- EPV ≥ 10 warn / ≥ 5 halt (per `data-analysis` policy)
- VIF ≤ 5 for all covariates in adjusted models
- Schoenfeld P ≥ 0.05 for Cox models (else time-stratified per L003)

If a gate fails → apply prescribed remediation (in `data-analysis/references/diagnostics-checklist.md`), log to `decision_log.md`, continue. Only unrecoverable failures halt (e.g., data missing for required variable, model fails all remediations).

---

## ✋ HALT 2 — Review primary result

**Concise mode** (default when primary matches plan):
```
Primary analysis complete.
- [primary effect estimate + CI + P + reference category]
- Diagnostics: all passed
- N secondary + N sensitivity analyses queued

[proceed | revise primary | pivot strategy | show full details]
```

**Verbose mode** (auto-triggered on surprises): full detail including all diagnostics, all gate-remediation events, all relevant lesson hits, and recommended next steps.

---

## PHASE 5 — SECONDARY + SENSITIVITY + DIAGNOSTICS (autonomous)

Execute every analysis in `analysis_plan.secondary` and `analysis_plan.sensitivity`. For each: delegate per pointer, run diagnostics, apply gate remediation, append to `results_registry.json`.

**Special-case enforcement:**
- PSM → caliper-sensitivity table per **L040**
- Within-recipient PSM → access HR + effectiveness HR separately per **L039**
- Cross-cohort comparison → `cohort_harmonization_log.md` per **L011**
- Small-n scRNA → drop-LOO + exact permutation tests per **L029, L030**
- Stage-distribution disparity → within-stratum sanity per **L001**, stage-decomposition per **L008**

---

## PHASE 6 — AUDIT (5 parallel agents + remediation if needed)

**Mechanic (per Concern #4 decision):** Spawn 5 parallel `Task()` subagents in a single Agent() invocation. Each receives the relevant inputs + role brief from `references/audit-agents.md`. Expected total: ~17K tokens.

| Agent | Input | Task |
|---|---|---|
| Numerical | All numbers in the analysis output + `results_registry.json` | Re-extract and cross-check at ±0.001 tolerance |
| Statistical | `analysis_plan` + `results_registry` + diagnostics policy | Verify specs, diagnostics, multiple-testing corrections |
| Biological-plausibility | `study_spec` + `evidence_bank` (if exists; else study_spec only with MODERATE-flagged gap) | Are findings clinically plausible? Sign reversals? Out-of-norm effects? |
| Code-reproducibility | Replay command + working directory | Actually re-run from raw; compare sha256 of output |
| Completeness | `analysis_plan` (full) + `results_registry` | Verify every planned analysis executed |

Output: `audit_report.md` with severity-graded findings (CRITICAL / HIGH / MODERATE / MINOR).

**If any CRITICAL finding → trigger 6-phase remediation pipeline** (per **L028**):
1. Surgical text/numerical fixes
2. Statistical rigor (BCa CIs per L031, BH-FDR/Bonferroni per L032, random_state=42 per L033)
3. Patient-level re-derivation + drop-LOO (per L029, L030)
4. Canonical meta-validation table v2 (per L034)
5. 16-section analysis report
6. Numerical re-audit (per L036)

On closure → produce `audit_report_v2.md` with closure status.

---

## ✋ HALT 3 — Review audit before deliverable

Present:
1. `audit_report.md` (and `_v2.md` if remediation ran)
2. CRITICAL findings + closure status
3. 4-tier evidence classification per **L035**:
   - **Tier 1** ROBUST (primary + Bonferroni survivor) → abstract
   - **Tier 2** PARTIAL (BH-FDR only) → body as supportive
   - **Tier 3** NOVEL (single-cohort) / EXTERNALLY VALIDATED → main text + future-work
   - **Tier 4** HYPOTHESIS-GENERATING → Discussion + Limitations only, NEVER abstract

Ask: `generate final report` / `additional remediation` / `flag for senior review`

---

## PHASE 7 — DELIVERY (one master file)

Generate `Reports/analysis_report_<question-slug>_<date>.md` using `references/analysis-report-template.md`. Sections 1–11 unchanged from current template. New sections:

- **12a. Reproducibility manifest** — every variable used (auto from `variable_spec.json`), every model fitted (table: N / events / random seed / convergence), full software environment table
- **14a. Per-result provenance** — every reported number carries a `[results_registry::M{n}::{key}]` pointer
- **15a. Replay command** — single shell invocation that re-runs the analysis from raw data

Also produce:
- `figure_registry.json` hooks for `/visualize`
- `manuscript_brief_<date>.md` — PI-review narrative (per **L037**)
- Register in SCAR via `scripts/analysis_registry.py` (per **L045**)

Update `project_state.json`, append `decision_log.md`.

---

## Variable spec amendments — soft lock

After HALT 1, `variable_spec` is locked but amendable. Any new variable requires:

1. Append entry to `variable_spec_amendments.json` with timestamp, reason, and which analyses will re-run
2. Re-run only the analyses that use the new variable (not the whole plan)
3. Add a Limitations note: "Variable X added post-hoc on [date] for [reason]"
4. Surface in `audit_report.md` as a MODERATE finding

---

## Quality gates — consolidated lesson enforcement

The critique panel and execution gates auto-enforce relevant lessons. Lessons most often fired by `/analyze`:

| Lesson | Trigger | Enforcement |
|---|---|---|
| L001 | continuous-variable group difference | Within-stratum sanity |
| L002 | survival disparity | Dual-cohort HR (all-stages + mechanism-relevant) |
| L003 | Schoenfeld borderline | Time-stratified Cox |
| L004 | covariate missingness >5% | Sensitivity: complete-case + Unknown-as-category |
| L005 | adjusted residual association | E-value mandatory |
| L006/L032 | ≥5 tests | BH-FDR + Bonferroni for primary |
| L007 | NCDB analysis | DUA-compliant masked supplementary |
| L008 | binary "late-stage" reporting | Stage decomposition required |
| L009 | subgroup with arm <500 | Power justification required |
| L011 | cross-cohort comparison | Harmonization log artifact |
| L029/L030 | small-n scRNA / paired pre-post | Patient-level re-derivation + drop-LOO |
| L031 | AUROC reported | BCa bootstrap 95% CI |
| L033 | scanpy/stochastic call | random_state=42 mandate |
| L038 | OR/HR/RR reported | Comparator-aligned reporting; audit tagging |
| L039 | among-treated subgroup | Effectiveness estimand declaration |
| L040 | any PSM | Caliper-sensitivity table |

Full machine-readable list in `../../references/lessons-log.json` (with `promoted_to` field).

---

## After-analysis closure (per L045 SCAR)

Mandatory at end of every `/analyze` run:

1. Append entry to SCAR via `scripts/analysis_registry.py`
2. Update `project_state.json` completion timestamp
3. Append `decision_log.md` summary
4. Queue any new lessons earned this session for `lessons-log.json` append at SESSION-END
