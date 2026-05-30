# Red-Team Reviewer Brief (clinically augmented)

> Added 2026-05-30. This is the brief handed to the SINGLE `science-superpowers:requesting-red-team-review` subagent at `/analyze` Phase 6 (and on a tripped checkpoint). It augments SP's generic reviewer with CRA's clinical checklist so one reviewer carries all the rigor the old 5-agent panel did. The reviewer receives the frozen pre-registration, the analysis_plan, results_registry.json, the Master Excel tabs, and the commit range — never the full session history.

## Generic attack vectors (from SP requesting-red-team-review)
Confounds & alternative explanations; assumption violations; data leakage; researcher degrees of freedom (p-hacking / HARKing / post-hoc choices); multiplicity (uncorrected comparisons); reproducibility (does it reproduce from raw + seed?); over-claiming (causal language from observational data, generalizing beyond the sample).

## CRA clinical checklist the reviewer MUST also run
- **Estimand & terminology** — primary = crude/unadjusted; secondary = adjusted (per L051). Flag any conflation.
- **Diagnostics thresholds** (per `clinical-analysis-policy.md` / `diagnostics-checklist.md`): EPV ≥10 (warn) / ≥5 (halt); VIF ≤5; Cox Schoenfeld p≥0.05 (else time-stratified, L003); PSM SMD <0.1 ideal/<0.2 acceptable + overlap + E-value (L005); logistic separation/Hosmer-Lemeshow.
- **Multiple testing** — BH-FDR within families + Bonferroni for primary (L006/L032). Bolding: p<0.05 in Table_1; q<0.05 in Table_2/Sensitivity/Supplementary.
- **Registry cautions** (per `registry-cautions.md`) — NCDB no cause-specific survival + facility clustering; SEER no systemic therapy; NSQIP 30-day only; immortal-time bias; missingness not MCAR.
- **Concordance** — crude (Phase 4) vs adjusted (Phase 5A) direction/magnitude/CI overlap; unexplained flips are findings.
- **Lessons-log L-rules** — scan `../../../references/lessons-log.json` trigger_patterns against this analysis; surface any HIGH/CRITICAL fire.
- **Observational language** — association not causation; flag causal verbs.
- **Evidence tiering (L035)** — does each claim sit at the tier its evidence supports (Tier 1 abstract … Tier 4 Discussion-only)?

## Output (severity-graded, like the old panel)
Return JSON findings: `[{severity: CRITICAL|HIGH|MODERATE|LOW, category, location, issue, recommended_fix, rationale}]` + `overall: approve | approve_with_fixes | reject`. Any CRITICAL → trigger the 6-phase remediation pipeline (L028). Merge into `audit_report.md`.
