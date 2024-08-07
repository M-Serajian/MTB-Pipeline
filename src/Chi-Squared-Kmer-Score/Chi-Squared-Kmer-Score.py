#!/usr/bin/env python
import time
import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd
import sys
import copy

# This function is defined to just calculate the Chi-score test on the 

def get_non_nan_indices(array):
    non_nan_indices = []
    for i in range(len(array)):
        if not np.isnan(array[i]):
            non_nan_indices.append(i)
    return non_nan_indices

# Parsing arguments
file_number=str(sys.argv[1]) 
drug_name_group=sys.argv[2] # abbreviation
Kmers_address=sys.argv[3] # address to the .npy files
Chi_score_addresses_for_each_drug=sys.argv[4] # where to save the chiscores
CV_fold=sys.argv[5] #number (0-4)
train_index_address=sys.argv[6] # Cross validation address
labels_address=sys.argv[7] # phenotypes

print(f"The drug is: {drug_name_group}")



train_index=np.load(train_index_address)

# processing the targets
df=pd.read_csv(labels_address)

# The columns in the dataframe:
drug_names= ["ERR","ENA_RUN","AMI",\
             "BDQ","CFZ","DLM","EMB",\
             "ETH","INH","KAN","LEV",\
             "LZD","MXF","RIF","RFB",\
             "RIA","AMG","FQS"]

try:
  CSV_index = drug_names.index(drug_name_group)
except Exception as error:
  raise ValueError("Could not find the drug name; \n \
                   The drug names are: \n \
                   AMI, \n \
                   BDQ,\n \
                   CFZ,\n \
                   DLM,\n \
                   EMB,\n \
                   ETH,\n \
                   INH,\n \
                   KAN,\n \
                   LEV,\n \
                   LZD,\n \
                   MXF,\n \
                   RIF,\n \
                   RFB,\n \
                   RIA,\n \
                   AMG,\n \
                   FQS")




group=CSV_index 
print("Column on CSV is {}".format(group),flush=True)
drug_name=drug_names[group]
target=np.array(df)


phenotype=target[:,group]
phenotype=phenotype[train_index] # Separating the train set
non_ambiguous_indecies=get_non_nan_indices(phenotype)


non_ambiguous_train_indecies=train_index[non_ambiguous_indecies]

phenotype=target[:,group] # recreating the phynotype to just use the non_ambiguous_train_indecies on them
phenotype=phenotype[non_ambiguous_train_indecies]
phenotype=phenotype.astype('int')


print("The shape of Targets (after removing ambiguous phenotypes) used in Chi_Square is:",flush=True)
print(np.shape(phenotype),flush=True)



# Reading the data
data=np.load(f"{Kmers_address}{file_number}.npy", allow_pickle=True)
data=np.stack(data, axis=0)



print(data[0])
print(np.shape(data))

train_data=data[:,non_ambiguous_train_indecies] # The color matrix generated by SBWT (rows are kmers and columns are strands)

print(train_data[0])
print(np.shape(train_data))

counter=0
chi_score=[]


for j in range (np.size(train_data,0)): # Kmers are in the rows
    row=train_data[j,:]  
    contigency_pct = pd.crosstab(row,phenotype)
    chi, _, _, _ = chi2_contingency((contigency_pct))
    chi_score.append(chi)

chi_score=np.array(chi_score)

np.save(Chi_score_addresses_for_each_drug+f"chi_square_{file_number}.npy",chi_score)

print(chi_score)
counter=0
for i in chi_score: 
   if i>4 :
    counter= counter+1

print("The number of times chiscore is higher than 4 is: {}".format(counter))
