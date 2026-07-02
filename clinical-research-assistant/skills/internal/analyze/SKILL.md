---
name: analyze
description: Manuscript-rigor orchestrator for clinical research analysis. Locks data, variables, table layouts, and figure intent upfront; generates and critiques the analysis plan inline (escalating to a single red-team only when needed); runs autonomously between approval halts and inline verification checkpoints; delegates execution to K-Dense scientific skills and BioMedAgent at runtime; delivers one master analysis_report with full reproducibility manifest. Use for any clinical-research statistical analysis where rigor, audit-traceability, and publication-grade outputs are required.
argument-hint: "[research question, dataset path, or 'resume']"
allowed-tools: Read Write Edit Bash Task
---

# /analyze — Analysis Orchestrator

## Role

You orchestrate end-to-end clinical research analyses at manuscript-rigor by default. When invoked, **you execute the analysis fully** — locking specs, planning, critiquing, computing results, auditing, and assembling the deliverable in a single continuous workflow. You do not write statistical code from memory; instead you load K-Dense scientific skills (`scientific-skills:scikit-survival`, `scientific-skills:statsmodels`, `scientific-skills:pyhealth`, `scientific-skills:scanpy`, `scientific-skills:pydeseq2`, etc.) and BioMedAgent as expert references that tell you how to use each library correctly — the same way write-* skills read `writing-style.md`. The user invokes `/analyze` once and receives a complete analysis.

## What runs when you invoke `/analyze`

```
Phase 0 PRE-DESIGN  pre-analysis literature recon — auto-invokes /literature-review
                    produces evidence_bank, citation_bank, novelty_assessment, differentiation_brief
   ✋ HALT 0        PI signs off on differentiation: novel | replication-with-extension | pivot | abandon
Phase 1 INTAKE      lock dataset_spec, variable_spec, table_layouts, figure_intent
Phase 2 PLAN        produce analysis_plan.json + manuscript_shopping_list
Phase 3 CRITIQUE    INLINE plan-sanity (Methodologist/Skeptic/Editor/Lessons run inline, no panel) + LOCK pre-registration (SP preregistering-analysis)
   ✋ HALT 1        user approves intake + plan + critique (bundle or section-by-section)
Phase 4 PRIMARY     resource check → cohort assembly → build Master Excel shells → PRIMARY (CRUDE / UNADJUSTED) analysis → fills Table_1 (bold p<0.05) → diagnostics
   ✓ CHECKPT A     INLINE verify (SP verifying-results-before-claiming): re-run, read estimate+CI, confirm reproduction
   ✋ HALT 2        user reviews Table_1 + crude effect estimates (concise by default; verbose if surprises)
   ✋ HALT 2A       user APPROVES matching + adjustment variables for Phase 5 (HARD STOP)
Phase 5A SECONDARY  PSM + multivariable + KM + IPTW with locked variables → fills Table_2 (bold q<0.05) (adjusted only)
   ✓ CHECKPT B     INLINE verify + crude-vs-adjusted concordance (SP verifying-results) before sensitivity runs
Phase 5B SENSITIVITY sensitivity battery + subgroups → Sensitivity + Supplementary_* (runs only after Checkpoint B passes)
Phase 6 AUDIT       ONE clinically-augmented red-team (SP requesting-red-team-review) — replaces the 5-agent panel; verify/repro/completeness already done inline at A/B
   ✋ HALT 3        user reviews audit + 4-tier evidence classification
Phase 7 DELIVER     master analysis_report.md with reproducibility manifest + SCAR registration
```

Five halts (Phase 0, HALT 1, HALT 2, HALT 2A, HALT 3). Phase 0 is a HARD GATE — Phase 1 cannot fire without PI sign-off on differentiation. HALT 2A is a HARD STOP — Phase 5 cannot fire without PI sign-off on matching + adjustment variables. Everything between halts is autonomous. Status emits at every phase boundary.

---

## `/analyze --quick` — exploratory tier (per L058)

**Purpose.** A deliberately lightweight path for exploratory looks (a single 2×2, one KM curve, a quick descriptive contrast) and for the moment you would otherwise abandon the plugin and hand-run Python. It keeps the load-bearing rigor — a reproducible seeded run, inline verification, and SCAR registration — while dropping the full halt ladder. It exists so that "quick" never means "outside the plugin" (the manual-execution reliability gap).

**Invoke:** `/analyze --quick "<one pre-named contrast>"`. What runs:

```
resource check (light)
→ single analysis with random_state=42 (appropriate test by outcome class, per Phase 4.1)
→ ✓ INLINE verify (science-superpowers:verifying-results-before-claiming): fresh re-run, read estimate + 95% CI + p, confirm reproduction
→ SCAR register the result as Tier 4 (HYPOTHESIS-GENERATING), tagged mode=quick
→ one concise result card → STOP
```

**Dropped vs. full `/analyze`:** Phase 0 lit-recon hard gate, HALT 0/1/2/2A/2B/3, Master Excel scaffolding + shell sign-off, pre-registration, the red-team subagent, the 16-section report. **Never dropped:** the random seed, the inline verification re-run, and SCAR registration.

**Hard guardrails — this is what keeps `--quick` from becoming a rigor bypass:**

- Every `--quick` result is **Tier 4 (hypothesis-generating)** by classification (per L035) and is **forbidden from any abstract or from a manuscript primary/secondary result.** The result card carries the banner: *"Exploratory (`--quick`) — not literature-vetted, not pre-registered, not eligible for the abstract. Promote via a full `/analyze` run before any confirmatory claim."*
- **No adjusted / matched / weighted models** in `--quick` — those require the HALT 2A variable-approval gate. If the question needs adjustment, `--quick` refuses and points to full `/analyze`.
- **One contrast only.** `--quick` runs a single pre-named comparison — no multiple-testing family. Needing several is the signal to switch to full `/analyze`.
- To turn a `--quick` finding into a manuscript result, re-run the full pipeline; the SCAR entry links the quick result to its confirmatory re-run.

---

## PREREQUISITE — read before anything else

Read `lessons-log.json` up front. Read each policy reference below **on demand, at the phase that needs it** — do not bulk-load (token-lean):

1. `references/clinical-analysis-policy.md` — methodological policy; parent contract
2. `references/method-selection-guide.md` — model selection
3. `references/diagnostics-checklist.md` — required diagnostics per method
4. `references/registry-cautions.md` — registry-specific rules
5. `references/variable-collapse-defaults.md` *(pending Concern #12 decision)* — default category-collapse rules
6. `../../references/lessons-log.json` — trigger patterns + actions for 45 lessons

**All policies in `clinical-analysis-policy.md` OVERRIDE defaults stated here.** Lessons in `lessons-log.json` are enforced via:
- Phase 3 INLINE plan-sanity (lessons checked inline against `trigger_patterns`; no subagent panel)
- Phase 4 / 5 execution gates (diagnostics-checklist enforcement; prescribed remediation on failure)
- Phase 6 red-team: one SP requesting-red-team-review subagent verifies multiple-testing, PH, EPV, etc. via `references/red-team-brief.md` (most checks already done inline at Checkpoints A/B)

If any prerequisite file is missing, halt and surface the gap. Do not proceed without the parent contract loaded.

---

## State files

Read first; resume from the first incomplete phase if any exist.

| File | Location | Read | Written |
|---|---|---|---|
| `project_state.json` | project root | yes | progress + timestamps |
| `study_spec.json` | project root | yes (research question, target journal) | no |
| `evidence_bank.json` | project root | yes (Phase 0 prerequisite) | by `/literature-review` |
| `citation_bank.json` | project root | yes (Phase 0 prerequisite) | by `/literature-review` |
| `novelty_assessment.json` | project root | yes (Phase 0 prerequisite + HALT 0 sign-off) | Phase 0 |
| `differentiation_brief.md` | project root | yes (Phase 0 prerequisite + HALT 0 sign-off) | Phase 0 |
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
- `references/critique-panel.md` — the four critique lenses' question checklist, now run INLINE (no subagent panel)
- `references/red-team-brief.md` — clinically-augmented brief for the single SP requesting-red-team-review subagent (supersedes the legacy 5-agent `audit-agents.md`)
- `references/sp-integration.md` — which science-superpowers skill fires at which phase (rigor layer contract)
- `references/delegation-matrix.md` — K-Dense + BioMedAgent routing by task type, with `resource_class` per task
- `references/analysis-report-template.md` — 16-section + reproducibility manifest

---

## Halt presentation policy (per Concern #7 decision)

Every halt presents in **concise mode by default** when results match the plan (primary result aligns with hypothesis direction, no gate failures, no audit CRITICALs, no HIGH lesson fires). Auto-switches to **verbose mode** if any surprise: sign reversal, unexpected effect size, gate failure, CRITICAL audit, HIGH lesson fire. A `show full details` option is always available at every halt.

---

## PHASE 0 — PRE-DESIGN LITERATURE RECON (HARD GATE)

**Goal:** Surface prior work that already answers the research question — BEFORE locking specs, BEFORE writing any analysis code. Force PI to explicitly classify the study as novel / replication-with-extension / pivot / abandon based on actual evidence of what is already published.

**Why this is a HARD GATE:** Per L048 (added 2026-05-24 after Esophageal-Organ-Preservation v2 vs Sakowitz 2025 JTCVS discovery), running Phase 1+ without Phase 0 is the canonical failure mode that produces analyses redundant with literature published in the prior 12 months. Phase 0 is non-skippable.

### 0.1 Prerequisite check

Phase 0 fires UNLESS all of the following exist AND are fresh (≤30 days old) AND the `research_question_sha256` in `novelty_assessment.json` matches the current `study_spec.research_question`:

| File | Required | Location |
|---|---|---|
| `evidence_bank.json` | yes, with ≥1 entry | project root |
| `citation_bank.json` | yes, with ≥1 verified entry | project root |
| `novelty_assessment.json` | yes, with PI sign-off | project root |
| `differentiation_brief.md` | yes, with PI signature | project root |

If any are missing, stale, or research-question-mismatched → **auto-invoke `/literature-review`**, then come back to 0.2.

### 0.2 Auto-invocation of /literature-review

Spawn `/literature-review` via Task() (subagent_type=`general-purpose`) with the briefing:

> "Phase 0 pre-design literature recon for `/analyze`. Read `study_spec.json` for the research question. Produce evidence_bank.json (prior work landscape), citation_bank.json (L041-verified citations), novelty_assessment.json (using `templates/state/novelty_assessment.template.json` schema), and differentiation_brief.md (using `templates/state/differentiation_brief.template.md` schema). Use K-Dense delegations per `references/kdense-delegations.md` §Phase-0. Hand control back to /analyze when all four artifacts exist and the differentiation brief is populated up to (but not including) PI signature."

/literature-review handles the search; /analyze does NOT proceed to HALT 0 until the four artifacts exist.

### 0.3 K-Dense skill delegations (Phase 0 specific)

Read these as expert reference, do not re-invoke if already loaded in /literature-review:

| Step | K-Dense skill | Purpose |
|---|---|---|
| Initial ideation if Q is broad | `scientific-skills:scientific-brainstorming` | Cast wider net before narrowing |
| Systematic search | `scientific-skills:literature-review` | Multi-database (PubMed + bioRxiv + OpenAlex) sweep |
| Search infrastructure | `scientific-skills:pubmed-database`, `scientific-skills:openalex-database` | Direct DB query when needed |
| Quality scoring of comparators | `scientific-skills:scholar-evaluation` | Rank prior papers by methodological rigor |
| Critical assessment of prior evidence | `scientific-skills:scientific-critical-thinking` | Identify limitations in prior work that justify our study |
| Hypothesis refinement | `scientific-skills:hypothesis-generation` | Sharpen research question post-recon if pivot needed |
| Citation verification | `scientific-skills:citation-management` | L041 hard gate — every entry in citation_bank verified |

Full delegation contracts in `../../references/kdense-delegations.md` §1 (citation), §5 (Phase 0 — Pre-design Lit Recon).

### 0.4 Required outputs

- `evidence_bank.json` — populated per `templates/state/evidence_bank.template.json` (existing schema)
- `citation_bank.json` — every entry `.verified = true` per L041
- `novelty_assessment.json` — per `templates/state/novelty_assessment.template.json` (new); includes search metadata, ranked nearest-comparators, evidence landscape, differentiation statement, staleness window
- `differentiation_brief.md` — per `templates/state/differentiation_brief.template.md` (new); PI-facing 8-section narrative ending in PI sign-off block

### 0.5 §HALT/AMBIGUITY behavior

If Phase 0 surfaces a comparator with HIGH overlap (e.g., same registry, same comparison, published within last 24 months), include in the differentiation_brief.md §6 an explicit "expected reviewer critique" entry + pre-planned response, and elevate PI sign-off urgency in the HALT 0 prompt.

---

## ✋ HALT 0 — PI sign-off on differentiation

Present, in this order:

1. **Differentiation brief** (`differentiation_brief.md` §1–6) rendered as readable markdown
2. **Nearest comparators table** (top 5 from novelty_assessment.json)
3. **The PI question:** "Given the prior work surfaced, is this study still justified?"

**Required answer — one of four:**

- **(a) Novel** — proceed normally to Phase 1
- **(b) Replication with extension** — proceed; Discussion will explicitly cite and differentiate from [list]; framing pre-locked in differentiation_brief
- **(c) Pivot scope** — research question requires modification; update `study_spec.research_question`, re-hash, re-enter Phase 0
- **(d) Abandon** — prior work makes this study redundant; archive project (`Archives/abandoned_<date>/`) and stop

PI rationale free-text is **required** regardless of verdict.

On sign-off:
- Compute SHA256 of differentiation_brief.md → write to `novelty_assessment.json.lock_hash`
- Write `novelty_assessment.json.staleness.valid_through = today + 30 days`
- Append to `decision_log.md` with verdict + rationale + lock hash
- Set `project_state.json.current_phase = "phase_1_intake_pending"`

Only after sign-off can `/analyze` proceed to Phase 1.

### 0.6 Resume behavior

If `/analyze` is re-invoked and Phase 0 artifacts exist + are fresh + research-question-matched + PI-signed → skip Phase 0 entirely, print:

```
Phase 0 already complete: differentiation verdict = [verdict] (signed [date], valid through [date]).
Proceeding to Phase 1.
```

If artifacts are stale (>30 days) or research_question has changed → re-fire Phase 0.

---

## PHASE 1 — INTAKE (lock specs)

Goal: produce five locked artifacts so nothing can sneak in mid-analysis. The first lock (objectives) is the source from which the other four derive — the Excel workbook tabs, dataset filters, variable spec, and analysis plan are all scoped to the locked objectives.

### 1.0 `objectives_locked.json` — PRIMARY + SECONDARY OBJECTIVES (locks first; added per L051)

Before any other spec is touched, lock the study objectives:

- **`primary_objective`** — one sentence pre-specifying the primary contrast: population, exposure, primary outcome, time horizon, comparator
- **`secondary_objectives[]`** — numbered list; each entry pre-specifies its own outcome, exposure, time horizon, and comparator
- Save to `specs/objectives_locked.json` (machine schema) **and** `Protocol/objectives_locked_<date>.md` (PI-facing markdown rendering)

**PI sign-off is mandatory at this sub-step.** Once locked, any change to a primary or secondary objective requires a dated SAP §9-style amendment logged in `Protocol/sap_amendments.md` — never a silent edit. The Master Excel Workbook tabs (1.3), the analysis plan (Phase 2), and downstream HALT presentations are all scoped to these objectives.

Rationale: locking objectives separately from the analysis plan prevents post-hoc objective drift. Under the new primary/secondary terminology (primary = crude/unadjusted, secondary = PSM/multivariable/KM/IPTW per L051), the objectives define WHAT is being tested; Phase 4 and Phase 5 define HOW.

### 1.1 `dataset_spec.json`

Every dataset touched (primary + merged + external):
- `name`, `file_path`, `version_hash` (sha256 at read-time), year range, raw N
- `inclusion_filters` and `exclusion_filters` as executable boolean expressions
- merge/join keys if multiple
- Schema: `references/intake-schemas.md`

#### 1.1.a Registry-specific inclusion/exclusion checklist (HARD GATE per L050)

**Before any filter is written to `dataset_spec.json`,** the assistant must invoke the registry-specific checklist from `../../references/registry-cohort-checklists.md`:

1. Identify the registry from `study_spec.dataset_type` (NCDB / SEER / NSQIP / UNOS / TriNetX / generic).
2. Load the corresponding checklist (~25 standard items per registry).
3. Present as a structured table with: filter name | common defaults in literature | proposed value for this study with rationale | `[ ]` PI checkbox.
4. PI selects yes / no / custom for each item. Custom values require free-text rationale.
5. PI must explicitly tick `[ ] I have reviewed every item; no filter is silently defaulted` before `dataset_spec.json` is written.
6. **Cross-registry studies (e.g., NCDB + SEER replication)** must present a side-by-side comparison table; every deviation between registries surfaces as a §HALT/AMBIGUITY note requiring justification.

The completed checklist (including filters considered AND rejected) is appended to `Reports/phase1_consort_<date>.md` as a permanent record.

**Failure mode this gate prevents (per L050 worked example):** Esophageal Organ-Preservation HTE — NCDB Phase 1 silently defaulted "all primaries" (no sequence-number filter); SEER Phase 1 silently defaulted "first primary only." The two cohorts were not methodologically comparable until the PI caught it. The root cause was that no structured checklist forced explicit review of each conventional filter at design lock.

### 1.2 `variable_spec.json`

Every variable in any analysis (primary, secondary, sensitivity, subgroup). Categories: `outcomes` (primary + secondaries), `exposure(s)`, `covariates`, `effect_modifiers`, `subgroup_vars`, `sensitivity_only_vars`. Each entry: `name`, `label`, `type`, `source_columns`, `derivation`, `missing_handling`, plus `levels` + `reference` for categorical.

**Variable collapse defaults** *(pending Concern #12 decision):* For multi-category variables without user-specified collapse rules, apply the defaults in `references/variable-collapse-defaults.md` and surface every auto-collapse decision in the Phase 3 critique. User overrides via section-by-section revise at HALT 1.

### 1.3 Master Excel Workbook — `Reports/MASTER_TABLES_<project>_<date>.xlsx` (per L051)

Pre-design every manuscript table as **a single Excel workbook with named tabs** — this is the source of truth for every numeric result in the project. Build the empty shell at Phase 1.3; cells stay empty until populated in Phase 4 (`Table_1`) and Phase 5 (`Table_2` / `Sensitivity` / `Supplementary_*`).

**Mandatory tabs:**

- `Table_1` — cohort characteristics by exposure (rows = variables from `variable_spec.json`, columns = exposure groups defined by `objectives_locked.json` primary contrast)
- `Table_2` — adjusted estimates (rows = variables, columns = crude / PSM / multivariable / IPTW)
- `Table_3`, `Table_4`, … — additional main tables per locked secondary objective
- `Sensitivity` — sensitivity analyses (caliper variants, MI, competing risks, stratum-specific, E-value)
- `Supplementary_1`, `Supplementary_2`, … — supplementary tables (subgroups, extended results)

Each tab: variables, row labels, and column headers defined from `variable_spec.json` + `objectives_locked.json`; cells empty. Map each row to a `variable_spec` entry; each statistical test to its method.

**This Excel workbook coexists with** `MASTER_ANALYSIS_REGISTRY.json` (per L045 — machine source of truth with `history[]`) and its auto-rendered `.md` index. Three-artifact role split:

- **JSON registry** = machine audit trail with supersede history (what catches drift)
- **Excel workbook** = production-ready tabular source for the manuscript (human-facing, formatted, bolded; what gets pulled into Word)
- **MD index** = quick scannable human view (auto-generated from JSON)

Backward-compat note: a markdown `table_layouts.md` is no longer required. If a legacy project still has one, the Phase 4 cohort-assembly step should convert it to the Excel workbook before any data is written.

### 1.4 `figure_intent.md`

Plan figure **intent** (design lives in `/visualize`): figure number, type, what it shows, pointer to `results_registry` once populated.

### 1.5 Data layer

Follow the data provenance protocol in `references/clinical-analysis-policy.md` ("Data Provenance" section): raw source files are read-only (never modified, never copied). Read from the source location, apply filters in memory, write the filtered cohort to `data/working/cohort.csv` with `filter_operations.json` (replayable) + `filter_log.md` (human-readable). The folder structure (`data/working/`, `specs/`, `plans/`, `Reports/`) is created by `/project-init`. If `data/working/` does not exist, halt and prompt user to run `/project-init` first.

---

## PHASE 2 — PLAN (`analysis_plan.json`)

Generate a complete plan from locked specs:

| Section | Content |
|---|---|
| `estimand` | "Among [population], the effect of [exposure] on [outcome]; primary = crude/unadjusted, secondary = adjusted for [adjustment_covariates] / matched on [matching_variables]." |
| `primary` | **Crude / unadjusted** per locked objective (per L051 terminology). Appropriate statistical test by outcome class: χ² (or Fisher exact) for categorical, t-test (or Wilcoxon rank-sum) for continuous, log-rank + univariable Cox for time-to-event, χ² + crude OR for cross-sectional binary. **Delegation pointer** + populates `Table_1` tab in Master Excel Workbook. |
| `matching_variables[]` (proposed) | Candidate variables for PSM matching. Each entry: `name`, `rationale` (DAG, clinical relevance, comparator paper precedent, missingness profile), `proposed_for_match` boolean. **Locked at HALT 2A** before Phase 5 fires. |
| `adjustment_covariates[]` (proposed) | Candidate covariates for multivariable adjustment (Cox / logistic / linear). Each entry: same fields as `matching_variables[]` with `proposed_for_adjust` boolean. **Locked at HALT 2A**. Distinct from `matching_variables[]` — overlap allowed but not required; a variable may be matched-but-not-adjusted (and vice versa). |
| `secondary[]` | **Adjusted, matched, weighted, survival** per locked objective (per L051 terminology): PSM (with HALT 2A-approved `matching_variables`) + multivariable (with HALT 2A-approved `adjustment_covariates`) + KM + IPTW + method variants (GBT-IPTW / AIPW / frailty Cox). **Delegation pointer** + populates `Table_2` tab. |
| `sensitivity[]` | missing-data, E-value (per L005), caliper sensitivity (per L040), alternative specs, alternative cohort definitions. Populates `Sensitivity` tab in Master Excel Workbook. |
| `subgroups[]` | pre-specified subgroups + power justification (per L009). Populates `Supplementary_*` tabs. |
| `diagnostics` | required per method (per `references/diagnostics-checklist.md`) |
| `multiple_testing` | BH-FDR within families; Bonferroni for primary (per L006, L032). **Bolding rule (per L051):** bold cells where p<0.05 in `Table_1`; bold cells where BH-FDR q<0.05 in `Table_2`, `Sensitivity`, and `Supplementary_*` tabs. |
| `manuscript_shopping_list` | required tables + figures (cross-ref Master Excel Workbook tab names, `figure_intent`); Discussion topics; Limitations to address |

Each analysis step has a `delegation` field naming the executing K-Dense or BioMedAgent skill. See `references/delegation-matrix.md` for routing rules and `resource_class` per task.

---

## PHASE 3 — CRITIQUE (inline, no panel) + PRE-REGISTRATION

**Mechanic (revised 2026-05-30 — token reduction):** Run the four critique lenses below INLINE against the locked specs + plan, using the question checklist in `references/critique-panel.md`. Do NOT spawn a 4-agent panel. Write findings to `plan_audit_report.md`. Escalate to ONE `science-superpowers:requesting-red-team-review` subagent ONLY if an inline lens surfaces a CRITICAL plan flaw. Then LOCK THE PRE-REGISTRATION with `science-superpowers:preregistering-analysis`: freeze hypotheses, directional predictions, decision rules, and the confirmatory/exploratory split for every objective BEFORE any outcome is seen → write `Protocol/preregistration_<date>.md`. Inline cost ~2–3K tokens vs. ~15K for the old panel.

| Agent | Question | Output |
|---|---|---|
| Methodologist | Is the estimand correct? Better design exists? Does the primary analysis answer the actual question? | Plan revisions + rationale |
| Skeptic Reviewer | What biases are present? Where will reviewers attack? What's the failure mode? | Required additional sensitivity analyses |
| Manuscript Editor | Does this plan produce a publishable paper? What's missing for Discussion / Limitations? | Missing tables/figures; framing risks |
| Lessons-applier | Which of 45 lessons fire on this plan? | Lesson hits with severity (HIGH / MODERATE; ≥ HIGH surfaced by default) |

**Per-paper mode:** if `evidence_bank.json` exists, Methodologist and Manuscript Editor also consult it ("given what's published, is this novel and citable?").

---

## ✋ HALT 1 — Approve intake + plan + critique + pre-registration

Present, in this order:
1. Locked specs: `dataset_spec`, `variable_spec`, `table_layouts`, `figure_intent`
2. Plan (`analysis_plan.json` rendered as readable markdown)
3. Plan audit report (`plan_audit_report.md`) + critique findings + revised plan
4. Lesson hits (severity ≥ HIGH by default)
5. **Pre-registration** (`Protocol/preregistration_<date>.md`) — frozen hypotheses, directional predictions, decision rules, confirmatory/exploratory split (per `science-superpowers:preregistering-analysis`)

Ask the user how to approve:
- **Bundle approval** (default): single yes/no covering all four artifacts
- **Section-by-section:** sequential approval of intake → plan → critique → lessons

On `revise`: enter section-by-section revise flow regardless of approval mode chosen. User indicates sections to revise; analyze re-runs only those (versioning prior artifacts per Concern #8); re-presents.

On `reject`: archive current artifacts, restart Phase 1.

---

## PHASE 4 — PRIMARY (CRUDE / UNADJUSTED) → fills Table_1 (autonomous, with resource check)

**Terminology lock (per L051):** "Primary analysis" in this skill = crude / unadjusted relationship between exposure and outcome for each locked objective. Adjusted models (PSM, multivariable, KM, IPTW) are SECONDARY and run in Phase 5. This terminology overrides any prior usage in this skill where "primary" meant "adjusted multivariable headline."

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
2. **Build Master Excel Workbook shells** (per L051) — instantiate `Reports/MASTER_TABLES_<project>_<date>.xlsx` with the tab structure defined in Phase 1.3 (`Table_1`, `Table_2`, `Table_3`, `Sensitivity`, `Supplementary_*`). Variables, row labels, and column headers defined from `variable_spec.json` + `objectives_locked.json`. **All cells empty.**
   - **SHELL SIGN-OFF GATE:** Show the empty workbook to the PI for shell sign-off BEFORE populating any cell. PI confirms tab structure, row/column labels, and variable assignments match intent. This gate is non-skippable.
3. **Primary (crude / unadjusted) analysis** per `analysis_plan.primary` — for each locked objective in `objectives_locked.json`, run the appropriate test by outcome class:
   - **Categorical outcome:** χ² (or Fisher exact if any expected cell <5) → counts, % (n/N), crude OR or RR with 95% CI, p
   - **Continuous outcome:** t-test (or Wilcoxon rank-sum if non-normal) → mean ± SD or median (IQR), mean difference with 95% CI, p
   - **Time-to-event outcome:** log-rank on KM survival + crude HR with 95% CI from univariable Cox; median follow-up
   - **Binary outcome (cross-sectional):** χ² + crude OR / RR with 95% CI
   - Delegate to named K-Dense skill per `analysis_plan.primary.delegation`
4. **Populate `Table_1` tab** in Master Excel Workbook from crude results. Add SMDs for the primary contrast.
5. **Apply bold formatting** (per L051) to every row/cell in `Table_1` where p < 0.05 — visual flag for what was significant on crude analysis.
6. **Required diagnostics** for the primary tests (χ² cell expectations, normality assumptions if t-test used, PH assumption on univariable Cox).

Each computation writes to `results_registry.json` AND to `MASTER_ANALYSIS_REGISTRY.json` (per L045) with full provenance: source CSV rows, model call, random seed (default 42 per L033), software version. Per-result keys are stable identifiers (e.g., `M0::crude_OR::asa_class_IV`) that downstream skills reference. The Excel workbook is the human-facing tabular view; the JSON registry is the machine source of truth with `history[]` for supersedes.

**Forbidden at Phase 4 (per L051):** matching, weighting, covariate adjustment, multivariable models, KM stratified by anything other than the primary exposure. Those are Phase 5 only, gated by HALT 2A.

### 4.2 Execution gates (no silent errors)

- Convergence on every model
- EPV ≥ 10 warn / ≥ 5 halt (per clinical-analysis policy)
- VIF ≤ 5 for all covariates in adjusted models
- Schoenfeld P ≥ 0.05 for Cox models (else time-stratified per L003)

If a gate fails → apply prescribed remediation (in `references/diagnostics-checklist.md`), log to `decision_log.md`, continue. Only unrecoverable failures halt (e.g., data missing for required variable, model fails all remediations).

---

## ✓ CHECKPOINT A — verify primary before proceeding (INLINE, no subagent)

Apply `science-superpowers:verifying-results-before-claiming` to the crude results, inline: (1) re-run the primary analysis fresh from `data/working/cohort.csv` with the recorded seed; (2) read the actual estimate + 95% CI + p for every objective; (3) confirm `Table_1` / `results_registry.json` match the fresh run; (4) confirm required diagnostics passed. If a number is implausible, irreproducible, or a diagnostic fails → invoke `science-superpowers:investigating-anomalous-results` (root-cause before any adjustment) and do NOT advance until resolved. No crude effect is claimed without fresh reproduced evidence.

---

## ✋ HALT 2 — Review Table_1 (crude / unadjusted)

**Concise mode** (default when crude estimates match plan):
```
Phase 4 complete — Table_1 populated.
- [primary objective: crude effect + 95% CI + p, bold if p<0.05]
- [secondary objective 1: crude effect + 95% CI + p]
- [secondary objective 2: crude effect + 95% CI + p]
- Diagnostics: all passed
- SMDs for primary contrast: [list]
- Bolded cells (p<0.05): [count]

[proceed to HALT 2A | revise primary | pivot strategy | show full details]
```

**Verbose mode** (auto-triggered on surprises): full detail including all diagnostics, all gate-remediation events, all relevant lesson hits, and recommended next steps.

---

## ✋ HALT 2A — Variable Pre-specification & Approval Gate (HARD STOP before Phase 5) (per L051)

**Mandatory before any Phase 5 analysis fires.** No matching, weighting, or adjusted model is fit until this halt is signed. This is non-skippable, even in autonomous resume mode.

At this halt, propose to the PI two distinct variable lists, each with per-variable rationale:

1. **`matching_variables[]`** — variables for PSM matching (the design dimension)
2. **`adjustment_covariates[]`** — covariates for multivariable adjustment in Cox / logistic / linear models (the estimation dimension)

Overlap between the two lists is allowed but not required — a variable may be matched-but-not-adjusted (e.g., demographics where match handles confounding) or adjusted-but-not-matched (e.g., a clinical severity score with high missingness that excludes it from the match but supports it as a covariate).

Present as a structured table per locked objective:

```
Variable | Match? | Adjust? | Rationale (DAG / clinical / comparator / missingness) | PMID
---------|--------|---------|------------------------------------------------------|------
[var 1]  | [ ]    | [ ]     | [text]                                               | [PMID]
[var 2]  | [ ]    | [ ]     | [text]                                               | [PMID]
```

PI selects yes / no per variable per role (match, adjust, both, neither). Custom additions require free-text rationale. PI must explicitly tick `[ ] I have reviewed every variable; no variable is silently included or excluded` before sign-off is accepted.

**On sign-off:**
- Write `Protocol/variables_locked_<date>.md` (PI-facing markdown) + `specs/variables_locked.json` (machine schema)
- Append to `decision_log.md`: matching + adjustment lists with PI's per-variable rationale
- Set `project_state.json.current_phase = "phase_5_secondary_pending"`

**Hard rule:** No matching, weighting, or adjusted model fires in Phase 5 until HALT 2A is signed. Any post-HALT-2A addition or removal of a variable is a SAP §9-style amendment logged in `Protocol/sap_amendments.md`, never a silent edit. Phase 5 reads `specs/variables_locked.json` at start and HALTS if the file is absent or unsigned.

---

## PHASE 5A — SECONDARY (ADJUSTED) → fills Table_2 (autonomous)

**Terminology lock (per L051):** "Secondary analysis" in this skill = PSM + multivariable adjusted models + KM survival curves + IPTW + method variants. These use ONLY the variables locked at HALT 2A.

**Variable load gate:** Read `specs/variables_locked.json` at the start of Phase 5. If absent or unsigned → HALT immediately with error: "Phase 5 cannot fire; HALT 2A not signed. Return to Phase 4 review." No exceptions.

Execute `analysis_plan.secondary` (adjusted models ONLY — PSM, multivariable, KM, IPTW) using the HALT 2A-approved variables. **Sensitivity and subgroup analyses do NOT run here — they are Phase 5B, gated on Checkpoint B.** For each: delegate per pointer, run diagnostics, apply gate remediation, append to `results_registry.json` AND `MASTER_ANALYSIS_REGISTRY.json` (per L045), and populate `Table_2`.

**Bolding rule (per L051):** every cell in `Table_2`, `Sensitivity`, or `Supplementary_*` where BH-FDR q < 0.05 is bolded — the rigor-gate threshold for secondary (adjusted) analyses. Cells where p<0.05 but q≥0.05 are NOT bolded; this distinguishes raw-significance from FDR-significance for the reader.

**Concordance check vs. Phase 4 crude (per L051):** for every primary objective, compare the Phase 5 adjusted estimate to the Phase 4 crude estimate. Direction agreement, magnitude within ~30%, CI overlap = concordant. Disagreement is itself a finding and gets logged in `decision_log.md` for Limitations section drafting.

**Special-case enforcement:**
- PSM → caliper-sensitivity table per **L040**
- Within-recipient PSM → access HR + effectiveness HR separately per **L039**
- Cross-cohort comparison → `cohort_harmonization_log.md` per **L011**
- Small-n scRNA → drop-LOO + exact permutation tests per **L029, L030**
- Stage-distribution disparity → within-stratum sanity per **L001**, stage-decomposition per **L008**

---

## ✓ CHECKPOINT B — verify secondary before sensitivity (INLINE, no subagent)

Apply `science-superpowers:verifying-results-before-claiming` to the adjusted results, inline: re-run each adjusted model fresh, read estimate + 95% CI (+ q), confirm `Table_2` matches the registry, confirm diagnostics (PH / EPV / VIF / PS-overlap) passed, and run the **crude-vs-adjusted concordance check** for every primary objective. If a result is irreproducible, a diagnostic fails, or a direction flips unexpectedly → `science-superpowers:investigating-anomalous-results` (root-cause) before continuing. **Phase 5B does not start until Checkpoint B passes** — never run the sensitivity battery on an unverified adjusted result.

---

## ✋ HALT 2B — Review Table_2 (adjusted) before sensitivity

Concise by default: per objective — adjusted effect + 95% CI + q (bold if q<0.05), crude-vs-adjusted concordance verdict, diagnostics status. Options: `proceed to sensitivity` | `revise adjustment` | `investigate anomaly` | `show full details`.

---

## PHASE 5B — SENSITIVITY & SUBGROUPS → fills Sensitivity + Supplementary_* (autonomous; only after Checkpoint B)

Execute `analysis_plan.sensitivity[]` (missing-data / multiple imputation, E-value per L005, caliper sensitivity per L040, alternative specifications, alternative cohort definitions) and `analysis_plan.subgroups[]` (pre-specified subgroups + power justification per L009) using the HALT 2A-locked variables. Populate `Sensitivity` and `Supplementary_*`; bold cells where BH-FDR q<0.05. Verify each result per `verifying-results-before-claiming` before recording. Sensitivity findings that contradict the primary/secondary result are themselves findings — log to `decision_log.md` for Limitations.

---

## PHASE 6 — AUDIT (one clinically-augmented red-team; replaces the 5-agent panel)

**Mechanic (revised 2026-05-30 — token reduction):** Numerical re-check, code-reproducibility replay, and completeness are already done INLINE at Checkpoints A and B via `science-superpowers:verifying-results-before-claiming`. Phase 6 therefore spawns exactly ONE subagent — a `science-superpowers:requesting-red-team-review` reviewer, briefed with `references/red-team-brief.md` (the generic SP reviewer AUGMENTED with CRA's clinical checklist: lessons-log L-rules, diagnostics thresholds, registry cautions, multiple-testing policy, observational-language rule). The reviewer attacks confounds, leakage, assumption violations, multiplicity, and over-claiming. Cost ~3–5K tokens vs. ~17K for the old panel.

| Old audit agent | Now handled by |
|---|---|
| Numerical (re-check numbers) | INLINE `verifying-results-before-claiming` at Checkpoints A/B |
| Code-reproducibility (replay from raw) | INLINE `verifying-results-before-claiming` (fresh re-run from raw + seed) |
| Completeness (every planned analysis ran) | INLINE completeness check at Checkpoint B + Phase 5B |
| Statistical (diagnostics, multiple-testing) | The single red-team reviewer (clinical checklist in `red-team-brief.md`) |
| Biological-plausibility (sign reversals, clinical sanity) | The single red-team reviewer (clinical checklist) |

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

---

## CHANGELOG / Lessons Learned

### 2026-05-28 — L051 — Analysis-skill internal workflow + Master Excel Workbook + bolding + HALT 2A

Refinements added by Bilal Mirza in an interactive workflow design session (2026-05-28). All seven sub-items are interrelated and were specified together; they should be propagated to working-rules.md, the clinical-research-playbook, and the parent CRA repo CHANGELOG.md as a single coherent update.

1. **Primary / secondary terminology locked.** Primary analysis = crude / unadjusted with the appropriate statistical test by outcome class (χ²/Fisher, t/Wilcoxon, log-rank + univariable Cox, χ² + crude OR). Secondary analysis = PSM + multivariable + KM + IPTW + method variants (GBT-IPTW / AIPW / frailty Cox). This terminology is enforced throughout this skill and overrides any prior usage where "primary" meant "adjusted multivariable headline." See §"Terminology lock" callouts in Phase 4 and Phase 5.

2. **Phase 1.0 objectives lock** (new sub-step before §1.1). PI pre-specifies and signs off on `primary_objective` (single contrast sentence) + numbered `secondary_objectives[]`, each with their own outcome, exposure, time horizon, and comparator. Output: `specs/objectives_locked.json` + `Protocol/objectives_locked_<date>.md`. Immutable after PI sign-off; any change is a dated SAP §9-style amendment in `Protocol/sap_amendments.md`.

3. **Phase 1.3 Master Excel Workbook** (replaces legacy markdown `table_layouts.md`). Single file `Reports/MASTER_TABLES_<project>_<date>.xlsx` with explicit named tabs: `Table_1`, `Table_2`, `Table_3`, …, `Sensitivity`, `Supplementary_1`, `Supplementary_2`, …. Coexists with `MASTER_ANALYSIS_REGISTRY.json` (per L045 — machine truth with `history[]`) and its auto-rendered `.md` index. The Excel is the human-facing tabular artifact the manuscript pulls from; the JSON is the audit trail.

4. **Phase 2 PLAN — `matching_variables[]` separated from `adjustment_covariates[]`.** Two distinct lists in `analysis_plan.json`, each entry carrying per-variable rationale (DAG, clinical relevance, comparator precedent, missingness profile). Overlap allowed but not required.

5. **Phase 4 restructured** as PRIMARY (CRUDE / UNADJUSTED) → fills `Table_1`. New shell sign-off gate before any cell is populated. Bold cells where p<0.05. No matching / weighting / adjustment at Phase 4 — those are forbidden until HALT 2A is signed.

6. **HALT 2A inserted** between Phase 4 and Phase 5 — Variable Pre-specification & Approval Gate. Propose matching + adjustment variables with rationale per locked objective; PI signs off; lock to `Protocol/variables_locked_<date>.md` + `specs/variables_locked.json`. Phase 5 reads `specs/variables_locked.json` at start; halts if absent or unsigned.

7. **Phase 5 restructured** as SECONDARY (ADJUSTED) → fills `Table_2` + `Sensitivity` + `Supplementary_*`. Bold cells where BH-FDR q<0.05. Concordance check vs. Phase 4 crude (direction agreement, magnitude within ~30%, CI overlap) for every primary objective; disagreement logged for Limitations.

**Why this matters:** Prior workflow conflated "primary" with "primary contrast" (the adjusted headline), bypassing the standard biostatistical convention that primary = unadjusted and secondary = adjusted. The bolding rule + Excel workbook give the PI an immediately scannable artifact that maps directly to the manuscript tables; the HALT 2A gate prevents covariates from sneaking into the adjusted model without explicit PI review. The objectives lock prevents post-hoc objective drift.

**Companion edits in this same release** (push together):
- `internal/project-init/SKILL.md` — added primary + secondary objective questions to STEP 1; added `Protocol/` folder to STEP 2 directory tree.
- `internal/manuscript-qc/SKILL.md` — added Check 16 (4-artifact numeric reconciliation: abstract ↔ manuscript ↔ Excel ↔ JSON).
- `iCloud:SESSION-END PROTOCOL.md` — added Step 4.6 per-project 4-artifact reconciliation (iCloud-local, not in this repo).
- `references/lessons-log.json` — L051 machine-readable entry with trigger patterns + actions.

**Worked example pending:** First clinical-research project initiated under this workflow will become the canonical worked example (link to be added here at first project completion).
