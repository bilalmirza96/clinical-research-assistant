# Delegation Rules

This document defines when and how `clinical-research-assistant` delegates work to its two execution engine layers:

1. **BioMedAgent** — for execution-heavy modality-specific workflows (omics, ML, non-tabular)
2. **K-Dense scientific-skills** — for citation integrity, peer-review-style audits, quality scoring, Zotero sync, and systematic-search execution (v3.3+)
3. **science-superpowers** — the RIGOR layer: pre-registration, inline result verification, red-team review, anomaly root-cause (v3.8+; see §E and `skills/internal/analyze/references/sp-integration.md`)

The core rule is the same for both:

- **Clinical Research Assistant is always the primary orchestrator**
- **The delegated engine is a runtime executor, not the manuscript authority**
- **Delegation is broad, but it is never invisible — the contract for each delegation is logged**

K-Dense delegations are defined as a single source of truth in `skills/references/kdense-delegations.md`. This file documents the BioMedAgent rules and points at `kdense-delegations.md` for the K-Dense layer.

---

## Primary Principle

Clinical Research Assistant owns:
- project framing
- evidence verification (with `scientific-skills:citation-management` as the hard-gate enforcer)
- analysis planning
- manuscript logic
- final synthesis
- final audit (with `scientific-skills:peer-review` + `scientific-skills:scholar-evaluation` as delegated review steps in `/manuscript-qc`)

BioMedAgent may own:
- execution-heavy sub-work
- modality-specific pipelines
- complex computational workflows outside standard clinical biostatistics

K-Dense scientific-skills may own:
- citation lookup + DOI/PMID verification (`citation-management`)
- reviewer-perspective structured audits (`peer-review`)
- quantitative quality scoring (`scholar-evaluation`)
- Zotero library sync (`pyzotero`)
- multi-database systematic search execution (K-Dense `literature-review`)

Neither BioMedAgent nor any K-Dense skill becomes the final manuscript authority. CRA stays in charge of the verdict.

---

## Default Delegation Policy

Per project requirements, the default rule is:

> Delegate to BioMedAgent for anything outside standard clinical biostatistics, including advanced visualization computation and exploratory or execution-heavy computation.

This corresponds to a broad delegation policy, but the orchestrator still decides when delegation is appropriate.

---

## Native vs Delegated Boundaries

## A. Native Clinical Research Assistant Scope

Keep work native when the task is standard clinical research analysis or manuscript work.

### Native examples
- literature review and gap analysis
- evidence bank creation
- citation verification
- standard Table 1 generation
- logistic, linear, and Cox regression
- standard diagnostics
- propensity score workflows
- sensitivity analyses common to observational surgical research
- figure planning from structured results
- Introduction, Methods, Results, Discussion, Abstract drafting
- manuscript assembly and audit

---

## B. BioMedAgent Delegation Scope

Delegate when the task is execution-heavy, non-tabular, or requires workflow machinery that exceeds normal clinical biostatistics.

### Delegate by default for

#### 1. Omics / genomics / transcriptomics
Examples:
- RNA-seq
- single-cell RNA-seq
- bulk differential expression
- variant analysis
- pathway enrichment
- WGCNA
- microarray preprocessing
- methylation workflows

#### 2. Biomedical machine learning
Examples:
- classification pipelines
- regression pipelines with feature engineering
- clustering workflows
- association rule mining
- deep learning or segmentation
- model benchmarking across multiple algorithms

#### 3. Non-tabular or complex file workflows
Examples:
- FASTQ, BAM, VCF, GTF, GFF
- h5ad, loom, CEL
- archives requiring staged extraction and parsing
- multimodal input bundles

#### 4. Advanced computational visualization workflows
Examples:
- data-intensive custom plots not easily served by the standard figure layer
- exploratory visual analytics requiring complex preprocessing
- omics-linked figure computation

#### 5. Multi-stage execution/debug loops
Examples:
- tasks requiring repeated retries
- environment/package dependency handling
- staged workflow redesign after failure

---

## C. Usually Native, but Delegatable When Complex

These tasks should stay native unless complexity justifies delegation.

Examples:
- survival analysis with standard tabular cohorts
- standard ROC/forest/KM figure work
- standard registry cohort analysis
- simple predictive models for tabular data

The orchestrator should delegate only when the execution burden, data modality, or workflow complexity is high enough to justify it.

---

## D. K-Dense scientific-skills (v3.3)

A narrow set of K-Dense skills act as runtime expert references — CRA loads their `SKILL.md` at runtime and uses their documented tools to execute a specific contract.

**Full delegation contract:** see `skills/references/kdense-delegations.md` (single source of truth — 319 lines covering invocation order, file-write contract, and combined runtime patterns).

| K-Dense skill | Used by | Mandatory? |
|---|---|---|
| `scientific-skills:citation-management` | `/literature-review` + all `/write-*` + `/manuscript-qc` | **Yes — hard gate per L041** |
| `scientific-skills:peer-review` | `/manuscript-qc` Check 13 | Yes |
| `scientific-skills:scholar-evaluation` | `/literature-review` STEP 5 + `/manuscript-qc` Check 14 | Yes (NOT READY if total < 14/20) |
| `scientific-skills:pyzotero` | `/literature-review` closure + `/write-manuscript` Phase 1 | Auto-on if `ZOTERO_API_KEY` env detected |
| `scientific-skills:literature-review` | CRA `/literature-review` STEP 2 + STEP 5 | Preferred execution backbone |

The K-Dense delegation layer is **always invisible-but-logged**, just like BioMedAgent delegation: every PASS/AMBIGUOUS/FAIL routing decision lands in `decision_log.md`, every Zotero sync result is logged, every audit report is written under `Reports/`.

Many additional K-Dense skills are vendored at `skills/external/scientific-agent-skills/scientific-skills/` (151 total skills as of v3.3). The router promotes them through `skill-registry.yaml` when their triggers match the user's request.

---

## Trigger Matrix

Use this logic during `/analyze` and related execution commands.

| Condition | Delegate to BioMedAgent? | Notes |
|---|---|---|
| Standard clinical Excel/CSV cohort, conventional regression | Usually no | Native path preferred |
| Standard registry export, conventional models | Usually no | Native unless execution becomes complex |
| Omics or sequencing files present | Yes | Default delegated |
| Non-tabular biomedical files present | Yes | Default delegated |
| Biomedical ML explicitly requested | Yes | Default delegated |
| Multi-stage environment-dependent pipeline needed | Yes | Default delegated |
| Advanced exploratory computation beyond standard stats | Yes | Default delegated |
| Figure generation from normal result registry only | Usually no | Native figure layer |
| Figure generation requiring complex computational preprocessing | Yes | Delegate compute, keep final figure registry native |

---

## Delegation Decision Fields

When delegation occurs, the orchestrator should record:

```json
{
  "delegation_id": "del_001",
  "phase": "analysis_execution",
  "delegate": "biomedagent",
  "trigger": "omics_pipeline",
  "reason": "Uploaded files include h5ad and gene-level count matrices requiring workflow design and execution-heavy processing.",
  "requested_outputs": [
    "updated dataset profile",
    "structured results",
    "artifact file paths",
    "execution notes"
  ],
  "status": "completed"
}
```

This should be stored in `project_state.json`.

---

## Required Delegation Workflow

When the orchestrator decides to delegate, it must follow this sequence.

### Step 1: classify the reason for delegation
Examples:
- `omics_pipeline`
- `biomedical_ml`
- `non_tabular_biomedical_files`
- `advanced_computational_visualization`
- `execution_heavy_multistage_pipeline`

### Step 2: define the subtask contract
The delegated subtask must specify:
- goal
- input files
- required outputs
- expected machine-readable return objects
- expected artifact file paths

### Step 3: pass only the needed context
BioMedAgent should receive:
- relevant study context
- file context
- analysis aim
- output requirements

It should not be given the entire manuscript problem when only a computational subtask is needed.

### Step 4: receive structured outputs back
BioMedAgent must return outputs that can be inserted into the Clinical Research Assistant state layer.

### Step 5: normalize returns into project state
Update:
- `dataset_profile.json`
- `analysis_plan.json` if needed
- `results_registry.json`
- `figure_registry.json` if relevant
- `decision_log.md`
- `project_state.json`

### Step 6: resume orchestration in Clinical Research Assistant
The orchestrator remains responsible for:
- interpreting delegated outputs in clinical context
- writing manuscript text
- auditing claims and citations

---

## Return Object Requirements

A BioMedAgent run is not considered valid unless it returns structured outputs.

### Minimum required return set
- execution summary
- artifact file paths
- any computed result tables in machine-readable form
- analysis metadata
- warnings and unresolved risks

### Preferred return object

```json
{
  "delegate": "biomedagent",
  "task_type": "omics_pipeline",
  "status": "completed",
  "artifacts": [
    {
      "type": "table",
      "path": "results/deseq2_results.csv"
    },
    {
      "type": "figure",
      "path": "results/volcano_plot.pdf"
    }
  ],
  "structured_results": [],
  "warnings": [],
  "notes": ""
}
```

### Prohibited return style
BioMedAgent must not return only a free-text summary with no structured result objects.

---

## Multi-Agent Debate and Delegation

Delegation should also be reviewed by the debate panel.

### Methodologist asks
- Is delegation justified by modality or complexity?
- Is the delegated plan still methodologically appropriate for the study question?

### Skeptic Reviewer asks
- Is delegation being used to hide uncertainty or weak planning?
- Are the outputs auditable and interpretable?

### Manuscript Editor asks
- Will the delegated outputs integrate cleanly into writing and final assembly?

If disagreement remains, the default weighting is:
- methodologist
- skeptic reviewer
- manuscript editor

---

## Delegation Guardrails

### 1. No citation delegation authority
BioMedAgent may surface references during computational work, but it does not control the verified citation bank.

### 2. No final manuscript authority
BioMedAgent may generate summaries or execution reports, but final manuscript prose remains owned by Clinical Research Assistant.

### 3. No hidden model drift
If BioMedAgent changes the analysis path materially, that change must be written into:
- `analysis_plan.json`
- `decision_log.md`

### 4. No silent execution-only interpretation
Clinical interpretation of delegated outputs must happen in the orchestrator layer.

---

## Examples

## Example 1: Standard NSQIP cohort
- files: CSV + dictionary
- task: logistic regression for SSI
- decision: native
- rationale: standard clinical biostatistics

## Example 2: Bulk RNA-seq with manuscript goal
- files: counts matrix + metadata
- task: differential expression + enrichment + manuscript
- decision: delegate computational analysis to BioMedAgent
- orchestrator retains evidence, framing, writing, and final synthesis

## Example 3: Multimodal exploratory ML pipeline
- files: tabular cohort plus derived imaging features
- task: predictive modeling with model comparison
- decision: delegate execution-heavy ML component to BioMedAgent
- orchestrator retains study framing, interpretation, and manuscript writing

## Example 4: Standard Kaplan-Meier and forest plot from final results
- files: existing analysis results
- task: figure package for manuscript
- decision: native, unless figure generation requires complex upstream computation

---

## Future Enhancements

Later versions may define a dedicated delegation manifest file such as `delegation_registry.json`.
For the first implementation pass, storing delegation history in `project_state.json` is sufficient.

---

## Bottom Line

The orchestrator should ask one question:

> Is this problem still a standard clinical research task, or has it become a specialized computational workflow?

If it is still standard clinical research, stay native.
If it becomes specialized, execution-heavy, or modality-specific, delegate to BioMedAgent — then pull the outputs back into the Clinical Research Assistant state layer and continue the manuscript pipeline from there.


---

## E. science-superpowers (rigor layer) + three-layer delegation (added 2026-05-30, v3.8)

**Principle — maximal delegation to the specialized, validated layers; CRA stays the brain.** Delegate execution and rigor to validated tools as much as possible. CRA orchestrates (decides WHAT/WHEN, owns clinical judgment, halts, reporting) and never freelances statistics from memory.

**Three layers**
1. **Rigor — `science-superpowers`.** `preregistering-analysis` (freeze predictions + decision rules + confirmatory/exploratory split before outcomes), `verifying-results-before-claiming` (inline, at every checkpoint), `requesting-red-team-review` (one adversarial reviewer), `investigating-anomalous-results` (root-cause).
2. **Orchestration — CRA.** `/analyze` + `/write-*` + `/visualize` + `/literature-review` + `/manuscript-qc` + `/project-init`.
3. **Execution — K-Dense `scientific-skills` + `biomedagent`.** Standard tabular biostatistics runs natively in CRA against the relevant `scientific-skills:*` reference loaded at runtime; omics/ML/non-tabular → `biomedagent`.

**Audit delegation (replaces the old 9-agent panels).** Inline `verifying-results-before-claiming` at Checkpoints A/B covers numerical/reproducibility/completeness; the single `requesting-red-team-review` (briefed by `analyze/references/red-team-brief.md`) covers statistical + biological-plausibility scrutiny. Full map: `analyze/references/sp-integration.md`.

**Category-error guard.** K-Dense `scientific-skills` are expert library references, not a no-code engine — using them still produces (governed) Python. Validation lives in the rigor + orchestration layers, not in raw library access.

**Bootstrap precedence.** For clinical-research analysis, CRA `/analyze` is the entry orchestrator and invokes the SP rigor skills at defined points; SP's framing/surveying/designing/reporting and the generic `superpowers` bootstrap are suppressed for clinical tasks. See `analyze/references/sp-integration.md`.
