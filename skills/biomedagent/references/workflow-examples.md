# Workflow Examples

These examples show how to design multi-stage workflows for common biomedical analysis
patterns. Each example follows the WorkflowDesigner format from Phase 1.

## Example 1: Variant Calling Pipeline (Omics)

**User request:** "Identify pathogenic variants on data (reads1.fq.gz, reads2.fq.gz)"

**Workflow:**
```
Stage 0: Align reads to the genome
  Tool: bwa_samtools_sambamba
  Input: reads1.fq.gz, reads2.fq.gz, file_type_flag="normal"
  Output: aligned.bam
  Description: Use BWA for alignment, Samtools for SAM-to-BAM conversion,
  Sambamba for sorting.

Stage 1: Mark duplicates
  Tool: gatk_markduplicates
  Input: aligned.bam
  Output: deduped.bam
  Description: Identify and mark duplicate reads to reduce PCR artifacts.

Stage 2: Base Quality Score Recalibration
  Tool: gatk_bqsr
  Input: deduped.bam
  Output: recalibrated.bam
  Description: Recalibrate base quality scores for more accurate variant calling.

Stage 3: Call variants
  Tool: bam_to_vcf
  Input: recalibrated.bam
  Output: variants.vcf
  Description: Use GATK HaplotypeCaller to identify genomic variants.

Stage 4: Annotate variants
  Tool: intervar_mutation_annotation
  Input: variants.vcf
  Output: annotated_variants.txt
  Description: Annotate variants with clinical significance using InterVar.

Stage 5: Identify pathogenic variants
  Tool: None (custom Python code)
  Input: annotated_variants.txt
  Output: pathogenic_variants.csv, summary_report.txt
  Description: Filter for pathogenic and likely pathogenic variants. Extract gene
  names and associated diseases. Generate a summary report.
```

**Python implementation pattern:**
```python
def action0(fastq1, fastq2):
    """Align reads to genome — implements bwa_samtools_sambamba"""
    import subprocess
    # BWA alignment
    subprocess.run(["bwa", "mem", "-t", "4", "ref.fa", fastq1, fastq2],
                   stdout=open("aligned.sam", "w"))
    # Convert to BAM and sort
    subprocess.run(["samtools", "view", "-bS", "aligned.sam"], stdout=open("aligned.bam", "w"))
    subprocess.run(["samtools", "sort", "aligned.bam", "-o", "sorted.bam"])
    return "sorted.bam"
```

---

## Example 2: Machine Learning Classification (ML)

**User request:** "Use random forest to predict heart disease from heart_disease.csv"

**Workflow:**
```
Stage 0: Split data into training and test sets
  Tool: split_data_tool
  Input: heart_disease.csv
  Output: train.csv, test.csv
  Description: Split the dataset 80/20 for training and testing.

Stage 1: Feature selection
  Tool: featureselect
  Input: train.csv, test.csv, target="target", n=10
  Output: train_selected.csv, test_selected.csv
  Description: Select top 10 most informative features.

Stage 2: Train and predict with Random Forest
  Tool: randomforest
  Input: train_selected.csv, test_selected.csv, target="target"
  Output: predictions.csv
  Description: Train Random Forest on training set, predict on test set.
  Output adds a "Predicted" column.

Stage 3: Calculate evaluation metrics
  Tool: calculate_classify_metrics
  Input: predictions.csv, target_col="target", predicted_col="Predicted"
  Output: metrics.csv, accuracy, precision, recall, f1_score
  Description: Calculate accuracy, precision, recall, F1 score.

Stage 4: Plot ROC curve
  Tool: ROC
  Input: predictions.csv
  Output: roc_curve.png
  Description: Generate ROC curve visualization.
```

**Python implementation pattern:**
```python
def action0(dataset_path):
    """Split data — implements split_data_tool"""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    df = pd.read_csv(dataset_path)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    train.to_csv("train.csv", index=False)
    test.to_csv("test.csv", index=False)
    return "train.csv", "test.csv"

def action2(train_path, test_path, target="target"):
    """Random Forest classification — implements randomforest"""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    X_train = train.drop(columns=[target])
    y_train = train[target]
    X_test = test.drop(columns=[target])
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    test["Predicted"] = clf.predict(X_test)
    test.to_csv("predictions.csv", index=False)
    return "predictions.csv"
```

---

## Example 3: Statistical Analysis (Statistics)

**User request:** "Perform a t-test comparing gene expression between treatment and control groups in expression_data.csv"

**Workflow:**
```
Stage 0: Load and validate data
  Tool: None (custom code)
  Input: expression_data.csv
  Output: validated_data.csv, group_summary.json
  Description: Load the CSV, verify it has group labels and expression values,
  produce summary statistics per group.

Stage 1: Perform t-test
  Tool: None (custom code using scipy.stats)
  Input: validated_data.csv
  Output: ttest_results.csv
  Description: For each gene, perform independent samples t-test between
  treatment and control. Record t-statistic, p-value, and mean difference.

Stage 2: Multiple testing correction
  Tool: None (custom code)
  Input: ttest_results.csv
  Output: corrected_results.csv
  Description: Apply Benjamini-Hochberg FDR correction. Mark genes with
  adjusted p-value < 0.05 as significant.

Stage 3: Visualization
  Tool: None (custom code using matplotlib)
  Input: corrected_results.csv
  Output: volcano_plot.png, significant_genes.csv
  Description: Create volcano plot showing fold change vs. -log10(p-value).
  Export list of significant genes.
```

---

## Example 4: Survival Analysis (Visualization)

**User request:** "Plot survival curve from clinical_data.csv using time, status, and treatment_group columns"

**Workflow:**
```
Stage 0: Plot survival curve
  Tool: survival_curve
  Input: clinical_data.csv, time="time", event="status", variable="treatment_group"
  Output: survival_curve.png
  Description: Generate Kaplan-Meier survival curves stratified by treatment group,
  with log-rank test p-value.
```

**Python implementation:**
```python
def action0(data_path, time_col, event_col, variable_col):
    """Survival curve — implements survival_curve"""
    import pandas as pd
    import matplotlib.pyplot as plt
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test

    df = pd.read_csv(data_path)
    fig, ax = plt.subplots(figsize=(10, 6))
    kmf = KaplanMeierFitter()

    groups = df[variable_col].unique()
    for group in groups:
        mask = df[variable_col] == group
        kmf.fit(df[mask][time_col], df[mask][event_col], label=str(group))
        kmf.plot_survival_function(ax=ax)

    # Log-rank test if exactly 2 groups
    if len(groups) == 2:
        g1 = df[df[variable_col] == groups[0]]
        g2 = df[df[variable_col] == groups[1]]
        result = logrank_test(g1[time_col], g2[time_col],
                              g1[event_col], g2[event_col])
        ax.set_title(f"Survival Curve (log-rank p={result.p_value:.4f})")

    ax.set_xlabel("Time")
    ax.set_ylabel("Survival Probability")
    plt.tight_layout()
    plt.savefig("survival_curve.png", dpi=150)
    plt.close()
    return "survival_curve.png"
```

---

## Example 5: Single-Cell RNA-seq Analysis (Omics)

**User request:** "Analyze single-cell RNA-seq data from my 10x Chromium run"

**Workflow:**
```
Stage 0: Preprocess with QC filtering
  Tool: seurat_preprocess (or scanpy equivalent)
  Input: genes.tsv, matrix.mtx, barcodes.tsv
  Output: qc_metrics.png, variable_features.png, filtered_data.h5ad
  Description: Filter cells by QC metrics (mitochondrial %, gene count, UMI count),
  normalize, find variable features.

Stage 1: Clustering
  Tool: seurat_clustering (or scanpy equivalent)
  Input: filtered_data.h5ad
  Output: clusters_umap.png, marker_genes.csv, heatmap.png
  Description: PCA, neighbor graph, Leiden/Louvain clustering, UMAP visualization,
  find marker genes per cluster.

Stage 2: Cell type annotation
  Tool: singleR_annotation (or manual annotation)
  Input: clustered_data.h5ad
  Output: annotated_umap.png, cell_type_counts.csv
  Description: Annotate clusters with cell types using reference datasets.

Stage 3: Pseudotime trajectory
  Tool: pseudotime
  Input: annotated_data.h5ad
  Output: trajectory.png
  Description: Construct cell trajectory to understand differentiation paths.
```

---

## Example 6: Differential Expression + Pathway Enrichment (Omics)

**User request:** "Find differentially expressed genes and enriched pathways from my microarray CEL files"

**Workflow:**
```
Stage 0: Extract expression matrix from CEL files
  Tool: cel2matrix
  Input: CEL_folder, output_folder, GPL_platform
  Output: expression_matrix.csv
  Description: Process CEL files to get gene-level expression matrix.

Stage 1: Differential expression analysis
  Tool: deg
  Input: expression_matrix.csv, group_file.csv
  Output: deg_results.csv
  Description: Identify differentially expressed genes between conditions.

Stage 2: Gene set enrichment
  Tool: KOBAS_enrichment
  Input: significant_genes.txt (from DEG results)
  Output: GO_enrichment.csv, KEGG_enrichment.csv
  Description: GO and KEGG pathway enrichment analysis.

Stage 3: Visualize enrichment results
  Tool: enrichment2bubble
  Input: GO_enrichment.csv, p_value=0.05
  Output: enrichment_bubble.png
  Description: Create bubble plot showing enriched pathways.
```

---

## Workflow Design Anti-Patterns

Avoid these common mistakes:

1. **Returning DataFrames** — Always save to file and return the path
2. **Skipping preprocessing** — Most raw data needs cleaning before analysis
3. **Using tools outside the catalog** — If it's not in the tool list, implement it as custom code
4. **Ignoring data flow** — Every stage's input must trace back to a file or previous output
5. **Over-engineering** — Simple requests can be a single stage of pure Python code
6. **Missing visualization** — Most analyses benefit from at least one plot
