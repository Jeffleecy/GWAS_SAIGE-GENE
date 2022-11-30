# The workflow of SAIGE/SAIGE-GENE software
SAIGE-GENE is developed to conduct variance component set-based tests, such as SKAT5 and SKAT-O6, for unbalanced case–control phenotypes in biobank-scale data [1]. SAIGE-GENE is incorporated into the SAIGE software.

## Installation
### Software:
Please check [here](https://saigegit.github.io/SAIGE-doc/docs/Installation.html) for the latest SAIGE version. 

### Installation:
- Please check [here](https://saigegit.github.io/SAIGE-doc/docs/Installation_sourcecode.html) for guidance from the developers of SAIGE-GENE.
- Here, I will explain some important steps of installing SAIGE under a high-performance computing (HPC) environment, which the developers did not fully explained in their website.
- The objective of installation is to install SAIGE in the R package of RSAIGE in the conda environment.
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

- ref: [SAIGE/SAIGE-GENE authors' documentation](https://saigegit.github.io/SAIGE-doc/docs/overview.html)
- We can perform SAIGE (designed for variant-based association testing) and SAIGE-GENE (designed for group-based association testing) with a single SAIGE package.
- The objective of step 1 is to fit the null generalized linear mixed model, in which the output file will be used by both variant-based and group-based association testing.
- In step 2, if we input a group file (described below) to SAIGE, then the software will perform SAIGE-GENE or undergo SAIGE.


## Data cleansing
- Before inputting bfile [(what are bfiles?)](https://www.cog-genomics.org/plink/1.9/input) files into SAIGE, I suggest filtering your VCF files by using [PLINK](https://www.cog-genomics.org/plink/) or similar genomic data processing tools. For instance, it may be appropriate to filter out the variants with a high missing rate (e.g. 20%).
- Remember to maintain the order of ref/alt in your file (e.g., --keep-allele-order command in plink) because some data cleansing tools may alter them, leading to false association results.
- If you are using whole genome sequencing (WGS) or whole exome sequencing (WES) data, you may want to target certain genomic regions (e.g., genes related to your research disease). You can apply [KGGseq](http://pmglab.top/kggseq/) to generate a VCF file focusing on the areas you are interested in. 
- Eventually, you'll have three bfiles (.bed/.bim/.fam) to run SAIGE-GENE. (SAIGE/SAIGE-GENE offers different input formats, but I prefer bfiles generated from PLINK for its convenience for data cleansing)
- My scripts for performing data cleansing are listed [here](https://github.com/Jeffleecy/GenomicDataProcessing)

## SAIGE-GENE step1
- Input: bfiles, a phenotype file
- Step 1 shell script
```
#!bin/bash
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
   -  .rda file (the model-fitted file, inpect with R)
   -  .varianceRatio.txt

## SAIGE-GENE step2
- Input: 
   - bfiles
   - a sample list
   - GMMAT model file (step 1 .rda file)
   - variance ratio file (step 1 .varianceRatio.txt)
   - a group file (for set-based association testing)
- Step 2 shell script

```
#!bin/bash
Rscript step2_SPAtests.R        \
     --bedFile=/xxxx/xxxx/prefix.bed       \
     --bimFile=/xxxx/xxxx/prefix.bim       \
     --famFile=/xxxx/xxxx/prefix.fam       \
     --SAIGEOutputFile=/xxxx/xxxx/prefix \ # your output file path and prefix
     --chrom=1 \ # specify the chromosome you want to investigate. SAIGE-GENE can only run one chromosome at a time.
     --LOCO=TRUE    \
     --AlleleOrder=alt-first \
     --minMAF=0 \
     --minMAC=0.5 \
     --sampleFile=/xxxx/xxxx/prefix.txt \
     --GMMATmodelFile=/xxxx/xxxx/prefix.rda \
     --varianceRatioFile=/xxxx/xxxx/prefix.varianceRatio.txt      \
     --groupFile=/xxxx/xxxx/prefix   \
     --annotation_in_groupTest=missense,        \ # you can specify the variant type you'd like to investigate
     --maxMAF_in_groupTest=0.01,0.04 # specify the max MAF that you hope your variants have. The higher, the more variants you can incorporate into your set-based testing; yet some of them may be less rare. 0.01, 0.04 means that SAIGE-GENE will perform with both variants with MAF lower than 0.04 and 0.01. 
```
- Sample File
```
SM_DE7605
SM_DE7599
SM_DE7598
...
```
(list the name of your sample in the .fam file)

- Group file
   - Basically, the group files encodes the region and variants that you use in the set-based association testing. It looks like this:
   ```
   ESPN_exon6	var	1:6504553:C:T
   ESPN_exon6	anno	missense,
   ESPN_exon8	var	1:6508717:G:A	1:6508872:C:T	1:6508945:C:T	1:6509064:G:C
   ESPN_exon8	anno	missense	missense	missense	missense,
   ```
   - The first column: regions
   - The second column: var = variants; anno = annotation of the variants
   - The third column: variants and annotations details
   - I wrote a python script to transform the variants' information from a .txt file generated by [ANNOVAR](https://annovar.openbioinformatics.org/en/latest/) to a group file. Please check "fromANNOVAR_To_GroupFile.py" in this directory.

- output file
   - A file with set-based association test results and a file with single association test results
   - The following are the column names of the set-based association test results
   ```
   Region  Group   max_MAF Pvalue  Pvalue_Burden   Pvalue_SKAT     BETA_Burden     SE_Burden       MAC     MAC_case             
   MAC_control     Number_rare     Number_ultra_rare
   ```
   ```
   Region: set name
   Group: annotation mask (annotation)
   max_MAF: maximum MAF cutoff
   Pvalue: p value for SKAT-O test
   Pvalue_Burden: p value for BURDEN test
   Pvalue_SKAT: p value for SKAT test
   BETA_Burden: effect size of BURDEN test
   SE_Burden: standard error of BETA_Burden
   ```
   (for a complete example, plese check "step2_Results_Exon_Based_Chr1.txt Go to file" in this directory)

## References:  
1. [SAIGE-GENE+ improves the efficiency and accuracy of set-based rare variant association tests](https://www.nature.com/articles/s41588-022-01178-w)
2. SAIGE documentation website:  
   https://saigegit.github.io/SAIGE-doc/docs/overview.html
   
   
