# The workflow of using  SAIGE-GENE software

## Introduction

## Installation
### software:
Please check [here](https://saigegit.github.io/SAIGE-doc/docs/Installation.html) for the latest SAIGE/SAIGE-GENE version. 

### installation explanation:
- Please check [here](https://saigegit.github.io/SAIGE-doc/docs/Installation_sourcecode.html) for the guidence from the developers of SAIGE/SAIGE-GENE.
- Here, I will explain certain steps of installing SAIGE under high performance computing (HPC) environment, which the developers did not fully explained in their website.
- The objective of installation is to install SAIGE in the R pacakge of RSAIGE in the conda environemnt (this is important!).
- Steps of installation:
   1. download the source file from [here](https://saigegit.github.io/SAIGE-doc/docs/Installation_sourcecode.html)
   2. download conda
   3. download RSAIGE as a conda environemnt 
   4. perform RSAIGE under the conda environemnt
   5. download R using the Rscript in the RSAIGE
   6. use R to download SAIGE as one of its package
   7. perform SAIGE/SAIGE-GENE when RSAIGE is activated

## Overview of the workflow
<img src="https://user-images.githubusercontent.com/80674585/196645099-cd9d9530-3f88-40c4-9b7a-620c42e1f58f.png" width="500" height="500">
- (ref: [SAIGE/SAIGE-GENE authors' documentation](https://saigegit.github.io/SAIGE-doc/docs/overview.html))
- We can perform SAIGE (designed for variant-based association testing) and SAIGE-GENE (designed for group-based association testing) with a single SAIGE pakcage.
- The objective of step 1 is to fit the null generalized linear mixed model, in which the output file will be used by both variant-based and group-based association testing.
- In step 2, if we input a group file (decribed below) to SAIGE, then the software will perform SAIGE-GENE, or it will undergo SAIGE.


## Data cleansing
- Before inputting bfile [(what are bfiles?)](https://www.cog-genomics.org/plink/1.9/input) files into SAIGE, I suggest filtering your VCF files by using [PLINK](https://www.cog-genomics.org/plink/) or similar genomic data processing tools. For instance, it may be appropriate to filter out the variants with high missing rate (e.g. 20%).
- Do not forget to maintain the order of ref/alt in your file (e.g., --keep-allele-order command in plink) because some data cleansing tools may alter them, leading to false association results.
- If you are using whole genome sequencing (WGS) or whole exome sequencing (WES) data, you may want to target certain genomic regions (e.g., genes related to your research disease). You can apply [KGGseq](http://pmglab.top/kggseq/) to generate a VCF file focusing on the areas you are interested in. 
- Eventually, you'll have three bfiles (.bed,.bim,.fam) to run SAIGE-GENE. (SAIGE/SAIGE-GENE offers different input format, but I prefer bfiles generated from PLINK for its convenience for data cleasing)

## SAIGE-GENE step1
- Input: bfiles, a phenotype file
- Step 1 shell script
```
#! bin/bash
Rscript step1_fitNULLGLMM.R     \
        --plinkFile=/xxxx/xxxx/prefix \ # your bfile path and prefix
        --phenoFile=/xxxx/xxxx/prefix.txt \ # path to access your phenotype file
        --phenoCol=y_binary \
        --sampleIDColinphenoFile=IID \
        --traitType=binary        \
        --outputPrefix=/xxxx/xxxx/prefix \ # your output file path and prefix
        --nThreads=24   \
        --IsOverwriteVarianceRatioFile=TRUE

```
(step1_fitNULLGLMM.R can be found in the source code file and is needed to be put under the same directory as the Step 1 shell script)


- Step 1 phenotype file example:
```
IID     y_quantitative  y_binary
SM_DE7605       70      1
SM_DE7599       70      1
SM_DE7598       51.25   1
...
```
(0 = affected, 1 = affected; SAIGE only accepts no more than two options)


- Step 1 output files
   -  .rda files (the model-fitted file, inpect with R)
   -  .varianceRatio.txt

## SAIGE-GENE step2

## References:  
1. SAIGE documentation website:  
   https://saigegit.github.io/SAIGE-doc/docs/overview.html
