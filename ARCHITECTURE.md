# Clinical Research Assistant v3.3 Architecture

> **Update history.** v3.0 introduced the router + shared-state architecture. v3.1–3.2 refactored `/analyze` and `/visualize` from monolithic executors to orchestrator-contract skills. v3.3 wired the K-Dense delegation layer (citation-management hard gate, peer-review, scholar-evaluation, pyzotero, K-Dense literature-review) — see `skills/references/kdense-delegations.md`.

## Purpose

This document defines the architecture for `clinical-research-assistant`.

The goal is to keep the plugin optimized for Bilal's personal workflow while making the internal system substantially more reliable, stateful, and capable of producing end-to-end manuscripts from heterogeneous biomedical data.

The core product decision is:

- **Clinical Research Assistant remains the primary orchestrator**
- **BioMedAgent is a delegated execution engine for omics / ML / non-tabular workflows**
- **K-Dense scientific-skills are delegated execution engines for citation / peer-review / quality-scoring / Zotero / systematic-search workflows** (v3.3)
- **The user-facing command surface remains familiar, with targeted additions where they clearly improve the workflow**

---

## Design Principles

### 1. Clinical Research Assistant stays in charge
The primary role of this repo is not generic biomedical automation. It is a high-rigor clinical research and manuscript system for one operator with a consistent workflow.

### 2. Preserve habits, upgrade internals
Existing top-level commands continue to work; v3.x has added narrowly-scoped commands where they reduce ambiguity:

- `/project-init`
- `/resume-project`
- `/literature-review`
- `/analyze`
- `/visualize`
- `/write-introduction`
- `/write-methods-results`
- `/write-discussion`
- `/write-abstract` *(v3.x — 12-principle editorial rubric, venue-specific structure)*
- `/write-manuscript`
- `/manuscript-qc` *(v3.x — 12 native checks + 3 K-Dense delegations: peer-review, ScholarEval, citation re-verification)*

New commands are added only when they reduce ambiguity or improve control.

### 3. Shared project state is mandatory
All major phases must read from and write to the same persistent project state.

### 4. Verified evidence is mandatory before narrative prose
Introduction and Discussion drafting must not proceed without a verified evidence bank and citation bank.

### 5. Semi-autonomous by default
The system should complete a major phase, then check in. It should not stop after every micro-step and should not run the entire pipeline blindly.

### 6. Multi-agent critique is a core feature, not a garnish
Every major phase should run a debate panel by default. The panel is visible to the user as a concise disagreement summary, not a full transcript.

### 7. Debate should improve quality, not create chaos
The default three-agent panel is:

- **Methodologist**
- **Skeptic Reviewer**
- **Manuscript Editor**

Default weighting:

- Methodologist > Skeptic Reviewer > Manuscript Editor

### 8. Delegation to BioMedAgent should be broad but explicit
BioMedAgent should be used for tasks outside standard clinical biostatistics, including advanced computation, non-tabular data, omics, biomedical machine learning, and execution-heavy workflows.

### 8a. K-Dense scientific-skills are delegated execution engines for citation / review / library workflows (v3.3)
Specific K-Dense skills act as runtime expert references for citation-integrity, peer-review-style audits, quantitative quality scoring, Zotero sync, and systematic-search execution. The CRA skill is the orchestrator; the K-Dense skill is the executor (the same orchestrator-contract pattern `/analyze` uses with `scientific-visualization`). All five delegations are documented as a single source of truth in `skills/references/kdense-delegations.md`:

| Delegation | K-Dense skill | Used by | Enforcement |
|---|---|---|---|
| Citation integrity (L041) | `scientific-skills:citation-management` | `/literature-review` + all `/write-*` + `/manuscript-qc` | **HARD GATE** — PASS/AMBIGUOUS/FAIL routing, no silent fallback, no "PMID: pending verification" placeholders |
| Peer-review simulation | `scientific-skills:peer-review` | `/manuscript-qc` Check 13 | Reports/peer_review_simulation_<date>.md |
| Quality scoring | `scientific-skills:scholar-evaluation` | `/literature-review` STEP 5 + `/manuscript-qc` Check 14 | Verdict = NOT READY if total < 14/20 |
| Zotero sync | `scientific-skills:pyzotero` | end of `/literature-review` + start of `/write-manuscript` | Auto-on if `ZOTERO_API_KEY` env detected, silent skip otherwise |
| Systematic search execution | `scientific-skills:literature-review` | CRA `/literature-review` STEP 2 + STEP 5 | CRA stays orchestrator (scope, schema, gap); K-Dense executes search/dedup/PRISMA |

### 9. Portability matters
The architecture should work across:

- Claude Code
- Cowork / marketplace installs
- local plugin development

### 10. Machine-readable artifacts are first-class outputs
The final product is not only a manuscript. It is also a durable research project state.

---

## System Overview

The system is organized into one orchestration layer and several specialist layers.

### A. Primary Orchestrator: Clinical Research Assistant
Responsible for:

- project intake
- study framing
- literature strategy
- evidence verification
- statistical planning
- manuscript assembly
- consistency auditing
- deciding whether to delegate sub-work to BioMedAgent

The concrete user-facing entry point is `skills/clinical-research-assistant/SKILL.md`. It reads `skills/references/skill-registry.yaml` and routes to first-party skills under `skills/internal/` or pasted support skills under `skills/external/`.

### B. Delegated Engine: BioMedAgent
Responsible for execution-heavy or modality-specific workflows such as:

- omics pipelines
- image-based biomedical analysis
- machine learning pipelines
- non-tabular file workflows
- complex multi-stage computational workflows
- advanced exploratory or custom computation beyond standard clinical biostatistics

BioMedAgent now lives inside the installable plugin at `skills/external/biomedagent/` to preserve its third-party/external provenance while still making it CRA's delegated execution engine.

### B'. Delegated K-Dense scientific-skills (v3.3)
Distinct from BioMedAgent: K-Dense scientific-skills are narrow, task-specific delegated executors loaded as **runtime expert references**. Five are formally wired today (see Design Principle 8a). Many more are vendored under `skills/external/scientific-agent-skills/scientific-skills/` and are discoverable through the router via `skill-registry.yaml`. The router promotes them when their triggers match the user's request.

### C. Shared State Layer
Persistent files that define the study and all downstream outputs.

### D. Agent Debate Layer
Runs the three-agent panel at every major phase.

### E. Audit Layer
Checks numerical, methodological, rhetorical, and structural consistency before final export.

---

## Architectural Layers

## 1. Intake and Routing Layer

### Responsibilities
- identify project status
- identify data type(s)
- identify study type
- identify target output
- select the next phase
- determine whether BioMedAgent delegation is required

### New internal concept
Every user request is mapped to a `phase_context` object with:

- current phase
- data modality
- evidence status
- analysis status
- writing status
- risk level
- whether debate is required
- whether delegation is required

---

## 2. Project State Layer

This repo should stop behaving like a set of isolated prompt files.
Each command must operate as a view over one persistent project.

Core artifacts:

- `project_state.json`
- `study_spec.json`
- `evidence_bank.json`
- `citation_bank.json`
- `analysis_plan.json`
- `dataset_profile.json`
- `results_registry.json`
- `figure_registry.json`
- `manuscript_state.json`
- `decision_log.md`

These are defined in `clinical-research-assistant/skills/references/state-schema.md` (moved from root in v3.3; root `STATE_SCHEMA.md` is now a pointer stub).

---

## 3. Evidence Layer

### Responsibilities
- literature search
- guideline retrieval
- trials search
- evidence tagging
- reference verification
- section-specific citation allocation

### Core policy
No Introduction or Discussion prose without verified evidence.

### Default evidence sources
- PubMed
- major guidelines
- ClinicalTrials.gov

Preprints and broad web sources remain allowed when necessary, but they are not the default citation backbone.

### Outputs
- `evidence_bank.json`
- `citation_bank.json`
- section tags for each reference

---

## 4. Analysis Planning Layer

This is the largest missing capability in the current repo.

### Responsibilities
- infer study archetype
- classify data modality
- inspect files before modeling
- build a prospective analysis plan before execution
- force explicit model choices and fallback logic
- define diagnostics and sensitivity analyses in advance

### Core rule
`/analyze` should not jump directly from dataset upload to modeling.
It should produce and approve an analysis plan first.

### Outputs
- `dataset_profile.json`
- `analysis_plan.json`
- updates to `study_spec.json`

---

## 5. Execution Layer

### Standard clinical biostatistics path
Handled natively by Clinical Research Assistant.
Examples:

- Table 1 generation
- logistic regression
- Cox regression
- mixed models where appropriate
- propensity methods
- diagnostics
- sensitivity analyses
- formatted analysis tables

### Delegated BioMedAgent path
Used when tasks fall outside standard clinical biostatistics.
Examples:

- omics pipelines
- advanced visualization computation
- biomedical ML
- non-tabular or multi-file workflows
- execution environments needing retries and staged debugging

### Design rule
Delegation must produce structured outputs back into the Clinical Research Assistant state layer, not a disconnected narrative.

---

## 6. Figure Layer

### Responsibilities
- convert verified results into figure candidates
- maintain one figure registry
- preserve figure-to-result traceability
- generate figure legends from structured figure objects

### Core rule
Figures should be built from `results_registry.json`, not from free-text recollection.

### Outputs
- `figure_registry.json`
- exported figure files
- legend drafts linked to figure IDs

---

## 7. Manuscript Layer

### Responsibilities
- section drafting
- section revision
- evidence-linked prose generation
- result-linked Results writing
- journal-ready exports

### Core rule
The writing system must consume structured state, not only chat context.

### Section dependencies
- Introduction requires verified citations (every reference passes `scientific-skills:citation-management` hard gate)
- Methods requires `study_spec.json` + `analysis_plan.json`
- Results requires `results_registry.json` + `figure_registry.json`
- Discussion requires `results_registry.json` + verified citation bank (comparator citations are highest fabrication risk — hard gate enforced)
- Abstract requires the body to be complete enough for consistency checking; `/write-abstract` runs the 12-principle editorial rubric and adapts to the target venue

### Owning skills
| Section | Skill |
|---|---|
| Introduction | `/write-introduction` |
| Methods + Results | `/write-methods-results` |
| Discussion | `/write-discussion` |
| Abstract | `/write-abstract` |
| Full assembly + Phase 8 audit | `/write-manuscript` |
| Pre-submission audit | `/manuscript-qc` |

---

## 8. Debate Layer

Every major phase runs a three-agent review.

### Agents

#### Methodologist
Focus:
- design correctness
- model appropriateness
- diagnostics
- bias and validity

#### Skeptic Reviewer
Focus:
- weak assumptions
- overclaiming
- novelty inflation
- alternative explanations
- audit-style attack on flaws

#### Manuscript Editor
Focus:
- clarity
- flow
- redundancy
- section logic
- user-facing usability

### Debate output format
Do not expose chain-of-thought.
Store only structured summaries:

- `recommended_action`
- `points_of_agreement`
- `key_disagreements`
- `decision_rationale`
- `unresolved_risks`

### User visibility
Show a concise disagreement summary, not the full transcript.

---

## 9. Audit Layer

Owned by `/manuscript-qc`. Runs as a final pre-submission audit, and is invoked at `/write-manuscript` Phase 8 for the assembly audit.

### Native CRA checks (12)
- numeric consistency (text ↔ tables ↔ results_registry)
- table/figure reference integrity
- abbreviation integrity
- observational language check
- claim-to-citation alignment
- reporting guideline compliance (STROBE/CONSORT/PRISMA/TRIPOD/STARD/SPIRIT/SQUIRE)
- word-count and deliverable completeness
- statistical-method correctness
- methods-results alignment
- figure-quality checks (resolution, units, comparator declaration, p-value formatting per L013, no text overlap)
- reference-list integrity (every inline [N] resolves; no duplicate PMIDs)
- abstract ↔ main-text consistency

### K-Dense delegated checks (v3.3)
- **Check 13 — Peer-review simulation** (`scientific-skills:peer-review`): reviewer-perspective structured pass; output `Reports/peer_review_simulation_<date>.md`; surfaces MAJOR comments
- **Check 14 — ScholarEval scoring** (`scientific-skills:scholar-evaluation`): 4-dimension rubric (problem/methodology/analysis/writing); halts at NOT READY if total < 14/20
- **Check 15 — Citation batch re-verification** (`scientific-skills:citation-management`): re-runs the L041 hard gate over every reference in the assembled manuscript; ANY FAIL = CRITICAL

---

## Command Strategy

### Commands to preserve
- `/literature-review`
- `/analyze`
- `/visualize`
- `/write-introduction`
- `/write-methods-results`
- `/write-discussion`
- `/write-manuscript`

### New commands recommended
- `/project-init` — explicit project creation and intake
- `/debate` — optional direct invocation of the critique panel on the current phase
- `/audit-manuscript` — run the final audit independently
- `/resume-project` — load persistent state explicitly when needed

These are optional externally, but useful for reducing ambiguity.

---

## Typical End-to-End Flow

1. `/project-init`
   - establish study scope and state files

2. `/literature-review`
   - build evidence bank and citation bank
   - run debate summary

3. `/analyze`
   - inspect data
   - create dataset profile
   - draft analysis plan
   - run debate summary
   - execute analysis or delegate to BioMedAgent
   - write results into registries

4. `/visualize`
   - propose figures from results registry
   - generate figures and legends
   - run debate summary

5. `/write-introduction`
   - draft from verified evidence bank only

6. `/write-methods-results`
   - Methods from study spec + analysis plan
   - Results from results registry + figure registry

7. `/write-discussion`
   - draft from results registry + verified citation bank
   - run debate summary

8. `/write-manuscript`
   - assemble all sections
   - run final audit
   - export documents and machine-readable artifacts

---

## Key Improvements Over Current Repo

### Current strengths to preserve
- strong clinical domain expertise
- good command names
- manuscript-oriented workflow
- strong methodological warnings
- differentiated writing-style reference

### Current weaknesses to fix
- duplicated instructions across files
- weak shared state outside manuscript orchestration
- insufficiently structured evidence-to-writing pipeline
- weak execution planning before analysis
- poor separation between skill responsibilities in some files
- limited formal delegation mechanism to BioMedAgent

---

## Non-Goals

This refactor is **not** intended to:

- make the plugin generic for all researchers
- replace clinical judgment with autonomous drafting
- turn every phase into a fully hidden black-box agent run
- force journal-specific formatting too early in the pipeline
- expose raw internal debate transcripts by default

---

## Success Criteria

The architecture succeeds if it produces:

1. a familiar command surface for Bilal
2. persistent project memory across sessions
3. verified evidence before prose
4. clearer routing between standard clinical analysis and BioMedAgent delegation
5. result-linked figures and prose
6. better final consistency and fewer fabricated or drifting claims
7. reproducible end-to-end manuscript deliverables plus machine-readable state

---

## Next Implementation Documents

This architecture is operationalized by:

- `clinical-research-assistant/skills/references/state-schema.md` (root `STATE_SCHEMA.md` is a pointer stub)
- `clinical-research-assistant/skills/references/command-contracts.md` (root `COMMAND_CONTRACTS.md` is a pointer stub)
- `clinical-research-assistant/skills/references/kdense-delegations.md` (K-Dense delegation contracts — v3.3)
- `DELEGATION_RULES.md` (BioMedAgent + K-Dense delegation policy at the root)
- `ROADMAP.md`
