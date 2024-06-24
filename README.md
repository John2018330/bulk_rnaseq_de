# BF528 Project 1 Bulk RNA-Seq DE

Johnathan Zhang (jzy0986@bu.edu)

In depth discussion and report found in `report/discussion_questions.html``

A snakemake pipeline for differential expression analysis using DESeq2. Raw RNA-Seq reads obtained from the following article: [Transcriptional Reversion of Cardiac Myocyte Fate During Mammalian Cardiac Regeneration](https://pubmed.ncbi.nlm.nih.gov/25477501/). 

### Quick Introduction
One of the aims of the paper was to develop a transcriptional profile for heart tissue in developing mice.
The objective of this project was to perform differential expression and gene set enrichment analysis using the raw RNA-Seq reads from 4 different time points of this study (p0, p4, p7, Ad).
Additionally, recreate figure 1D from the article using these time points as well. 
In terms of learning objectives, this project shows how to use Snakemake to streamline a typical RNA-Seq pipeline, utilize conda environments within workflow managers, and submitting workflows to HPCs

### Software
- [FastQC 0.12.1-0](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [MultiQC 1.20](https://multiqc.info/)
- [STAR 2.7.11b](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3530905/)
- [samtools 1.19.2](https://www.htslib.org/)
- [verse 0.1.5](https://kim.bio.upenn.edu/software/verse.shtml#:~:text=A%20versatile%20and%20efficient%20RNA,computing%20the%20same%20gene%20counts.)
- Custom python scripts found in `scripts`

## Workflow Outline
### Quality Control
Upon obtaining raw reads, the first step in most bioinformatics pipelines is performing quality assessment and quality control.
We use [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) to generate reports on each of the raw `fastq.gz` files, and then [MultiQC](https://multiqc.info/) to concatenate all those reports into one.

### Alignment to Mouse Reference Genome
After QC/QA of raw reads, the next major step is read mapping to a reference genome. 
For this we will use [STAR](https://github.com/alexdobin/STAR?tab=readme-ov-file).
Aside from the raw reads, we will need the genome fasta to align to, and downstream we will also need the genome's annotation file (gtf).
We will download GRCm39, mouse genome m39 provided by gencode, with the [ncbi datasets](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/) tool.
With the genome fasta, we can first use STAR to build a genome index which will greatly speed up the alignment process.
After creating the index, we can align our smaple's raw reads to the reference mouse genome and create SAM or BAM files.

### Post-Alignment QC
A quick way of testing how well your alignments were is to use's [samtool's](https://www.htslib.org/) flagstat command.

### Generating Counts
[VERSE](https://kim.bio.upenn.edu/software/verse.shtml) takes the alignment files and annotation file and quantifies how many reads map to gene regions of the reference genome.
We can also elect to extract gene symbols or gene ID's from the annotation file, depending on which is more useful for downstream analyses.

### Counts Matrix 
Custom python scripts are used to combine all of the verse output files (`scripts/concat_df.py`) and filter the matrix to remove genes that have 0 counts across all samples (`scripts/filter_cts_mat.py`)

### Differential Expression
To perform Differential Expression Analyses, utilize [R](https://www.r-project.org/) and Bioconductor's [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) package.

### Gene Set Enrichment Analysis
After generating results from DESeq2, we can perform GSEA using Bioconductor's [fGSEA](https://bioconductor.org/packages/release/bioc/html/fgsea.html) package. As a part of this project, we analyze the Canonical Pathways (C2) collection from MSIGDB. 

Both DE and fGSEA R analyses can be found in `differential_expression.Rmd`
