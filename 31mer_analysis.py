#!/usr/bin/env python
import os
import sys
import subprocess

import argparse

import random

import string
import csv

import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

def concatenate_dataframes_with_padding(dfs):
    """
    Concatenate a list of dataframes vertically, ensuring that all dataframes have the same number of rows.
    If a dataframe has fewer rows, it is padded with NaNs.

    :param dfs: List of pandas DataFrames to concatenate
    :return: Concatenated DataFrame
    """
    # Determine the maximum number of rows in any of the dataframes
    max_rows = max(df.shape[0] for df in dfs)

    # Function to pad dataframe with NaNs to match the max number of rows
    def pad_df(df):
        rows_to_add = max_rows - df.shape[0]
        if rows_to_add > 0:
            # Create a DataFrame of NaNs with the required number of rows and columns
            padding_df = pd.DataFrame(np.nan, index=range(rows_to_add), columns=df.columns)
            # Use concat instead of append
            return pd.concat([df, padding_df], ignore_index=True)
        else:
            return df

    # Pad each dataframe and concatenate them
    padded_dfs = [pad_df(df) for df in dfs]
    concatenated_df = pd.concat(padded_dfs, axis=1)

    return concatenated_df

# defining colors for print to make debugs and .log files readable
green_color = "\033[32m"
blue_color = "\033[34m"
red_color= "\033[31m"
yellow_color = "\033[33m"
reset_color = "\033[0m"



# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root) of the current directory
project_root = os.path.dirname(current_dir)

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


def line_parser (string):
    count = string.count("(")
    first_paranthesis_index = string.find("(")
    
    kmer_index=int(string[0:first_paranthesis_index-1]) # This is index of the kmer which is at the end of each array _ the size will be 6225, in which the first 6224 ones are the mains and the last is kmer index
    return count, kmer_index



# Custom Help Formatter
class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super(CustomHelpFormatter, self)._format_action_invocation(action)
        else:
            default = action.dest.upper()
            parts = []
            for option_string in action.option_strings:
                if option_string in ['-i', '--I', '-o', '--O', '-b', '--B', '-f', '--F', '-t', '--temporary-directory']:
                    option_string = f'{green_color}{option_string}{reset_color}'
                parts.append(option_string)
            return ', '.join(parts) + f' {default}'

# Custom Argument Parser
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        # You can customize the error message below
        custom_message = f"\n{red_color}Error: {message}{reset_color}\n"
        sys.stderr.write(custom_message)
        sys.exit(2)


def main():
        # Initialize argument parser with custom formatter and parser
    parser = CustomArgumentParser(
        description="This code reports the number of occurrences of the 31-mers associated with each class of antibiotic",
        formatter_class=CustomHelpFormatter,
        usage=f'{green_color}%(prog)s{reset_color} -{green_color}i{reset_color} PATH/resistant_genome_IDs.csv -{green_color}o{reset_color} PATH/output.csv -{green_color}b{reset_color} Base_directory_of_FASTA_File -{green_color}f{reset_color} FASTA_extension -{green_color}t{reset_color} Temporary_directory'
    )

    # Define the command-line arguments
    parser.add_argument("-i", "--I", dest="input_file", type=str, required=True, help="Input resistant_genome_IDs.csv, the header of the CSV file should be the antibiotics (Amikacin, ....)")
    parser.add_argument("-o", "--O", dest="output_file", type=str, required=True, help="The output file which will be .csv (required)")
    parser.add_argument("-b", "--B", dest="base_directory", type=str, required=True, help="The directory including the FASTA files (required)")
    parser.add_argument("-f", "--F", dest="fasta_extension", type=str, required=True, help="The extensions of the Fasta files. The valid FASTA extensions are: ['fasta', 'fa', 'fas', 'fna', 'ffn']")
    parser.add_argument("-t", "--temporary-directory", dest="temporary_directory", type=str, required=True, help="This is a directory of Temporary files. Depending on the number of Genomes to be Processed, the free space to increase")

    # Parse the arguments
    args = parser.parse_args()


    # Assigning values from arguments
    
    FASTA_extension = args.fasta_extension
    output_file_address = os.path.abspath(args.output_file) if not os.path.isabs(args.output_file) else args.output_file
    base_directory = os.path.abspath(args.base_directory) if not os.path.isabs(args.base_directory) else args.base_directory

    # Check if the temporary directory exists
    if not os.path.isdir(args.temporary_directory):
        print(f"{red_color}Error: The directory '{args.temporary_directory}' does not exist.{reset_color}")
        print(f"{red_color}Aborted!{reset_color}")
        sys.exit(1)

    # Assign temp_dir and genome_id_csv_file
    temp_dir = args.temporary_directory
    genome_id_csv_file = args.input_file
    print(f"{green_color}{temp_dir}{reset_color}")

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
        SBWT_index = os.path.join(project_root,"MTB-plus-plus","data", "SBWT_indexes","{}.sbwt".format(drug))
        
        #Temporary random file names that will be removed later on
        #temporary_file=current_dir+"/temp/"+prefix_temporary_files+"_"+drug+".txt"
        temporary_kmer_list_file = os.path.join(temp_dir, prefix_temporary_files+"_31mers_"+drug+".txt")

        #Address to the dump_kmers
        address_to_dump_kmers= os.path.join(project_root,"MTB-plus-plus",'src',"SBWT-kmer-counters","dump_kmers") 

        command= address_to_dump_kmers+ " "+ SBWT_index + " > "+temporary_kmer_list_file

        #Runing the SBWT Kmer_dump to extract the top kmers for each antibiotic 
        try:
            subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{green_color}SBWT dump_kmers was successfully run for {drug}{reset_color}")
        except subprocess.CalledProcessError as e:
            error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
            print(f"{red_color}{error_message}{reset_color}")
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
            print(f"{yellow_color}There are ZERO genome IDs for {drug} {reset_color}")
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
#################result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                #For devug purpose
                print(f"{green_color}SBWT multi_genome_counters was successfully run for {drug}{reset_color}")
            except subprocess.CalledProcessError as e:
                error_message = f"Could not run SBWT dump_kmers {drug}, aborted. Error: {e.stderr.strip()}"
                print(f"{red_color}{error_message}{reset_color}")
                os.remove(temporary_kmer_list_file)
                raise  

            color_matrix_file = open(temporary_color_matrix_file,"r")
            
            for line in color_matrix_file:
                orrucance, _31_mer_index= line_parser(line)
                pairs_list[_31_mer_index][1]=orrucance
            
            pairs_list = [pair for pair in pairs_list if ("$" not in pair[0] and len(pair[0])!=0)]
            sorted_list = sorted(pairs_list, key=lambda x: x[1],reverse=True)

            mid_df=pd.DataFrame(sorted_list, columns=['{} top 31-mer'.format(drug),\
                                                '{} Kmer occurance (out of {})'.format(drug,len(drug_column))])
            dfs.append(mid_df) 

    output_dataframe = concatenate_dataframes_with_padding(dfs)  
    output_dataframe.to_csv("output_sorted.csv",index=False)

    

    
        
        


        
if __name__ == "__main__":
    main()
