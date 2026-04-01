# Command Contracts

This document defines the command behavior for Clinical Research Assistant v3.

The external command surface should remain familiar, but each command must operate against persistent shared state and must follow a clear contract.

---

## Global Command Rules

These rules apply to every major command.

### 1. Every command reads project state first
At minimum:
- `project_state.json`
- `study_spec.json`
- `manuscript_state.json`

If relevant, also read:
- `evidence_bank.json`
- `citation_bank.json`
- `analysis_plan.json`
- `results_registry.json`
- `figure_registry.json`

### 2. Every command writes state before exit
A command is not complete unless it updates the relevant machine-readable artifacts.

### 3. Every major command runs the debate layer
Default panel:
- methodologist
- skeptic reviewer
- manuscript editor

The user should see a concise disagreement summary and the synthesized recommendation.

### 4. Phase-level autonomy only
Commands should complete a major phase, then check in with the user.
They should not pause after every micro-step and should not silently run the full pipeline unless the command is explicitly defined to do so.

### 5. Verified evidence is mandatory for narrative prose
`/write-introduction` and `/write-discussion` must halt if no valid citation bank exists.

### 6. Delegation to BioMedAgent must be explicit and logged
If delegation happens:
- write the reason into project state
- record the delegated subtask
- convert the return objects into the Clinical Research Assistant shared state

---

## `/project-init`

### Purpose
Create or initialize a project and establish the shared state files.

### When to use
- new study
- new manuscript project
- when starting from a dataset or question without project files

### Inputs
- research question
- study design if known
- data source if known
- target output
- current project status

### Required reads
None if project is new. If files already exist, read all existing state first.

### Required writes
- `project_state.json`
- `study_spec.json`
- `manuscript_state.json`
- `decision_log.md`

### Output
- project summary
- inferred starting phase
- any missing required information

---

## `/resume-project`

### Purpose
Resume from persistent state instead of rebuilding context from chat memory.

### Required reads
All existing state files.

### Required writes
- `project_state.json` updated with resume timestamp
- `decision_log.md` resume entry

### Output
- current project status
- next required phase
- blockers or missing files

---

## `/literature-review`

### Purpose
Build the evidence layer for a study and prepare verified citations for downstream writing.

### Inputs
- research question
- scope modifiers
- target journal if known
- disease / procedure / population specifics

### Required reads
- `project_state.json`
- `study_spec.json`
- existing `evidence_bank.json` if present
- existing `citation_bank.json` if present

### Workflow contract
1. confirm or refine the scope
2. perform evidence search using default sources:
   - PubMed
   - major guidelines
   - ClinicalTrials.gov
3. build/update `evidence_bank.json`
4. construct `citation_bank.json` from verified evidence only
5. run debate summary
6. update state

### Required writes
- `evidence_bank.json`
- `citation_bank.json`
- `project_state.json`
- `decision_log.md`

### Must not do
- draft full Introduction prose unless explicitly invoked through a writing command
- fabricate or guess citations

### Completion condition
Evidence bank exists, citation bank exists, and project state marks evidence as complete enough for writing.

---

## `/analyze`

### Purpose
Plan and execute the study analysis, either natively or through BioMedAgent delegation.

### Inputs
- uploaded dataset(s)
- data dictionary if available
- study objective
- primary outcome
- primary exposure
- covariates / model expectations if known

### Required reads
- `project_state.json`
- `study_spec.json`
- `dataset_profile.json` if present
- `analysis_plan.json` if present
- `decision_log.md`

### Workflow contract
1. inspect the files and build/update `dataset_profile.json`
2. classify the analysis archetype
3. decide whether BioMedAgent delegation is required
4. produce or revise `analysis_plan.json`
5. run debate on the analysis plan
6. get phase-level approval
7. execute the analysis
8. write structured results into `results_registry.json`
9. generate/export analysis tables
10. update state

### Required writes
- `dataset_profile.json`
- `analysis_plan.json`
- `results_registry.json`
- `project_state.json`
- `decision_log.md`
- analysis deliverables such as `.xlsx`

### Native analysis scope
Default native scope includes standard clinical biostatistics such as:
- descriptive tables
- logistic regression
- linear regression
- Cox regression
- propensity score workflows
- diagnostics
- sensitivity analyses

### Delegated scope
If delegation is triggered, BioMedAgent may handle execution-heavy or modality-specific sub-work, but the command must still return structured results into the Clinical Research Assistant state layer.

### Must not do
- skip the planning stage
- run final models without writing an analysis plan
- write narrative Results prose
- create manuscript figures unless explicitly requested through `/visualize`

### Completion condition
Approved analysis plan exists, results registry exists, and analysis state is updated.

---

## `/visualize`

### Purpose
Generate figures from verified results.

### Inputs
- specific requested figure type, or figure package generation request

### Required reads
- `project_state.json`
- `results_registry.json`
- `figure_registry.json` if present
- `study_spec.json`

### Workflow contract
1. propose figure set from `results_registry.json`
2. build or update `figure_registry.json`
3. run debate on figure selection and figure messaging
4. generate figures one phase at a time
5. draft legends linked to figure objects
6. update state

### Required writes
- `figure_registry.json`
- exported figure files
- `project_state.json`
- `decision_log.md`

### Must not do
- invent figures from chat memory when no structured results exist
- disconnect figure legends from the source result objects

### Completion condition
Figure registry updated and generated figures linked to result IDs.

---

## `/write-introduction`

### Purpose
Write the Introduction using the verified evidence layer.

### Required reads
- `project_state.json`
- `study_spec.json`
- `evidence_bank.json`
- `citation_bank.json`
- `manuscript_state.json`

### Workflow contract
1. verify citation bank exists
2. identify burden, what-is-known, what-is-unknown, gap, and aim claims
3. map each claim to verified citation IDs
4. run debate on framing and novelty language
5. draft the Introduction
6. update manuscript state

### Required writes
- `manuscript_state.json`
- optional manuscript text artifacts
- `decision_log.md`

### Must not do
- write narrative prose without a verified citation bank
- use uncited novelty claims

### Completion condition
Introduction drafted and manuscript state updated.

---

## `/write-methods-results`

### Purpose
Write Methods and Results from structured study and analysis state.

### Required reads
- `study_spec.json`
- `analysis_plan.json`
- `results_registry.json`
- `figure_registry.json` if present
- `manuscript_state.json`

### Workflow contract
1. draft Methods from `study_spec.json` + `analysis_plan.json`
2. draft Results from `results_registry.json`
3. reference tables and figures from registries
4. run debate on methodological clarity and claim wording
5. update manuscript state

### Required writes
- `manuscript_state.json`
- manuscript text artifacts
- `decision_log.md`

### Must not do
- invent numbers from memory
- report results not present in the registry
- use causal language for observational studies

### Completion condition
Methods and Results drafted with table and figure traceability intact.

---

## `/write-discussion`

### Purpose
Write the Discussion from structured results plus verified literature context.

### Required reads
- `results_registry.json`
- `evidence_bank.json`
- `citation_bank.json`
- `study_spec.json`
- `manuscript_state.json`

### Workflow contract
1. verify citation bank exists
2. identify the principal findings from the results registry
3. map comparisons and interpretation to verified sources
4. run debate on overclaiming, interpretation, and clinical significance
5. draft the Discussion
6. update manuscript state

### Required writes
- `manuscript_state.json`
- manuscript text artifacts
- `decision_log.md`

### Must not do
- write Discussion prose without verified evidence
- import new data claims not present in the results registry
- overstate causality or novelty

### Completion condition
Discussion drafted and manuscript state updated.

---

## `/write-manuscript`

### Purpose
Orchestrate assembly of the full manuscript and perform final audit.

### Required reads
All major state files:
- `project_state.json`
- `study_spec.json`
- `evidence_bank.json`
- `citation_bank.json`
- `analysis_plan.json`
- `results_registry.json`
- `figure_registry.json`
- `manuscript_state.json`
- `decision_log.md`

### Workflow contract
1. inspect project completeness
2. determine missing sections
3. invoke or synthesize required section workflows
4. assemble manuscript structure
5. run final debate and final audit
6. export final deliverables
7. update state

### Required writes
- `manuscript_state.json`
- exported `.docx` files
- exported `.xlsx` files if relevant
- final machine-readable project artifacts
- `project_state.json`
- `decision_log.md`

### Final export defaults
- manuscript `.docx`
- tables `.docx`
- figures `.docx`
- abstract `.docx`
- analysis `.xlsx`
- machine-readable state files

### Must not do
- claim full manuscript completion if key sections or audits are missing
- produce final Discussion or Introduction if verified citation requirements are unmet

### Completion condition
Final deliverables exist and project state marks final assembly complete.

---

## `/debate`

### Purpose
Run the three-agent critique layer independently on the current phase or a specified artifact.

### Required reads
Depends on target artifact or phase.

### Required writes
- debate summary entry in `project_state.json` or future dedicated debate file
- `decision_log.md`

### Output
- points of agreement
- key disagreements
- recommended action
- unresolved risks

### Must not do
- expose internal chain-of-thought
- replace the need for state updates in the main command

---

## `/audit-manuscript`

### Purpose
Run the final consistency and reporting audit independently.

### Required reads
- `study_spec.json`
- `citation_bank.json`
- `results_registry.json`
- `figure_registry.json`
- `manuscript_state.json`
- manuscript text artifacts if available

### Audit scope
- numeric consistency
- table/figure reference integrity
- abbreviation integrity
- observational language check
- claim-to-citation alignment
- reporting guideline compliance
- deliverable completeness

### Required writes
- audit summary into `project_state.json`
- `decision_log.md`
- optional future `audit_report.json`

---

## Command Dependency Rules

### Evidence-gated commands
These require a valid citation bank:
- `/write-introduction`
- `/write-discussion`
- the narrative portions of `/write-manuscript`

### Analysis-gated commands
These require valid structured results:
- `/visualize`
- Results portion of `/write-methods-results`
- final assembly in `/write-manuscript`

### Figure-gated behavior
Figures are optional for some projects, but if figures are referenced in prose they must exist in the figure registry.

---

## Failure Behavior

If a command cannot safely proceed, it should:
1. explain what prerequisite is missing
2. update state to `blocked`
3. propose the next correct command or missing artifact

It should not silently proceed with guessed state.

---

## Future Command Changes

New commands may be added later, but any new command must:
- declare required reads
- declare required writes
- declare whether debate is mandatory
- declare whether BioMedAgent delegation is allowed
- specify completion conditions
