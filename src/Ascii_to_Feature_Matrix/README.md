# Ascii_to_Matrix: Distributed Processor for SBWT Color Matrix

This script performs distributed processing on the output of SBWT (color matrix). It splits the file into equal line-based chunks across multiple CPUs or processes. Each chunk is processed independently to extract binary presence/absence vectors for k-mers.

During this process, k-mers that appear in fewer samples than a minimum threshold or in more samples than a maximum threshold are filtered out. The output is saved as a NumPy `.npy` file containing the filtered binary matrix for that chunk.

**Important Notes:**
- The SBWT input file must end with a newline character (`\n`) to ensure accurate line counting.
- Use `awk 'END{print NR}' color_matrix.txt` for reliable line count.
- The number of CPUs or parallel tasks must match `--total-files`.
- Each CPU/process must be assigned exactly one file index (`--file-index`), and `--total-files` must be equal to the number of CPUs used.
- Each process must have enough memory to load and process its chunk of the binary matrix.

---

## Input Format

Each line in the SBWT color matrix should look like:

<kmer_index> (<sample_index>:<value>) (<sample_index>:<value>) ...

---

## Arguments

--file-index (-f): 1-based index of the chunk assigned to this process  
--num-samples (-n): Total number of samples (FASTA files)  
--color-matrix (-c): Path to the SBWT color matrix file  
--output-dir (-o): Directory to save the output `.npy` file  
--total-lines (-tl): Total number of lines in the color matrix (use `wc -l`)  
--total-files (-tf): Total number of chunks / CPUs (must match number of parallel jobs)  
--min-occurrence (-min): Minimum number of samples a k-mer must appear in  
--max-occurrence (-max): Maximum number of samples a k-mer can appear in

---

## Example

```bash
python src/ascii_to_matrix/Ascii_to_Matrix.py \
  -f 3 -n 6224 -c /path/to/color_matrix.txt \
  -o /path/to/output/ -tl 700000000 -tf 100 \
  -min 5 -max 6500
```
