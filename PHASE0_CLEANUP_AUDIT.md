# Phase 0 Cleanup Audit

Date: 2026-04-01

## Scope
This audit records the first cleanup pass on `clinical-research-assistant` before implementation of the v3 architecture.

## Findings

### 1. `/analyze` was miswired
The file at `clinical-research-assistant/skills/analyze/SKILL.md` was not an analysis skill. It duplicated visualization content and declared `name: visualize`.

### 2. Visualization contract was duplicated
Visualization content existed under both:
- `clinical-research-assistant/skills/analyze/SKILL.md`
- `clinical-research-assistant/skills/visualize/SKILL.md`

This created ambiguity in command routing and ownership.

### 3. Analysis responsibilities were split across two competing homes
There was a second analysis-oriented skill at:
- `clinical-research-assistant/skills/data-analysis/SKILL.md`

This created uncertainty about which file was the canonical contract for `/analyze`.

### 4. Instruction duplication remains substantial
Large blocks of overlapping policy exist across:
- `clinical-research-assistant/CLAUDE.md`
- `clinical-research-assistant/skills/data-analysis/SKILL.md`
- `clinical-research-assistant/skills/write-manuscript/SKILL.md`
- `clinical-research-assistant/skills/write-methods-results/SKILL.md`
- `clinical-research-assistant/skills/references/writing-style.md`

This is acceptable for now, but should be reduced in later cleanup phases.

## Decisions Applied in This Pass

### Decision 1
`clinical-research-assistant/skills/analyze/SKILL.md` is now treated as the canonical home of `/analyze`.

### Decision 2
The canonical `/analyze` contract is now plan-first and state-aware. It explicitly:
- profiles datasets
- creates an analysis plan before execution
- supports native clinical biostatistics execution
- supports explicit delegation to BioMedAgent
- writes machine-readable outputs for downstream commands

### Decision 3
`/visualize` remains owned by `clinical-research-assistant/skills/visualize/SKILL.md`.

## Decisions Deferred

### Deferred 1
Whether `clinical-research-assistant/skills/data-analysis/SKILL.md` should be:
- deprecated,
- merged into `/analyze`, or
- retained as an auto-triggered background statistical policy file.

### Deferred 2
How much top-level instruction content should remain in `CLAUDE.md` versus reference files.

### Deferred 3
How aggressively to split house style, section rules, and journal-adaptation rules.

## Next Cleanup Targets

1. decide the future role of `skills/data-analysis/SKILL.md`
2. reduce duplicated statistical policy between `CLAUDE.md` and the canonical `/analyze` contract
3. begin implementing the shared state layer
4. gate literature-backed narrative writing on the verified citation bank

## Success Criteria for Phase 0

Phase 0 is considered successful when:
- `/analyze` has one unambiguous canonical contract
- `/visualize` has one unambiguous canonical contract
- the repo has a documented ownership map for major responsibilities

This audit document should be updated as the cleanup continues.
