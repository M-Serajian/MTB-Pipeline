#!/usr/bin/env python
import os
import sys
import subprocess

import argparse

from src.resistance_predictor import resistance_predictor
import random
import string
import subprocess
import csv

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root) of the current directory
project_root = os.path.dirname(current_dir)

# Add the project root directory to PYTHONPATH
sys.path.append(project_root)

# Global varible, drug names:

# Drug_number, orders 
drug_names=["Amikacin",\
            "Bedaquiline",\
            "Clofazimine",\
            "Delamanid",\
            "Ethambutol",\
            "Ethionamide",\
            "Isoniazid",\
            "Kanamycin",\
            "Levofloxacin",\
            "Linezolid",\
            "Moxifloxacin",\
            "Rifampicin",\
            "Rifabutin",\
            "RIA",\
            "AMG",\
            "FQS"]


def main():
    # Parsing input arguments:

    parser = argparse.ArgumentParser(description="Mtb++ (Mycobacterium tuberculosis antimicrobial resistance detector)",usage="-f PATH/FASTAfile -o PATH/output.csv")
    
    parser.add_argument("-f", help="Input MTB assembled sequence or FASTA file (required)", type=str)
    
    parser.add_argument("-o", help="The output file which will be .csv (required)", type=str)
    
    args = parser.parse_args()


    # Check if the output file path is an absolute path or a relative path
    if not os.path.isabs(args.o):
        # Construct the absolute path for the output file based on the current working directory
        output_file_address = os.path.abspath(args.o)
    else:
        output_file_address = args.o

    
    input_file_address=args.f
    file_name = os.path.basename(input_file_address)



    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits
    # Generate a random 20-character string to be used as the name for temporary files during the processing
    prefix_temporary_files = ''.join(random.choice(characters) for _ in range(20))

    current_directory = os.getcwd()

    #Calculating the color matrix and parsing 
    #the Ascii code and doing the classification 
    #at the same time
    

    #These lists contain the information that will further be reported

    header= [" "]+drug_names
    LR_report=["Logistic Regression"]
    RF_report=["Random Forest"]
    drug_number=0

    for drug in drug_names:

        #Address to the SBWK index for each specific drug
        #SBWT_index = os.path.join(current_dir, "data", "SBWT_indexes","{}.sbwt".format(drug))
        SBWT_index = os.path.join( "data", "SBWT_indexes","{}.sbwt".format(drug))

        #Temporary random file names that will be removed later on
        #temporary_file=current_dir+"/temp/"+prefix_temporary_files+"_"+drug+".txt"
        #temporary_file = os.path.join(current_dir, "temp", prefix_temporary_files+"_"+drug+".txt")
        temporary_file = os.path.join("temp", prefix_temporary_files+"_"+drug+".txt")

        #Runing the SBWK Kmer Counter to create the color matrix

        #Address to the SBWK Kmer Counter executable
        address_to_kmer_counters_executable= "."+ os.path.join('/src',"SBWT-kmer-counters","counters") 

        command= address_to_kmer_counters_executable+ " "+ SBWT_index + " " + input_file_address+">"+temporary_file
        #Runing the command
        subprocess.run(command, check=False, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        #Prediciting AMR by pretrained models
        prediction=resistance_predictor.AMR_predictor(temporary_file,drug_number)

        #Saving to the lists
        LR_report.append(prediction[0]) #LR
        RF_report.append(prediction[1]) #RF
        os.remove(temporary_file)
        drug_number=drug_number+1
    
        # Create and open the CSV file in write mode
    with open(output_file_address, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow(LR_report)
        csv_writer.writerow(RF_report)
        
    # ANSI escape code for blue color
    blue_color = "\033[34m"
    reset_color = "\033[0m"  # Reset color to default

    # Print the message with the output_file_address in blue
    print("The MTB MR predictions for {}{}{} are stored at {}{}{} directory!".format(blue_color,file_name,reset_color,blue_color, output_file_address, reset_color))



if __name__ == "__main__":
    main()
