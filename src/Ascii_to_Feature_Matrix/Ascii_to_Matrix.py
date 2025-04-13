#!/usr/bin/env python
import time
import numpy as np
import argparse
import os

#!/usr/bin/env python
import argparse

def parse_arguments():
    """
    Parses command-line arguments for distributed processing of the SBWT color matrix file.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Extract a chunk of binary presence/absence vectors from a SBWT color matrix file."
    )

    parser.add_argument(
        "--file-index", "-f",
        type=int,
        required=True,
        help="Index (1-based) of the file chunk being processed."
    )

    parser.add_argument(
        "--num-samples", "-n",
        type=int,
        required=True,
        help="Total number of samples (FASTA files); defines length of binary vector."
    )

    parser.add_argument(
        "--color-matrix", "-c",
        type=str,
        required=True,
        help="Path to the SBWT color matrix file (output of SBWT)."
    )

    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        required=True,
        help="Directory where the output .npy file will be saved."
    )

    parser.add_argument(
        "--total-lines", "-tl",
        type=int,
        required=True,
        help="Total number of lines in the SBWT color matrix file (can be obtained using `wc -l`)."
    )

    parser.add_argument(
        "--total-files", "-tf",
        type=int,
        required=True,
        help="Total number of output files (i.e., number of chunks/processes)."
    )

    parser.add_argument(
        "--min-occurrence", "-min",
        type=int,
        required=True,
        help="Minimum number of samples in which a k-mer must appear to be kept."
    )

    parser.add_argument(
        "--max-occurrence", "-max",
        type=int,
        required=True,
        help="Maximum number of samples in which a k-mer can appear to be kept."
    )

    return parser.parse_args()


# Kmer index is added now, its the first element (index zero)
def parse_color_matrix_line(line: str, num_samples: int):
    """
    Parses a single line from the SBWT color matrix and returns a binary vector indicating
    presence (1) or absence (0) of a k-mer in each sample.

    Each line in the SBWT color matrix represents the presence of a single k-mer across samples 
    in the format: <k-mer-index> (<sample_index>:<value>)... 

    Args:
        line (str): A line from the color matrix.
        num_samples (int): Total number of samples (length of the binary vector).

    Returns:
        tuple: 
            - binary_vector (List[int]): Binary vector with length `num_samples + 1` 
              (last entry stores the original k-mer index).
            - num_occurrences (int): Number of samples where the k-mer was present.
    """
    # Track positions of special characters to extract tuple data
    left_parens_indices = [i for i, char in enumerate(line) if char == "("]
    colon_indices       = [i for i, char in enumerate(line) if char == ":"]
    right_parens_indices= [i for i, char in enumerate(line) if char == ")"]

    num_occurrences = len(left_parens_indices)

    # Initialize presence vector of 0s (absent) for all samples
    binary_vector = [0] * num_samples

    # Parse each (<sample_index>:<value>) tuple
    for i in range(num_occurrences):
        sample_index = int(line[left_parens_indices[i] + 1 : colon_indices[i]])
        presence_value = int(line[colon_indices[i] + 1 : right_parens_indices[i]])
        binary_vector[sample_index] = presence_value

    # Extract k-mer index from the beginning of the line and append as the last element
    kmer_index = int(line[0 : left_parens_indices[0] - 1])
    binary_vector.append(kmer_index)

    return binary_vector, num_occurrences


def main():
    """
    Main execution function to process a specific chunk of the SBWT color matrix file.

    This script assumes that the total number of output files (chunks) is equal to the
    number of parallel CPUs or processes being used. Each CPU is assigned a unique 
    --file-index to determine its portion of the input file.

    Important:
        - The input SBWT file must be pre-counted to determine --total-lines using `wc -l`.
        - The total number of CPUs used in parallel must match --total-files.
        - Each CPU/process must have sufficient memory to load and process its chunk
          of the binary feature matrix (which can be large depending on the number of samples).

    The function filters lines based on k-mer occurrence thresholds and converts each
    valid line into a binary presence/absence vector (plus the k-mer index). The result
    is saved as a NumPy `.npy` file for downstream analysis.
    """

    # Parse command-line arguments
    args = parse_arguments()

    file_index = args.file_index
    num_samples = args.num_samples
    color_matrix_path = args.color_matrix
    output_directory = args.output_dir
    total_lines = args.total_lines
    total_files = args.total_files
    min_occurrence_threshold = args.min_occurrence
    max_occurrence_threshold = args.max_occurrence

    # Calculate the range of lines this file should process
    lines_per_chunk = total_lines // total_files
    start_line_index = (file_index - 1) * lines_per_chunk
    # Ensure last chunk captures any remaining lines
    if file_index < total_files:
        end_line_index = file_index * lines_per_chunk
    else:
        end_line_index = total_lines

    print(f"[INFO] File index {file_index} will process lines {start_line_index} to {end_line_index - 1}", flush=True)

    binary_matrix = []  # To store the output rows (binary vectors)
    line_counter = -1

    # For progress timing at 10% of chunk
    tenth_line_index = start_line_index + int(0.1 * (end_line_index - start_line_index))
    print(f"[INFO] 10% progress checkpoint at line: {tenth_line_index}", flush=True)

    # Open and process the file line-by-line
    with open(color_matrix_path, "r") as color_matrix_file:
        for line in color_matrix_file:
            line_counter += 1

            # Start timing when we reach the start of our chunk
            if line_counter == start_line_index:
                start_time = time.time()

            # Progress update at 10%
            if line_counter == tenth_line_index:
                tenth_time = time.time()
                elapsed = round(tenth_time - start_time, 2)
                print(f"[INFO] 10% of file index {file_index} processed in {elapsed} seconds", flush=True)

            # Process only lines in our assigned range
            if start_line_index <= line_counter < end_line_index:
                occurrence_count = line.count(":")

                if min_occurrence_threshold < occurrence_count < max_occurrence_threshold:
                    binary_vector, _ = parse_color_matrix_line(line, num_samples)
                    binary_matrix.append(binary_vector)

            # Stop reading once our chunk ends
            if line_counter >= end_line_index:
                break

    # Convert result to NumPy array and save to file
    binary_matrix = np.array(binary_matrix)
    print(f"[INFO] Final matrix shape for file index {file_index}: {binary_matrix.shape}", flush=True)

    output_file_path = os.path.join(output_directory, f"chunck{file_index}.npy")

    np.save(output_file_path, binary_matrix)

    print(f"[SUCCESS] Saved binary matrix to: {output_file_path}", flush=True)



if __name__ == '__main__':
    main()
