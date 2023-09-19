#!/usr/bin/env python
import argparse
import os

def main(input_file, output_directory):
    # Your main script logic here
    print("Input file:", input_file)
    print("Output directory:", output_directory)



if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="MTB++ usage")

    # Add the required input file argument
    parser.add_argument("-i", "--input", required=True, help="Input file, should be a FASTA file")

    # Add the optional output directory argument with a default value
    parser.add_argument("-o", "--output", required=True, help="Output directory (CSV file)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.input, args.output)