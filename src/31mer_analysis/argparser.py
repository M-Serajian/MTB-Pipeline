#!/usr/bin/env python
import os
import sys
import argparse

def parse_arguments():
    green_color = "\033[32m"
    red_color = "\033[31m"
    reset_color = "\033[0m"

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

    class CustomArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            custom_message = f"\n{red_color}Error: {message}{reset_color}\n"
            sys.stderr.write(custom_message)
            sys.exit(2)

        def validate_args(self, args):
            if not os.path.isfile(args.input_file):
                self.error(f"The input file '{args.input_file}' does not exist.")
            if not os.path.isdir(args.base_directory):
                self.error(f"The base directory '{args.base_directory}' does not exist.")
            if not os.path.isdir(args.output_dir):
                self.error(f"The output directory '{args.output_dir}' does not exist.")
            if not os.path.isdir(args.temporary_directory):
                self.error(f"The temporary directory '{args.temporary_directory}' does not exist.")

    parser = CustomArgumentParser(
        description="This code reports the number of occurrences of the 31-mers associated with each class of antibiotic",
        formatter_class=CustomHelpFormatter,
        usage=f'{green_color}%(prog)s{reset_color} -{green_color}i{reset_color} PATH/resistant_genome_IDs.csv -{green_color}o{reset_color} PATH/output_dir -{green_color}b{reset_color} Base_directory_of_FASTA_File -{green_color}f{reset_color} FASTA_extension -{green_color}t{reset_color} Temporary_directory'
    )

    parser.add_argument("-i", "--I", dest="input_file", type=str, required=True, help=f"({green_color}required{reset_color}) Input resistant_genome_IDs.csv, the header of the CSV file should be the antibiotics (Amikacin, ....)")
    parser.add_argument("-o", "--O", dest="output_dir", type=str, required=True, help=f"({green_color}required{reset_color}) The output directory where the results will be saved")
    parser.add_argument("-b", "--B", dest="base_directory", type=str, required=True, help=f"({green_color}required{reset_color}) The directory including the FASTA files")
    parser.add_argument("-f", "--F", dest="fasta_extension", type=str, required=True, help=f"({green_color}required{reset_color}) The extensions of the Fasta files. The valid FASTA extensions are: fasta, fa, fas, fna, ffn ")
    parser.add_argument("-t", "--temporary-directory", dest="temporary_directory", type=str, required=True, help=f"({green_color}required{reset_color}) This is a directory of Temporary files. Depending on the number of Genomes to be Processed, the free space to increase")

    args = parser.parse_args()

    # Validate the arguments after parsing
    parser.validate_args(args)

    return args

