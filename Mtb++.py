import argparse
import os
import subprocess
import numpy as np
import os
from src.resistance_predictor import resistance_predictor
import random
import string
import subprocess
import csv
import sys
# Set the working directory to the directory containing your main script
print(sys.argv[0])
os.chdir(os.path.dirname(__file__))
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



    # Define the characters that can be used in the random string
    characters = string.ascii_letters + string.digits
    # Generate a random 20-character string to be used as the name for temporary files during the processing
    prefix_temporary_files = ''.join(random.choice(characters) for _ in range(20))

    current_directory = os.getcwd()

    #Calculating the color matrix and parsing 
    #the Ascii code and doing the classification 
    #at the same time
    
    header= [" "]+drug_names
    LR_report=["Logistic Regression"]
    RF_report=["Random Forest"]
    drug_number=0
    for drug in drug_names:
        address_to_kmer_counters_executable= "."+ os.path.join('/src',"SBWT-kmer-counters","counters") 
        SBWT_index="/home/m.serajian/projects/MTB-plus-plus/data/SBWT_indexes/{}.sbwt".format(drug)
        temporary_file="temp/"+prefix_temporary_files+"_"+drug+".txt"
        command= address_to_kmer_counters_executable+ " "+ SBWT_index + " " + input_file_address+">"+temporary_file
        subprocess.run(command, check=False, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        prediction=resistance_predictor.AMR_predictor(temporary_file,drug_number)
        LR_report.append(prediction[0])
        RF_report.append(prediction[1])
        os.remove(temporary_file)
        drug_number=drug_number+1
    

        # Create and open the CSV file in write mode
    with open(output_file_address, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerow(LR_report)
        csv_writer.writerow(RF_report)


if __name__ == "__main__":
    main()
