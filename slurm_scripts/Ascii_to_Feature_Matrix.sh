#!/bin/bash
#SBATCH --job-name=ASCII2Matrix   # Job name
#SBATCH --output=logs/ASCII2Matrix_%A_%a.log
#SBATCH --mail-type=ALL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=m.serajian@ufl.edu  # Where to send mail
#SBATCH --ntasks=1                      # Run a single task
#SBATCH --cpus-per-task=1
#SBATCH --mem=195gb                     # Job Memory
#SBATCH --time=500:00:00                 # Time limit hrs:min:sec
#SBATCH --array=5-5                    # Array range

ml python
chmod a+x projects/MTB-plus-plus/src/Ascii_to_Feature_Matrix/Ascii_to_Matrix.py

file_number=${SLURM_ARRAY_TASK_ID}
Color_matrix_address="/blue/boucher/share/Deep_TB_Ali/Final_TB/SBWT_Output/color_matrix.txt"
Npy_files_address="/blue/boucher/share/Deep_TB_Ali/Final_TB/NPY_Binary_Files_with_index/"
Number_of_Samples=6224
Number_of_kmers_in_file=30000000
min_filter_kmers_occurring_less_than=10 # Less than 10 times occurance, the kmer will be ignored
max_filter_kmers_occurring_more_than=3000

mkdir -p $Npy_files_address

python projects/MTB-plus-plus/src/Ascii_to_Feature_Matrix/Ascii_to_Matrix.py $file_number $Number_of_Samples \
          $Color_matrix_address $Npy_files_address\
          $Number_of_kmers_in_file \
          $min_filter_kmers_occurring_less_than\
          $max_filter_kmers_occurring_more_than

