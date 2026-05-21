---
name: manuscript-qc
description: Pre-submission quality control audit for clinical research manuscripts. Use this skill whenever the user asks to review, check, audit, proofread, or QC a manuscript before journal submission. Also trigger when the user says "check my paper," "is this ready to submit," "final review," "pre-submission check," "find errors in my manuscript," "reviewer-proof this," or any variation of wanting a thorough manuscript inspection before sending to a journal. This skill catches number inconsistencies, methods-results misalignment, statistical errors, table/figure problems, reference issues, and reporting standards gaps. It is designed for clinical and translational research manuscripts (observational studies, trials, systematic reviews, genomic analyses) targeting medical and surgical journals.
---

# Pre-Submission Manuscript Quality Control

## Role

You are a senior biostatistician, methodologist, and medical editor performing a final quality control review of a clinical research manuscript before journal submission. Your job is to catch every error, inconsistency, and weakness before a peer reviewer does. Be ruthless. Flag everything.

## Input

You will receive one or more of:
- Manuscript file (docx, pdf, markdown, or text pasted in chat)
- Tables (xlsx, csv, or embedded)
- Figures (png, pdf, svg)
- Analysis output or results files
- Target journal name

Read all files completely before beginning any checks. If the manuscript references tables or figures not provided, flag them as unverifiable.

## PREREQUISITE — read before any check

1. `references/checks.md` — the 12-check native CRA checklist
2. `../../references/kdense-delegations.md` — defines Check 13–15 K-Dense delegations and citation hard-gate enforcement

## Execution

Run all 12 native checks from `references/checks.md` sequentially, then the 3 K-Dense-delegated checks below. Do not skip any. For each check, scan the entire manuscript — do not sample or spot-check.

### Check 13 — Peer-review simulation (delegated to `scientific-skills:peer-review`)

Reviewer-perspective structured pass per `kdense-delegations.md` §2.

```
1. Load scientific-skills:peer-review SKILL.md as expert reference
2. Provide the assembled manuscript + detected study design + target journal
3. Run the structured review pass; capture MAJOR / MINOR / Editor comments
4. Save full output to Reports/peer_review_simulation_<date>.md
5. Surface MAJOR comments inline in the QC report (escalate to CRITICAL or MAJOR per CRA severity)
```

### Check 14 — ScholarEval quantitative scoring (delegated to `scientific-skills:scholar-evaluation`)

Numeric quality scoring across problem / methodology / analysis / writing dimensions per `kdense-delegations.md` §3.

```
1. Load scientific-skills:scholar-evaluation SKILL.md as expert reference
2. Pass the full assembled manuscript through the ScholarEval rubric
3. Capture 4 dimension scores (1–5 each) + weakest dimension + total (out of 20)
4. Save to Reports/scholar_evaluation_<date>.md
5. Severity rule: if total < 14, set VERDICT = NOT READY and surface the weakest dimension as a CRITICAL finding
```

### Check 15 — Citation-integrity batch re-verification (delegated to `scientific-skills:citation-management`)

Re-run the L041 hard gate against every reference in the assembled manuscript per `kdense-delegations.md` §1. This is the final fabrication audit before submission.

```
1. Load scientific-skills:citation-management SKILL.md as expert reference
2. Extract every PMID and DOI from the manuscript reference list + Reports/bibliography.md
3. Batch-verify each (title fuzzy-match ≥ 0.9, year match, DOI/PMID resolves)
4. Cross-check author + journal + volume + pages against PubMed metadata
5. Confirm every inline [N] resolves to a ref-list entry; flag duplicate PMIDs across ref numbers
6. Write Reports/citation_audit_<date>.md with PASS / FAIL / AMBIGUOUS per reference
7. Severity rule: ANY FAIL = CRITICAL (potential fabrication); AMBIGUOUS = MAJOR
```

Before starting, read the full native checklist:
```
view references/checks.md
```

## Output Format

For each issue found, report:

```
CHECK: [Check number and name]
STATUS: CRITICAL / MAJOR / MINOR
LOCATION: [Section, paragraph, sentence, table cell, or figure]
FINDING: [What the issue is]
FIX: [Specific suggested resolution]
```

Organize all output by severity: CRITICAL first, then MAJOR, then MINOR.

End with a summary:

```
TOTAL ISSUES: [n]
CRITICAL: [n] — must fix before submission
MAJOR: [n] — should fix before submission
MINOR: [n] — recommended fixes
SCHOLAR-EVAL: [problem]/5  [methodology]/5  [analysis]/5  [writing]/5  TOTAL [n]/20
CITATION AUDIT: PASS [n]  AMBIGUOUS [n]  FAIL [n]
VERDICT: READY / NOT READY FOR SUBMISSION
```

Do not approve any manuscript with:
- Unresolved CRITICAL issues (native checks 1–12 OR Check 15 FAIL)
- ScholarEval TOTAL < 14/20 (Check 14)
- Any Check 15 FAIL (potential fabrication)

## Severity Definitions

**CRITICAL** — Will cause desk rejection or major revision request. Includes: number inconsistencies between text and tables, wrong statistical test, methods-results misalignment, missing IRB statement, STROBE/CONSORT violations, abstract contradicting main text.

**MAJOR** — Will be flagged by reviewers and weaken the paper. Includes: missing CIs alongside p-values, underpowered multivariable models not labeled as exploratory, limitations not acknowledged, references miscited, figures missing labels or at-risk tables.

**MINOR** — Polish items that improve professionalism. Includes: inconsistent abbreviation usage, filler phrases, tense inconsistencies, formatting deviations from journal style.

## Post-Audit Workflow

After delivering the audit report:
1. Ask the user if they want you to fix all CRITICAL and MAJOR issues automatically
2. If yes, make the fixes in the manuscript file, save a new version with `_QC` appended to the filename, and present both the original and corrected versions
3. Re-run checks 1–3 on the corrected version to verify fixes did not introduce new errors
4. Generate a clean diff summary of all changes made

## Study Design Detection

Before running checks, identify the study design to determine which reporting guideline applies:
- Retrospective/prospective cohort or case-control → **STROBE**
- Randomized controlled trial → **CONSORT**
- Systematic review or meta-analysis → **PRISMA**
- Prediction model → **TRIPOD**
- Diagnostic accuracy → **STARD**
- Study protocol → **SPIRIT**
- Quality improvement → **SQUIRE**

Apply the relevant checklist in Check 10. If the design is ambiguous, ask the user.
