## SAIGE-GENE
In order to conduct rare variant association study using SAIGE-GENE, I annotated VCF files with ANNOVAR (version 2019) and transformed the annotated files with a python script. The python script and some sample results are listed in this repository. 

### Overview of Files 
- ANNOVAR_To_GroupFile.py
  * A python script processing text files annotated from ANNOVAR and outputing group files for rare variant association study.
  * Time complexity of this program is O(n^2)
- Step2_Results_Exon_Based_Chr1.txt
  * The output text of SAIGE-GENE step2
- Step2_Results_Gene_Based_Chr1.txt
- GroupFile_Exon_Based_Chr1.txt
  * A sample input exon-based group file for SAIGE-GENE software
- GroupFile_Gene_Based_Chr1.txt
  * A sample input gene-based group file for SAIGE-GENE software

