import pandas as pd
import numpy as np
import os as os

# set working directory
os.chdir('')

# read a txt files annotated by ANNOVAR from the drive
df=pd.read_table('',sep = "\t",header=None)

# drop the row one which is the original column's names
df.drop([0],axis = 0,inplace = True)

# split the column recording chromosome information into a column with only integers
df[['chr','chr_number']] = df[0].str.split(pat="r",expand=True)

# replacing X with 23
df['chr_number'] = df['chr_number'].replace(['X'],'23')

# rename column names
df.rename(columns = {1:'Start',3:'Ref',4:'Alt',6:'Gene',8:'MutType',9:'Info'}, inplace = True)

# split the Info columns
df['Info'].loc[1]
df_Info = df['Info'].str.split(pat=':',expand=True)
df_Info.rename(columns = {0:'Info_Gene',1:'Info_NM',2:'Info_exon'},inplace = True)
df_Info_Exon = df_Info['Info_exon']

# merge the split Info columns into original dataframe
df = df.join(df_Info_Exon)

# concatenate columns to create keys and values we intended
## group file variant format (1:1234:G:A)
df['value1'] = df['chr_number'].astype(str) + ":" + df['Start']
df['value2'] = df['value1'].astype(str) + ":" + df['Ref']
df['value3'] = df['value2'].astype(str) + ":" + df['Alt']

## create a column with the format "GeneX_exonY" as a key column
df['Gene_Exon'] = df['Gene'].astype(str) + "_" + df['Info_exon']

# filtering out nonsynonymous SNV for we only use missense mutation in the study
df_filteredMut = df[df['MutType'] == 'nonsynonymous SNV']

# transform the 'value' column into an array
value = df_filteredMut['value3'].to_numpy()

# make arrays used for creating the group file
## an array of the chromosome number with duplications
ChrListRepeated = df_filteredMut['chr_number'].to_numpy()

## a array of chromosome number without duplication
ChrListNoRepeat = df_filteredMut['chr_number'].drop_duplicates()
ChrListNoRepeat = ChrListNoRepeat.to_numpy()

## an array of genes of each variants
GeneListRepeated = df_filteredMut['Gene'].to_numpy()

## an array of genes without duplication
df2 = df_filteredMut.drop_duplicates(subset=['Gene'])
GeneListNoRepeat= df2['Gene'].to_numpy()

## filtered Gene_exon array without duplication
df3 = df_filteredMut.drop_duplicates(subset=['Gene_Exon'])
GeneExonListNoRepeat = df3['Gene_Exon'].to_numpy()

## filtered Gene_exon array with duplication
GeneExonListRepeated = df_filteredMut['Gene_Exon'].to_numpy()

#make lists for indexing
## make a Gene list for indexing
GeneListRepeated_List = list(GeneListRepeated)

## make Gene_Exon list for indexing
GeneExonListRepeated_list = list(GeneExonListRepeated)


# make a group file specific to a chromosome
## create an exon-based group file
for x in ChrListNoRepeat:
    txt = open("Gene_exon_chr"+x+".txt", 'w')
    for j in range(0, (len(GeneListNoRepeat)-1)):
        if (x == ChrListRepeated[GeneExonListRepeated_list.index(GeneExonListNoRepeat[j])]):
            txt.write(GeneExonListNoRepeat[j] + "\tvar")
            for i in range(0, (len(GeneExonListRepeated) - 1)):
                if (GeneExonListNoRepeat[j] == GeneExonListRepeated[i]):
                    if (x == ChrListRepeated[i]):
                        txt.write("\t" + value[i])
            txt.write("\n")

        if (x == ChrListRepeated[GeneExonListRepeated_list.index(GeneExonListNoRepeat[j])]):
            txt.write(GeneExonListNoRepeat[j] + "\tanno")
            for i in range(0, (len(GeneExonListRepeated) - 1)):
                if (GeneExonListNoRepeat[j] == GeneExonListRepeated[i]):
                    if (x == ChrListRepeated[i]):
                        txt.write("\tmissense")
            txt.write(",")
            txt.write("\n")
    txt.close()

## create a gene-based groups file

for x in ChrListNoRepeat:
    txt = open("Gene_chr"+x+".txt", 'w')
    for j in range(0, (len(GeneListNoRepeat)-1)):
        if (x == ChrListRepeated[GeneListRepeated_List.index(GeneListNoRepeat[j])]):
            txt.write(GeneListNoRepeat[j] + "\tvar")
            for i in range(0, (len(GeneListRepeated) - 1)):
                if (GeneListNoRepeat[j] == GeneListRepeated[i]):
                    if (x == ChrListRepeated[i]):
                        txt.write("\t" + value[i])
            txt.write("\n")

        if (x == ChrListRepeated[GeneListRepeated_List.index(GeneListNoRepeat[j])]):
            txt.write(GeneListNoRepeat[j] + "\tanno")
            for i in range(0, (len(GeneListRepeated) - 1)):
                if (GeneListNoRepeat[j] == GeneListRepeated[i]):
                    if (x == ChrListRepeated[i]):
                        txt.write("\tmissense")
            txt.write(",")
            txt.write("\n")
    txt.close()
