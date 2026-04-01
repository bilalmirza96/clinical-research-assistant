# Clinical Research Assistant — Plugin for Claude Code

A personal end-to-end clinical research and manuscript system for Claude Code. Guides the full research pipeline — literature review, statistical analysis, figure generation, and manuscript writing — with shared state across sessions, verified citations, numeric cross-verification, and publication-ready outputs.

## Architecture

**Clinical Research Assistant** is the primary orchestrator. It owns project setup, study framing, literature review, analysis planning, manuscript writing, assembly, and audit.

**BioMedAgent** is a delegated execution engine, called only when the task exceeds standard clinical biostatistics — omics, genomics, biomedical ML, or execution-heavy computational workflows.

All commands share a persistent state layer (`project_state.json`, `results_registry.json`, `citation_bank.json`, etc.) that enables cross-session continuity and cross-command data flow.

## Commands

| Command | Purpose |
|---|---|
| `/project-init` | Initialize a new research project with state files and directory structure |
| `/resume-project` | Resume an existing project from saved state |
| `/literature-review` | Deep literature search, evidence synthesis, gap analysis, citation verification |
| `/analyze` | Full statistical analysis: data intake → cleaning → modeling → diagnostics → Excel output |
| `/visualize` | Publication-quality figures using R + tidyplots/ggplot2 |
| `/write-introduction` | Introduction section — funnel-down structure (Aga & Nissar 2022) |
| `/write-methods-results` | Methods & Results — AMA style, numeric cross-verification against analysis |
| `/write-discussion` | Discussion — reverse-funnel pyramid with Introduction loop closure |
| `/write-manuscript` | Full manuscript orchestrator — coordinates all phases through final audit |

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
/project-init → /literature-review → /analyze → /visualize → /write-introduction → /write-methods-results → /write-discussion → /write-manuscript
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

**`/visualize`** — Generates publication-quality figures using **R + tidyplots** (preferred) or **ggplot2** (fallback). Assigns each figure type the appropriate backend. Outputs PDF (vector) + PNG (600 DPI). Tracks figures in `figure_registry.json` with backend, script path, and approval status.

**`/write-introduction`** — Drafts the Introduction paragraph by paragraph using a funnel-down structure. Draws citations from the verified citation bank. Persists the gap statement and aim statement for Discussion loop closure.

**`/write-methods-results`** — Writes Methods and Results from structured state. Every number in the Results text is cross-verified against `results_registry.json` before the user sees it — mismatches halt presentation. Association language is enforced automatically for observational studies.

**`/write-discussion`** — Drafts the Discussion using a reverse-funnel pyramid with the 3Cs framework (Content-Context-Conclusion). Draws concordant/discordant literature from the citation bank. The Conclusion must close the loop with the Introduction gap statement.

**`/write-manuscript`** — Orchestrates all phases, tracks section completion, runs the final consistency audit (abstract vs results, table/figure references, association language, reporting guideline compliance), and generates assembled Word documents.

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

Default figure backend: **R** with **tidyplots** (preferred) and **ggplot2** (fallback).

| Figure Type | Backend |
|---|---|
| Group comparisons (bar + beeswarm) | tidyplots |
| Violin + box + jitter | tidyplots |
| Heatmaps, dot plots, line + ribbon | tidyplots |
| Histogram, density, scatter + fit | tidyplots |
| Forest plot | ggplot2 (forestploter) |
| ROC curve | ggplot2 (pROC) |
| Kaplan-Meier curve | ggplot2 (survminer) |
| Cumulative incidence | ggplot2 (tidycmprsk) |
| CONSORT flow diagram | ggplot2 / DiagrammeR |
| Spline, Love plot, volcano | ggplot2 |

Python/matplotlib is not the default for manuscript figures.

## Key Features

- **Stateful across sessions** — persistent project state via JSON files, resume from any checkpoint
- **Verified citations** — evidence bank (broad) + citation bank (DOI/PMID verified only), no citing from memory
- **Numeric cross-verification** — every number in Methods/Results is checked against `results_registry.json` before presentation
- **Association language enforcement** — causal language automatically detected and corrected for observational studies
- **R-first figures** — tidyplots + ggplot2, PDF vector + PNG 600 DPI, colorblind-safe palettes
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
├── ARCHITECTURE.md                                  # System architecture
├── OWNERSHIP_MAP.md                                 # Command ownership map
├── PHASE0_CLEANUP_AUDIT.md                          # Cleanup audit log
├── STATE_SCHEMA.md                                  # State file schemas
├── COMMAND_CONTRACTS.md                             # Command contracts
├── DELEGATION_RULES.md                              # BioMedAgent delegation rules
├── ROADMAP.md                                       # Development roadmap
├── clinical-research-assistant/                     # Plugin directory
│   ├── .claude-plugin/plugin.json                   # Plugin metadata
│   ├── CLAUDE.md                                    # Orchestrator config
│   ├── skills/
│   │   ├── project-init/                            # /project-init
│   │   ├── resume-project/                          # /resume-project
│   │   ├── analyze/                                 # /analyze — canonical owner
│   │   ├── literature-review/                       # /literature-review
│   │   ├── visualize/                               # /visualize — R/tidyplots/ggplot2
│   │   ├── write-introduction/                      # /write-introduction
│   │   ├── write-methods-results/                   # /write-methods-results
│   │   ├── write-discussion/                        # /write-discussion
│   │   ├── write-manuscript/                        # /write-manuscript — orchestrator
│   │   ├── data-analysis/                           # Analytical policy (not a command)
│   │   └── references/                              # Writing style guide
│   └── templates/state/                             # State file templates
├── skills/biomedagent/                              # BioMedAgent skill
├── README.md
├── CHANGELOG.md
└── LICENSE
```

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
