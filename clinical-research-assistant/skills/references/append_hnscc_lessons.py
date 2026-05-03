"""
One-shot script to append L027-L037 (HNSCC-TAM rigor remediation lessons) to
lessons-log.json. Idempotent: re-runs are safe — checks for existing IDs before
appending.

Run from the repo root:
    python3 skills/references/append_hnscc_lessons.py

Date: 2026-05-03
"""

import json
from pathlib import Path

LOG = Path(__file__).parent / "lessons-log.json"

NEW_LESSONS = [
    {
        "id": "L027-five-agent-self-audit-before-manuscript",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation (Bilal Mirza, U Arizona) — pre-submission rigor pass",
        "category": "Pre-submission rigor: audit-first methodology",
        "trigger_patterns": [
            "secondary analysis manuscript drafting",
            "multiple intermediate analyses already completed",
            "ready for manuscript drafting",
            "claim of N/N validated findings",
            "any manuscript with >5 cohorts or >5 statistical claims"
        ],
        "lesson": "Before drafting a manuscript from already-completed analyses, run a structured 5-agent self-audit (numerical, statistical, biological-plausibility, code-reproducibility, completeness). The HNSCC-TAM session caught 4 critical issues — wrong AUROC value, pseudoreplication in cross-compartment correlations, an N/N validated overclaim, and missing random seeds — none of which were detectable from the report itself without comparing claimed numbers against source CSVs and re-deriving p-values at the proper sample size.",
        "action": "Whenever an analysis is being staged for manuscript drafting, run a 5-agent self-audit producing AUDIT_REPORT.md with severity-graded findings (CRITICAL / HIGH / MODERATE / MINOR). Each finding cites the source CSV row and the claimed value. Do not begin manuscript drafting until critical issues are resolved or explicitly deferred with a documented gating plan.",
        "deprecated": False
    },
    {
        "id": "L028-six-phase-rigor-remediation-pipeline",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Pre-submission rigor: standardized remediation sequence",
        "trigger_patterns": [
            "AUDIT_REPORT.md identifies critical issues",
            "manuscript drafting blocked on rigor issues",
            "user wants to systematically address audit findings",
            "claim of multi-cohort meta-validation",
            "BCa CIs and BH-FDR not yet applied"
        ],
        "lesson": "A 6-phase remediation sequence cleanly closes most audit issues without requiring a full pipeline re-run: (1) surgical text/numerical fixes against source CSVs, (2) bootstrap BCa 95% CIs + BH-FDR + Bonferroni multiple-testing correction, (3) patient-level cross-compartment re-derivation + drop-LOO sensitivity, (4) canonical meta-validation table consolidating all evidence, (5) mandatory 16-section analysis report, (6) numerical re-audit cross-walking all claims against source CSVs.",
        "action": "Set up phase-numbered remediation folders (phase1_remediation/, phase2_remediation/, ..., phase6_audit/) under the project Analysis/ root. Each phase produces (a) one Python script in scripts/, (b) machine-readable outputs in results/, and (c) one PHASE*_REPORT.md narrative. Phase 6 must be a programmatic re-audit producing a PASS/FAIL log — target 100% PASS at 3-decimal precision before manuscript submission.",
        "deprecated": False
    },
    {
        "id": "L029-pseudoreplication-in-paired-prepost-cohorts",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Statistical methodology: pseudoreplication detection",
        "trigger_patterns": [
            "paired pre/post scRNA cohort with small n_patients",
            "correlation computed on (patient × treatment) observations",
            "claim of n=8 with 4 patients × 2 timepoints",
            "discovery cohort cross-compartment correlation",
            "Spearman rho with degrees of freedom > true patient n"
        ],
        "lesson": "When a small discovery cohort (e.g., n=4 patients with paired pre/post sampling) is analyzed by treating each (patient, treatment) pair as an independent observation, the resulting n=8 correlations are pseudoreplicated and overstate statistical certainty. The proper patient-level analysis is n=4 (averaging pre+post within patient or using pre-only). At n=4 the minimum two-sided EXACT Spearman p-value is 2/24 = 0.083 — a structural floor, NOT a property of the data — so no patient-level n=4 correlation can reach p<0.05 by exact testing.",
        "action": "For any correlation in a small discovery cohort with paired timepoints, derive THREE framings: (a) pseudorep n_obs (sanity check vs original number), (b) patient-level n_patients (averaged or pre-only — addresses pseudoreplication), (c) pre-treatment baseline only. Use scipy.stats.permutation_test with permutation_type='pairings' for n<=5 (full enumeration) or n_resamples=10_000 for n=6-8 (Monte Carlo). The asymptotic Spearman p-value formula breaks at |rho|=1 (returns p=0 spuriously); always use exact / Monte Carlo for small n. Reframe the patient-level finding as HYPOTHESIS-GENERATING in the manuscript.",
        "deprecated": False
    },
    {
        "id": "L030-one-patient-dominance-flag-for-scrna",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Statistical methodology: subject-level sensitivity",
        "trigger_patterns": [
            "scRNA-seq cell-type composition analysis",
            "small discovery cohort (n_patients <= 6)",
            "rare cell-type analysis",
            "TREM2+ TAM analysis",
            "any subtype analysis where N cells >> N patients"
        ],
        "lesson": "In small scRNA-seq discovery cohorts, a single patient can dominate a cell-type pool. In the HNSCC-TAM session, Patient_2 contributed 96.66% of all TREM2+ TAM cells (984 of 1,018). Every TREM2+ TAM downstream finding (DEGs, TF activity, metabolic programs, ligand-receptor scores) is mathematically a Patient_2 finding. The dramatic 0.32x post-treatment fold change attenuated to 0.44x with Patient_2 dropped, and the Wilcoxon p-value remained non-significant in either framing.",
        "action": "For every cell-type / subtype analysis in a discovery cohort with n_patients <= 6, compute per-patient cell-pool contribution (n_cells_patient_X / n_cells_total). If any patient contributes >50% of any subtype, generate an automatic Drop-Patient-X leave-one-out sensitivity analysis covering: (a) per-patient mean proportion with vs without that patient, (b) Pre/Post fold change with vs without, (c) Wilcoxon paired test in each framing. Report both versions in the manuscript and reframe the finding as HYPOTHESIS-GENERATING if the magnitude is patient-dependent.",
        "deprecated": False
    },
    {
        "id": "L031-bca-bootstrap-cis-on-every-auroc",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Statistical methodology: CI reporting standard",
        "trigger_patterns": [
            "AUROC reported in clinical research manuscript",
            "biomarker-response prediction",
            "any signature-vs-binary-outcome analysis",
            "small validation cohort (n < 30)",
            "ICI response prediction"
        ],
        "lesson": "Reviewers of biomarker-prediction manuscripts routinely flag 'AUROC without 95% CI' as a critical methodological gap. Point estimates without uncertainty bands are not interpretable, especially at small N. Paired bootstrap with bias-correction-and-acceleration (BCa) 95% CI is the rigorous gold standard. At n=12 (TJU nivolumab stratum), some BCa CIs spanned [0, 1] — reflecting the true uncertainty.",
        "action": "Compute paired bootstrap BCa 95% CI on EVERY AUROC reported in the manuscript. Use 500-1000 paired (scores, labels) resamples with random_state=42; skip resamples that lose class diversity. BCa requires bias-correction z0 (from boot empirical distribution) and acceleration a (from jackknife). scipy.stats.bootstrap with method='BCa' and paired=True works; or implement manually with norm.ppf. Report as 'AUROC = X [95% BCa CI, low, high]' uniformly. Flag CIs that span 0.5 as 'not statistically distinguishable from chance.'",
        "deprecated": False
    },
    {
        "id": "L032-bh-fdr-and-bonferroni-mandatory",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Statistical methodology: multiple-testing correction",
        "trigger_patterns": [
            "panel of N signatures tested in same cohort",
            "cell-type AUROC table",
            "biomarker signature comparison",
            "any signature batch >= 5 in single cohort"
        ],
        "lesson": "When >=5 signatures are tested against the same outcome in the same cohort, family-wise testing inflates false positives. In GSE159067 (n=102, 14 signatures), three findings survived BH-FDR (CXCL9/10, CYT, CXCL9/CD8A) but only ONE survived Bonferroni (CXCL9/10 at alpha=0.05/14=0.0036). The Bonferroni-survivor is the load-bearing claim; BH-FDR-only survivors should be framed as 'supportive of, not independent confirmation of' the Bonferroni-survivor.",
        "action": "For every (cohort × signature panel) batch >= 5 tests, apply Benjamini-Hochberg FDR using statsmodels.stats.multitest.multipletests(method='fdr_bh'). For the largest validation cohort (typically the manuscript's anchor), additionally apply Bonferroni at alpha = 0.05/n_tests. Report BH_q and Bonferroni_significant columns alongside raw P. Frame manuscript claims by tier: Bonferroni-survivor = lead finding; BH-FDR-only = supporting; raw-P-only = hypothesis-generating.",
        "deprecated": False
    },
    {
        "id": "L033-random-state-42-everywhere",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Reproducibility: deterministic pipelines",
        "trigger_patterns": [
            "scanpy pipeline",
            "Leiden clustering",
            "UMAP embedding",
            "PCA",
            "train_test_split",
            "any stochastic call without explicit seed"
        ],
        "lesson": "Without random_state=42, scanpy's sc.tl.pca / umap / leiden / neighbors / diffmap calls produce non-deterministic results. Cluster identity may be preserved across runs (Leiden is deterministic given seeded igraph + identical input) but cluster *labels* permute, which can scramble downstream analyses.",
        "action": "Add a seeded helper `seed_all.py` to every project that imports os, random, numpy, scanpy, torch and sets seed=42 across all of them. At the top of every analysis script, call seed_everything(42) before any stochastic operation. ALSO pass random_state=42 explicitly to every: sc.tl.pca, sc.tl.umap, sc.tl.leiden, sc.tl.tsne, sc.tl.diffmap, sc.tl.dpt, sc.pp.neighbors, sklearn.model_selection.train_test_split, sklearn.cluster.* . Use np.random.default_rng(42) instead of np.random.* for new code. Document this in CLAUDE.md as a project-wide rule.",
        "deprecated": False
    },
    {
        "id": "L034-canonical-meta-validation-table-as-source-of-truth",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Manuscript drafting: source-of-truth artifact",
        "trigger_patterns": [
            "multi-cohort meta-validation paper",
            "claim of N/N findings validated",
            "Manuscript Table 1 needs cross-cohort summary",
            "drafting after Phase 1-3 rigor remediation"
        ],
        "lesson": "After audit-driven rigor remediation, the manuscript's Table 1 should be a CANONICAL meta-validation table consolidating: (a) v1-corrected effect sizes, (b) bootstrap 95% CIs, (c) raw P-values, (d) BH-FDR q-values, (e) Bonferroni status, (f) status grading (ROBUST / PARTIAL / NOVEL / HYPOTHESIS-GENERATING / EXTERNALLY VALIDATED), (g) per-finding source-CSV provenance.",
        "action": "Build a Phase 4 consolidation script `phase4_build_meta_validation_v2.py` that reads all upstream CSVs (phase1_corrections, phase2_aurocs, phase3_xc_correlations) and produces: meta_validation_v2_long.csv (one row per Finding × Cohort × Statistic with full provenance), meta_validation_v2_summary.csv (one row per Finding with audit-correct headline), and meta_validation_v2.xlsx (formatted workbook). Headline-selection priority: EXTERNALLY VALIDATED > HYPOTHESIS-GENERATING (audit-corrected) > PARTIAL > ROBUST > NOVEL > largest-N fallback.",
        "deprecated": False
    },
    {
        "id": "L035-four-tier-evidence-framework",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Manuscript drafting: claim-tiering",
        "trigger_patterns": [
            "manuscript drafting after rigor remediation",
            "deciding what goes in abstract vs body vs discussion",
            "claim of N/N findings validated",
            "post-audit evidence base partition"
        ],
        "lesson": "After rigor remediation, partition every finding into 4 tiers for placement in the manuscript: TIER 1 (ROBUST + Bonferroni-survivor) leads the abstract and primary results; TIER 2 (PARTIAL = BH-FDR-only) appears as supportive in the body; TIER 3 (NOVEL single-cohort + EXTERNALLY VALIDATED cross-compartment) appears in main text + future-work hooks; TIER 4 (HYPOTHESIS-GENERATING) appears in Discussion + Limitations only — NEVER in the abstract or primary tables.",
        "action": "When drafting the manuscript, apply tier-based placement: (1) Abstract leads with Tier 1 findings + effect sizes + 95% CIs; (2) Results sections present Tiers 1-3 in the body with explicit multiple-testing flags; (3) Discussion §Limitations explicitly addresses Tier 4 as 'directionally consistent but not statistically distinguishable from chance after multiple-testing correction at this sample size.' This pre-empts reviewer critique of overclaiming.",
        "deprecated": False
    },
    {
        "id": "L036-numerical-reaudit-before-submission",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Pre-submission rigor: programmatic verification",
        "trigger_patterns": [
            "manuscript draft complete",
            "ready for PI review",
            "post-Phase 5 analysis report",
            "before AUDIT_REPORT_v2.md"
        ],
        "lesson": "Manual claim-by-claim verification of a multi-cohort manuscript is error-prone. A programmatic re-audit script that cross-walks every numerical claim in the manuscript against its source CSV at 3-decimal precision is the durable verification artifact.",
        "action": "Build a Phase 6 script `phase6_numerical_reaudit.py` that adds named checks via add_check(name, claimed, observed_in_source, tolerance, unit) and writes phase6_audit_log.csv + phase6_audit_summary.txt. Cover at minimum: (a) claimed text values vs source CSV cells, (b) summary-table values vs upstream long-table values, (c) document-internal stale-string scans, (d) sample-size sums. Target 100% PASS before submission. Produce AUDIT_REPORT_v2.md as the closure document.",
        "deprecated": False
    },
    {
        "id": "L037-manuscript-document-hierarchy",
        "date_added": "2026-05-03",
        "originating_session": "HNSCC-TAM Multi-Cohort Validation",
        "category": "Project organization: artifact hierarchy",
        "trigger_patterns": [
            "manuscript drafting workflow",
            "multiple working documents accumulating",
            "PIs need a single brief vs full report",
            "post-Phase 4 deliverable handoff"
        ],
        "lesson": "Multi-cohort manuscript projects accumulate multiple narrative documents. A clear hierarchy prevents confusion: (a) `Reports/insights_report_v*.md` = working insights document with full numerical detail; (b) `Reports/analysis_report_<question-slug>_<date>.md` = mandatory 16-section technical analysis report (per working-rules.md); (c) `Reports/FINAL_manuscript_brief_<date>.md` = manuscript-ready narrative brief consolidating story arc + cohort contributions + tier-graded evidence (this is the document PIs read first); (d) `Manuscripts/manuscript_complete_<date>.docx` = the actual manuscript deliverable.",
        "action": "Whenever a manuscript project exits the rigor remediation phases, produce the FINAL manuscript brief BEFORE drafting the manuscript itself. The brief contains: §1 Executive summary, §2 Why this project exists, §3 What we did chronologically, §4 Cohort-by-cohort contribution, §5 Four-tier evidence base, §6 Audit story, §7 Manuscript story arc with 3 title options, §8 Suggested abstract, §9 Section-by-section content map, §10 Path to submission, §11 Document index, §12 One-sentence elevator pitch. PIs review the brief first to confirm direction, then the manuscript drafts against the brief.",
        "deprecated": False
    }
]


def main() -> None:
    with LOG.open() as f:
        data = json.load(f)

    existing_ids = {entry["id"] for entry in data["lessons"]}
    appended = 0
    for entry in NEW_LESSONS:
        if entry["id"] in existing_ids:
            print(f"SKIP (already present): {entry['id']}")
            continue
        data["lessons"].append(entry)
        appended += 1
        print(f"APPEND: {entry['id']}")

    if appended == 0:
        print("\nNo new lessons appended (all already present).")
        return

    data["_meta"]["last_updated"] = "2026-05-03"
    with LOG.open("w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nAppended {appended} new lessons. Total now: {len(data['lessons'])}.")


if __name__ == "__main__":
    main()
