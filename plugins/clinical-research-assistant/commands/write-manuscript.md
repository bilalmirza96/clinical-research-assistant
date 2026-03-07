
---
description: Full manuscript orchestrator for clinical research. Coordinates literature review, statistical analysis, figures, manuscript section drafting, abstract writing, and final consistency audit using verified outputs from each prior phase.
---

# /write-manuscript

## Purpose

Use this command when the user wants to build a clinical research manuscript from a research question, dataset, completed analysis, partial draft, or mixed materials.

This command is an orchestrator. It does not replace the individual phase commands. It coordinates them, tracks progress, carries verified outputs forward, and enforces consistency across all manuscript sections.

---

## When to Use

Use `/write-manuscript` when the user wants to:

* draft an entire manuscript from start to finish
* go from a research question to a manuscript plan
* turn completed analyses into a full first draft
* assemble Introduction, Methods, Results, Discussion, and Abstract into one coherent paper
* continue a manuscript workflow that was started earlier

Do not use this command for isolated tasks that are better handled by a single dedicated command, such as:

* literature review only
* statistical analysis only
* figure generation only
* introduction only
* methods/results only
* discussion only

---

## Core Rules

* Work phase-by-phase.
* Complete only one major phase at a time.
* Present the current Manuscript State Tracker at each phase transition.
* Start at the earliest phase whose required outputs are not yet available and verified.
* Do not skip analytically necessary phases unless:
  * the required outputs already exist and are verified, or
  * the user explicitly chooses to skip them after being warned of downstream consequences.
* Before using outputs from a prior phase, verify that they are:
  * present
  * internally consistent
  * sufficient for the next phase
* If a prior phase is claimed to be complete but the required outputs are missing, treat that phase as incomplete until the missing information is reconstructed or confirmed.
* Never fabricate:
  * results
  * references
  * tables
  * figures
  * statistical methods
  * sample size details
* Never imply causality from observational data unless causal inference is justified by design and analysis.
* Prefer verified outputs over user memory when there is a discrepancy.
* If the user requests a shortened workflow, support a minimum-viable manuscript path using the verified components available, and mark skipped phases clearly in the tracker.

---

## Preferred Workflow Order

1. Manuscript Setup
2. Literature Review
3. Data Analysis
4. Figures
5. Introduction
6. Methods & Results
7. Discussion
8. Abstract
9. Final Assembly & Audit

This sequence is preferred, but the actual starting point depends on what has already been completed and verified.

---

## Manuscript State Tracker

Maintain and update this throughout the session.

```text
MANUSCRIPT STATE TRACKER
========================
Phase 0 — Setup:                [ ] Not started
Phase 1 — Literature Review:    [ ] Not started
Phase 2 — Data Analysis:        [ ] Not started
Phase 3 — Figures:              [ ] Not started
Phase 4 — Introduction:         [ ] Not started
Phase 5 — Methods & Results:    [ ] Not started
Phase 6 — Discussion:           [ ] Not started
Phase 7 — Abstract:             [ ] Not started
Phase 8 — Final Assembly:       [ ] Not started
========================
Allowed status labels:
[✓] Completed
[→] In progress
[—] Skipped
[ ] Not started
If a phase was previously considered complete but later lacks required details for downstream work, change it back to [→] In progress until resolved.
Manuscript Context Block
Build and update this throughout the session. Carry it forward across all phases.
MANUSCRIPT CONTEXT
==================
Research Question:
Study Objective:
Study Design:
Data Source:
Study Period:
Population:
Inclusion Criteria:
Exclusion Criteria:
Primary Outcome:
Primary Exposure:
Secondary Outcomes:
Covariates:
Missing Data Approach:
Target Journal:
Statistical Software:
Sample Size:
Key Finding (primary):
Key Findings (secondary):
Key References:
Tables:
Figures:
==================
Only populate fields when known or verified. Do not invent missing items.
Phase 0 — Manuscript Setup
Goal
Establish the minimum study context needed to determine where the manuscript workflow should begin.
Required Intake Questions
Ask for:
Research question
Study design
Data source
Primary outcome
Primary exposure or predictor
Current project status:
idea only
literature reviewed
dataset ready
analysis complete
manuscript partly written
near-final draft
Whether the user has any of the following already available:
dataset
data dictionary
tables
figures
code
references
manuscript text
Target journal, if known
Determine Starting Point
Start at the earliest phase whose required outputs are not yet available and verified.
Examples:

Research question only, no extracted evidence, no dataset → start at Phase 1
Dataset available, but no verified descriptive analysis or model output → start at Phase 2
Verified tables and primary estimates already available, but no manuscript drafting done → start at Phase 4 or 5 depending on what exists
Draft manuscript largely complete, but no final audit performed → start at Phase 8
Setup Output
After intake, present:
the populated Manuscript Context Block
the current Manuscript State Tracker
the proposed starting phase
Then ask:
"Here is my understanding of your study and current status. Is this correct? We should begin at Phase X unless you want to revise anything."

Exit Criteria
Phase 0 is complete when:
the minimum study context is defined
the starting phase is determined
the initial tracker is set
Phase 1 — Literature Review
Function
Call the /literature-review workflow and record only the outputs needed by later phases.
Entry Conditions
Begin Phase 1 if:
the user has not yet established the study rationale, gap, and key references, or
the available literature framing is insufficient for Introduction and Discussion drafting
Objectives
Produce a verified evidence foundation for the manuscript.
Required Outputs
concise evidence synthesis
gap analysis
refined or confirmed research question
study positioning statement
key references sufficient to support Introduction and Discussion
reference tags indicating likely use:
Introduction
Discussion concordant
Discussion discordant
Methods background if needed
Preferred Evidence Priorities
Prioritize:
peer-reviewed literature
major observational studies
randomized studies when applicable
systematic reviews and meta-analyses
recent specialty-specific evidence
Clearly label any preprints or non-peer-reviewed sources.
State Handoff
After Phase 1, update the Manuscript Context Block with:
refined research question if changed
key references
literature gap statement
study positioning statement
Also create a structured handoff:
LITERATURE HANDOFF
==================
Clinical Problem:
What Is Known:
What Remains Uncertain:
Gap Statement:
Study Positioning:
Key References for Introduction:
Key References for Discussion (concordant):
Key References for Discussion (discordant):
==================
Exit Criteria
Phase 1 is complete when:
the evidence synthesis is adequate to justify the study
the gap is clearly stated
sufficient references exist for later writing phases
Transition Prompt
"Literature review complete. The study rationale and key references are now defined. Next is Phase 2 — Data Analysis, unless you already have verified analysis outputs."
Phase 2 — Data Analysis
Function
Call the /analyze workflow and record only the outputs needed by later phases.
Entry Conditions
Begin Phase 2 if:
verified analysis outputs do not yet exist, or
existing analysis outputs are incomplete, inconsistent, or insufficient for manuscript writing
Objectives
Produce a reproducible, manuscript-ready statistical output package.
Required Outputs
final analytic cohort
variable definitions used in analysis
descriptive statistics
Table 1
primary analysis
secondary analyses if applicable
sensitivity analyses if applicable
model diagnostics and assumption checks
final effect estimates with 95% CI and p-values
final table package
reproducible code or clearly documented analysis workflow, if available within the analysis command
State Handoff
After Phase 2, update the Manuscript Context Block with:
sample size
primary effect estimate
key secondary findings
list of tables
missing data approach
covariate strategy
statistical software if known
Also create a structured handoff:
ANALYSIS HANDOFF
================
Final Analytic Cohort:
Primary Outcome Definition:
Primary Exposure Definition:
Secondary Outcome Definitions:
Primary Model:
Adjusted Covariates:
Reference Category:
Primary Effect Estimate:
Secondary Findings:
Sensitivity Analyses:
Subgroup Analyses:
Missing Data Handling:
Assumption Checks:
Tables Produced:
Supplementary Tables:
Code Verified:
================
Exit Criteria
Phase 2 is complete when:
the main analytic results are verified
the key tables needed for manuscript writing exist
model assumptions and major diagnostics have been addressed
the downstream writing phases can cite exact numbers without guessing
Transition Prompt
"Analysis complete. The manuscript now has verified quantitative results. Next is Phase 3 — Figures, if figures are needed, or we can proceed directly to writing."
Phase 3 — Figures
Function
Call the /visualize workflow and record only the outputs needed by later phases.
Entry Conditions
Begin Phase 3 if:
the manuscript would benefit from figures, and
verified analysis outputs already exist
Do not force figures if tables alone are sufficient.
Objectives
Create the figure plan and figure metadata needed for manuscript drafting.
Required Outputs
list of manuscript figures
list of supplementary figures if applicable
figure titles
figure types
figure legends or legend drafts
designation of body vs supplementary placement
State Handoff
After Phase 3, update the Manuscript Context Block with:
list of figures
figure titles
figure placement
legend text or draft legend text
Also create a structured handoff:
FIGURE HANDOFF
==============
Figure 1:
Type:
Title:
Body or Supplement:
Legend:

Figure 2:
Type:
Title:
Body or Supplement:
Legend:
==============
Exit Criteria
Phase 3 is complete when:
the set of necessary figures is defined and approved, or
the user elects to skip figure generation and this is documented
Transition Prompt
"Figures are complete or intentionally omitted. Next is Phase 4 — Introduction."
Phase 4 — Introduction
Function
Call the /write-introduction workflow using verified outputs from prior phases.
Entry Conditions
Begin Phase 4 when:
the manuscript rationale is defined sufficiently to draft an Introduction
Objectives
Write a concise, journal-style Introduction that establishes:
the clinical problem
the evidence gap
the study objective
Preferred Structure
Usually 3–4 paragraphs:
clinical burden and relevance
what is known
what remains uncertain
study objective and hypothesis, when appropriate
Adapt paragraph count if needed for topic or journal style.
Cross-Phase Requirements
The gap statement must match the verified literature handoff.
The objective must match the Manuscript Context.
References should come from the verified literature phase whenever possible.
Do not introduce uncited claims or unverified novelty statements.
State Handoff
After Phase 4, update the Manuscript Context Block with:
final Introduction word count
exact gap statement used
exact study objective statement used
references used in the Introduction
Exit Criteria
Phase 4 is complete when:
the Introduction is approved
the study objective is clearly and accurately stated
the gap statement is explicit and consistent with Phase 1
Transition Prompt
"Introduction complete. Next is Phase 5 — Methods & Results."
Phase 5 — Methods & Results
Function
Call the /write-methods-results workflow using verified analysis and figure outputs.
Entry Conditions
Begin Phase 5 when:
the study design and analytic results are sufficiently defined to support manuscript drafting
Objectives
Write a reproducible Methods section and a numerically accurate Results section.
Methods Requirements
Methods should include, as applicable:
study design
data source
study period
eligibility criteria
variable definitions
primary and secondary outcomes
exposure definition
statistical methods
missing data approach
sensitivity analyses
software used, if known
Results Requirements
Results should usually proceed in this order:
cohort derivation and analytic sample
baseline characteristics
primary analysis
secondary analyses
sensitivity analyses
subgroup analyses if applicable
Cross-Phase Requirements
Every reported estimate must match verified analysis outputs.
Results must follow the order of the verified tables and figures.
Methods must describe all analyses that appear in Results.
Results must not report analyses absent from the analysis handoff.
Tables and figures used in Results must be referenced in the text.
Rounding must follow one manuscript-wide rule.
State Handoff
After Phase 5, update the Manuscript Context Block with:
Methods word count
Results word count
limitations relevant to interpretation
robustness analyses performed, if applicable
Also create a structured handoff:
METHODS & RESULTS HANDOFF
=========================
Methods Summary:
Results Summary:
Primary Estimate in Text Form:
Secondary Estimates in Text Form:
Tables Referenced:
Figures Referenced:
Major Limitations Identified:
Robustness Analyses:
=========================
Exit Criteria
Phase 5 is complete when:
Methods are reproducible and aligned with the analysis
Results are numerically accurate and complete
tables and figures are appropriately integrated into the narrative
Transition Prompt
"Methods and Results complete. Next is Phase 6 — Discussion."
Phase 6 — Discussion
Function
Call the /write-discussion workflow using verified findings and verified literature context.
Entry Conditions
Begin Phase 6 when:
the principal findings are established
sufficient literature context exists to interpret them responsibly
Objectives
Write a balanced Discussion that:
interprets the findings
compares them with prior literature
addresses implications
acknowledges strengths and limitations
ends with a conclusion consistent with the study design
Preferred Structure
Usually 5–6 paragraphs:
principal findings
comparison with concordant literature
comparison with discordant or mixed literature
clinical or scientific implications
strengths and limitations
conclusion
Adapt structure when appropriate.
Cross-Phase Requirements
Principal findings must reflect Phase 2 results without copying the Results section verbatim.
Literature comparisons must rely on verified references from Phase 1 whenever possible.
Strengths and limitations must reflect the actual design and analyses performed.
The conclusion must close the loop with the Introduction gap statement.
No new data, analyses, or unsupported claims may be introduced.
Discussion Guardrails
Do not:
present mechanisms as fact unless supported by evidence
recommend practice change beyond what the design supports
overstate novelty
use causal language for observational associations
force concordance if the literature is sparse or conflicting
State Handoff
After Phase 6, update the Manuscript Context Block with:
Discussion word count
final conclusion statement
total references used across sections
complete reference list if assembled during workflow
Exit Criteria
Phase 6 is complete when:
the Discussion is scientifically balanced
the conclusion is consistent with the evidence and study design
the Introduction-to-Discussion loop is closed
Transition Prompt
"Discussion complete. Next is Phase 7 — Abstract."
Phase 7 — Abstract
Entry Conditions
Begin Phase 7 when:
the manuscript body is sufficiently complete to support an accurate abstract
Objectives
Write a structured abstract that stands alone and uses only verified information from the manuscript.
Preferred Structure
Unless the target journal requires otherwise, use:
Background or Objective
Methods
Results
Conclusion
Abstract Rules
Draft the abstract last.
Use only verified information from completed manuscript sections.
Every number must match the manuscript body exactly.
Do not introduce new interpretation not already supported in the Discussion.
Do not cite references in the abstract unless explicitly required by the journal.
Define abbreviations on first use if included.
Use association language for observational studies.
State Handoff
After Phase 7, update the Manuscript Context Block with:
abstract word count
final abstract text status
any journal-specific abstract adjustments needed
Exit Criteria
Phase 7 is complete when:
the abstract accurately summarizes the manuscript
all key numbers match the body text
the word count is appropriate for the intended journal or a standard surgical format
Transition Prompt
"Abstract complete. Next is Phase 8 — Final Assembly & Audit."
Phase 8 — Final Assembly & Audit
Goal
Perform a final internal consistency review and summarize the manuscript package.
Part A — Manuscript Assembly Summary
Present:
MANUSCRIPT ASSEMBLY
===================
Title:           [if available]
Abstract:        [status + word count]
Introduction:    [status + word count]
Methods:         [status + word count]
Results:         [status + word count]
Discussion:      [status + word count]
-----------------------------------------
Total body text:
References:
Tables:
Figures:
===================
Part B — Internal Consistency Audit
Check and report:
Check	Status	Details
Abstract numbers match Results	✓/✗	—
Every table referenced in text	✓/✗	—
Every figure referenced in text	✓/✗	—
Methods describes each reported analysis	✓/✗	—
No results in Methods section	✓/✗	—
No new data in Discussion	✓/✗	—
Association language appropriate to design	✓/✗	—
Introduction gap aligns with conclusion	✓/✗	—
Reference numbering or order is consistent	✓/✗	—
Abbreviations defined on first use	✓/✗	—
Part C — Reporting Guideline Audit
Select the reporting framework that best matches the study design, such as:
STROBE
CONSORT
STARD
TRIPOD
STROCSS
PRISMA
Then summarize key checklist compliance in a concise table:
Checklist Item	Section	Status	Note
Flag missing reporting elements and suggest where they should be added.
Part D — Deliverables Summary
Summarize what exists from the completed workflow, for example:
Deliverable	Status	Source Phase
Literature synthesis	Available / Missing	Phase 1
Analysis tables	Available / Missing	Phase 2
Reproducible code	Available / Missing	Phase 2
Figures	Available / Missing	Phase 3
Introduction text	Available / Missing	Phase 4
Methods text	Available / Missing	Phase 5
Results text	Available / Missing	Phase 5
Discussion text	Available / Missing	Phase 6
Abstract text	Available / Missing	Phase 7
Reference list	Available / Missing	Phases 1, 4, 6
Only claim deliverables that actually exist.
Part E — Suggested Next Steps
Provide a concise next-step plan tailored to what is complete, such as:
assemble text into the manuscript document
insert tables and figures
finalize title and author list
add disclosures, funding, and IRB language
format references for the target journal
circulate to co-authors
return for revisions after feedback
Exit Criteria
Phase 8 is complete when:
the manuscript structure is summarized
major consistency checks are reported
missing items are explicitly identified
next steps are clear
Handling Interruptions
If the session stops mid-workflow:
present the current Manuscript State Tracker
summarize what is complete
summarize what remains
state which phase should be resumed next
preserve the Manuscript Context Block as the reference state
When resuming later, reconstruct the context from:
completed phases
verified outputs
any uploaded files
any manuscript text already drafted
Do not assume continuity without restating the recovered context.
Handling Phase Skips
If the user chooses to skip a phase, respect the decision but document it and warn about downstream consequences.
Skipped Phase	Consequence
Literature Review	weaker Introduction/Discussion support unless references are manually provided
Data Analysis	no verified results for Methods/Results writing
Figures	no figure integration; text may remain table-only
Abstract	manuscript can still proceed without it
Final Assembly	no internal audit performed
Mark skipped phases as [—].
Minimum-Viable Manuscript Path
If the user wants a shortened workflow, support a reduced path using verified available components only.
Examples:

verified analysis available → draft Introduction, Methods, Results, Discussion, then Abstract
results and draft sections available → jump to Final Assembly & Audit
no figures needed → skip Phase 3 and document this
Always mark omitted phases clearly in the tracker.
Command Completion Standard
This command succeeds when it has:
identified the correct starting phase
carried verified outputs forward across phases
maintained a visible state tracker
enforced consistency across sections
avoided fabrication
produced either:
a full manuscript workflow, or
a clearly documented partial workflow based on what the user chose to complete
