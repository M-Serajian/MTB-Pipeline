import argparse
import os
import subprocess
from src.Resistance_Predictor import Resistance_Predictor

def main():
    parser = argparse.ArgumentParser(description="Process data")
    parser.add_argument("-f", help="Input MTB assembled sequence or FASTA file (mandatory)", type=str)
    parser.add_argument("-o", help="The output file which will be .CSV (optional, default: input_file_name.csv)", type=str, default=None)
    
    args = parser.parse_args()
    
    # Ensure that input_file is provided
    if not args.f:
        parser.error("The input file is mandatory.")
    
    # If output_file is not provided, set it to input_file + '.csv'
    if args.o is None:
        args.o = args.f + '.csv'
    
    # Your code to process the data goes here
    print(f"Input sequence is : {args.f}")

    

if __name__ == "__main__":
    main()
