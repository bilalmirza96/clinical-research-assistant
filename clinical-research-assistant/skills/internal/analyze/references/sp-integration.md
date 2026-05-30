# science-superpowers integration map (rigor layer)

> Added 2026-05-30. Defines exactly where each `science-superpowers` (SP) skill fires inside `/analyze`, and the precedence between the SP bootstrap, the generic `superpowers` bootstrap, and the CRA session-start. SP is the RIGOR layer of the three-layer architecture (see `DELEGATION_RULES.md` §E).

## Three layers
1. **Rigor — science-superpowers.** Pre-registration, inline verification, red-team, anomaly root-cause.
2. **Orchestration — CRA (the brain).** `/analyze` decides WHAT/WHEN; owns clinical method selection, registry cautions, halts, Master Excel, the 16-section report.
3. **Execution — K-Dense `scientific-skills` + `biomedagent`.** Validated how-to references. Standard tabular biostatistics runs natively in CRA against the relevant `scientific-skills:*` reference; omics/ML/non-tabular → `biomedagent`.

## Where each SP skill fires
| /analyze point | SP skill | Mode | Replaces |
|---|---|---|---|
| Phase 0 (lit recon) | `surveying-prior-work` (optional) | inline / via `/literature-review` | — |
| Phase 3 (after PLAN) | `preregistering-analysis` | inline — writes `Protocol/preregistration_<date>.md` | formalizes the old "locked specs" |
| Phase 3 (only on CRITICAL plan flaw) | `requesting-red-team-review` | 1 subagent | escalation only |
| Checkpoint A (end of PRIMARY) | `verifying-results-before-claiming` | INLINE, no subagent | old Numerical + Code-repro + Completeness audit agents |
| Checkpoint B (end of SECONDARY) | `verifying-results-before-claiming` + concordance | INLINE | same |
| Any tripped checkpoint | `investigating-anomalous-results` | inline (may parallelize) | old ad-hoc gate remediation |
| Phase 6 (final audit) | `requesting-red-team-review` | 1 subagent, briefed by `red-team-brief.md` | the old 5-agent audit panel |
| Phase 7 (delivery) | `reporting-and-archiving-findings` principles | inline | — |

## Bootstrap precedence (resolves competing session-starts)
For clinical-research analysis: **CRA `/analyze` is the entry orchestrator.** It invokes the SP rigor skills at the points above. SP's own framing / surveying / designing / reporting skills and the generic `superpowers` (software-dev, TDD) bootstrap are SUPPRESSED for clinical tasks — CRA owns those. Outside clinical research (pure translational/omics exploration), SP may lead and `biomedagent` carries more execution.

## Token rationale
Old: 4-agent plan critique (~15K) + 5-agent audit (~17K) = ~32K subagent tokens/run. New: inline lenses + inline verification + ONE red-team reviewer (~3-5K). Routine checks cost ~0 extra; a subagent fires only for escalation or the final red-team.
