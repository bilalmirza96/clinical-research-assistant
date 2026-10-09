# `/analyze` — CHANGELOG / Lessons Learned

**Load trigger:** only when you need the history behind a rule or phase (why it looks the way it does), or when appending a dated entry at SESSION-END. Never needed to run an analysis; `SKILL.md` holds enforcement, `../../references/lessons-log.json` holds the machine-readable lessons. Newest first.

---

### 2026-10-10 — ladder_table change column undefined at the null (L111)

A SEER stage III chemoradiation ladder with a crude OR of 0.997 printed "change from unadjusted" of -7777.8%,
because the percent change divides by log(crude). `ladder_table.py` now prints "n/a (unadjusted at null)" when
|log crude| < 0.01 (`NEAR_NULL_LOG`). Test: `tools/tests/test_linters.py::test_ladder_change_suppressed_when_crude_at_null`.


### 2026-09-28 — Scope-triage step for bounded/quick requests (L100)

Regression eval evidence: asked for one adjusted model plus its E-value, `/analyze` insisted on
running the full analysis ladder and ran out of turns before answering. Added a **scope-triage**
step at the very start of "What runs when you invoke `/analyze`": a single unadjusted/small bounded
computation now routes automatically to `--quick` (`references/quick-tier.md`), labeled
`EXPLORATORY`; a single bounded computation that names exactly one adjusted model (e.g., one model
+ its E-value) is **not** routed to `--quick` because `quick-tier.md`'s own guardrail excludes
adjusted/matched/weighted models — instead it answers only the named question inside full
`/analyze` (one-line HALT 2A decision, fit only the requested model, compute only the requested
downstream quantity), labeled `EXPLORATORY`, with promotion to a manuscript/abstract/slide/registry
`current` value still requiring the full ladder. Author-approved 2026-09-28; principle: both
standing rules (the full ladder, and quick-tier's own guardrails) stay intact, only their scope of
application is clarified — no HALT/CHECKPOINT/HARD GATE/HARD STOP/NON-NEGOTIABLE text moved or
weakened (counts verified unchanged before/after). Regression check: `evals/L005-e-value-adjusted-estimate`.
Lessons-log **L100**.

### 2026-09-28 — Phase 6 red-team is now a real fresh-context subagent

Phase 6's reviewer was, in practice, a skill (`science-superpowers:requesting-red-team-review`)
loaded and executed inline — the same context window that ran the analysis was also asked to
find its own mistakes. Every error this lab has actually caught in production (GENIE off-panel
genes silently coded wild-type; the HNSCC scRNA-seq audit's 4 critical + 8 high-severity issues,
found only after four sessions of in-context review; the REPEAT DISPARITIES penalizer bias and
race x era product-term artifact) was caught by a reviewer that did not share the blind spots of
the context that produced the error, not by that same context re-reading itself.

Added `agents/cra-red-team.md` at the plugin root: a genuine fresh-context subagent (Read, Glob,
Grep, Bash only — Bash restricted to re-deriving numbers from source CSVs/the registry and
running the project's own linters; it never writes, edits, or deletes) invoked via the Agent
tool, `model: inherit` so judgment work stays on the frontier model. Its brief is distilled from
`references/red-team-brief.md`, `references/audit-agents.md`, and `references/critique-panel.md`
into ten adversarial lenses (denominators, dictionary labels, cohort N reconciliation,
off-panel/not-tested coding, penalizer and sparse levels, multiplicity, precision and rounding,
absence claims, period-trend product terms, plus the standard SP attack vectors) under one rule:
re-derive, never transcribe. It writes `Reports/red_team_<date>.md` with CRITICAL/HIGH/MEDIUM/LOW
tiers (each finding as file:line or registry key, expected vs found, and the exact reproducing
command) and a SHIP / FIX FIRST verdict.

Phase 6 (`SKILL.md`) now dispatches this agent via the Agent tool instead of loading the SP
skill in-context; its output is copied to `audit_report.md` so every downstream reference (HALT 3,
the remediation pipeline, State files) is unchanged. Phase 3's inline critique (methodologist /
skeptic / editor / lessons-applier, `references/critique-panel.md`) is untouched — it still
escalates to the SP skill only on a CRITICAL plan flaw; that escalation was out of scope for this
change. `skills/internal/manuscript-qc/SKILL.md` gained Check 18, invoking the same agent before
any READY FOR SUBMISSION verdict. No HALT / CHECKPOINT / HARD GATE / HARD STOP / NON-NEGOTIABLE
criterion moved or weakened; counts verified unchanged before/after (`grep -c "^## ✋ HALT"`,
`"HARD GATE"`, `"HARD STOP"`, `"NON-NEGOTIABLE"`, `"CHECKPOINT"`) and
`tests/test_study_design_tools.py` still passes (untouched — this change never touched
`scripts/` or `tests/`).

### 2026-09-27 — Progressive-disclosure restructure of SKILL.md (L099)

SKILL.md was carrying its own changelog and text already held by reference files into every `/analyze` run (10,086 words, 1,143 of them this changelog). Enforcement is unchanged: frontmatter, Role, the phase map, PREREQUISITE, the four standing rules, State files, References index, Halt presentation policy, every `✋ HALT` and `✓ CHECKPOINT`, Variable spec amendments, Quality gates and After-analysis closure stay in SKILL.md, and every HARD GATE / HARD STOP / NON-NEGOTIABLE criterion is still stated there. What moved:

- **`## CHANGELOG / Lessons Learned`** → this file (`references/changelog.md`), verbatim. SKILL.md keeps a pointer with the load trigger.
- **`## /analyze --quick`** → `references/quick-tier.md`, verbatim. Loaded only on `--quick`.
- **Phase 0.3 K-Dense delegation table** → replaced by a pointer to `../../references/kdense-delegations.md` §4b, which already held the same seven-row chain (the old pointer said §5, which is the systematic-review section; the Phase 0.2 briefing's `references/kdense-delegations.md` §Phase-0 pointer was corrected to the same target).
- **Phase 1.1.a six-step procedure + the L050 worked example** → replaced by the gate's must-be-true list and a pointer to `../../references/registry-cohort-checklists.md`, whose enforcement contract and Origin held the same text.
- **HALT 2A item 2 covariate-set definitions** → shortened to the gate mechanics plus a pointer to `references/analysis-ladder.md` → "Covariate sets".

Left in place deliberately: Phase 1.0a (dossier HARD GATE), 1.1.b (curation summary), 1.3 (Master Excel workbook, unique to this skill), 1.6 (cohort provenance HARD GATE with its rationale), Phase 2 plan table, Phase 4.0 resource-check options, the L071 result-logging HARD GATE (S1-S6, registry_lint H1-H9: not held by any reference), and 4.2 execution gates. Phases 3, 5A, 5B, 5C, 6, 7 untouched. Verified by a scratchpad script: moved blocks byte-identical in their destinations; HALT / CHECKPOINT / NON-NEGOTIABLE / HARD GATE / HARD STOP counts unchanged; `tests/test_study_design_tools.py` green. Rule going forward: SKILL.md holds enforcement and a phase checklist only; history lives here, detail in `references/` with an explicit load trigger, lessons in `lessons-log.json`.

### 2026-09-26 — Audit lessons from REPEAT DISPARITIES v01 (L092-L095)
- **No ridge on exposure models (L092).** lifelines' penalizer scales with the mean log-likelihood; 0.05 inflated an exposure HR. Fit unpenalized; fix singular fits by finding sparse levels (count and disclose), never by penalizing.
- **Genomic platforms and units (L093).** Never pool TMB across platforms or scales; compare within sequencing assay; gate unit conversions against the source's bins (GENIE TMB is per base). Mask off-panel genes; withdraw gene-level claims when coverage is unknown.
- **Test differences, not significance (L094).** Compare stratum estimates formally (product term, or ratio of independent estimates per Altman and Bland 2003).
- **Treatment fields before approval (L095).** Tabulate a registry drug-class field by year and histology against approval dates before interpreting it; restrict the primary analysis to the approval era.
- **Period trends need period-specific covariates (L096).** A race x era product term with every covariate effect held constant across eras manufactured a widening disparity (histology x era change absorbed by the race term). Estimate change across periods from within-period models (ratio of independent estimates) or let major prognostic covariates vary by period; report the common-effects product term only as a labelled sensitivity.

### 2026-09-25 — L087-L090 — Analysis ladder, cohort curation, data-dictionary dossier, denominators

Author directive after the REPEAT DISPARITIES project (esophageal cancer, NCDB + SEER; ITSOS 2026
podium): "compute and compare in this order... always care about inclusion and exclusion
criteria... study the data dictionaries in detail... use consistent and most appropriate
denominators for the question being asked."

1. **Analysis ladder (L087).** Phase 5 now runs fixed rungs in order on one cohort: unadjusted,
   Model A (clinical only), Model B (clinical plus everything else), adjusted survival, IPTW
   (+PSM), E-values, causal mediation (new Phase 5C), ML / novel methods. Two adjusted models only
   (author: "A only clinical, B includes everything else too"). `Table_2` columns follow the
   rungs; HALT 2A approves covariate sets by ladder role; `scripts/ladder_table.py` (table,
   attenuation, E-values, flags) gates Checkpoint B. `evalue()` refuses an OR or HR without a
   stated outcome frequency (the project's circulating surgery E-value of 3.41 was the RR formula
   on a common-outcome OR; the correct value was 2.17).
2. **Cohort curation (L088).** New §1.1.b and `references/cohort-curation.md`: baseline-only
   eligibility, explicit unknowns, endpoint sub-cohorts, CONSORT by exposure group with
   differential-exclusion flags, one builder (`scripts/cohort_flow.py`), exact N reconciliation
   (the project's KM export and Cox model differed by 119 zero-follow-up patients).
3. **Data-dictionary dossier (L089).** New HARD GATE §1.0a, `references/data-dictionary-dossier.md`,
   `scripts/dictionary_audit.py`. Five project defects it catches: "Refused" mapped to a code that
   NAACCR 1340 does not have; code 1 labelled "not recommended"; the 2023 alphanumeric surgery
   field parsed as numeric (a false era-narrowing claim, P=.0011 → .35); a coding break by year;
   surgery flag vs reason code 0.
4. **Denominators (L090).** `references/denominators.md`; Phase 2 `denominators` plan section;
   Master Excel percentage cells name their denominator. The project's "Black patients refused
   less" came from comparing shares among non-operated patients.
5. **L010 withdrawn** (provider-side "not recommended" reading of the reason field).

Tested RED/GREEN: three pressure scenarios run against the pre-change skill failed (a single adjusted
model with no clinical-only comparison and IPTW/PSM "descoped" under deadline; reason shares
compared across races among the non-operated; the old recode map reused with refusals reported
as 0 vs 0) and passed when re-run against this version. A transfer test on an unrelated SEER
study exposed a "don't redo the analysis, just tighten the sentence" loophole, which was closed
and re-tested. Tool tests:
`python3 tests/test_study_design_tools.py`.

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
