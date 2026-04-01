# Roadmap

This roadmap translates the v3 architecture into an implementation sequence.

The goal of the first pass is not to rebuild the entire repo at once. It is to create a clean migration path from the current command-rich prompt system to a stateful, evidence-gated, debate-enhanced research operating system.

---

## Guiding Priorities

Implementation order should follow these priorities:

1. fix structural confusion and duplicate responsibilities
2. establish shared project state
3. gate writing on verified evidence
4. insert an analysis planning layer before execution
5. wire explicit delegation to BioMedAgent
6. make figures and prose consume structured outputs
7. add final audit and export hardening

---

## Phase 0 — Repo Triage and Cleanup

### Goals
- identify command/skill mismatches
- reduce duplication
- define one source of truth for each major responsibility

### Tasks
- audit all existing skill files for naming and routing consistency
- resolve any skill-mapping problems, especially around analysis vs visualization
- identify duplicated instruction blocks in:
  - `CLAUDE.md`
  - skill files
  - reference files
- decide what remains in:
  - top-level `CLAUDE.md`
  - skill-specific contracts
  - reference documents

### Deliverables
- clarified skill ownership map
- list of files to keep, merge, split, or deprecate

### Success condition
No major command is ambiguously mapped to the wrong skill contract.

---

## Phase 1 — Shared State Foundation

### Goals
- create persistent project memory across sessions
- make every major phase write to structured state

### Tasks
- implement creation and loading of:
  - `project_state.json`
  - `study_spec.json`
  - `manuscript_state.json`
  - `decision_log.md`
- add project initialization logic
- add resume logic
- ensure every major command reads state before acting

### Deliverables
- initial state files created automatically or via `/project-init`
- `/resume-project` behavior defined and usable

### Success condition
A user can stop and resume a project without relying on chat memory.

---

## Phase 2 — Evidence and Citation Layer

### Goals
- make verified evidence mandatory for narrative prose
- create durable literature artifacts

### Tasks
- implement `evidence_bank.json`
- implement `citation_bank.json`
- update `/literature-review` to populate both
- define source priority:
  - PubMed
  - major guidelines
  - ClinicalTrials.gov
- define verification rules
- prevent `/write-introduction` and `/write-discussion` from running without a citation bank

### Deliverables
- machine-readable evidence bank
- machine-readable citation bank
- evidence-gated writing commands

### Success condition
Introduction and Discussion can only be drafted from verified references.

---

## Phase 3 — Analysis Planning Layer

### Goals
- force an approved plan before execution
- improve method selection and reliability

### Tasks
- implement `dataset_profile.json`
- implement `analysis_plan.json`
- add file inspection logic before modeling
- add study archetype classification
- add explicit decision logic for:
  - primary model
  - missing data strategy
  - diagnostics
  - sensitivity analyses
- update `/analyze` to pause at the phase level after plan generation

### Deliverables
- structured dataset profile
- structured analysis plan
- plan-first `/analyze` workflow

### Success condition
The repo no longer jumps directly from uploaded files to final models.

---

## Phase 4 — Debate Layer

### Goals
- introduce structured adversarial improvement across all major phases
- keep the output concise and useful

### Tasks
- define the three-agent panel:
  - methodologist
  - skeptic reviewer
  - manuscript editor
- implement debate summaries for:
  - literature review
  - analysis plan
  - execution results interpretation
  - figure selection
  - discussion drafting
  - final manuscript audit
- store only structured debate summaries, not raw transcripts
- apply default weighting:
  - methodologist > skeptic reviewer > manuscript editor

### Deliverables
- reusable debate template
- debate summaries written to state and decision log

### Success condition
Every major phase gets a quality-improvement pass without overwhelming the user.

---

## Phase 5 — BioMedAgent Delegation Wiring

### Goals
- make delegation explicit, auditable, and useful
- keep Clinical Research Assistant as orchestrator

### Tasks
- implement delegation trigger logic using `DELEGATION_RULES.md`
- define minimum return object requirements from BioMedAgent
- write delegation history into `project_state.json`
- make `/analyze` capable of routing computational sub-work to BioMedAgent
- normalize delegated outputs into:
  - `dataset_profile.json`
  - `analysis_plan.json`
  - `results_registry.json`
  - `figure_registry.json` if relevant

### Deliverables
- explicit delegation handshake
- state-normalized returns from BioMedAgent

### Success condition
Delegated work cleanly re-enters the manuscript pipeline.

---

## Phase 6 — Structured Result and Figure Registries

### Goals
- make numeric and figure truth persistent and reusable
- eliminate prose drift from analytic outputs

### Tasks
- implement `results_registry.json`
- implement `figure_registry.json`
- update `/analyze` to write final result objects
- update `/visualize` to read from `results_registry.json`
- update figure legend generation to use figure objects rather than chat memory

### Deliverables
- canonical result registry
- canonical figure registry

### Success condition
Methods/Results text and figures can be generated from structured state rather than recollection.

---

## Phase 7 — Writing Layer Refactor

### Goals
- make writing commands state-driven
- keep Bilal's house style while reducing overfit and duplication

### Tasks
- update `/write-introduction` to use citation bank only
- update `/write-methods-results` to use:
  - `study_spec.json`
  - `analysis_plan.json`
  - `results_registry.json`
  - `figure_registry.json`
- update `/write-discussion` to use:
  - `results_registry.json`
  - `citation_bank.json`
- separate style concerns into cleaner layers if needed:
  - house style
  - section rules
  - journal-conversion rules for future phases

### Deliverables
- state-driven writing commands
- reduced duplication of writing instructions

### Success condition
Narrative prose is grounded in structured evidence and results.

---

## Phase 8 — Final Assembly and Audit Hardening

### Goals
- make final manuscript export dependable
- catch inconsistencies before output

### Tasks
- implement independent `/audit-manuscript`
- add final audit checks for:
  - numeric consistency
  - table/figure reference integrity
  - abbreviation integrity
  - claim-to-citation alignment
  - observational language compliance
  - reporting guideline checks
- make `/write-manuscript` consume all state files and assemble final deliverables
- export defaults:
  - manuscript `.docx`
  - tables `.docx`
  - figures `.docx`
  - abstract `.docx`
  - analysis `.xlsx`
  - machine-readable project artifacts

### Deliverables
- reliable final assembly
- explicit audit summary

### Success condition
The plugin can produce a full manuscript package plus project-state artifacts with fewer silent inconsistencies.

---

## Phase 9 — Benchmarking and Validation

### Goals
- test the architecture against Bilal's actual use cases
- prevent regression after future edits

### Suggested benchmark project types
- retrospective surgical cohort with binary outcome
- registry study with time-to-event outcome
- propensity score treatment comparison
- biomarker + ROC + cutoff project
- omics project requiring BioMedAgent delegation
- trauma or acute care outcomes manuscript
- transplant outcomes manuscript

### Tasks
- define test cases
- define expected outputs
- define common failure cases
- document where the pipeline still breaks

### Deliverables
- benchmark suite specification
- regression testing checklist

### Success condition
Changes can be evaluated against real workflows rather than only intuition.

---

## Immediate Next Actions

The next implementation work should start with these concrete moves:

1. audit current skill wiring and resolve `analyze` vs `visualize` ambiguity
2. add the core state files and `/project-init` + `/resume-project`
3. update `/literature-review` to build evidence and citation banks
4. update `/analyze` to create `dataset_profile.json` and `analysis_plan.json` before execution
5. wire the debate layer into literature review and analysis planning first

These five steps create the foundation for everything else.

---

## What Not to Do Yet

Do not start by:
- rewriting every skill prompt in one pass
- making the system fully autonomous end to end
- overcomplicating journal-specific formatting early
- adding more agents before the three-agent panel works well
- building benchmark automation before the state layer exists

---

## Definition of “First Major Milestone”

The first major milestone is reached when the repo can do this reliably:

1. initialize a project
2. perform literature review into a verified citation bank
3. inspect a dataset and produce an approved analysis plan
4. run native or delegated execution as appropriate
5. write grounded Methods/Results and a citation-backed Introduction/Discussion
6. export a manuscript package plus machine-readable state

That milestone is the minimum viable v3 system.
