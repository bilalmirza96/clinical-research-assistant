# Clinical Research Assistant — Plugin for Claude Code

A personal end-to-end clinical research and manuscript system for Claude Code. Guides the full research pipeline — literature review, statistical analysis, figure generation, and manuscript writing — with shared state across sessions, verified citations, numeric cross-verification, and publication-ready outputs.

## Architecture

**Clinical Research Assistant** is the primary orchestrator and user-facing router. You can invoke CRA once, and it selects the best internal workflow skill, delegated engine, or pasted external skill.

**BioMedAgent** is an external delegated execution engine, called only when the task exceeds standard clinical biostatistics — omics, genomics, biomedical ML, or execution-heavy computational workflows.

All commands share a persistent state layer (`project_state.json`, `results_registry.json`, `citation_bank.json`, etc.) that enables cross-session continuity and cross-command data flow.

## Commands

The preferred user-facing entry point is:

| Entry point | Purpose |
|---|---|
| `clinical-research-assistant` / "use CRA" | Router that classifies the task and selects the best internal or external skill |

Internal workflow skills remain available as the execution layer:

| Command | Purpose |
|---|---|
| `/project-init` | Initialize a new research project with state files and directory structure |
| `/resume-project` | Resume an existing project from saved state |
| `/literature-review` | Deep literature search, evidence synthesis, gap analysis, citation verification |
| `/analyze` | Full statistical analysis: data intake → cleaning → modeling → diagnostics → Excel output |
| `/visualize` | Publication-quality figures via K-Dense Python (default) or R + tidyplots/ggplot2 (override) |
| `/write-introduction` | Introduction section — funnel-down structure (Aga & Nissar 2022) |
| `/write-methods-results` | Methods & Results — AMA style, numeric cross-verification against analysis |
| `/write-discussion` | Discussion — reverse-funnel pyramid with Introduction loop closure |
| `/write-abstract` | Abstract — 12-principle editorial rubric, venue-specific structure |
| `/write-manuscript` | Full manuscript orchestrator — coordinates all phases through final audit |
| `/manuscript-qc` | Pre-submission audit — 12 native checks + K-Dense peer-review + ScholarEval + citation re-verify |

## Quick Start

### 1. Install the plugin

```bash
/plugin marketplace add bilalmirza96/clinical-research-assistant
/plugin install clinical-research-assistant@clinical-research-assistant
```

### 2. Start a project

```
/project-init
```

This creates the shared state files and project directory. You can also skip this and jump straight to any command — state files are created on demand if you opt in.

### 3. Recommended workflow

```
use CRA → project-init → literature-review → analyze → visualize → write-introduction → write-methods-results → write-discussion → write-abstract → write-manuscript → manuscript-qc
```

Each command reads from the prior command's state output. You can run them in any order, but this sequence produces the most coherent manuscript.

### 4. Resume later

```
/resume-project
```

Loads all state files, shows project progress, and recommends the next action.

## What Each Command Does

**`/project-init`** — Creates the project directory with 10 state files (`project_state.json`, `study_spec.json`, `analysis_plan.json`, `evidence_bank.json`, `citation_bank.json`, `results_registry.json`, `figure_registry.json`, `manuscript_state.json`, `dataset_profile.json`, `decision_log.md`).

**`/literature-review`** — Searches PubMed, bioRxiv, Scholar Gateway, and ClinicalTrials.gov. Builds an evidence bank (broad inventory) and citation bank (verified-only references with DOI/PMID). Produces gap analysis, novelty assessment, competing work alerts, and a draft Introduction outline. Citations are tagged for Introduction or Discussion use.

**`/analyze`** — Walks through data intake, cleaning, missing data assessment, study design inference, analysis plan, Table 1, unadjusted and adjusted analyses, diagnostics, causal inference (if applicable), sensitivity analyses, and reproducible code. Writes results to `results_registry.json` with exact effect estimates, CIs, p-values, and cohort flow numbers. Supports stateful resume from any checkpoint.

**`/visualize`** — Generates publication-quality figures via **K-Dense Python** (default: `scientific-skills:scientific-visualization` for charts, `scientific-skills:scientific-schematics` for diagrams). R + tidyplots/ggplot2 is supported as an override when the user requests it (see `skills/internal/visualize/references/r-templates.md`). Outputs PDF (vector) + PNG (600 DPI), Anthropic-brand typography (Poppins headings, Lora body), colorblind-safe palettes. Tracks figures in `figure_registry.json` with backend, script path, and approval status.

**`/write-introduction`** — Drafts the Introduction paragraph by paragraph using a funnel-down structure. Draws citations from the verified citation bank. Persists the gap statement and aim statement for Discussion loop closure. Every reference passes the `scientific-skills:citation-management` hard gate (L041) before insertion.

**`/write-methods-results`** — Writes Methods and Results from structured state. Every number in the Results text is cross-verified against `results_registry.json` before the user sees it — mismatches halt presentation. Association language is enforced automatically for observational studies.

**`/write-discussion`** — Drafts the Discussion using a reverse-funnel pyramid with the 3Cs framework (Content-Context-Conclusion). Draws concordant/discordant literature from the citation bank. The Conclusion must close the loop with the Introduction gap statement. Concordant/discordant comparison citations carry the highest fabrication risk — all pass the citation-management hard gate before insertion.

**`/write-abstract`** — Drafts or audits a structured abstract against a 12-principle editorial rubric (coherence, falsification arc, calibrated language, race terminology, therapeutic implications, etc.). Adapts to venue (AATS / ITSOS / JAMA Surgery / JTCVS / JCO / Annals / NEJM / Lancet).

**`/write-manuscript`** — Orchestrates all phases, tracks section completion, runs the final consistency audit (abstract vs results, table/figure references, association language, reporting guideline compliance, citation integrity per L041), and generates assembled Word documents.

**`/manuscript-qc`** — Pre-submission audit. Runs 12 native CRA checks (number consistency, methods-results alignment, statistical correctness, table/figure quality, reference integrity, reporting-standard compliance, etc.) plus three K-Dense delegations: Check 13 reviewer-perspective simulation (`scientific-skills:peer-review`), Check 14 quantitative ScholarEval scoring (`scientific-skills:scholar-evaluation`; halts if total < 14/20), Check 15 batch citation re-verification (`scientific-skills:citation-management`; any FAIL = CRITICAL).

## Shared State

Every command reads from and writes to a common set of state files:

| File | Written By | Read By |
|---|---|---|
| `project_state.json` | `/project-init`, all commands | `/resume-project`, all commands |
| `study_spec.json` | `/project-init`, `/analyze` | `/analyze`, `/literature-review`, `/write-*` |
| `dataset_profile.json` | `/analyze` | `/write-methods-results` |
| `analysis_plan.json` | `/analyze` | `/write-methods-results`, `/write-manuscript` |
| `evidence_bank.json` | `/literature-review` | `/write-introduction`, `/write-discussion` |
| `citation_bank.json` | `/literature-review` | `/write-introduction`, `/write-discussion` |
| `results_registry.json` | `/analyze` | `/visualize`, `/write-methods-results`, `/write-discussion` |
| `figure_registry.json` | `/visualize` | `/write-methods-results`, `/write-manuscript` |
| `manuscript_state.json` | `/write-manuscript`, `/write-*` | `/resume-project`, `/write-manuscript` |
| `decision_log.md` | All commands | `/resume-project` |

All commands work standalone without state files (backward compatible), but state enables cross-session continuity and verified data flow between commands.

## Plotting

Default figure backend: **K-Dense Python** — `scientific-skills:scientific-visualization` for charts, `scientific-skills:scientific-schematics` for diagrams. See `skills/internal/visualize/references/delegation-by-figure-type.md` for the full mapping.

| Figure Type | Backend |
|---|---|
| Bar + beeswarm / violin + box + jitter | `scientific-visualization` (matplotlib + seaborn) |
| Heatmaps, dot plots, line + ribbon | `scientific-visualization` |
| Histogram, density, scatter + fit | `scientific-visualization` |
| Forest plot | `scientific-visualization` (matplotlib custom) |
| ROC curve | `scientific-visualization` (sklearn.metrics + matplotlib) |
| Kaplan-Meier curve | `scikit-survival` (data) + `scientific-visualization` (style) |
| Cumulative incidence (competing risks) | `scikit-survival` (Fine-Gray) + `scientific-visualization` |
| CONSORT flow diagram | `scientific-schematics` |
| Mechanism / workflow diagram | `scientific-schematics` |
| Spline, Love plot, volcano | `scientific-visualization` |

Anthropic-brand typography enforced (Poppins headings always bold, Lora body). Colorblind-safe palettes (Okabe-Ito / viridis) by default. Visual no-overlap inspection gate before any figure is declared complete.

**R override:** when the user explicitly requests R, `skills/internal/visualize/references/r-templates.md` provides equivalent patterns using `tidyplots`, `ggplot2`, `forestploter`, `survminer`, `tidycmprsk`. The aesthetic standards apply identically.

## Key Features

- **Stateful across sessions** — persistent project state via JSON files, resume from any checkpoint
- **Verified citations** — evidence bank (broad) + citation bank (DOI/PMID verified only), no citing from memory
- **Numeric cross-verification** — every number in Methods/Results is checked against `results_registry.json` before presentation
- **Association language enforcement** — causal language automatically detected and corrected for observational studies
- **K-Dense delegation layer** — `skills/references/kdense-delegations.md` defines a single source of truth for citation-management (hard gate, L041), peer-review, scholar-evaluation, pyzotero (auto-on if `ZOTERO_API_KEY` env detected), and K-Dense literature-review (systematic-review execution backbone)
- **K-Dense Python figures by default** — `scientific-visualization` + `scientific-schematics`, PDF vector + PNG 600 DPI, Anthropic-brand typography, colorblind-safe palettes, no-overlap visual inspection gate; R + tidyplots/ggplot2 override available
- **Publication-ready output** — Excel tables (Times New Roman 12pt, formatted), Word manuscripts (double-spaced, 1-inch margins)
- **Methodologically rigorous** — flags EPV violations, immortal time bias, overadjustment, collider bias, poor PS overlap
- **Introduction-Discussion bridge** — gap statement persisted and verified for Conclusion loop closure
- **Multi-agent critique** — Methodologist, Skeptic Reviewer, Manuscript Editor panel for key decisions
- **BioMedAgent delegation** — automatic handoff for omics, genomics, and ML-heavy work

## Domain Expertise

Built-in knowledge across general surgery and subspecialties:

- **General surgery**: SSI, anastomotic leak, Clavien-Dindo, 30-day/90-day outcomes
- **Surgical oncology**: colorectal, gastric, hepatobiliary, pancreatic, breast, esophageal, melanoma/sarcoma
- **Pancreatic surgery**: POPF (ISGPS B/C), DGE, PPH, drain amylase, pancreatic texture, duct diameter
- **Esophageal cancer**: TNM (AJCC 8th ed), Mandard TRG, MIE vs open, survival endpoints
- **Transplant surgery**: graft survival, rejection, immunosuppression, DCD vs DBD, machine perfusion
- **Bariatric surgery**: sleeve vs bypass, %EWL/%TWL, diabetes remission, MBSAQIP metrics
- **MIS**: robotic vs laparoscopic vs open, learning curves, cost-effectiveness
- **Trauma/critical care**: damage control, ISS/GCS/TRISS, massive transfusion, REBOA
- **Biomarker discovery**: cytokine panels, Youden index, multiple testing correction, ROC analysis
- **Registry analyses**: NCDB, NSQIP, UNOS/OPTN, SEER, NTDB, MBSAQIP — including known limitations

## Plugin Structure

```
clinical-research-assistant/                         # Marketplace root
├── ARCHITECTURE.md                                  # System architecture (v3.3)
├── OWNERSHIP_MAP.md                                 # Command ownership map
├── DELEGATION_RULES.md                              # BioMedAgent + K-Dense delegation policy
├── ROADMAP.md                                       # Development roadmap
├── STATE_SCHEMA.md                                  # Pointer → skills/references/state-schema.md
├── COMMAND_CONTRACTS.md                             # Pointer → skills/references/command-contracts.md
├── docs/archive/                                    # Obsolete docs (e.g., PHASE0_CLEANUP_AUDIT.md)
├── clinical-research-assistant/                     # Plugin directory
│   ├── .claude-plugin/plugin.json                   # Plugin metadata
│   ├── CLAUDE.md                                    # Orchestrator config
│   ├── tools/
│   │   ├── update_skill_registry.py                 # Regenerates internal/external skill registry
│   │   └── archive/                                 # One-shot scripts (e.g., append_hnscc_lessons.py)
│   ├── skills/
│   │   ├── clinical-research-assistant/             # User-facing CRA router
│   │   ├── internal/                                # First-party CRA workflows (12 skills)
│   │   │   ├── project-init/                        # /project-init
│   │   │   ├── resume-project/                      # /resume-project
│   │   │   ├── analyze/                             # /analyze — orchestrator-contract (v3.1)
│   │   │   ├── literature-review/                   # /literature-review
│   │   │   ├── visualize/                           # /visualize — K-Dense Python default (v3.2)
│   │   │   ├── write-introduction/                  # /write-introduction
│   │   │   ├── write-methods-results/               # /write-methods-results
│   │   │   ├── write-discussion/                    # /write-discussion
│   │   │   ├── write-abstract/                      # /write-abstract
│   │   │   ├── write-manuscript/                    # /write-manuscript — orchestrator
│   │   │   ├── manuscript-qc/                       # /manuscript-qc — final audit (v3.x)
│   │   │   └── data-analysis/                       # Analytical policy (not a command)
│   │   ├── external/                                # Vendored K-Dense + biomedagent (151 total)
│   │   │   ├── biomedagent/                         # External delegated execution engine
│   │   │   └── scientific-agent-skills/             # K-Dense scientific-skills (139 vendored)
│   │   └── references/                              # Shared CRA-internal references
│   │       ├── writing-style.md                     # Bilal's house style
│   │       ├── lessons-log.json                     # 45 lessons + promoted_to audit trail
│   │       ├── kdense-delegations.md                # K-Dense delegation contracts (v3.3)
│   │       ├── state-schema.md                      # State file schemas (moved from root v3.3)
│   │       ├── command-contracts.md                 # Command contracts (moved from root v3.3)
│   │       ├── biomedagent-methodology.md           # BioMedAgent Plan→Execute→Verify
│   │       ├── external-skills.md                   # Generated index of external skills
│   │       └── skill-registry.yaml                  # Generated machine-readable registry
│   └── templates/state/                             # State file templates
├── README.md
├── CHANGELOG.md
└── LICENSE
```

### External Skill Intake

Paste skills into:

```text
clinical-research-assistant/skills/external/<skill-name>/SKILL.md
clinical-research-assistant/skills/external/<skill-name>.skill
```

Then run from the plugin directory:

```bash
python3 tools/update_skill_registry.py
```

This regenerates `skills/references/skill-registry.yaml` and `skills/references/external-skills.md`, which the CRA router reads before choosing a route.

## Installation

### Claude Code (Terminal)

```bash
/plugin marketplace add bilalmirza96/clinical-research-assistant
/plugin install clinical-research-assistant@clinical-research-assistant
```

### Local Development

```bash
git clone https://github.com/bilalmirza96/clinical-research-assistant.git
cd clinical-research-assistant
```

## License

MIT License — use freely, modify as needed.

## Author

Bilal Mirza — General Surgery Resident
