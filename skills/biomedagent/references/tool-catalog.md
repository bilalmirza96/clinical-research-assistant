# BioMedAgent Tool Catalog

This catalog contains all 65 biomedical analysis tools from the BioMedAgent system.
Each tool is documented with its inputs, outputs, and description. Use this catalog
during the ToolScorer and WorkflowDesigner steps to select and chain tools.

## Table of Contents

### By Category

**Genomics & Alignment:**
bwa_samtools_sambamba, fastq_to_bam, fastqc, gatk_bqsr, gatk_markduplicates,
HISAT2, Samtools, stringtie, stringtie_merge, gffcompare, cellranger_count

**Variant Calling & Annotation:**
bam_to_vcf, bam_to_vcf_mutect2, vcf_to_maf, maf_filter, maf_to_drug,
intervar_mutation_annotation, gene_to_diseases, signature

**Expression & Omics:**
cel2matrix, deg, kallisto, GSEA, ssGSEA, KOBAS_enrichment, wgcna, mcpcounter

**Single-Cell:**
seurat_preprocess, seurat_preprocess_rds, seurat_clustering, singleR_annotation,
pseudotime

**Machine Learning — Classification:**
adaboost, decisiontree, gaussianNB, gbdt, lda, logistic, mlp, qda, randomforest, svm

**Machine Learning — Regression:**
regression, randomforest_regression, svm_regression

**Machine Learning — Clustering:**
kmeans, hierarchical

**ML Utilities:**
featureselect, split_data_tool, calculate_classify_metrics, mse_calculate_tool

**Visualization:**
ROC, venn, survival_curve, enrichment2bubble

**Metagenomics:**
metagenome_annotation, metagenome_get_taxon_file, metagenome_merge, lefse

**Pathology / Cell Segmentation:**
basicunet, basicunet_predict, hovernet, hovernet_predict, mihatp_hovernet,
mihatp_hovernet_predict

---

## Python Library Mapping

When implementing these tools in Python, use these library equivalents:

| Tool Category | Python Libraries |
|---|---|
| Classification (adaboost, svm, etc.) | `scikit-learn` (sklearn.ensemble, sklearn.svm, etc.) |
| Regression | `scikit-learn` (sklearn.linear_model, sklearn.ensemble) |
| Clustering (kmeans, hierarchical) | `scikit-learn` (sklearn.cluster) |
| Feature selection | `scikit-learn` (sklearn.feature_selection) |
| Data splitting | `scikit-learn` (sklearn.model_selection.train_test_split) |
| Metrics (accuracy, F1, etc.) | `scikit-learn` (sklearn.metrics) |
| Survival analysis | `lifelines` (KaplanMeierFitter, CoxPHFitter) |
| Statistics (t-test, etc.) | `scipy.stats` |
| Differential expression | `pydeseq2` or `scanpy` (scanpy.tl.rank_genes_groups) |
| Gene set enrichment | `gseapy` |
| Single-cell analysis | `scanpy`, `anndata` |
| Visualization | `matplotlib`, `seaborn`, `matplotlib_venn` |
| Genomics CLI tools | `subprocess` calls to `bwa`, `samtools`, `gatk`, `cellranger` |
| Pathology | `torch`, custom model loading |
| Metagenomics | `subprocess` calls to `kraken2`, `metaphlan`, etc. |
| File I/O | `pandas` (CSV/TSV), `anndata` (h5ad), `pysam` (BAM/VCF) |

---

### adaboost
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is AdaBoost algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### bam_to_vcf
**Description:** GATK haplotype caller to identify genomic variants, it converting BAM alignment files of individual samples into VCF (Variant Call Format) format
**Inputs:**
- `bam_file` (file): BAM alignment files
**Outputs:**
- `vcf_file` (file): Variant Call Format files

### bam_to_vcf_mutect2
**Description:** GATK mutect2 caller to identify somatic variants, it converting BAM alignment files of paired samples (tumor and normal) into VCF (Variant Call Format) format
**Inputs:**
- `bam_file` (file): BAM alignment files of tumor
- `bam_file` (file): BAM alignment files of normal
**Outputs:**
- `vcf_file` (file): somatic Variant Call Format files

### basicunet
**Description:** Construct a cell segmentation model with basicunet using the training dataset of pathological images.
**Inputs:**
- `training_dataset_path` (file): training dataset path, Compressed file containing training data
- `cell_type` (string): The types of cells to be divided can be inflammatory, epithelial, spindle shaped, all, where inflammatory, epithelial and spindle shaped represent inflammatory cells respectively. epithelial cell, spindle shaped cell, and all stands for dividing all type of cells.
**Outputs:**
- `model_file_path` (file): cell segmentation model file

### basicunet_predict
**Description:** Using basicunet model to perform cell segmentation on testing dataset of pathological images.
**Inputs:**
- `testing_dataset_path` (file): testing dataset path, Compressed file containing testing data
- `model_file_path` (file): cell segmentation model file
**Outputs:**
- `result_file_path` (folder path): cell segmentation result file path

### bwa_samtools_sambamba
**Description:** This tool convert fastq files into alignment BAM files. It firstly uses BWA for sequence alignment, then use Samtools convert the alignment results into BAM file, and finally uses Sambamba for sorting the Bam file.
**Inputs:**
- `fastq_file1` (file): In high-throughput sequencing, one of the two related FASTQ files obtained contains the sequence information and quality scores of one end of a DNA fragment.
- `fastq_file2` (file): In high-throughput sequencing, one of the two related FASTQ files obtained contains the sequence information and quality scores of one end of a DNA fragment.
- `file_type_flag` (string): The type of fastq file ("tumor" or "normal")
**Outputs:**
- `bam_file` (file): BAM alignment files

### calculate_classify_metrics
**Description:** This is a tool for calculating evaluation metrics for classification tasks. Input a prediction file and input the column name of the label column and the column name of the prediction column in the prediction file. This tool is then used to calculate the evaluation metrics for the classification. The tool finally outputs a result file of evaluation metrics. And output four floating point numbers, namely accuracy, precision, recall, and F1 score.
**Inputs:**
- `csv_file` (file): This is the input csv file. It contains label columns and predicted value columns
- `target_col` (string): This is the column name of the label column in the input csv file. it is a string
- `predicted_col` (string): This is the column name of the predicted value column in the input csv file. it is a string
**Outputs:**
- `result_csv_file` (file): The result file contains the evaluation metrics of the classification task, such as TP, TN, FP, FN, accuracy, precision, recall, f1 score. It is a csv file
- `accuracy` (float): This is the output accuracy value. It is a floating point number
- `precision` (float): This is the output precision value. It is a floating point number
- `recall` (float): This is the output recall value. It is a floating point number
- `f1_score` (float): This is the output f1_score value. It is a floating point number

### cel2matrix
**Description:** Cel2matrix is a tool for extracting expression profile data from CEL files and annotating probes.
**Inputs:**
- `CEL_file` (Folder path): The folder containing CEL format files for chip data.
- `out_folder` (Folder path): A unique run id and output folder name [a-zA-Z0-9_-]+
- `gpl_name` (string): Probe annotation corresponding to CEL file.
**Outputs:**
- `matrix_file` (file): The expression profile file extracted from the CEL format file of chip data, in the form of gene, is listed as a sample.

### cellranger_count
**Description:** cellranger count takes FASTQ files and performs alignment, filtering, barcode counting, and UMI counting. It uses the Chromium cellular barcodes to generate feature-barcode matrices, determine clusters, and perform gene expression analysis.
**Inputs:**
- `fastq_files` (file): compressed file path to input FASTQ data(A sample contains I1:SRRXXX_S1_LOO1_I1_001.fastq.gz;R1:SRRXXX_S1_LOO1_R1_001.fastq.gz;R2:SRRXXX_S1_LOO1_R2_001.fastq.gz)
- `sample_name` (string): Prefix of the filenames of FASTQs to select
**Outputs:**
- `filtered_feature_bc_matrix_file` (file): Filtered Barcode Information HDF5 Format File.
- `raw_feature_bc_matrix_file` (file): Raw Barcode Information HDF5 Format File.

### decisiontree
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set.
The algorithm used is Decision tree algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### deg
**Description:** For extracting differentially expressed genes from samples under two different experimental conditions.
**Inputs:**
- `exp_file` (file): gene expression profile data file.
- `group_file` (file): File Contains grouping information for samples.
**Outputs:**
- `deg_file` (file): The set of genes significantly differentially expressed under the two experimental conditions.

### enrichment2bubble
**Description:** enrichment2bubble is a tool to Display the results of pathway enrichment using a bubble chart.
**Inputs:**
- `enrichment_file` (file): The enrichment text file. The following column names must be included: Term, Input_number, Enrich_ratio, P_Value
- `p_value` (str): The column name in enrichment file where the p-value is located.
- `term` (str): The column name in enrichment file where the pathway is located.
- `input_number` (str): The column name in enrichment file where the input number is located.
- `background_number` (str): The column name in enrichment file where the background number is located.
**Outputs:**
- `out_bubble_image` (file): The bubble figure.

### fastqc
**Description:** fastqc is a tool used for quality control of high throughput sequence data. It provides a simple way to perform quality checks on raw sequence data coming from high throughput sequencing pipelines.
**Inputs:**
- `fq1_data` (file): The input file is a FASTQ file containing the forward reads from a paired-end sequencing run. This file contains raw sequencing reads.
- `fq2_data` (file): The input file is a FASTQ file containing the reverse reads from a paired-end sequencing run. This file contains raw sequencing reads
**Outputs:**
- `fq1_data_txt` (file): The output file is a text file that contains detailed quality metrics for the forward reads from the input sequence data. It includes various statistics and data points to help assess the quality of the data.
- `fq2_data_txt` (file): The output file is a text file that contains detailed quality metrics for the reverse reads from the input sequence data. It includes various statistics and data points to help assess the quality of the data.
- `fq1_summary_txt` (file): The output file is a summary text file that provides a high-level overview of the quality metrics for the forward reads from the input sequence data. It includes key quality statistics and indicators.
- `fq2_summary_txt` (file): The output file is a summary text file that provides a high-level overview of the quality metrics for the reverse reads from the input sequence data. It includes key quality statistics and indicators.

### fastq_to_bam
**Description:** This tool is a pipeline that uses the following tools in sequence:1bwa_samtools_sambamba 2gatk_markduplicates 3gatk_bqsr, complete the conversion from fastq to bam file, gatk_markduplicates is used to identify and label duplicate reads generated during the PCR process to avoid bias in subsequent analysis. Finally, gatk_bqsr recalibrates the base mass fraction in the BAM file
**Inputs:**
- `fastq_file1` (file): One of the paired sequencing, Genetic testing data files for patients with genetic diseases
- `fastq_file2` (file): One of the paired sequencing, Genetic testing data files for patients with genetic diseases
- `file_type_flag` (string): The type of fastq file ("tumor" or "normal")
**Outputs:**
- `bam_file` (file): BAM file that has had duplicates removed and Base Quality Score Recalibration (BQSR)

### featureselect
**Description:** Input two csv files with m columns, which are the training set and the test set. And input the column name of the label column, and the number of features to be selected, n, where n is less than m. Use this tool to perform feature selection on the training set. Then filter the feature columns of the test set according to the n feature columns selected from the training set. The output result files are two csv files, which are the training set and test set files after feature extraction. Each csv file contains filtered n feature columns and label columns.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of m columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of m columns.
- `target` (string): This is the column name of the input label column. It is a string
- `n` (int): This is the number of feature columns that need to be filtered out. It is an integer type
**Outputs:**
- `train_result_file` (file): This is the result file of the feature extraction of the training set. It is a csv file with n+1 columns in total. It contains the extracted n highly correlated feature columns and a label column.
- `test_result_file` (file): This is the result file of the feature extraction of the test set. It is a csv file with n+1 columns in total. It contains the extracted n highly correlated feature columns and a label column.

### gatk_bqsr
**Description:** A tool in GATK for Base Quality Score Recalibration (BQSR)
**Inputs:**
- `bam_file1` (file): BAM alignment files
**Outputs:**
- `bam_file2` (file): BAM alignment files

### gatk_markduplicates
**Description:** A tool in GATK to identify and mark duplicate reads in alignment bam file.
**Inputs:**
- `bam_file1` (file): BAM alignment files
**Outputs:**
- `bam_file2` (file): BAM alignment files

### gaussianNB
**Description:** Input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. The output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is GaussianNB algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted".

### gbdt
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set.
The algorithm used is GBDT algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### gene_to_diseases
**Description:** The tool utilizes pathgenic variant gene names to perform searches within the OMIM database
**Inputs:**
- `pathogenic_genes_file` (file): maf file or json file include pathgenic variant gene name
**Outputs:**
- `diseases_name` (string): a list include names of diseases that may be caused by genetic mutations

### gffcompare
**Description:** It is a tool for comparing and merging GTF/GFF format files.
**Inputs:**
- `gtf_file` (file): This is StringTie's output file containing information about the assembled transcripts, usually generated by StringTie's merge operation.
**Outputs:**
- `merged_stats` (file): Includes statistics on the number of transcripts matched, the number of new transcripts, the number of known transcripts, etc.
- `merged_loci` (file): Each of these transcripts contains detailed information corresponding to a gene in the reference genome.
- `merged_tracking` (file): Detailed information on the correspondence between the input transcripts and the genes in the reference genome.

### GSEA
**Description:** Detect the expression changes of differentially expressed gene sets under specific conditions through predefined gene sets, thereby revealing the biological functions influenced by these differentially expressed genes.
**Inputs:**
- `DEG_file` (file): Differentially expressed genes under specific conditions.
- `Predefined_gene_set_file` (file): This file contains information on biological functions and corresponding gene sets, which can be defined by users themselves, such as KEGG pathway-gene and GO term-gene relationships.
**Outputs:**
- `GSEA_file` (file): GSEA enrichment result file, including which biological functions were activated or inhibited by differentially expressed genes.

### hierarchical
**Description:** This is a clustering tool. Input a csv file and also enter the number of clusters. Use this tool to perform cluster analysis on csv files and output the clustering result file and a silhouette score value. Compared with the input csv file, the clustering result file adds the clustered category column "Cluster" column. The algorithm used is hierarchical clustering algorithm.
**Inputs:**
- `data_csv_file` (file): This is the input original data set. It is a csv file with n columns.
- `n_clusters` (integer): This is the number of clusters to be clustered. It is an integer.
**Outputs:**
- `result_csv_file` (file): This is the result file of the clustering. It is a csv file with (n+1) columns. The column name of the new column is "Cluster"
- `silhouette` (float): This is the average silhouette score of the output. It is a floating point number between -1 and 1 used to evaluate the quality of the clustering.

### HISAT2
**Description:** A tool for aligning RNA sequences to a reference genome.
**Inputs:**
- `FASTQ_file1` (file): This is the forward read of the FASTQ file and contains the raw RNA sequence data from sequencing.
- `FASTQ_file2` (file): This is the reverse read FASTQ file containing the reverse read sequence corresponding to the first file.
**Outputs:**
- `SAM_file` (file): Results after alignment of FASTQ sequence data to the reference genome.

### hovernet
**Description:** Construct a cell segmentation model with hovernet using the training dataset of pathological images.
**Inputs:**
- `training_dataset_path` (file): training dataset path, Compressed file containing training data
- `cell_type` (string): The types of cells to be divided can be inflammatory, epithelial, spindle shaped, all, where inflammatory, epithelial and spindle shaped represent inflammatory cells respectively. epithelial cell, spindle shaped cell, and all stands for dividing all type of cells.
**Outputs:**
- `model_file_path` (file): cell segmentation model file

### hovernet_predict
**Description:** Using hovernet model to perform cell segmentation on testing dataset of pathological images.
**Inputs:**
- `testing_dataset_path` (file): testing dataset path, Compressed file containing testing datami
- `model_file_path` (file): cell segmentation model file
**Outputs:**
- `result_file_path` (folder path): cell segmentation result file path

### intervar_mutation_annotation
**Description:** This tool analyzes genetic mutations in VCF files and automatically queries the InterVar database to determine whether these mutations are pathogenic.
**Inputs:**
- `vcf_file` (file): Variant Call Format files
**Outputs:**
- `annotated_file` (file): The file is a JSON array containing information about genetic mutations, where "Pathogenicity" being "Pathogenic" indicates that the gene is a disease-causing gene.

### kallisto
**Description:** kallisto is a tool used for quantifying transcript abundances from RNA-seq data.
**Inputs:**
- `fq1_data` (file): The input file is a FASTQ file containing the forward reads from an RNA-seq experiment. This file contains raw sequencing reads.
- `fq2_data` (file): The input file is a FASTQ file containing the reverse reads from an RNA-seq experiment. This file contains raw sequencing reads.
**Outputs:**
- `out_file` (file): The output file is a tab-delimited text file containing the quantification results. Each row represents a gene and its corresponding expression abundance value.

### kmeans
**Description:** This is a clustering tool. Input a csv file and also enter the number of clusters. Use this tool to perform cluster analysis on csv files and output the clustering result file and a silhouette score value. Compared with the input csv file, the clustering result file adds the clustered category column "Cluster" column. The algorithm used is kmeans clustering algorithm.
**Inputs:**
- `data_csv_file` (file): This is the input original data set. It is a csv file with n columns.
- `n_clusters` (integer): This is the number of clusters to be clustered. It is an integer.
**Outputs:**
- `result_csv_file` (file): This is the result file of the clustering. It is a csv file with (n+1) columns. The column name of the new column is "Cluster"
- `silhouette` (float): This is the average silhouette score of the output. It is a floating point number between -1 and 1 used to evaluate the quality of the clustering.

### KOBAS_enrichment
**Description:** Gene Set Enrichment (GSE) to resolve the enriched biological functions for a gene set.
**Inputs:**
- `gene_list_file` (file): A gene set that will be used to perform functional enrichment analysis(No preprocessing required).
**Outputs:**
- `GO_enrichment_result` (file): GO term affected by the input gene set.
- `KEGG_enrichment_result` (file): KEGG pathway affected by the input gene set.

### lda
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is LDA algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### lefse
**Description:** lefse is a tool used for the analysis of high-dimensional biomarker data. It is particularly useful in the field of microbiome research, where it can identify and interpret biomarkers such as taxonomic classifications that exhibit significant differences in abundance across various samples or conditions.
**Inputs:**
- `feature_file` (file): A text file containing feature abundance. The file's row names are features and column names are samples.(Necessary)
- `sample_file` (file): The sample information text file. The file's row names are samples and column names are sample metadata such as grouping information.(Necessary)
- `tax_file` (file): A text file containing taxonomic information. The file's row names are features and column names are taxonomic classes.(Necessary)
- `method` (str): Statistical Analysis Methods.("lefse", "rf", "metastat", "metagenomeSeq", "KW", "KW_dunn", "wilcox", "t.test", "anova", "scheirerRayHare", "lm", "ancombc2", "ALDEx2_t", "ALDEx2_kw", "DESeq2", "linda", "maaslin2", "betareg", "lme", "glmm", "glmm_beta"),default "lefse"
- `group` (str): The column name where grouping information is located in sample_file.(Necessary)
- `alpha` (number): default 0.05;significance threshold to select taxa when method is "lefse" or "rf"; or used to generate significance letters when method is 'anova' or 'KW_dunn' like the alpha parameter in cal_diff of trans_alpha class.
- `taxa_level` (str): default "all"; 'all' represents using abundance data at all taxonomic ranks; For testing at a specific rank, provide taxonomic rank name, such as "Genus". If the provided taxonomic name is neither 'all' nor a colname in tax_table of input dataset, the function will use the features in input microtable$otu_table automatically.
- `p_adjust_method` (str): p.adjust method("holm", "hochberg", "hommel", "bonferroni", "BH", "BY","fdr", "none"),default "fdr". When p_adjust_method = "none"’, P.adj is same with P.unadj
**Outputs:**
- `out_lefse_file` (file): A text file including results of LEfSe.

### logistic
**Description:** input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is logistic algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The  column name of the predicted value column is "Predicted"

### maf_filter
**Description:** This tool can filter out pathogenic mutation genes from MAF files.
**Inputs:**
- `maf_file` (file): Mutation annotation information (MAF) format file
**Outputs:**
- `filtered_maf_file` (file): Mutation annotation information (MAF) format file filtered by maf_filter tool

### maf_to_drug
**Description:** A querying tool that returns a list of drugs related to a OncoKB query items. The tool accepts a maf file and returns a two-dimensional list, each element of subarray is a dictionary consisting of two key-value pairs: drug and level.
**Inputs:**
- `maf_file` (file): maf file
**Outputs:**
- `drugs` (list): Two-dimensional list, each element of subarray is a dictionary consisting of two key-value pairs: drug and level.

### mcpcounter
**Description:** quantification of the absolute abundance of immune cells from gene expression data
**Inputs:**
- `gene_expression` (file): gene expression profile in tab-delimited text format.
**Outputs:**
- `out_file` (file): The output file is a tab-delimited text file. It includes different types of immune cells and absolute abundance.

### metagenome_annotation
**Description:** metagenome_annotation is a tool to conduct taxonomic identification and quantitative analysis of metagenomic data by using Kraken2 and Bracken, which can obtain the file including count data at the species level for the sample, as well as the taxonomic file.
**Inputs:**
- `id` (str): The sample name.
- `type` (str): The type of input data files,"paired" for Paired-end sequencing and "single" for Single-end sequencing.
- `db` (str): The database used for annotaion. kraken2_16S is used for the annotation of 16S sequencing data.
- `fq1` (file): A fastq file.
- `fq2` (file): A fastq file. If type="single",fq2 is the default null value.
**Outputs:**
- `out_taxon_file` (file): A text file containing taxonomic results at seven hierarchical levels.
- `out_count_file` (file): A text file including count data at the species level for the sample.

### metagenome_get_taxon_file
**Description:** metagenome_get_taxon_file is a tool to merging multiple taxonomic files from metagenome_annotation into one file which can be used for LEfSe analysis. All the taxonomic files should be placed individually in a single directory.
**Inputs:**
- `work_dir` (str): The absolute path where the input taxonomic files are located such as "/workdir".
**Outputs:**
- `out_merge_taxon_file` (file): A text file containing taxonomic results at seven hierarchical levels in all the samples' taxonomic files.

### metagenome_merge
**Description:** metagenome_merge is a tool for merging multiple similar files which should be placed individually in a single directory , capable of combining multiple out_count_files obtained from metagenome_annotation into a single count matrix file.
**Inputs:**
- `path` (str): The absolute path where the input taxonomic files are located, such as "/workdir/".
- `item` (str): Specifications of the columns used for merging.
**Outputs:**
- `out_merge_count_file` (file): A text file containing taxonomic results at seven hierarchical levels.

### mihatp_hovernet
**Description:** Construct a cell segmentation model with mihatp_hovernet using the training dataset of pathological images.
**Inputs:**
- `training_dataset_path` (file): training dataset path, Compressed file containing training data
- `cell_type` (string): The types of cells to be divided can be inflammatory, epithelial, spindle shaped, all, where inflammatory, epithelial and spindle shaped represent inflammatory cells respectively. epithelial cell, spindle shaped cell, and all stands for dividing all type of cells.
**Outputs:**
- `model_file_path` (file): cell segmentation model file

### mihatp_hovernet_predict
**Description:** Using mihatp_hovernet model to perform cell segmentation on testing dataset of pathological images.
**Inputs:**
- `testing_dataset_path` (file): testing dataset path, Compressed file containing testing data
- `model_file_path` (file): cell segmentation model file
**Outputs:**
- `result_file_path` (folder path): cell segmentation result file path

### mlp
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set.
The algorithm used is MLP algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### mse_calculate_tool
**Description:** For testing logistic regression tasks, mean square error should be used as much as possible for logistic regression tasks. Input a csv file. And input the column name of the label column and the column name of the predicted value column in the csv file. Then use this tool to calculate the MSE of the prediction and output a floating point number of MSE.
**Inputs:**
- `csv_file` (file): This is the input csv file. It contains label columns and predicted value columns
- `target_col` (string): This is the column name of the label column in the input csv file. it is a string
- `predicted_col` (string): This is the column name of the predicted value column in the input csv file. it is a string
**Outputs:**
- `accuracy` (float): This is the output MSE value. It is a floating point number

### pseudotime
**Description:** Pseudotime is a tool used to construct the trajectory of changes between cells to reshape the process of cell changes over time.
**Inputs:**
- `annotation_file` (file): A preprocessed RDS file with cell clustering annotations.
**Outputs:**
- `cell_trajectory_image` (file): The image file contains images colored with pseudotime values and colored with cell types.

### qda
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is QDA algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### randomforest
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is randomforest algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### randomforest_regression
**Description:** This is a tool for regression. Input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. The output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is randomforest algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### regression
**Description:** A linear regression model tool,This tool should be called directly without the need for an "import" statement. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set.
The algorithm used is linear regression algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted".

### ROC
**Description:** ROC is a tool to plot receiver operating characteristic curve.
**Inputs:**
- `input_file` (file): A text file. The first column is the classification label, and the other columns are different variables along with their corresponding observed values.
**Outputs:**
- `out_ROC_file` (file): The ROC curve figure.

### Samtools
**Description:** It is a toolset for working with SAM and BAM files.
**Inputs:**
- `SAM_file` (file): Contains sequence alignment results generated by HISAT2 or other alignment tools.
**Outputs:**
- `BAM_file` (file): The BAM format is a binary version of the SAM file, which takes up less space and is faster to read and process.

### seurat_clustering
**Description:** Seurat_clustering is a tool for cell clustering of 10x single-cell transcriptome data generated by Cell Ranger.
**Inputs:**
- `filtered_file` (file): Quality controlled and standardized seurat objects.
**Outputs:**
- `clusters_feature_image` (file): The image contains the expression level of some markers in all cluster groups
- `clusters_Marker_file` (file): The csv file is the matrix composed of the top 10 differentially expressed genes in each cluster.
- `clusters_HeatMap_image` (file): Heat map of the top 10 differentially expressed genes in each cluster.
- `clusters_umap_image` (file): UMAP of cluster groups.
- `clusters_data_file` (file): Seruat objects after clustering, including barcodes, genes, and expression.

### seurat_preprocess
**Description:** seurat_preprocess is a single cell data preprocessing tool based on QC indicators for cell selection and filtering, data normalization and scaling, and detection of highly variable features.
**Inputs:**
- `genes_file` (file): The genes information file contains gene name and gene ID.
- `matrix_file` (file): The matrix file is an mtx file that stores matrix representation data in sparse matrix format.
- `barcodes_file` (file): The barcodes information tsv file contains all cellular barcodes present for that sample. Barcodes are listed in the order of data presented in the matrix file (i.e. these are the column names).
**Outputs:**
- `QC_metrics_image` (file): QC indicators visualization.("nFeature_RNA", "nCount_RNA", "percent.mt")
- `variable_features_image` (file): The figure of feature subsets with high intercellular variability.
- `filtered_file` (file): Quality controlled and standardized seurat objects.

### seurat_preprocess_rds
**Description:** seurat_preprocess is a single cell data preprocessing tool based on QC indicators for cell selection and filtering, data normalization and scaling, and detection of highly variable features.
**Inputs:**
- `rds_file` (file): 10x single-cell transcriptome data created using seruat
**Outputs:**
- `QC_metrics_image` (file): QC indicators visualization.("nFeature_RNA", "nCount_RNA", "percent.mt")
- `variable_features_image` (file): The figure of feature subsets with high intercellular variability.
- `filtered_file` (file): Quality controlled and standardized seurat objects.

### signature
**Description:** signature is a tool used for analyzing somatic variants in samples and determining the abundance of mutational signatures.
**Inputs:**
- `sig_input` (file): The input file is a tab-delimited text file containing genetic variant information for samples. It includes columns for sample ID, chromosome, position, reference allele, and alternate allele.
- `bsg_type` (string): This parameter specifies the reference genome to be used for variant annotation. It can be either "BSgenome.Hsapiens.UCSC.hg19" or "BSgenome.Hsapiens.UCSC.hg38".
**Outputs:**
- `out_file` (file): The output file is a tab-delimited text file containing the results of the mutational signature analysis. It includes the sample ID and the abundance of mutational signatures observed in the samples.

### singleR_annotation
**Description:** singleR_annotation is a tool for cell type recognition from single-cell RNA sequencing data using a reference transcriptome dataset.
**Inputs:**
- `clusters_file` (file): Seurat objects after preprocessing, dimensionality reduction, and clustering.
**Outputs:**
- `annotion_umap_image` (file): UMAP diagram automatically annotated by SingleR.
- `scores_within_cells_image` (file): Heat map of cell scores in an annotated label.
- `annotation_file` (file): Annotated single-cell data, including annotated labels, scores, and other data.

### split_data_tool
**Description:** Input a csv file, which is the original data set. The column name of the label column is "Target". Use this tool to divide this csv file into a training set and a test set, and then output the result files of the training set and test set.
The default split ratio for the tool is 0.8-0.2.File loading has been implemented internally within the tool, and no additional file loading is required before the tool.
**Inputs:**
- `dataset_csv_file` (file): This is the input original data set. It is a csv file with a total of n columns. The column name of the label column is "Target"
**Outputs:**
- `train_csv_file` (file): This is the result file of the output training set. It is a csv file with a total of n columns. The column name of the label column is "Target"
- `test_csv_file` (file): This is the result file of the output test set. It is a csv file with a total of n columns. The column name of the label column is "Target"

### ssGSEA
**Description:** ssGSEA (single-sample gene set enrichment analysis) is a method for gene set enrichment analysis, used to analyze the enrichment level of biological processes or pathways in gene expression data.
**Inputs:**
- `inf_set` (file): The file format is a text file, with tab (\t) used as the delimiter between fields. It contains two columns, each representing a biological pathway (TGF_pathway and BMP_pathway). Each row lists the genes belonging to the respective pathway.
- `inf_exp` (file): The file is an expression file delimited by tabs (\t), with rows representing genes and columns representing samples.
**Outputs:**
- `out_file` (file): A text file including results of ssGSEA

### stringtie
**Description:** This is a tool for assembling and quantifying RNA-Seq data.
**Inputs:**
- `bam_file` (file): The BAM format is a binary version of the SAM file, which takes up less space and is faster to read and process.
**Outputs:**
- `gtf_file` (file): Contains information on assembled transcripts.

### stringtie_merge
**Description:** stringtie_merge is a subfunction of stringtie, used to integrate transcript assembly results from multiple RNA-Seq samples.
**Inputs:**
- `gtf_file` (file): Contains information on assembled transcripts.
**Outputs:**
- `gtf_file` (file): Merged transcript file

### survival_curve
**Description:** survival_curve is a tool to plot the survival curve using survival time, event status, and variables that may affect survival.
**Inputs:**
- `survival_file` (file): The survival-related text file. # The following information must be included:Survival Time,Event Status,Covariates
- `time` (str): The column name in survival_file where the survival time is located.
- `event` (str): The column name in survival_file where the event status is located.
- `variable` (str): The column name in survival_file where variables that may affect survival is located.
**Outputs:**
- `out_survival_curve_image` (file): The survival curve figure.

### svm
**Description:** This is a tool for classification. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set. The algorithm used is SVM algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### svm_regression
**Description:** This is a tool for regression. input two csv files, namely the training set and the test set. Also input a column name for the label column. Use this tool to train on the training set, then predict on the test set, and output the prediction result file on the test set. the output result file adds a predicted value column "Predicted" compared to the input test set.
The algorithm used is SVM algorithm.
**Inputs:**
- `train_csv_file` (file): This is the input training set. It is a csv file with a total of n columns.
- `test_csv_file` (file): This is the input test set. It is a csv file with a total of n columns.
- `target` (string): This is the column name of the input label column. It is a string.
**Outputs:**
- `result_csv_file` (file): The output is the result file of the test set. It is a csv file with a total of (n+1) columns. The column name of the predicted value column is "Predicted"

### vcf_to_maf
**Description:** A tool used to convert a VCF file into a MAF file
**Inputs:**
- `vcf_file` (file): Variant Call Format files
**Outputs:**
- `maf_file` (file): Mutation annotation information (MAF) format file, The naming convention for output files is to replace ".vcf" in the input file name with ".maf". e.g:Input:"tumor.recal.vcf" Output: "tumor.recal.maf", Input:"tumor_paired.vcf" Output: "tumor_paired.maf"

### venn
**Description:** venn is a tool to plot the venn diagram.
**Inputs:**
- `dataset_file` (file): The text file containing datasets from various groups. Each column is a dataset for a group, with the column name being the name of the group.
**Outputs:**
- `out_venn_image` (file): The venn diagram.

### wgcna
**Description:** The wgcna algorithm is used to mine gene modules with strong correlation between gene expression profiles and group information.
**Inputs:**
- `exp_file` (file): The expression profile csv file(No preprocessing required).
- `group_file` (file): The group information csv file(No preprocessing required).
**Outputs:**
- `genes_modules_image` (file): Gene module clustering diagram, used to display how many gene modules are divided.
- `module_relationships_trait_image` (file): Used to show the correlation between gene modules and group information.
- `top_hub_gene_file` (file): The gene module with the strongest correlation with group information.

