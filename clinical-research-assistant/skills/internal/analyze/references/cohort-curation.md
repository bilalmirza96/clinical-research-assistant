# Cohort curation: inclusion and exclusion criteria

**Rule (author directive 2026-09-25, L088).** The cohort is designed, not typed on the way to a
model. Criteria come from the question, the data-dictionary dossier (L089), the registry
checklist (L050) and the comparator papers. They are reviewed with the PI at HALT 1, before any
outcome is computed, then built once, by one script, into one cohort that every downstream
artifact reads. Time spent here is the cheapest time in a project: each defect below cost a
re-run, a withdrawn claim, or a slide corrected hours before a talk.

## Curating the criteria (Phase 1.1)

For each criterion record: the expression; the dictionary reference (item and codes by name); the
rationale; whether it is a literature convention or study-specific; whether unknowns are in or
out; and, after assembly, the N removed overall and by exposure group. Record the criteria that
were considered and rejected too.

1. **Start from the question.** Who could have received the exposure and experienced the outcome?
   Define eligibility from information available at baseline (diagnosis or index date).
2. **Never select on what the exposure or treatment changed.** A field that folds in post-baseline
   information conditions on it. NCDB `ANALYTIC_STAGE_GROUP` uses pathologic stage when it exists,
   and pathologic stage exists only after resection, so selecting or adjusting on it conditions on
   surgery; use clinical stage. Exclusions on survival time or on treatment received belong only in
   an explicit landmark or target-trial design (L069).
3. **Decide unknowns explicitly.** `stage.isin([1, 2, 3])` silently drops unknown stage. Say for
   each criterion whether unknown is in or out, and why. `cohort_flow.py` raises when a mask
   contains missing values.
4. **Missing covariates are not exclusion criteria.** Handle them in the analysis (Unknown
   category or multiple imputation, L004). If a ladder rung needs complete cases, apply that
   restriction to every rung it is compared with (analysis-ladder.md, constant cohort).
5. **Define the unit**: patient, tumour or admission; first primary only or all primaries (L050);
   duplicates.
6. **Endpoint eligibility is a named sub-cohort, not a separate filter chain.** Survival needs
   follow-up time and a known vital status. NCDB PUFs carry no follow-up for the most recent
   diagnosis year, and a patient with 0 months of follow-up contributes no person-time. Define the
   survival sub-cohort once, register its N, and have the Kaplan-Meier export, the Cox model, the
   figures and the slides all read it.
7. **Check differential exclusion.** Look at every step's removals by exposure group. A step that
   removes a visibly different share of one group is a selection-bias risk: in REPEAT DISPARITIES,
   missing clinical stage removed 20.1% of Black and 15.3% of White patients. Register it and run
   a selection sensitivity analysis (a broader cohort that keeps them, or inverse-probability-of-
   selection weights).
8. **Harmonize across datasets** (L011, L050): identical criteria, a side-by-side table, every
   deviation justified.
9. **Assert consistency and read year-by-year rates** in the builder (`dictionary_audit.py` D5,
   D6). The REPEAT DISPARITIES 2023 surgery defect showed as a 0% surgery rate in 2023 and as
   2,192 patients with reason code 0 ("surgery performed") but surgery = 0.

## Building it (Phase 4.1)

`scripts/cohort_flow.py` is the only code that filters raw data: `CohortFlow.include` and
`.exclude` for each step, `.endpoint` for endpoint sub-cohorts, and `.write("data/working")` for
`filter_operations.json` plus `filter_log.md` (a CONSORT table by exposure group, with
differential-exclusion flags). Analysis scripts load the cohort artifact; they never re-filter raw
data.

## Reconciling it (before every deliverable)

- **Exact, not approximate.** `assert_n(registered_n, len(df), label)` and
  `assert_same_cohort(ids_a, ids_b, label)` wherever two artifacts claim the same cohort. "119 of
  114,000 is nothing" is how a deck ends up with two Ns for one population and a gap printed as
  9.9 points on one slide and 9.8 on another.
- **Strata sum to the parent.** Stratum Ns plus the explicitly excluded categories equal the
  registered cohort N.
- **Reproduce before stratifying.** A subgroup or stratified analysis first re-derives the
  registered overall estimate on the same cohort object, exactly. The REPEAT DISPARITIES histology
  analysis reproduced the registered overall Model A HR of 1.140 before any stratum was trusted.
- **Fix at the source.** A mismatch is fixed by rebuilding the artifact from the cohort, never by
  footnoting two Ns.

## Red flags

- A script with its own `df = df[...]` filters on raw data
- An N in a figure, table or slide that is not a registered cohort or sub-cohort N
- "Close enough" about a cohort count
- An exclusion step whose removal share by group was never looked at
- A cohort variable that is only known after treatment
