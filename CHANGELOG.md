# Changelog

All notable changes to the clinical-research-assistant plugin will be documented in this file.

## [2.4.0] - 2026-04-26

### Added — Mandatory analysis-report rule

Every analysis must end with a date-stamped, structured markdown report. The report is the durable deliverable that the manuscript Methods and Results sections are drafted from, that co-authors audit, and that future sessions read first before re-deriving anything. No analysis is considered complete without it.

- **`skills/analyze/SKILL.md`** — added new `Step 9 — Generate the Analysis Report (MANDATORY)` section between `/visualize` reminder and `Reporting Standards`. Defines filename pattern (`analysis_report_<short-question-slug>_YYYY-MM-DD.md`), required-section template (16 sections in fixed order), per-claim requirements (effect size + 95% CI + P + BH-FDR Q + numerator/denominator), versioning rule (re-generate on re-run; archive prior), and a compliance checklist that must pass before the report is declared complete.
- **`skills/data-analysis/SKILL.md`** — added `<mandatory_analysis_report>` block summarising the 16-section template and pointing to `analyze/SKILL.md` Step 9 for the full template and compliance rules.
- **`skills/references/lessons-log.json`** — added entry `L026-mandatory-analysis-report` so the rule is machine-readable and trigger-pattern-routable for future sessions.

The report is the single source of truth for what was done; future sessions read it first before re-deriving findings, and the manuscript-writing skills (`/write-methods-results`, `/write-discussion`, `/write-abstract`) draw their Methods/Results/Limitations content from the report rather than from chat history.

## [2.3.0] - 2026-04-26

### Added — `write-abstract` sub-skill (Bilal Mirza editorial rubric)

A new sub-skill at `skills/write-abstract/SKILL.md` codifies a 12-principle editorial philosophy for writing and auditing abstracts, with a 12-point gate that runs explicitly before any draft is declared submission-ready.

**The 12 principles:** (1) coherence as primary editing criterion, (2) hypothesis-falsification narratives in three places, (3) calibrated language tracking epistemic standing, (4) race terminology matching what was measured, (5) audience calibration leaning biologist for translational, (6) Results as largest section, (7) therapeutic implications at the level data supports, (8) confounders in manuscript not abstract, (9) honesty over impact, (10) compliance as final pass, (11) four-criterion rigor gate (BH-FDR + bootstrap BCa + permutation + jackknife) before any claim earns abstract space, (12) prose over bullets.

**Priority order for use:** principles 3, 7, 9 for active editing; principles 1, 2, 6 for narrative architecture; principle 10 for compliance; principle 11 for rigor.

**Includes** a venue cheat-sheet (AATS / ITSOS / Summit; JTCVS; JAMA Oncology; JCO; ASCO; AHA / ACC; NEJM; Lancet; Annals of Surgery), workflows for both drafting and auditing, and a worked example applying the gate to the ITSOS 2026 esophageal disparity abstract.

**Wired into** `write-manuscript/SKILL.md` Phase 7 (Abstract) — the orchestrator now delegates abstract drafting to the new sub-skill.

**Lessons log additions** (`skills/references/lessons-log.json`): 9 new entries (L017–L025) covering coherence, falsification arc, calibrated language, race terminology, section weight, therapeutic implications, honesty-over-impact, four-criterion rigor gate, and the 12-point final-pass gate.

## [2.2.0] - 2026-04-25

### Added — BioMedAgent-adapted methodology (the *ideas*, not the tool catalog)

Inspired by Bu et al., *Empowering AI data scientists using a multi-agent LLM framework with self-evolving capabilities for autonomous, tool-aware biomedical data analyses*, Nat Biomed Eng 2026 (https://github.com/BOBQWERA/BioMedAgent.git).

- **`skills/references/biomedagent-methodology.md`** — new cross-cutting reference for clinical research that distils the four transferable BioMedAgent ideas: (1) three-phase pipeline (Plan → Execute → Verify with self-correcting feedback loops), (2) task classification before method selection (six-way routing table for clinical research), (3) memory retrieval before re-deriving (read the lessons log first), and (4) anti-misclassification rules (Cox-PH violation, complete-case bias, immortal-time bias, causal language for observational data, NCDB DUA cell-N≥11, etc.).
- **`skills/references/lessons-log.json`** — new machine-readable memory log seeded with 16 entries from real sessions: 10 from the V3 Esophageal Cancer Disparity analysis (Simpson's-paradox prevention, time-stratified Cox, multiple-imputation sensitivity, E-value reporting, master significance with BH-FDR, NCDB DUA compliance, stage decomposition, subgroup-power justification, provider-vs-patient-side gating), 3 from the V4 cross-cohort harmonization and JAMA-table rebuild (cohort harmonization before cross-cohort comparison, JAMA table-formatting discipline, JAMA P-value formatting), and 3 from the BioMedAgent methodology adaptation itself (three-phase pipeline, task classification, memory retrieval).
- **`skills/analyze/SKILL.md`** — added `<biomedagent_adapted_methodology>` block at the top instructing every analysis to read `lessons-log.json` and `biomedagent-methodology.md` first, classify the task before method selection, and append a new lesson at session end.
- **`skills/data-analysis/SKILL.md`** — same pointer block (shorter form).
- **`skills/write-manuscript/SKILL.md`** — same pointer block, framing the existing 9-phase manuscript orchestrator as an instance of the BioMedAgent three-phase pipeline (Plan = Phase 0–1, Execute = Phases 2–7, Verify = Phase 8).

### Maintenance philosophy
The lessons log is append-only. Mark superseded entries `"deprecated": true` rather than deleting them; the audit trail matters. Each new clinical-research session that surfaces a new pattern (pitfall, default sensitivity, classification trap) should append an entry. This is the self-evolution mechanism BioMedAgent uses; here it is the explicit clinical-research analogue.

### What this is NOT
- Not a port of BioMedAgent's 65-tool catalog (those are bioinformatics tools, mostly duplicated by the existing `bio-research`, `scientific-skills`, and `pyhealth` plugins).
- Not a new top-level skill — the four ideas are integrated into the three existing analytic/manuscript skills.
- Not a replacement for the standalone `biomedagent` Cowork plugin if you have it installed; this just brings the *ideas* into clinical-research-assistant so the two plugins can coexist or you can choose to uninstall the standalone one.

## [2.1.0] - 2026-03-10

### Added
- **Research connector integration**: Each skill now declares exactly which research tools it needs via `allowed-tools` in frontmatter
- PubMed connector (search articles, get metadata, find related, full text, citation lookup)
- bioRxiv/medRxiv connector (search preprints, get details, track publications)
- Scholar Gateway connector (semantic search across academic literature)
- ClinicalTrials.gov connector (search trials, trial details, sponsor search, endpoint analysis)
- BioRender connector (search icons and templates for scientific figures)
- CONNECTOR-SETUP.md guide for enabling all required research connectors

### Changed
- `/literature-review` now has access to PubMed, bioRxiv, Scholar Gateway, Clinical Trials, and web search
- `/write-manuscript` (orchestrator) has access to all connectors since it coordinates all phases
- `/write-introduction` and `/write-discussion` have PubMed + Scholar Gateway for finding additional references
- `/visualize` has BioRender access for scientific icons and templates
- `/analyze` and `/write-methods-results` are scoped to local tools only (data crunching, no web access needed)

## [2.0.0] - 2026-03-08

### Added
- Migrated all 7 commands from `commands/` to `skills/` directory structure (preferred by Anthropic)
- Each command is now an independent skill with proper frontmatter (`name`, `description`, `argument-hint`)
- `argument-hint` support for `/analyze`, `/literature-review`, and `/visualize`
- Plugin settings template (`settings-template.md`) for configurable defaults (target journal, citation style, voice, etc.)
- MIT LICENSE file
- `user-invocable: false` on data-analysis skill (knowledge base, not directly invoked)

### Changed
- **BREAKING**: Commands directory removed — all commands are now skills under `skills/`
- Version bump to 2.0.0 (major structural change)
- Updated plugin.json description and author name

### Removed
- `commands/` directory (replaced by `skills/`)

## [1.4.0] - 2026-03-08

### Added
- XML tags (`<role>`, `<rules>`, `<interaction_rules>`, `<examples>`, etc.) across all command files for improved prompt structure
- Concrete examples in 6 command files (Introduction paragraph, Results paragraph, Toggle Rule, Table 1 format, forest plot code, evidence summary table)
- Anti-hallucination guardrails (`<citation_integrity>`) in literature-review command
- Parallel search guidance for literature-review (PubMed, bioRxiv, Scholar Gateway simultaneously)
- JSON-based state persistence (`manuscript_state.json`, `manuscript_context.json`) in write-manuscript
- Context window refresh recovery in write-manuscript
- "Why" context for key rules (funnel structure, association language, loop-closing)
- Reference files: `method-selection-guide.md`, `registry-cautions.md`, `diagnostics-checklist.md`
- CHANGELOG.md

### Changed
- Shortened plugin description in plugin.json for cleaner display
- Fixed "HTML table" references to "formatted markdown table" in analyze command
- Consolidated domain expertise to SKILL.md as single source of truth (removed duplicates from analyze.md and literature-review.md)
- Compressed 14 less-common figure types into compact reference table in visualize command
- Cleaned SKILL.md frontmatter to use only recognized fields (`name`, `description`)

### Removed
- Duplicated domain expertise sections from analyze.md and literature-review.md
- Redundant Excel formatting specifications in analyze.md
- Non-standard frontmatter fields (`metadata`, `category`) from SKILL.md

## [1.3.0] - 2025-12-01

### Added
- Initial plugin release with 7 slash commands
- /analyze — Full statistical analysis workflow
- /visualize — Publication-quality figure generation
- /write-manuscript — Full manuscript orchestrator
- /write-introduction — Introduction section writer
- /write-methods-results — Methods and Results writer
- /write-discussion — Discussion and Conclusion writer
- /literature-review — Evidence synthesis and search strategy
- Clinical statistical analyst skill (SKILL.md)
