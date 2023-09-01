#!/usr/bin/env python
import pandas as pd
import copy
from sklearn.impute import SimpleImputer #Added in case of simple mode imputation for ambiguous phenotypes yet was removed
import numpy as np
from tabulate import tabulate

def logical_or_with_nan(a, b):

  result=np.logical_or(a,b) * 1

  if(np.isnan(a) and np.isnan(np.nan)):
    result=np.nan

  if ((np.isnan(a) and b==True) or (np.isnan(b) and a==True)):
    result=1

  if ((np.isnan(a) and b==False) or (np.isnan(b) and a==False)):
    result=np.nan

  return (result)


def main():
    # reading csv data
    df1 = pd.read_excel('projects/MTB-plus-plus/Data/ERR_files.xlsx')# this is the list of the data downloaded from ENA
    df2 = pd.read_excel('projects/MTB-plus-plus/Data/Json.xlsx')

    # Merging the 2 dataframes based on the RUN numbers
    inner_join = pd.merge(df1, df2, on ='ERR', how ='inner')
    
    
    df3 = pd.read_excel('phenotypes.xlsx') # This is the CSV file of the phenotypes given by GWAS paper
    #

    Data = pd.merge(inner_join, df3, on ='ERS', how ='inner')
   

    # Considering Suciptible as 0 and Intermediate and Resistance as 1
    mapping = {'S': int(0), 'I': int(1), 'R': int(1),'NA': np.nan}
    phenotypes=["AMI_BINARY_PHENOTYPE","BDQ_BINARY_PHENOTYPE","CFZ_BINARY_PHENOTYPE",
            "DLM_BINARY_PHENOTYPE","EMB_BINARY_PHENOTYPE","ETH_BINARY_PHENOTYPE",
            "INH_BINARY_PHENOTYPE","KAN_BINARY_PHENOTYPE","LEV_BINARY_PHENOTYPE",
            "LZD_BINARY_PHENOTYPE","MXF_BINARY_PHENOTYPE","RIF_BINARY_PHENOTYPE",
            "RFB_BINARY_PHENOTYPE"]
    
    df=copy.copy(Data) 
    for i in phenotypes:
        df[i] = df[i].map(mapping)
        #df[i].fillna(df[i].mode()[0])
        #df[i]=df[i].astype(int)

    # Mode imputation to get rid of NA
    Mode_imputation_activator=0
    if (Mode_imputation_activator==1):
        imp = SimpleImputer(strategy='most_frequent')
        df = pd.DataFrame(imp.fit_transform(df), columns=df.columns)

    #Making targets integer
  
    # New Abbreviations
    df['RIA'] = df.apply(lambda row: logical_or_with_nan(row['RIF_BINARY_PHENOTYPE'], row['RFB_BINARY_PHENOTYPE']), axis=1)
    df['AMG'] = df.apply(lambda row: logical_or_with_nan(row['AMI_BINARY_PHENOTYPE'], row['KAN_BINARY_PHENOTYPE']), axis=1)
    df["mid"]= df.apply(lambda row: logical_or_with_nan(row['LEV_BINARY_PHENOTYPE'], row['MXF_BINARY_PHENOTYPE']), axis=1)
    df["FQS"]= df.apply(lambda row: logical_or_with_nan(row["mid"], row['CFZ_BINARY_PHENOTYPE']), axis=1)
    df = df.drop("mid", axis=1)
    
    # Renaming Drugs
    df = df.rename(columns={'AMI_BINARY_PHENOTYPE': 'AMI',
                            'BDQ_BINARY_PHENOTYPE': 'BDQ',
                            'CFZ_BINARY_PHENOTYPE': 'CFZ',
                            'DLM_BINARY_PHENOTYPE': 'DLM',
                            'EMB_BINARY_PHENOTYPE': 'EMB',
                            'ETH_BINARY_PHENOTYPE': 'ETH',
                            'INH_BINARY_PHENOTYPE': 'INH',
                            'KAN_BINARY_PHENOTYPE': 'KAN',
                            'LEV_BINARY_PHENOTYPE': 'LEV',
                            'LZD_BINARY_PHENOTYPE': 'LZD',
                            'MXF_BINARY_PHENOTYPE': 'MXF',
                            'RIF_BINARY_PHENOTYPE': 'RIF',
                            'RFB_BINARY_PHENOTYPE': 'RFB'})
    
    #saving the output
    df.to_csv('6224_Targets_NA_3_letters.csv', index=False)
   #saving the output
    """
    #Abbreviations
    phenotypes=['AMI',
                'BDQ',
                'CFZ',
                'DLM',
                'EMB',
                'ETH',
                'INH',
                'KAN',
                'LEV',
                'LZD',
                'MXF',
                'RIF',
                'RFB',
                'RIFBB',
                'Ami_Kan',
                'Fluoroquinolone']
    """


    phenotypes=['AMI',
                'BDQ',
                'CFZ',
                'DLM',
                'EMB',
                'ETH',
                'INH',
                'KAN',
                'LEV',
                'LZD',
                'MXF',
                'RIF',
                'RFB',
                'RIA',
                'AMG',
                'FQS']
    

    #print(df)
    Latex_report=1
    if Latex_report==1 :
        for i in phenotypes: 
            sum_b = df[i].sum(skipna=True)
            print(i + " & " + str(int(sum_b)) + " & " + str (df[i].value_counts()[0]) + " \\\\")
            print("\hline")
    
    Na_checker=1
    if Na_checker==1 : 
        columns_to_check = df.columns[3:]

        # Calculate the number of NaN values in each column
        nan_counts = df[columns_to_check].isna().sum()
        # nan_counts = df.isna().sum()
        # print the results
        print(nan_counts)

    print("Full latex tabular:")
    
    Latex_report=1
    if Latex_report==1 :
        columns_to_check = df.columns[3:]
        nan_counts = df[columns_to_check].isna().sum()
        report_list=[]

        counter=0
        for i in phenotypes: 


            report_list.append([i, nan_counts.iloc[counter],df[i].value_counts()[0]\
                                ,df[i].sum(skipna=True),round(100*df[i].\
                                sum(skipna=True)/df[i].value_counts()[0],2) ])
            counter=counter+1
        
        

        # Assuming you have a 2D list called 'data' and a header list called 'headers'

        # Create the LaTeX tabular representation
        headers=["Drug", "# Ambiguous", "# Susceptible", "# Resistant","R/S %"]
        latex_table = tabulate(report_list, headers, tablefmt="latex")

        # Print the LaTeX table
        print(latex_table)



if __name__ == '__main__' :
    main()