# Delegation Matrix

Maps each analysis task type in `analysis_plan.json` to the K-Dense scientific skill or BioMedAgent that executes it. Used by `/analyze` Phase 4 / 5 execution.

**Pattern at runtime:**

1. Read the `delegation` field on each plan step (e.g., `scientific-skills:scikit-survival`)
2. Load that skill's `SKILL.md` as expert reference (same pattern as write-* skills reading `writing-style.md`)
3. Write code following the loaded skill's documented patterns; never write statistical code from memory

If a task type isn't in this matrix → fall back to BioMedAgent. If a task requires a resource class the host environment doesn't have → halt per Phase 4.0 resource check.

## Namespace resolution — how `scientific-skills:<name>` resolves at runtime (per L058)

Every `scientific-skills:<name>` string in this matrix (and everywhere else in CRA) is a **delegation label, not an invokable skill name**. Resolve it in this order:

1. **Native skill `<name>` (authoritative).** The `claude-scientific-skills` plugin installs the full K-Dense library (173 skills) natively; each surfaces under its **bare** name — `scikit-survival`, `statsmodels`, `scanpy`, `citation-management`, etc. That bare name is the form to load or invoke: **strip the `scientific-skills:` prefix.** (Fully-qualified `claude-scientific-skills:<name>` is the fallback only if a bare name ever collides with another plugin's skill.)
2. **Vendored copy (offline / Codex fallback only).** `skills/external/scientific-agent-skills/scientific-skills/<name>/SKILL.md` is a **version-pinned** copy for environments where the native plugin is absent (Codex packaging, offline). Read it only when the native skill is unavailable; it drifts from upstream, so never prefer it when the native skill exists.

**Coverage.** The native library is a superset of the 138 vendored skills — every vendored skill has a native namesake **except** these 10 CRA-local skills, which have no native equivalent and must be retained on any de-vendoring: `autoskill, bids, database-lookup, exa-search, hugging-science, optimize-for-gpu, paper-lookup, paperzilla, polars-bio, primekg`. Staged migration: `tools/cra-devendor.sh` (dry-run by default).

---

## Tabular clinical analysis (the bulk of CRA work)

| Task | Primary skill | Resource class | BioMedAgent fallback |
|---|---|---|---|
| Cox proportional hazards | `scientific-skills:scikit-survival` | light | optional |
| Kaplan-Meier + log-rank | `scientific-skills:scikit-survival` | light | optional |
| Restricted Mean Survival Time (RMST) | `scientific-skills:scikit-survival` | light | optional |
| Competing risks (Fine-Gray) | `scientific-skills:scikit-survival` (CompetingRisks module) | light | yes if module unavailable |
| Logistic regression (binary outcome) | `scientific-skills:statsmodels` | light | optional |
| Firth logistic (rare events) | `scientific-skills:statsmodels` (penalized) or BioMedAgent | light | yes |
| Linear regression | `scientific-skills:statsmodels` | light | optional |
| Poisson / negative binomial | `scientific-skills:statsmodels` | light | optional |
| Ordinal logistic | `scientific-skills:statsmodels` | light | yes if niche |
| GEE / mixed models | `scientific-skills:statsmodels` | light–medium | optional |
| Quantile regression | `scientific-skills:statsmodels` | light | optional |

## Propensity score / causal inference

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| PS estimation (logistic / GBM) | `scientific-skills:statsmodels` + `scientific-skills:scikit-learn` | light | optional |
| PS matching (with caliper sensitivity per L040) | `scientific-skills:statsmodels` (or `psmatch2` via R bridge) | light | yes |
| IPTW with stabilized weights | `scientific-skills:statsmodels` | light | optional |
| Doubly-robust estimation | `scientific-skills:statsmodels` | light | optional |
| Within-recipient PSM (per L039) | Same as PS matching + estimand declaration in code comments | light | optional |
| E-value (per L005) | inline computation per VanderWeele-Ding formula | light | n/a |

## Bayesian methods

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| Bayesian regression | `scientific-skills:pymc` | medium | optional |
| Hierarchical models | `scientific-skills:pymc` | medium | optional |
| Posterior predictive checks | `scientific-skills:pymc` | medium | optional |

## Healthcare-specific ML

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| Clinical prediction models | `scientific-skills:pyhealth` + `scientific-skills:scikit-learn` | light–medium | yes for deep learning |
| Survival prediction with ML | `scientific-skills:scikit-survival` | medium | optional |
| Calibration analysis | `scientific-skills:pyhealth` | light | optional |
| AUROC + BCa bootstrap CI (per L031) | `scientific-skills:scikit-learn` + `scientific-skills:statsmodels` | light | optional |
| SHAP interpretability | `scientific-skills:shap` | light–medium | yes for very large models |

## Single-cell / omics

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| scRNA-seq QC + clustering | `scientific-skills:scanpy` | ram-heavy (>32GB for >500K cells) | BioMedAgent (Modal cloud) |
| scVI integration | `scientific-skills:scvi-tools` | gpu-recommended | BioMedAgent |
| RNA velocity | `scientific-skills:scvelo` | ram-heavy + gpu-recommended | BioMedAgent |
| Cell-cell communication | `scientific-skills:scanpy` ecosystem | ram-heavy | BioMedAgent |
| Bulk RNA-seq DE | `scientific-skills:pydeseq2` | medium | optional |
| Gene regulatory networks | `scientific-skills:arboreto` | ram-heavy | BioMedAgent |
| ATAC-seq / multimodal | `scientific-skills:scanpy` + `scientific-skills:anndata` | ram-heavy | BioMedAgent |
| Drop-LOO sensitivity for scRNA (per L029, L030) | `scientific-skills:scanpy` + custom loop | ram-heavy | BioMedAgent |

## Variant / genomics

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| Variant calling (FASTQ → VCF) | n/a | gpu-recommended | **always BioMedAgent** |
| Variant annotation (VCF → annotated) | `scientific-skills:pysam` + databases | medium | BioMedAgent |
| GWAS-style analysis | dedicated tooling | ram-heavy | BioMedAgent |
| Population genetics | `scientific-skills:scikit-bio` | medium | BioMedAgent |

## Time series

| Task | Primary skill | Resource class | Fallback |
|---|---|---|---|
| Time series classification | `scientific-skills:aeon` | medium | optional |
| Time series forecasting | `scientific-skills:timesfm-forecasting` | medium–heavy | BioMedAgent |
| Physiological signals (ECG/EEG) | `scientific-skills:neurokit2` | medium | optional |

## Visualization (defer to /visualize)

`/analyze` produces structured outputs in `results_registry.json` + `figure_intent.md`. Actual figure rendering belongs to `/visualize` (next refactor). However, **diagnostic plots** during execution (residuals, calibration, Schoenfeld, balance) may be generated inline using `scientific-skills:matplotlib` or `scientific-skills:seaborn`.

| Task | Primary skill | Resource class |
|---|---|---|
| Diagnostic plots (residuals, calibration) | `scientific-skills:matplotlib` | light |
| Schoenfeld plot | `scientific-skills:scikit-survival` + matplotlib | light |
| PS balance Love plot | `scientific-skills:matplotlib` | light |

---

## Resource class definitions

| Class | Typical needs |
|---|---|
| `light` | < 4 GB RAM, no GPU, runs in seconds–minutes |
| `medium` | 4–16 GB RAM, no GPU required, runs in minutes–hour |
| `ram-heavy` | > 16 GB RAM (often > 32 GB), no GPU required, runs in hours |
| `gpu-recommended` | benefits from GPU; will run on CPU but slow (hours) |
| `gpu-required` | does not run usefully without GPU |

---

## When to escalate to BioMedAgent (instead of K-Dense)

- Multi-step pipelines (e.g., raw FASTQ → final VCF → annotated table)
- Any task marked "always BioMedAgent" above
- Any task whose K-Dense execution fails after one remediation attempt
- Any task whose resource class exceeds host environment AND user picks (b) cloud route at Phase 4.0 halt
- Any task involving non-tabular biomedical file formats (BAM, FASTQ, VCF when full pipeline needed, h5ad with > 1M cells, etc.)

BioMedAgent invocation pattern:

```python
# Inside /analyze Phase 4 execution
Task(
    subagent_type="general-purpose",
    description="Delegate to BioMedAgent",
    prompt=f"""
You are invoking the BioMedAgent skill located at
{external_path}/biomedagent/SKILL.md

The task: {plan_step.description}
Inputs: {plan_step.inputs}
Expected outputs: {plan_step.expected_outputs}
Resource constraints: {available_resources}
Output destination: data/working/biomedagent_output_<step>.csv

Execute autonomously. Return the registry-ready result JSON.
"""
)
```

---

## Updating this matrix

When a new K-Dense skill becomes available (e.g., a new method gets added to the scientific-agent-skills bundle), update this matrix in a follow-up commit. The router pulls the registry index from `skills/references/skill-registry.yaml` which auto-updates on `tools/update_skill_registry.py` run.
