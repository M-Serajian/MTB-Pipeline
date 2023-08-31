#!/usr/bin/env python
import numpy  as np
import pandas as pd
from   scipy.stats import chi2_contingency
import sys
from   sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt



import argparse
parser = argparse.ArgumentParser(description="Process arguments")
parser.add_argument('-1', dest='arg1', type=str, required=True, help="Drug name")
parser.add_argument('-2', dest='arg2', type=str, required=True, help="Number of significant Kmers to be choosed")
parser.add_argument('-3', dest='arg3', type=str, required=True, help="Number of samples (fasta files)")
parser.add_argument('-4', dest='arg4', type=str, required=True, help="Address to the Kmers stored")
parser.add_argument('-5', dest='arg5', type=str, required=True, help="Desierd directory for the outputs")
parser.add_argument('-6', dest='arg6', type=str, required=True, help="Address to the Chi-square test scores files")
parser.add_argument('-7', dest='arg7', type=str, required=True, help="Address to the phenotypes")
parser.add_argument('-8', dest='arg8', type=str, required=True, help="Which fold of cross-validation (which fold to be validation and the rest are training) (from zero to 4 for 5 fold cross-validation)")
args = parser.parse_args()

# Argument 1: drug name
# Argument 2: Top kmers number
drug_name_group=args.arg1
Number_of_Top_Kmers=int(args.arg2)
Number_of_samples=int(args.arg3)
Kmers_address=args.arg4 
Top_kmers_for_each_drug_address=args.arg5
Chi_score_addresses_for_each_drug=args.arg6
Phenotypes_address=args.arg7
Cross_validation_index=args.arg8

# Loading Phenotypes
df=pd.read_csv(Phenotypes_address)
print("Columns in the CSV file are:",flush=True)
print(df.columns,flush=True)






drug_names=['ERR', 'ID', 'ERS',"Amikacin"\
            ,"Bedaquiline", "Clofazimine","Delamanid"\
            ,"Ethambutol", "Ethionamide", "Isoniazid"\
            ,"Kanamycin","Levofloxacin","Linezolid"\
            ,"Moxifloxacin", "Rifampicin","Rifabutin"\
            ,"RIA","AMG","FQS"]

try:
  
  CSV_index = drug_names.index(drug_name_group)
  
except Exception as error:
  raise ValueError("Could not find the drug name; \
                   The drug names are: \n \
                   Amikacin ,\n \
                   Bedaquiline ,\n \
                   Clofazimine,\n \
                   Delamanid ,\n \
                   Ethambutol ,\n \
                   Ethionamide ,\n \
                   Isoniazid ,\n \
                   Kanamycin ,\n \
                   Levofloxacin ,\n \
                   Linezolid ,\n \
                   Moxifloxacin ,\n \
                   Rifampicin ,\n \
                   Rifabutin ,\n \
                   RIA ,\n \
                   AMG ,\n \
                   FQS ")

print("Drug Found!",flush=True)

# Columns of the target file are: 
#IDX:0      1     2      3      4      5      6
# ['ERR', 'ID', 'ERS', 'AMI', 'BDQ', 'CFZ', 'DLM',
# 'EMB', 'ETH', 'INH','KAN', 'LEV', 'LZD', 'MXF',
# 'RIF', 'RFB', 'RIFBB', 'Ami_Kan','Fluoroquinolone']


group=CSV_index 
print("Column number on CSV is {}".format(group),flush=True)
drug_name=drug_names[group]
print(drug_name)

def kmer_index_selector(*args,Number_of_top_kmers_output):
  files_count= np.size(args)
  print("the number of files is : {}".format(files_count),flush=True)
  length_files=[0]
  array_concat=np.array([])
  for i in range (files_count):
    sz=np.size(args[i])
    length_files.append(sz)
    array_concat=np.hstack((array_concat,args[i]))

  cum_length= np.cumsum(length_files)
  print(cum_length)
  
  print(np.shape(array_concat))
  top_kmers_index=sorted(range(len(array_concat)), key=lambda i: array_concat[i])[-Number_of_top_kmers_output:]
  
  list_of_numbers=[] # creating a list of lists
  for i in range(files_count):
    list_of_numbers.append([])

  for i in top_kmers_index:
    for j in range(files_count):
      
      if (cum_length[j] <= i and i < cum_length[j+1]):
        (list_of_numbers[j]).append(i-cum_length[j])

  return (list_of_numbers)

def kmer_selector (files_count,list_of_numbers,number_of_top_kmers):
  output_size=Number_of_samples + 1
  output=np.zeros((output_size,1)) # The +1 is for the kmer index
  list_file_names=["counts_file"+str(i)+"_fold_number_{}.npy".format(Cross_validation_index)+".npy" for i in range(1,13)]
  
  base_address=Kmers_address

  data=1 # to be deleted later, minimizing ram usage overhead
  for i in range(files_count):
    del data
    data=np.load(base_address+list_file_names[i])
    kmers_in_file=list_of_numbers[i]
    selected_kmers=(data[kmers_in_file,:]).T
    output=np.hstack((output,selected_kmers))

  print(np.shape(output))

  save_address=Top_kmers_for_each_drug_address

  np.save(save_address+drug_name+"/top_"+ str(number_of_top_kmers)+".npy",output[:,1:])

    

def main(number_of_top_kmers):
  base_chi_score_adress=Chi_score_addresses_for_each_drug+drug_name+"/"
  file_names=["chi_score_file"+str(i)+".npy" for i in range(1,13)]  
  a0=np.load(base_chi_score_adress+file_names[0])
  a1=np.load(base_chi_score_adress+file_names[1])
  a2=np.load(base_chi_score_adress+file_names[2])
  a3=np.load(base_chi_score_adress+file_names[3])
  a4=np.load(base_chi_score_adress+file_names[4])
  a5=np.load(base_chi_score_adress+file_names[5])
  a6=np.load(base_chi_score_adress+file_names[6])
  a7=np.load(base_chi_score_adress+file_names[7])
  a8=np.load(base_chi_score_adress+file_names[8])
  a9=np.load(base_chi_score_adress+file_names[9])
  a10=np.load(base_chi_score_adress+file_names[10])
  a11=np.load(base_chi_score_adress+file_names[11])

  index_lists=kmer_index_selector(a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,Number_of_top_kmers_output=number_of_top_kmers)
  
  for i in range (12):
    print(np.size(index_lists[i]))

  kmer_selector(np.size(file_names),index_lists,number_of_top_kmers)

  print("Finished Successfully!!!")

if __name__ == "__main__" :
  main(Number_of_Top_Kmers)
  




