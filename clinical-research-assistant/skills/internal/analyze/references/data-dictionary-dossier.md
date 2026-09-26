# Data-dictionary dossier: study every variable before using it

**Rule (author directive 2026-09-25, L089).** Before any filter, recode or model, read the
official data dictionary for the exact data vintage and write a dossier entry for every variable
the study touches: exposure, outcomes, covariates, cohort filters and every derived variable. A
variable without a dossier entry cannot enter `dataset_spec.json` or `variable_spec.json`.

An existing script, a recode map from an earlier project, a column name, a label file and memory
are not dictionaries. A map that an abstract already used gets audited like any other; if it is
wrong, the abstract is wrong too, and the PI is told.

## Sources, by dataset

| Dataset | Dictionary to read |
|---|---|
| NCDB | NCDB PUF Data Dictionary for the PUF year in hand, with the SAS/SPSS label file shipped with it; NAACCR Data Standards and Data Dictionary for each item's full coding instructions; STORE manual for treatment items |
| SEER | SEER*Stat variable documentation for the release, the export `.dic`, the SEER Program Coding and Staging Manual |
| NSQIP / MBSAQIP | PUF User Guide for the year |
| Any other | The provider's dictionary for the release, plus the coding manual behind it |

Record document, version and page for each entry. If the dictionary is not in the project, get
it before proceeding: it is part of the data.

## What an entry holds

`specs/data_dictionary_dossier.md` for people and `specs/data_dictionary_dossier.json` for
`scripts/dictionary_audit.py` (fields `item`, `ref`, `storage`, `codes`, `missing_codes`,
`pattern`/`range`, `years`, `derived_from`, `forbidden_labels`, plus top-level `year_column`
and `consistency` rules; see the tool docstring).

| Field | Why it matters | Example (NCDB esophagus) |
|---|---|---|
| Item | Name and item number, per vintage | `REASON_FOR_NO_SURGERY`, NAACCR 1340 |
| Source | Document, version, page | NCDB PUF 2023 Data Dictionary, p. 239 |
| Storage | How the value is stored, not how it looks | `RX_SUMM_SURG_PRIM_SITE_2023` (NAACCR 1291) is alphanumeric, A000-A990 |
| Codes | Every allowable value with the dictionary's definition, unknown codes included | NAACCR 1340: 0, 1, 2, 5, 6, 7, 8, 9. There is no 3 or 4 |
| Years | Vintages in which the field is populated, and changes over time | legacy surgery field 2004-2022, the `_2023` field from 2023; AJCC 6th/7th/8th eras |
| Derived from | What a derived field folds in | `ANALYTIC_STAGE_GROUP` uses pathologic stage when available, so it conditions on surgery |
| Level | Individual or area-level measure | NCDB income and education are zip-code area measures, not the patient's own |
| Consistency | Cross-field rules to assert | reason code 0 ("surgery performed") implies the surgery flag is 1 |
| Claim boundary | Words prose may and may not use for each code | code 1: "surgery was not part of the planned first course of treatment"; never "not recommended", "not offered", "denied" |

## Using it

1. **Labels come from the dossier.** Write recode maps from the dossier and check them:
   `python3 scripts/dictionary_audit.py --dossier specs/data_dictionary_dossier.json --map map.json --var X`.
   Every key must be an allowable code (M1), every allowable code mapped or deliberately excluded
   (M2), and no label may contradict a definition (M3). Merged codes are listed for review.
2. **Audit the data at load.** `audit_frame(raw, dossier)` in the cohort builder: values outside
   the allowable set (D2), storage-type loss (D3), years with no values (D4), coding breaks by
   year (D5), consistency rules (D6). A hard failure stops the build.
3. **Carry the claim boundary downstream.** Table labels, figure legends, slide text, abstract and
   manuscript sentences about a coded variable use the dossier's words. When a claim is challenged,
   cite the page.
4. **A new vintage is a new dictionary.** Diff item lists, code tables and field splits before
   re-running anything on a new PUF year or SEER release.

## Alarms that send you back to the dictionary

- **A category that counts 0 in every group.** It is almost never a finding; the map points at a
  code that does not exist. REPEAT DISPARITIES mapped "Refused" to code 3; NAACCR 1340 has no code
  3, so refusal read 0% in both races while 1,891 documented refusals (code 7) were being counted
  as "not recommended". Every refusal statement made before the fix was void.
- **A label that names an actor or an intent the code's own definition does not name.** NAACCR
  1340 code 1 also covers a patient who chose an offered non-operative option, so "not
  recommended", "not offered" and "denied" are all wrong for it. Code 7 is defined as a
  recommended operation refused by the patient or family, so "refused" is right for code 7 and
  wrong for every other code. Use each code's own definition, nothing broader.
- **A rate that drops to 0% or jumps in one year** (a field split, rename or type change).
- **A value the code list does not contain**, or an allowable code that never appears.
- **Numeric parsing of an alphanumeric field.** `pd.to_numeric("A200")` is NaN, so every 2023
  patient read as unoperated. That manufactured an apparent narrowing of the surgery disparity in
  the immunotherapy era (race-by-era interaction P=.0011) that disappeared after the fix (P=.35),
  and the claim was withdrawn.

## Rationalizations

| Thought | Reality |
|---|---|
| "The abstract already used this map; no time to redo it" | Then the abstract carries the error. Reading one code table takes minutes; retracting a podium claim does not. |
| "0 vs 0: neither group has any refusals" | A zero in every group is a mapping alarm. Check which code refusal is. |
| "The column name says what it is" | Names do not carry coding instructions. Code 1 of `REASON_FOR_NO_SURGERY` includes patient choice. |
| "I'll use the PI's wording for the category" | The label is the dictionary's. The PI's interpretation goes in the Discussion, hedged. |
| "Some raw codes are unmapped; they'll drop out as missing" | Unmapped codes are counted or excluded on purpose, never lost silently (M2). |
