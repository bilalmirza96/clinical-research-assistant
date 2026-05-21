# Roadmap

This roadmap translates the v3 architecture into an implementation sequence.

The goal of the first pass is not to rebuild the entire repo at once. It is to create a clean migration path from the current command-rich prompt system to a stateful, evidence-gated, debate-enhanced research operating system.

## Status snapshot (2026-05-20)

| Phase | Status |
|---|---|
| Phase 0 — Repo triage and cleanup | ✅ Complete (2026-04-01) |
| Phase 1 — Shared state foundation | ✅ Complete (2026-04-01) |
| Phase 2 — Evidence and citation layer | ✅ Complete |
| Phase 3 — Analysis planning layer | ✅ Complete (refactored to orchestrator-contract in v3.1) |
| Phase 4 — Debate layer | ✅ Complete (multi-agent critique panels in `/analyze` references) |
| Phase 5 — BioMedAgent delegation wiring | ✅ Complete |
| Phase 6 — Structured result and figure registries | ✅ Complete (figure registry + visualize refactor v3.2) |
| **Phase 7 — Writing layer refactor** | ⏳ Pending (planned below) |
| **Phase 8 — Audit tooling + validators** | ⏳ Pending (planned below) |
| **Phase 9 — Real-world stress test** | ⏳ Pending |

In addition to the original 7 phases, v3.3 added the K-Dense delegation layer (citation-management hard gate, peer-review, scholar-evaluation, pyzotero auto-sync, K-Dense systematic-search backbone) — see `skills/references/kdense-delegations.md`.

---

## Guiding Priorities

Implementation order should follow these priorities:

1. fix structural confusion and duplicate responsibilities ✅
2. establish shared project state ✅
3. gate writing on verified evidence ✅
4. insert an analysis planning layer before execution ✅
5. wire explicit delegation to BioMedAgent ✅
6. make figures and prose consume structured outputs ✅
7. add final audit and export hardening — *in progress (Phase 7 + 8)*

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

## Phase 7 — Writing Layer Refactor (UPDATED 2026-05-20)

### Goals
- apply the orchestrator-contract pattern (already proven in `/analyze` v3.1 and `/visualize` v3.2) to the four write-* skills
- eliminate ~600 lines of duplicated state-management blocks across `/write-introduction`, `/write-discussion`, `/write-methods-results`, `/write-manuscript`
- preserve Bilal's house style + the K-Dense citation hard gate
- shrink each write-* SKILL.md by ~40% without behavior loss

### State of play (pre-refactor)
| Skill | Current size | Target size after refactor |
|---|---|---|
| `/write-introduction` | 437 lines | ≤ 280 |
| `/write-discussion` | 631 lines | ≤ 380 |
| `/write-methods-results` | 552 lines | ≤ 330 |
| `/write-manuscript` | 516 lines | ≤ 320 |
| `/write-abstract` | 247 lines | leave as-is (recent, focused) |

### Tasks
1. **Create `skills/references/manuscript-state-schema.md`** — single source of truth for the Mode A / Mode B / state read-write blocks duplicated across four write-* skills. Documents:
   - Stateful-vs-standalone mode detection
   - All read-from / write-to contracts per state file
   - Citation-bank entry schema
   - manuscript_state.json section status enums
2. **Refactor each write-* SKILL.md** to read this file at PREREQUISITE instead of inlining state schemas. Keep only:
   - The skill's drafting rubric (paragraph structure, voice, transitions)
   - The skill-specific writing-style rules
   - The skill-specific citation-bank tag filter
   - Pointers to the shared schema for everything else
3. **Verify behavior unchanged** — manual pass against a real project's state files.

### Deliverables
- `skills/references/manuscript-state-schema.md` (~250 lines, shared)
- four refactored write-* SKILL.md files (~600 lines cut total)
- per-skill diff review before commit

### Success condition
- All write-* skills reduced to target sizes
- Citation hard gate still enforced
- No behavior change in a real-project dry-run

---

## Phase 8 — Audit Tooling + Validators (NEW)

### Goals
- automate the validation checks I currently run by hand at every commit
- catch drift between `lessons-log.json`, `kdense-delegations.md`, `skill-registry.yaml`, and the actual skill files

### Tasks
1. **`tools/validate_lessons_log.py`** — JSON validity + every `promoted_to` path exists + every `id` is unique + dates well-formed
2. **`tools/audit_kdense_delegations.py`** — every K-Dense skill referenced in `kdense-delegations.md` exists under `skills/external/`; every internal skill that mentions a K-Dense skill in its PREREQUISITE actually has that skill indexed
3. **`tools/audit_state_schema.py`** — every state file referenced in the write-* PREREQUISITEs matches `skills/references/state-schema.md` (after Phase B5 move)
4. **`tools/audit_all.sh`** — single entry point that runs all validators + the indexer in dry-run mode; exits non-zero on any failure
5. **(optional)** add a `.git/hooks/pre-commit` hook that runs `tools/audit_all.sh`

### Deliverables
- 3 validator scripts in `tools/`
- one composite runner
- regression catch on next commit

### Success condition
Running `bash tools/audit_all.sh` on the current tree exits 0; introducing a stale `promoted_to` path or a missing K-Dense reference exits non-zero with a clear error.

---

## Phase 9 — Real-world stress test + Benchmarking

### Goals
- run the assembled v3.3 system against a real project (e.g., NSQIP CR-POPF or a fresh question) end-to-end
- catch what doesn't actually work in practice — vs what looks fine on paper
- only then do further refactor work

### Tasks
- pick one real project; run `/project-init` → `/literature-review` → `/analyze` → `/visualize` → `/write-*` → `/manuscript-qc`
- log every halt that surprised the user; log every hard-gate fail; log every behavior that contradicted SKILL.md
- decide whether to address findings now (small edits) or batch them into the next refactor pass

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
