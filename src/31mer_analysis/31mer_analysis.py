#!/usr/bin/env python
import os
import sys
import subprocess



import random

import string
import csv

import pandas as pd
import numpy as np



import df_concatination as dfc
import SBWT_string_parser as ssp
import argparser
# defining colors for print to make debugs and .log files readable
green_color = "\033[32m"
blue_color = "\033[34m"
red_color= "\033[31m"
yellow_color = "\033[33m"
magenta_color = '\033[35m'
reset_color = "\033[0m"



# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root) of the current directory
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
project_root = os.path.dirname(parent_dir)

# Add the project root directory to PYTHONPATH
sys.path.append(project_root)

# Global varible, drug names:

# Drug_number, orders 
drug_names=["Amikacin",
            "Bedaquiline",
            "Clofazimine",
            "Delamanid",
            "Ethambutol",
            "Ethionamide",
            "Isoniazid",
            "Kanamycin",
            "Levofloxacin",
            "Linezolid",
            "Moxifloxacin",
            "Rifampicin",
            "Rifabutin",
            "RIA",
            "AMG",
            "FQS"]


#                                   Drug number
# drug_names=["Amikacin",\              0       
#             "Bedaquiline",\           1
#             "Clofazimine",\           2
#             "Delamanid",\             3
#             "Ethambutol",\            4
#             "Ethionamide",\           5
#             "Isoniazid",\             6
#             "Kanamycin",\             7
#             "Levofloxacin",\          8
#             "Linezolid",\             9
#             "Moxifloxacin",\          10
#             "Rifampicin",\            11
#             "Rifabutin",\             12
#             "RIA",\                   13
#             "AMG",\                   14
#             "FQS"]                    15










# Main function

def main():

    args = argparser.parse_arguments()


    # Assigning values from arguments
    
    FASTA_extension = args.fasta_extension
    output_file_address = os.path.abspath(args.output_dir) if not os.path.isabs(args.output_dir) else args.output_dir
 
    base_directory = os.path.abspath(args.base_directory) if not os.path.isabs(args.base_directory) else args.base_directory

    # Check if the temporary directory exists
    if not os.path.isdir(args.temporary_directory):

        print(f"{red_color}Error: The directory '{args.temporary_directory}' does not exist.{reset_color}",flush=True)
        print(f"{red_color}Aborted!{reset_color}",flush=True)
        sys.exit(1)

    # Assign temp_dir and genome_id_csv_file
    temp_dir = args.temporary_directory
    
    genome_id_csv_file = args.input_file
    # Read the CSV file using pandas
    genome_id_df = pd.read_csv(genome_id_csv_file)

    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits
    
    # Generate a random 20-character string to be used as the name for temporary files during the processing
    prefix_temporary_files =''.join(random.choice(characters) for _ in range(25))
    prefix_temporary_files =''.join("2PIn9iqosr6LyveTjUYDf4STC")
    #Calculating the color matrix and parsing 
    #the Ascii code and doing the classification 
    #at the same time
    

    #These lists contain the information that will further be reported
    dfs = []
    output_dataframe=pd.DataFrame()
    for drug in drug_names:

        #Address to the SBWK index for each specific drug
        #SBWT_index = os.path.join(current_dir, "data", "SBWT_indexes","{}.sbwt".format(drug))
        #SBWT_index = os.path.join(project_root,"MTB-plus-plus","data", "SBWT_indexes","{}.sbwt".format(drug))
        SBWT_index = os.path.join(project_root,"MTB-plus-plus","data", "SBWT_indexes","{}.sbwt".format(drug))
        
        #Temporary random file names that will be removed later on
        #temporary_file=current_dir+"/temp/"+prefix_temporary_files+"_"+drug+".txt"
        temporary_kmer_list_file = os.path.join(temp_dir, prefix_temporary_files+"_31mers_"+drug+".txt")

        #Address to the dump_kmers
        address_to_dump_kmers= os.path.join(project_root,"MTB-plus-plus",'src',"SBWT-kmer-counters","dump_kmers") 

        command= address_to_dump_kmers+ " "+ SBWT_index + " > "+temporary_kmer_list_file

        #Runing the SBWT Kmer_dump to extract the top kmers for each antibiotic 
        try:
            print(f"{magenta_color}Runing SBWT dump_kmers for {drug}:{reset_color}",flush=True)            
            subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{green_color}SBWT dump_kmers was successfully run for {drug}{reset_color}",flush=True)
        except subprocess.CalledProcessError as e:
            error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
            print(f"{red_color}{error_message}{reset_color}",flush=True)
            os.remove(temporary_kmer_list_file)
            raise  
        
        with open(temporary_kmer_list_file, "r") as file:
            text_content = file.read()

        pairs_list = [[line.strip(), 0] for line in text_content.split('\n')]
    


        # 
        temporary_genome_list_file = os.path.join(temp_dir, prefix_temporary_files+"_genome_list_"+drug+".txt")

        drug_column = genome_id_df[drug]
        #dropin Nans
        drug_column = drug_column.dropna()
        
        # Checking if the number of genome IDs are not zero since SBWT will crush if no genome IDs are present in it
        if len(drug_column) == 0:
            print(f"{yellow_color}There are ZERO genome IDs for {drug}{reset_color}",flush=True)
            mid_df=pd.DataFrame([["_","0 genome IDs exist"]], columns=['{} top 31-mer'.format(drug),\
                                                '{} Kmer occurance (out of {}) '.format(drug,len(drug_column))])
            dfs.append(mid_df)
        else: # RUN SBWT multi genome color matrix
            # creating the list 
            absolute_addresses = [os.path.join(base_directory, str(genome_id)+"."+ FASTA_extension) for genome_id in drug_column]
            # Write the absolute addresses to the output text file
            with open(temporary_genome_list_file, "w") as outfile:
                outfile.write("\n".join(absolute_addresses))
            
            temporary_color_matrix_file = os.path.join(temp_dir, prefix_temporary_files+"_multi_genome_color_matrix_"+drug+".txt")

            address_to_multi_genome_counters= os.path.join(project_root,"MTB-plus-plus",'src',"SBWT-kmer-counters","multi_genome_counters") 

            command= address_to_multi_genome_counters+ " "+ SBWT_index + " "+ temporary_genome_list_file + " > "+temporary_color_matrix_file

            try:
                print(f"{magenta_color}Runing SBWT multi_genome_counters for {drug}:{reset_color}",flush=True)            
                subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #For devug purpose
                print(f"{green_color}SBWT multi_genome_counters was successfully run for {drug}{reset_color}")
            except subprocess.CalledProcessError as e:
                error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
                print(f"{red_color}{error_message}{reset_color}",flush=True)
                os.remove(temporary_kmer_list_file)
                raise  

            color_matrix_file = open(temporary_color_matrix_file,"r")
            
            for line in color_matrix_file:
                orrucance, _31_mer_index= ssp.line_parser(line)
                pairs_list[_31_mer_index][1]=orrucance
            
            pairs_list = [pair for pair in pairs_list if ("$" not in pair[0] and len(pair[0])!=0)]
            sorted_list = sorted(pairs_list, key=lambda x: x[1],reverse=True)

            mid_df=pd.DataFrame(sorted_list, columns=['{} top 31-mer'.format(drug),\
                                                '{} Kmer occurance (out of {})'.format(drug,len(drug_column))])
            dfs.append(mid_df) 

    output_dataframe = dfc.concatenate_dataframes_with_padding(dfs)  
    
    #creating the name of the output report

    input_csv_file_name = os.path.basename(genome_id_csv_file)

    if input_csv_file_name.endswith('.csv'):

        input_csv_file_name = input_csv_file_name[:-4]  # Remove the last 4 characters (".csv")

    # Add "_31mer_analysis.csv" to the file name
    output_report_csv_file = input_csv_file_name + "_31mer_analysis.csv"

    #creating the absolute path
    output_report_csv_file= os.path.join(output_file_address, output_report_csv_file)
    import json

    try:
        output_dataframe.to_csv(output_report_csv_file, index=False)
        # JSON output for success
        print(f"{blue_color}The report is accisible at : {output_report_csv_file}{reset_color}",flush=True)
    except Exception as e:
        # Print error message
        print(f"An error occurred while saving the DataFrame to CSV: {e}",flush=True)
    


        
if __name__ == "__main__":
    main()


