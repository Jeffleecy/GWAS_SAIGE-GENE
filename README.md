## SAIGE-GENE

## Description 
 This repository includes the codes used in:
1. performing rare variant association study through set-based testing using the [SAIGE-GENE](https://saigegit.github.io/SAIGE-doc/) software
2. generating group files required in the SAIGE-GENE
3. example results

## Dependencies
These codes are based on Python 3.10 and shell scripts and are executed in the Linux environment.
 
## Scripts
#### SAIGE-GENE_UserManual.md:
  - a step-by-step explanation of the entire SAIGE-GENE workflow 
  - specification of input and output formats used in the SAIGE-GENE

#### ANNOVAR_To_GroupFile.py
  - convert the text files annotated by [ANNOVAR](https://annovar.openbioinformatics.org/en/latest/) into the group files required in the AIGE-GENE step 2 
  - two kinds of group files will be generated: one is gene-based the other is exon-based

#### GroupFile_Gene_Based_Chr1.txt
 - A sample gene-based group file used in the SAIGE-GENE step 2

#### GroupFile_Exon_Based_Chr1.txt
- A sample exon-based group file used in the SAIGE-GENE step 2

#### Step2_Results_Gene_Based_Chr1.txt
- An example file with gene-based association test results from the SAIGE-GENE 

#### Step2_Results_Exon_Based_Chr1.txt
- An example file with exon-based association test results from the SAIGE-GENE 
