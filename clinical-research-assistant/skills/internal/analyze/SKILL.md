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

**Scope triage — read `references/quick-tier.md` first, then classify the request before Phase 0 fires:**

- **A single unadjusted estimate or a small bounded computation** (a single 2x2, one KM curve, one test, or pulling and formatting an existing registry value) → route automatically to `/analyze --quick` (below). Label every output `EXPLORATORY`. State plainly that the full analysis ladder (unadjusted → Model A → Model B → adjusted survival → IPTW → E-values → causal mediation → ML/novel) is required before any number from this run may reach an abstract, manuscript, slide, or a registry `current` value.
- **A single bounded computation that names exactly one adjusted model** (e.g., "fit one adjusted model for X, adjusting for A/B/C, and give me its E-value") → `references/quick-tier.md`'s own guardrail excludes adjusted, matched, and weighted models from `--quick`, so this request does not route there. Instead answer only the named question inside full `/analyze`: record the HALT 2A covariate-approval decision in one line and continue, fit exactly the one requested model (do not run ladder rungs the user did not ask for), and compute the requested downstream quantity (e.g., the E-value). Label the output `EXPLORATORY` and state that promotion to an abstract, manuscript, slide, or registry `current` value still requires completing the full ladder, in order.
- **Anything broader** — a request spanning multiple models, a comparison table, or any request the user has not explicitly bounded to one named estimate — runs the full ladder below, in order, with no rung skipped.

This triage narrows how many phases run and how many turns they take; it never narrows rigor. The four standing study-design rules further below, and every halt and gate in the diagram, bind the bounded paths exactly as they bind the full ladder.

```
Phase 0 PRE-DESIGN  pre-analysis literature recon — auto-invokes /literature-review
                    produces evidence_bank, citation_bank, novelty_assessment, differentiation_brief
   ✋ HALT 0        PI signs off on differentiation: novel | replication-with-extension | pivot | abandon
Phase 1 INTAKE      data-dictionary dossier (L089) → curated inclusion/exclusion (L050, L088) → lock dataset_spec, variable_spec, table_layouts (denominators named, L090), figure_intent
Phase 2 PLAN        produce analysis_plan.json (analysis ladder, L087) + manuscript_shopping_list
Phase 3 CRITIQUE    INLINE plan-sanity (Methodologist/Skeptic/Editor/Lessons run inline, no panel); no pre-registration step (removed 2026-10-08, L108)
   ✋ HALT 1        user approves intake + plan + critique (bundle or section-by-section)
Phase 4 PRIMARY     resource check → cohort assembly (cohort_flow.py, CONSORT by exposure group) → build Master Excel shells → rung 1 UNADJUSTED → fills Table_1 (bold p<0.05) → diagnostics
   ✓ CHECKPT A     INLINE verify (SP verifying-results-before-claiming): re-run, read estimate+CI, confirm reproduction
   ✋ HALT 2        user reviews Table_1 + crude effect estimates (concise by default; verbose if surprises)
   ✋ HALT 2A       user APPROVES matching variables + Model A (clinical) and Model B (everything else) covariate sets + mediators for Phase 5 (HARD STOP)
Phase 5A SECONDARY  ladder rungs 2-5 in order: Model A clinical → Model B fully adjusted → adjusted survival → IPTW (+PSM) → fills Table_2 (bold q<0.05)
   ✓ CHECKPT B     INLINE verify + ladder_table.py (one cohort, rung order, attenuation, sign) before sensitivity runs
Phase 5B SENSITIVITY rung 6 E-values + sensitivity battery + subgroups/effect modification → Sensitivity + Supplementary_* (runs only after Checkpoint B passes)
Phase 5C EXPLAIN    rung 7 causal mediation → rung 8 ML / novel methods, when they answer a question rungs 1-6 cannot
Phase 6 AUDIT       ONE fresh-context red-team (Agent tool → `cra-red-team`) — replaces the 5-agent panel; verify/repro/completeness already done inline at A/B
   ✋ HALT 3        user reviews audit + 4-tier evidence classification
Phase 7 DELIVER     master analysis_report.md with reproducibility manifest + SCAR registration
```

Five halts (Phase 0, HALT 1, HALT 2, HALT 2A, HALT 3). Phase 0 is a HARD GATE — Phase 1 cannot fire without PI sign-off on differentiation. HALT 2A is a HARD STOP — Phase 5 cannot fire without PI sign-off on matching + adjustment variables. Everything between halts is autonomous. Status emits at every phase boundary.

---

## `/analyze --quick` — exploratory tier (per L058)

Load `references/quick-tier.md` only when `/analyze` is invoked with `--quick`. It defines the exploratory tier: what runs, the structural firewall (results go to `Reports/exploratory_quick_log.md` only, never to SCAR or any Master Excel tab; class `EXPLORATORY-UNGATED`, not an L035 tier), what is dropped versus never dropped, and the guardrails (no adjusted / matched / weighted models, one contrast, promotion only through full `/analyze`).

---

## PREREQUISITE — read before anything else

Read `lessons-log.json` up front. Read each policy reference below **on demand, at the phase that needs it** — do not bulk-load (token-lean):

1. `references/clinical-analysis-policy.md` — methodological policy; parent contract
2. `references/method-selection-guide.md` — model selection
3. `references/diagnostics-checklist.md` — required diagnostics per method
4. `references/registry-cautions.md` — registry-specific rules
5. `references/variable-collapse-defaults.md` *(pending Concern #12 decision)* — default category-collapse rules
6. `../../references/lessons-log.json` — trigger patterns + actions for every lesson
7. `references/data-dictionary-dossier.md` — Phase 1.0a, before any filter or recode (L089)
8. `references/cohort-curation.md` — Phase 1.1 and Phase 4.1 (L088)
9. `references/denominators.md` — Phase 1.3 table shells, and every proportion anywhere (L090)
10. `references/analysis-ladder.md` — Phase 2 plan, HALT 2A, Phase 5 (L087)

**All policies in `clinical-analysis-policy.md` OVERRIDE defaults stated here.** Lessons in `lessons-log.json` are enforced via:
- Phase 3 INLINE plan-sanity (lessons checked inline against `trigger_patterns`; no subagent panel)
- Phase 4 / 5 execution gates (diagnostics-checklist enforcement; prescribed remediation on failure)
- Phase 6 red-team: one `cra-red-team` agent (spawned fresh-context via the Agent tool) verifies multiple-testing, PH, EPV, etc. via `references/red-team-brief.md` (most checks already done inline at Checkpoints A/B)

If any prerequisite file is missing, halt and surface the gap. Do not proceed without the parent contract loaded.

---

## Four standing study-design rules (NON-NEGOTIABLE; L087-L090)

Author directive 2026-09-25, from the REPEAT DISPARITIES project. They bind full `/analyze`,
`--quick`, and every number another CRA skill reports.

1. **Study the data dictionary before using a variable (L089).** One dossier entry per variable,
   written from the official dictionary for the exact data vintage; recode maps and raw data
   checked with `scripts/dictionary_audit.py`. → `references/data-dictionary-dossier.md`
2. **Curate the inclusion and exclusion criteria (L088).** Designed from the question, reviewed at
   HALT 1, built once by `scripts/cohort_flow.py`, counted by exposure group, reconciled exactly.
   → `references/cohort-curation.md`
3. **One question, one denominator (L090).** Write "Among [population], what share...", name that
   population on every artifact, and keep it for that question everywhere.
   → `references/denominators.md`
4. **Compute and compare in ladder order (L087).** Unadjusted → Model A (clinical only) →
   Model B (clinical plus everything else) → adjusted survival → IPTW → E-values → causal
   mediation → ML or other novel methods, on one cohort, side by side (`scripts/ladder_table.py`).
   Two adjusted models only.
   → `references/analysis-ladder.md`

**Violating the letter of these rules is violating their spirit.** Each thought below appeared
in testing or in the project, and each was wrong:

| Thought | Reality |
|---|---|
| "The abstract already used this script's recode map" | A script is not a dictionary. Audit the map; if it is wrong, the abstract is wrong too, and the PI is told before the talk. |
| "0 vs 0: neither group has refusals in this extract" | A zero in every group is a mapping alarm (the map pointed at code 3, which NAACCR 1340 does not have; refusals were code 7). |
| "Code 1 is the provider-side 'not recommended' category" | Code 1 is "not part of the planned first course", which includes a patient choosing an offered non-operative option. L010 is withdrawn. |
| "Deadline: one adjusted model, PSM/IPTW deferred" | The ladder is the analysis. Shorten the prose, not the ladder; a skipped rung needs a written reason. |
| "Don't redo the analysis; just tighten the existing result into a sentence" | A single model that never went through the ladder is not a reportable finding. The fix is running the ladder on the reconciled cohort (same day with `ladder_table.py`), not a caveat on the old number. |
| "Compare the races on the reason mix among the non-operated" | Shares within a subgroup are compositional. Compare likelihood on all eligible patients; show the mix only within a group. |
| "119 of 114,000 is close enough" | Two Ns for one cohort is a defect. Rebuild from the cohort artifact and assert the N exactly. |

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
- `references/red-team-brief.md` — clinically-augmented brief distilled into the `cra-red-team` agent (`../../../agents/cra-red-team.md`); this file remains the source the agent brief was distilled from (supersedes the legacy 5-agent `audit-agents.md`)
- `references/sp-integration.md` — which science-superpowers skill fires at which phase (rigor layer contract)
- `references/delegation-matrix.md` — K-Dense + BioMedAgent routing by task type, with `resource_class` per task
- `references/analysis-report-template.md` — 16-section + reproducibility manifest
- `references/analysis-ladder.md`, `references/cohort-curation.md`, `references/data-dictionary-dossier.md`, `references/denominators.md` — the four study-design standards (L087-L090)
- `references/quick-tier.md` — the `--quick` exploratory tier (what runs, the exploratory-log firewall, guardrails); load only when invoked with `--quick`
- `references/changelog.md` — dated history of every change to this skill (L051, L087-L090, L092-L096, restructures); load only to learn why a rule exists or to append an entry at SESSION-END
- `../../references/kdense-delegations.md` §4b — Phase 0 K-Dense delegation chain and contracts; load during Phase 0 only
- `../../references/registry-cohort-checklists.md` — per-registry inclusion/exclusion checklist and its enforcement contract; load at Phase 1.1.a before any filter is written
- `scripts/ladder_table.py` (ladder table, attenuation, E-values), `scripts/cohort_flow.py` (cohort builder, CONSORT by group, exact reconciliation), `scripts/dictionary_audit.py` (data and recode-map audit against the dossier); tests: `python3 tests/test_study_design_tools.py`

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

> "Phase 0 pre-design literature recon for `/analyze`. Read `study_spec.json` for the research question. Produce evidence_bank.json (prior work landscape), citation_bank.json (L041-verified citations), novelty_assessment.json (using `templates/state/novelty_assessment.template.json` schema), and differentiation_brief.md (using `templates/state/differentiation_brief.template.md` schema). Use K-Dense delegations per `../../references/kdense-delegations.md` §4b (Phase 0). Hand control back to /analyze when all four artifacts exist and the differentiation brief is populated up to (but not including) PI signature."

/literature-review handles the search; /analyze does NOT proceed to HALT 0 until the four artifacts exist.

### 0.3 K-Dense skill delegations (Phase 0 specific)

Read these as expert reference, do not re-invoke if already loaded in /literature-review. The Phase 0 delegation chain (brainstorming if the question is broad → `literature-review` sweep → direct PubMed/OpenAlex queries → `scholar-evaluation` ranking of comparators → `scientific-critical-thinking` → `hypothesis-generation` on pivot → `citation-management`, the L041 hard gate on every `citation_bank` entry) and its full contracts: `../../references/kdense-delegations.md` §4b (Phase 0 — Pre-design Lit Recon) and §1 (citation). Load that reference only while Phase 0 is running.

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

### 1.0a Data-dictionary dossier — HARD GATE (per L089)

Before any filter is written or any variable is recoded, read the official dictionary for the
exact data vintage (for NCDB: the PUF Data Dictionary for that PUF year plus the NAACCR item
definitions) and write `specs/data_dictionary_dossier.md` + `.json` with one entry per variable
the study touches: item and number, source page, storage type, every allowable code with its
definition, years populated, what a derived field folds in, individual vs area level,
cross-field consistency rules, and the claim boundary (the words prose may use for each code).
Then:

- Run `scripts/dictionary_audit.py` on the raw frame (D1-D6) and on every recode map (M1-M3).
  Hard failures stop Phase 1.
- Labels in tables, figures, slides and prose come from the dossier's claim boundary, never from
  an existing script or the PI's phrasing.
- Present the dossier at HALT 1 with the specs. Procedure, fields and alarms:
  `references/data-dictionary-dossier.md`.

### 1.1 `dataset_spec.json`

Every dataset touched (primary + merged + external):
- `name`, `file_path`, `version_hash` (sha256 at read-time), year range, raw N
- `inclusion_filters` and `exclusion_filters` as executable boolean expressions
- merge/join keys if multiple
- Schema: `references/intake-schemas.md`

#### 1.1.a Registry-specific inclusion/exclusion checklist (HARD GATE per L050)

**Before any filter is written to `dataset_spec.json`,** load `../../references/registry-cohort-checklists.md` for the registry named in `study_spec.dataset_type` (NCDB / SEER / NSQIP / UNOS / TriNetX / generic) and run its enforcement contract in full. What must be true before `dataset_spec.json` is written:

- every item (~25 per registry) presented as a table: filter | common defaults in literature | proposed value with rationale | `[ ]` PI checkbox; PI decides yes / no / custom (custom requires free-text rationale);
- PI has explicitly ticked `[ ] I have reviewed every item; no filter is silently defaulted`;
- cross-registry studies (e.g., NCDB + SEER replication) presented side by side, every deviation surfaced as a §HALT/AMBIGUITY note requiring justification;
- the completed checklist, including filters considered AND rejected, appended to `Reports/phase1_consort_<date>.md` as a permanent record.

The failure this gate prevents (the L050 NCDB "all primaries" vs SEER "first primary only" mismatch) is recorded under Origin at the top of that reference.

#### 1.1.b Curate the criteria, not just the checklist (per L088)

The checklist says which filters to consider; curation decides them well. Per
`references/cohort-curation.md`, every criterion carries its dictionary reference, rationale,
and an explicit in/out decision for unknowns. Eligibility uses only baseline information (never a
field that folds in post-treatment data, such as NCDB `ANALYTIC_STAGE_GROUP`). Missing covariates
are handled in the analysis, not by exclusion. Endpoint eligibility (for survival: follow-up > 0
and a year with vital status) is a named sub-cohort of the one analytic cohort, never a second
filter chain.

### 1.2 `variable_spec.json`

Every variable in any analysis (primary, secondary, sensitivity, subgroup). Categories: `outcomes` (primary + secondaries), `exposure(s)`, `covariates`, `effect_modifiers`, `subgroup_vars`, `sensitivity_only_vars`. Each entry: `name`, `label`, `type`, `source_columns`, `derivation`, `missing_handling`, plus `levels` + `reference` for categorical, `dossier_ref` (its data-dictionary dossier entry, L089) and, for covariates, `ladder_role` (`clinical` = in Model A and B / `model_b` = added in Model B / `mediator` / `effect_modifier`, L087).

**Variable collapse defaults** *(pending Concern #12 decision):* For multi-category variables without user-specified collapse rules, apply the defaults in `references/variable-collapse-defaults.md` and surface every auto-collapse decision in the Phase 3 critique. User overrides via section-by-section revise at HALT 1.

### 1.3 Master Excel Workbook — `Reports/MASTER_TABLES_<project>_<date>.xlsx` (per L051)

Pre-design every manuscript table as **a single Excel workbook with named tabs** — this is the source of truth for every numeric result in the project. Build the empty shell at Phase 1.3; cells stay empty until populated in Phase 4 (`Table_1`) and Phase 5 (`Table_2` / `Sensitivity` / `Supplementary_*`).

**Mandatory tabs:**

- `Table_1` — cohort characteristics by exposure (rows = variables from `variable_spec.json`, columns = exposure groups defined by `objectives_locked.json` primary contrast)
- `Table_2` — the analysis ladder per objective (columns in rung order: unadjusted / Model A clinical / Model B fully adjusted / adjusted survival / IPTW / PSM / E-value, L087)
- **Denominators (L090):** every cell holding a percentage names its denominator population in the column header or a footnote, and prints n/N.
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

### 1.6 Cohort provenance check — HARD GATE (per L069)

**Before writing any analysis code on a cohort you did not build in the same script**,
interrogate that cohort's construction and PRINT the answers. A derived cohort carries
its builder's design decisions, and those decisions are silently incompatible with a new
estimand more often than not.

Check and assert, each as a gate that exits non-zero on failure:

1. **Minimum and median follow-up.** A minimum well above zero exposes an applied
   landmark instantly. This single check is the cheapest and catches the most.
2. **Landmark / minimum-survival / immortal-time filters.** Read `filter_operations.json`
   or the assembly script. Never assume; the cohort file name will not tell you.
3. **Complete-case status** and on which variables, since a design matrix is usually a
   strict subset of the cohort it came from.
4. **Time origin**, and whether it matches the new analysis's time zero. If it does not,
   the cohort must be REBUILT, not reused.
5. **Row-index alignment** with any companion design matrix or weight file, verified on a
   patient identifier rather than on row order.

State the cohort's provenance in the script docstring, so a reader meets the mismatch
before they meet the code.

**Why this is a gate and not advice.** A target trial emulation with a grace period was
once built on a post-landmark cohort whose early deaths had already been deleted. The
grace period existed solely to attribute those deaths correctly, so the analysis could
not do the one thing it was written for, and it produced a confident headline number and
a verdict asserting the opposite of the truth. Three rounds of debugging were spent on a
design that was invalid from its first line. Minimum follow-up was 6.01 months, and one
print statement at the start would have shown it.

---

---

## PHASE 2 — PLAN (`analysis_plan.json`)

Generate a complete plan from locked specs:

| Section | Content |
|---|---|
| `estimand` | "Among [population], the effect of [exposure] on [outcome]; primary = crude/unadjusted, secondary = the analysis ladder (Model A clinical adjustment, Model B full adjustment, adjusted survival, IPTW / matching on [matching_variables])." |
| `ladder` | Per objective, the rungs of `references/analysis-ladder.md` in order (1 unadjusted, 2 Model A clinical, 3 Model B fully adjusted, 4 adjusted survival, 5 IPTW + PSM, 6 E-values, 7 causal mediation, 8 ML / novel), each with its method and delegation, and `skipped{rung: reason}` for any rung not run. A rung is never dropped silently. **(per L087)** |
| `denominators` | Per proportion the plan will report: the question in words, the denominator population, whether Unknown is in it, and the registered cohort or sub-cohort it equals. **(per L090)** |
| `primary` | **Crude / unadjusted** per locked objective (per L051 terminology). Appropriate statistical test by outcome class: χ² (or Fisher exact) for categorical, t-test (or Wilcoxon rank-sum) for continuous, log-rank + univariable Cox for time-to-event, χ² + crude OR for cross-sectional binary. **Delegation pointer** + populates `Table_1` tab in Master Excel Workbook. |
| `matching_variables[]` (proposed) | Candidate variables for PSM matching. Each entry: `name`, `rationale` (DAG, clinical relevance, comparator paper precedent, missingness profile), `proposed_for_match` boolean. **Locked at HALT 2A** before Phase 5 fires. |
| `adjustment_covariates[]` (proposed) | Candidate covariates for multivariable adjustment (Cox / logistic / linear), each tagged with its `ladder_role`: `clinical` (Model A, carried into Model B), `model_b` (added in Model B: socioeconomic, access, facility and any other non-clinical confounder), or `mediator` (rung 7 only, never adjusted in Model A or B). Each entry: same fields as `matching_variables[]` with `proposed_for_adjust` boolean. **Locked at HALT 2A**. Distinct from `matching_variables[]` — overlap allowed but not required; a variable may be matched-but-not-adjusted (and vice versa). |
| `secondary[]` | **Ladder rungs 2-5** per locked objective (per L051 terminology, ordered per L087): Model A clinical and Model B fully adjusted (HALT 2A-approved covariate sets), adjusted survival for time-to-event outcomes, IPTW, and PSM (HALT 2A-approved `matching_variables`). All fit on one cohort. **Delegation pointer** + populates `Table_2` tab. |
| `sensitivity[]` | E-values for every adjusted estimate (rung 6; per L005, formula by measure and outcome frequency per L087), missing-data, caliper sensitivity (per L040), selection sensitivity for any differential exclusion (per L088), alternative specs, alternative cohort definitions. Populates `Sensitivity` tab in Master Excel Workbook. |
| `explanatory[]` | Rung 7 causal mediation (pre-specified mediators, counterfactual method, scale) and rung 8 ML / novel methods (the question each answers that rungs 1-6 cannot; exploratory unless pre-specified in the HALT 1-approved plan). **(per L087)** |
| `subgroups[]` | pre-specified subgroups + power justification (per L009). Populates `Supplementary_*` tabs. |
| `diagnostics` | required per method (per `references/diagnostics-checklist.md`) |
| `multiple_testing` | BH-FDR within families; Bonferroni for primary (per L006, L032). **Bolding rule (per L051):** bold cells where p<0.05 in `Table_1`; bold cells where BH-FDR q<0.05 in `Table_2`, `Sensitivity`, and `Supplementary_*` tabs. |
| `manuscript_shopping_list` | required tables + figures (cross-ref Master Excel Workbook tab names, `figure_intent`); Discussion topics; Limitations to address |

Each analysis step has a `delegation` field naming the executing K-Dense or BioMedAgent skill. See `references/delegation-matrix.md` for routing rules and `resource_class` per task.

---

## PHASE 3 — CRITIQUE (inline, no panel)

**Mechanic (revised 2026-05-30 — token reduction):** Run the four critique lenses below INLINE against the locked specs + plan, using the question checklist in `references/critique-panel.md`. Do NOT spawn a 4-agent panel. Write findings to `plan_audit_report.md`. Escalate to ONE `science-superpowers:requesting-red-team-review` subagent ONLY if an inline lens surfaces a CRITICAL plan flaw. There is no pre-registration step (author directive 2026-10-08, L108): do not invoke `science-superpowers:preregistering-analysis` and do not write `Protocol/preregistration_<date>.md`. The HALT 1-approved `analysis_plan.json` is the record of what was planned, and any analysis added after outcomes are seen is labelled exploratory. Inline cost ~2–3K tokens vs. ~15K for the old panel.

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

1. **Cohort assembly** per `dataset_spec`, in ONE builder script: `dictionary_audit.audit_frame` on the raw frame first (L089), then `scripts/cohort_flow.py` for every inclusion/exclusion step and endpoint sub-cohort (L088). It writes `data/working/cohort.csv` + `filter_operations.json` + `filter_log.md` with CONSORT counts by exposure group and differential-exclusion flags. Register the cohort N and each endpoint sub-cohort N; every later script loads these artifacts and never re-filters raw data. Any differential-exclusion flag goes to HALT 2 with a proposed selection-sensitivity analysis.
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

#### Result-logging discipline — HARD GATE per L071

L045 says *where* numbers live. **L071 says they must be logged as work completes and every key must be self-describing.** A registry of ambiguous keys is a database of traps. This failed once already: a matched estimate from one arm was written into an abstract beside an unmatched estimate from the other, and a subgroup reported as INFERIOR was actually INCONCLUSIVE on the like-for-like comparison.

Six safeguards, mechanical wherever possible:

| # | Safeguard | What it forbids |
|---|---|---|
| **S1** | **Real-time logging.** Each analysis script upserts its own results before the session moves on. | End-of-session batch upserts. A number that lives only in a JSON file or console log does not exist. If a script computes variants (1:1 *and* 1:3; all-cause *and* cancer-specific), it registers **all** of them or its docstring says which it omits and why. |
| **S2** | **Self-describing keys.** The KEY carries population + specification (`NCDB.scc.matched11.*`, `SEER.adeno.cancerspecific.*`). | Relying on the label for something a reader must know to use the number. One arm gets exactly **one** token everywhere — never mix `scc`/`SCC`/`squamous`. |
| **S3** | **Mandatory label.** Non-empty, naming population, design, endpoint, and for any margin-tested quantity the **VERDICT** (INFERIOR / NON-INFERIOR / INCONCLUSIVE). | `label=None`. Note `analysis_registry.py` stores label at **entry** level and does **not** overwrite it on later upserts — get it right the first time. |
| **S4** | **Parallel-arm parity.** Every registered suffix exists for every arm, or the absence is annotated. | Silently registering one arm of a two-arm comparison. |
| **S5** | **Scope tag on pooled keys.** Any pooled/marginal estimate is annotated `POOLED` and names its stratified counterparts. | A pooled estimate being quoted as stratum-specific. |
| **S6** | **Like-for-like gate.** Both sides of any cross-arm comparison come from the same design family. | Matched vs unmatched, landmark vs grace-period, all-cause vs cancer-specific, tau=36 vs tau=60. |

**Enforcement (run before any deliverable ships):**

```bash
python3 tools/registry_lint.py <registry.json> --arms 'adeno|adenocarcinoma,scc|SCC|squamous' --results-dir Reports --deliverable Reports/abstract.md
```

Checks: `H1` label present · `H2` effect keys carry a CI · `H3` margin implies a stated verdict · `H4` specification in the key not only the label · `H5` arm parity · `H6` pooled keys tagged · `H7` no orphan result files · `H8` every decimal in a deliverable traces to a registry value · `H9` one arm, one token. **Non-zero exit means no deliverable ships.**

Also maintain a per-project **`Reports/REGISTRY_KEY_MAP.md`** (+ `.json`) tagging every namespace on five axes — registry, population, endpoint, design, role — with the near-homonym traps listed explicitly. Regenerate it whenever a namespace is added.


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

1. **`matching_variables[]`** — variables for PSM matching and the IPTW propensity model (the design dimension)
2. **`adjustment_covariates[]`** — covariates for multivariable adjustment in Cox / logistic / linear models (the estimation dimension), grouped by ladder role (per L087): **Model A** = the clinically relevant variables and confounders; **Model B** = Model A plus everything else pre-specified. No other adjusted models. Candidate **mediators** are listed separately for rung 7 and are never adjusted in Model A or B; in a disparities study, say for each socioeconomic or access variable whether it is treated as a confounder or a possible mediator. Definitions of each set, the never-in-A-or-B list and the disparities caveat: `references/analysis-ladder.md` → "Covariate sets".

Overlap between the two lists is allowed but not required — a variable may be matched-but-not-adjusted (e.g., demographics where match handles confounding) or adjusted-but-not-matched (e.g., a clinical severity score with high missingness that excludes it from the match but supports it as a covariate).

Present as a structured table per locked objective:

```
Variable | Match? | Adjust? | Ladder role (clinical/model_b/mediator)  | Rationale (DAG / clinical / comparator / missingness) | PMID
---------|--------|---------|------------------------------------------|------------------------------------------------------|------
[var 1]  | [ ]    | [ ]     | [role]                                   | [text]                                               | [PMID]
[var 2]  | [ ]    | [ ]     | [role]                                   | [text]                                               | [PMID]
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

Execute `analysis_plan.secondary` as **ladder rungs 2-5, in this order** (per L087, `references/analysis-ladder.md`), using the HALT 2A-approved covariate sets:

1. **Model A — clinical** (the clinically relevant variables and confounders)
2. **Model B — fully adjusted** (Model A plus everything else: socioeconomic, access, facility and any other pre-specified confounder)
3. **Adjusted survival** for time-to-event outcomes (standardized survival from Model B, or IPTW-weighted Kaplan-Meier; adjusted difference at the project's time horizon with a bootstrap CI)
4. **IPTW** (stabilized, truncation stated, SMD < 0.1 after weighting, robust SEs) and **PSM** as the matched design variant

No other adjusted models. Rungs 1-3 run on one cohort (same N). Registry keys carry the rung suffix (`.crude`, `.modelA`, `.modelB`, `.adjsurv`, `.iptw`, `.psm`). A rung not run is recorded in `analysis_plan.ladder.skipped` with its reason, never dropped silently, and a deadline is not a reason. **Sensitivity and subgroup analyses do NOT run here — they are Phase 5B, gated on Checkpoint B.** For each: delegate per pointer, run diagnostics, apply gate remediation, append to `results_registry.json` AND `MASTER_ANALYSIS_REGISTRY.json` (per L045), and populate `Table_2` in rung order.

**Bolding rule (per L051):** every cell in `Table_2`, `Sensitivity`, or `Supplementary_*` where BH-FDR q < 0.05 is bolded — the rigor-gate threshold for secondary (adjusted) analyses. Cells where p<0.05 but q≥0.05 are NOT bolded; this distinguishes raw-significance from FDR-significance for the reader.

**Ladder comparison vs. Phase 4 crude (per L051, L087):** for every objective, build the ladder table with `scripts/ladder_table.py` (estimate, 95% CI, N, change from unadjusted on the log scale, E-value). Direction agreement, magnitude within ~30%, CI overlap = concordant. Disagreement or a sign flip is itself a finding and gets logged in `decision_log.md` for Limitations section drafting.

**Special-case enforcement:**
- PSM → caliper-sensitivity table per **L040**
- Within-recipient PSM → access HR + effectiveness HR separately per **L039**
- Cross-cohort comparison → `cohort_harmonization_log.md` per **L011**
- Small-n scRNA → drop-LOO + exact permutation tests per **L029, L030**
- Stage-distribution disparity → within-stratum sanity per **L001**, stage-decomposition per **L008**

---

## ✓ CHECKPOINT B — verify secondary before sensitivity (INLINE, no subagent)

Apply `science-superpowers:verifying-results-before-claiming` to the adjusted results, inline: re-run each adjusted model fresh, read estimate + 95% CI (+ q), confirm `Table_2` matches the registry, confirm diagnostics (PH / EPV / VIF / PS-overlap) passed, and run `scripts/ladder_table.py` for every objective with **zero unresolved flags** (rungs in order, no rung missing without a recorded reason, the same N across rungs 1-3, no unexplained sign flip). If a result is irreproducible, a diagnostic fails, or a direction flips unexpectedly → `science-superpowers:investigating-anomalous-results` (root-cause) before continuing. **Phase 5B does not start until Checkpoint B passes** — never run the sensitivity battery on an unverified adjusted result.

---

## ✋ HALT 2B — Review Table_2 (adjusted) before sensitivity

Concise by default: per objective — adjusted effect + 95% CI + q (bold if q<0.05), crude-vs-adjusted concordance verdict, diagnostics status. Options: `proceed to sensitivity` | `revise adjustment` | `investigate anomaly` | `show full details`.

---

## PHASE 5B — SENSITIVITY & SUBGROUPS → fills Sensitivity + Supplementary_* (autonomous; only after Checkpoint B)

Execute **rung 6 first: E-values** for every adjusted estimate reported as a finding (point and CI limit), with the formula for the measure and the outcome frequency: `ladder_table.evalue(est, lo, hi, measure=, common=)`, which refuses an OR or HR without `common=` (per L005, L087). Then `analysis_plan.sensitivity[]` (missing-data / multiple imputation, caliper sensitivity per L040, selection sensitivity for any differential-exclusion flag per L088, alternative specifications, alternative cohort definitions) and `analysis_plan.subgroups[]` (pre-specified subgroups + power justification per L009; effect modification by a formal interaction test on the full cohort, LRT, before any stratum-specific claim) using the HALT 2A-locked variables. A stratified analysis first reproduces the registered overall estimate on the same cohort object, exactly (L088). Populate `Sensitivity` and `Supplementary_*`; bold cells where BH-FDR q<0.05. Verify each result per `verifying-results-before-claiming` before recording. Sensitivity findings that contradict the primary/secondary result are themselves findings — log to `decision_log.md` for Limitations.

---

## PHASE 5C — EXPLAIN: causal mediation → ML / novel methods (autonomous; after Phase 5B)

Execute `analysis_plan.explanatory[]` (per L087, `references/analysis-ladder.md` rungs 7-8). For
every objective, each of these rungs is either run or recorded in `ladder.skipped` with its reason
("no why-question for this objective" is a reason; silence is not):

- **Rung 7, causal mediation**, when the question asks why or through what and a pre-specified
  mediator is measured after the exposure and before the outcome (treatment received, stage at
  diagnosis). Counterfactual methods only: regression-based or g-formula natural direct and
  indirect effects with the exposure-mediator interaction tested, or interventional effects when
  the exposure cannot be manipulated (race). Survival on an additive, AFT or g-formula scale, never
  a difference of hazard ratios. Proportion mediated with a bootstrap CI, the E-value of the
  residual direct effect, and a joint share when several mediators are asked about together.
- **Rung 8, ML or other novel methods**, only for a question rungs 1-7 cannot answer
  (heterogeneity, non-linearity, gap decomposition, doubly robust estimation, target-trial
  emulation, competing risks, quantitative bias analysis). Seed 42, honest validation, own registry
  keys, labelled exploratory unless pre-specified in the HALT 1-approved plan. They never replace the ladder.

Both are reported in calibrated language ("mediation analysis suggests about half...", never
"explains"), and both are tiered at HALT 3 like every other result (L035).

---

## PHASE 6 — AUDIT (one fresh-context red-team; replaces the 5-agent panel)

**Mechanic (revised 2026-09-28 — fresh-context reviewer):** Numerical re-check, code-reproducibility replay, and completeness are already done INLINE at Checkpoints A and B via `science-superpowers:verifying-results-before-claiming`. Phase 6 therefore invokes exactly ONE subagent — the `cra-red-team` agent, dispatched via the **Agent tool** (`subagent_type: cra-red-team`), which runs in its own fresh context window, separate from the session that produced the analysis. Every error this lab has actually caught in production (GENIE off-panel genes coded wild-type, the HNSCC 4-critical/8-high audit, the REPEAT DISPARITIES penalizer and era-trend artifacts) was found by a reviewer who did not share the blind spots of the context that made the mistake — an in-context critique inherits the same assumptions that caused the error. Hand the agent, explicitly: the project path, `results_registry.json` / `MASTER_ANALYSIS_REGISTRY.json`, every deliverable path under review, and `analysis_plan.json`. The agent's own brief (`agents/cra-red-team.md`, distilled from `references/red-team-brief.md`) carries CRA's clinical checklist: lessons-log L-rules, diagnostics thresholds, registry cautions, multiple-testing policy, observational-language rule. It attacks confounds, leakage, assumption violations, multiplicity, and over-claiming, and re-derives every number it checks rather than transcribing it. Cost ~3–5K tokens vs. ~17K for the old panel.

| Old audit agent | Now handled by |
|---|---|
| Numerical (re-check numbers) | INLINE `verifying-results-before-claiming` at Checkpoints A/B |
| Code-reproducibility (replay from raw) | INLINE `verifying-results-before-claiming` (fresh re-run from raw + seed) |
| Completeness (every planned analysis ran) | INLINE completeness check at Checkpoint B + Phase 5B |
| Statistical (diagnostics, multiple-testing) | The fresh-context `cra-red-team` agent (clinical checklist in `red-team-brief.md`) |
| Biological-plausibility (sign reversals, clinical sanity) | The fresh-context `cra-red-team` agent (clinical checklist) |

Output: the agent is read-only and returns its review in its response; analyze saves it verbatim to `Reports/red_team_<date>.md` (tiered CRITICAL/HIGH/MEDIUM/LOW, SHIP/FIX FIRST verdict); analyze copies this into `audit_report.md` with severity-graded findings (CRITICAL / HIGH / MODERATE / MINOR) so downstream references below are unchanged.

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
- **Run `tools/registry_lint.py` and clear every hard failure (per L071).** Regenerate `Reports/REGISTRY_KEY_MAP.md`. A non-zero lint exit blocks the deliverable.
- **Run `tools/claim_audit.py <deliverable> --registry <registry.json>` and clear every hard failure (per L073).** It flags assertions that something was not tested, not compared, or is not recorded, where a registered result says otherwise. `registry_lint` H8 checks numbers that are present; this checks claims that a number is absent. Never assert a negative about the analysis state from memory - query the registry. Never cite generated prose (a draft, a report, a prior turn) as evidence of what an analysis found.

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
| L087 | any adjusted comparison | Analysis ladder in order on one cohort; `ladder_table.py` zero flags at Checkpoint B |
| L088 | any cohort | Curated criteria; one builder (`cohort_flow.py`); CONSORT by group; exact N reconciliation |
| L089 | any coded registry variable | Dictionary dossier; `dictionary_audit.py` D1-D6 + M1-M3 clean before Phase 2 |
| L090 | any proportion or rate | Denominator from the question, named on every artifact, consistent across the project |

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

History lives in `references/changelog.md` (dated entries, newest first: L092-L096 audit lessons, the L087-L090 study-design standard, the L051 workflow redesign, and every later restructure). Load it only when you need to know why a rule or phase looks the way it does, or when appending a dated entry at SESSION-END. Machine-readable lessons stay in `../../references/lessons-log.json`.
