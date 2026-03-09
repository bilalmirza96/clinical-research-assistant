# Changelog

All notable changes to the clinical-research-assistant plugin will be documented in this file.

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
