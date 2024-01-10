#!/bin/bash
#SBATCH --job-name=31mer_analysis   # Job name
#SBATCH --output=/blue/boucher/share/MTB/MTB_Database/BV_BRC_MTB++_temp_files/logs/%x_%j.out
#SBATCH --mail-type=ALL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=m.serajian@ufl.edu  # Where to send mail
#SBATCH --ntasks=1                      # Run a single task
#SBATCH --cpus-per-task=16
#SBATCH --mem=10gb                     # Job Memory
#SBATCH --time=20:00:00                 # Time limit hrs:min:sec
#SBATCH --array=0-0                    # single job 

date;

export OMP_NUM_THREADS=16
ml python
ml perl
perl 31mer_analysis.pl \
    -i resistant_genomes.csv \
    -o . \
    -b /blue/boucher/share/MTB/MTB_Database/BV_BRC_corrected \
    -f fna \
    -t /blue/boucher/share/MTB/MTB_Database/BV_BRC_MTB++_temp_files

date;