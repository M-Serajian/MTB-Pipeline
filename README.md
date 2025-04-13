# MTB++



## Introduction
MTB++ is a software developed to predict antimicrobial resistance in MTB bacteria using machine learning for 13 groups of antibiotics including Amikacin, Bedaquiline, Clofazimine, Delamanid, Ethambutol, Ethionamide, Isoniazid, Kanamycin, Levofloxacin, Linezolid, Moxifloxacin, Rifampicin, Rifabutin; and 3 antibiotic families including Rifampin, Aminoglycosides, Fluoroquinolone. This README contains instructions on how to run the trained classifier or to rebuild the classifier from raw data.

[Rebuilding](https://github.com/M-Serajian/MTB-Pipeline#classifying-data-using-mtb) is an advanced use case.  We expect most users to only run the trained classifier.   This software is maintained by Ali Serajian (ma.serajian@gmail.com).  Please post an Issue on GitHub if there are any issues with these instructions.

## Citation ##
This software is under GNU license.  If you use the software please cite the following paper: [Scalable de novo classification of antibiotic resistance of Mycobacterium tuberculosis](https://academic.oup.com/bioinformatics/article/40/Supplement_1/i39/7700900)


## Installation ##
Two methods of installation are considered for MTB++ according to the user's preference. [Automatic Installation](https://github.com/M-Serajian/MTB-Pipeline#automatic-installation), and [Manual Installation](https://github.com/M-Serajian/MTB-Pipeline#manual-installation). In case your system supports the "module load" environment, you can use the Automatic Installation, otherwise, Manual Installation is recommended. 

Regardless of the installation method used, the following dependencies should be installed first. 

#### Dependencies ####

* [python](https://www.python.org/) 3.0+ (3.6+ recommended)
    - [sklearn](https://scikit-learn.org/stable/whats_new/v1.1.html#version-1-1-2) (Version 1.1.2) 
    - [joblib](https://joblib.readthedocs.io/en/stable/) (Pre-exists on python3+)
* [Cmake](https://cmake.org/)(tested on v3.26.4)
* [GCC](https://gcc.gnu.org/) (9.3.3 recommended)


### Automatic Installation ###

#### Installation Instructions ####

To simplify the installation process, the provided `setup.sh` script automates the setup by utilizing the "module load" environment. The script loads essential modules such as GCC and CMake (they need to be installed), compiles SBWT, and verifies the version of Scikit-learn. To use the script, follow these steps:

1. **Cloning MTB++ and installing it:**
```bash
git clone https://github.com/M-Serajian/MTB-Pipeline.git
cd MTB-Pipeline
sh setup.sh
```

### Manual Installation ###

If the setup script is not applicable to your system (for example, if your system does not support the "module load" environment), follow these manual installation steps:

1. **Cloning MTB++ getting into the project:**
```bash
git clone https://github.com/M-Serajian/MTB-Pipeline.git
cd MTB-Pipeline
```
2. **Compiling and Installing SBWT_Kmer_Counters:**
    Compile [SBWT_Kmer_Counters](https://github.com/M-Serajian/SBWT-kmer-counters) as follows:

```bash
cd src
git clone https://github.com/M-Serajian/SBWT-kmer-counters.git
cd SBWT-kmer-counters
git submodule update --init --recursive
cd SBWT/build
cmake ..
make -j
```

3. **Install Scikit-learn version 1.1.2:**
```bash
pip3 install scikit-learn==1.1.2
```
Now, MTB++ is ready to be used. 

# Usage
Mtb++.py can be located at the MTB-Pipeline directory (the root on the cloned directory).
 
```bash
python Mtb++.py -f FASTAfile -o Output.csv
```

# Example 
```bash
python Mtb++.py -f data/sample_genomes/ERR8665561.fasta -o ERR8665561.csv
```


# MTB++ Report Consolidation #

If MTB++ is utilized for a substantial number of isolates, individual .csv reports are generated for each isolate in the directory specified by the **`-o`** flag for the "Mtb++.py" script. To streamline and unify this data into comprehensive reports, the **MTB++_Report_Consolidation.rb** script has been developed.

## Purpose

The primary purpose of MTB++_Report_Consolidation.rb is to process the individual CSV files and create two finalized reports:

1. **Logistic Regression Prediction Report:** This report consolidates predictions made by the Logistic Regression classifier for each genome.

2. **Random Forest Prediction Report:** This report aggregates predictions based on the Random Forest classifier for each genome.


## Usage
To use **`MTB++_Report_Consolidation.rb`** effectively, make sure to run it after executing MTB++ for the isolates. The script is designed to consolidate individual reports found in the directory specified by the **`-d`**  or **`--data-directoryd`** flag. It identifies all CSV files in that directory, creating two distinct CSV files that offer a comprehensive overview of the predictions made by MTB++ for each isolate.

### How to Run

```bash
ruby MTB++_Report_Consolidation.rb -d [DATA_DIRECTORY] -o [OUTPUT_DIRECTORY]
```

- **-d or --data-directory:** Specify the directory where all the individual MTB++ reports (CSV files) for each isolate are stored. This parameter is mandatory.

- **-o or --output-directory:** (Optional) Specify the directory where you want the unified reports for Logistic Regression and Random Forest predictions to be saved. If not provided, the default is the current directory.



# MTB++ 31mer Analysis Multi-thread Tool#

## Purpose
This code reports the number of occurrences of the 31-mers associated with each class of antibiotic.

## Usage

- `-h, --help HELP`: Show the help message and exit.
- `-i, --I INPUT_FILE`: (required) Input `resistant_genome_IDs.csv`, the header of the CSV file should be the antibiotics (Amikacin, ....).
- `-o, --O OUTPUT_DIR`: (required) The output directory where the results will be saved.
- `-b, --B BASE_DIRECTORY`: (required) The directory including the FASTA files.
- `-f, --F FASTA_EXTENSION`: (required) The extensions of the Fasta files. The valid FASTA extensions are: `fasta`, `fa`, `fas`, `fna`, `ffn`.
- `-t, --temporary-directory TEMPORARY_DIRECTORY`: (required) This is a directory of Temporary files. Depending on the number of Genomes to be Processed, the free space to increase.

### How to Run
```bash
perl 31mer_analysis -i PATH/to/resistant_genome_IDs.csv -o PATH/to/output_dir -b Base_directory_of_FASTA_Files -f FASTA_extension -t Temporary_directory
```

# Classifying Data using MTB++ #
Below are the instructions to use the classifier. Here, we assume that the data to be classified is available as a set of paired-end sequence reads.  In our example, we will have `reads1.fq` and `reads2.fq`

### Dependencies for training classifiers from scratch ###
* python 3.0+ (3.6+ recommended)
    - [sklearn](https://scikit-learn.org/stable/whats_new/v1.1.html#version-1-1-2) (Version 1.1.2) 
* [Cmake](https://cmake.org/)(tested on v3.26.4)
* [GCC](https://gcc.gnu.org/) (9.3.3 recommended)
* [SBWT_Kmer_counters](https://github.com/M-Serajian/SBWT-kmer-counters)
* [SPAdes](https://github.com/ablab/spades)
* [enaBrowserTools](https://github.com/M-Serajian/enaBrowserTools/blob/c9ed1a39510bb976079177f2726f0a0ec9cf1275/Projects.txt)

#### Pipeline
The following image demonstrates the data analysis pipeline in MTB++ model developement. 
<div style="display: flex; align-items: center;">
  <div style="flex: 1;">
    <img src="https://github.com/M-Serajian/MTB-Pipeline/blob/main/images/Pipeline_transparent_backgrounds.png" alt="MTB++ Image" style="width: 100%;">
  </div>
</div>

### Assemble the data into contigs ###
Use SPAdes to assemble the data
```bash
spades.py -r1 reads1.fastq -r2 reads2.fastq -o contigs.fa
```
### Classify the data using the models ###
Take the `contigs.fa` file to make a prediction using the models
```bash
run.py -i contigs.fa -o prediction.txt 
```


## Building the Classifier ##
Below are the instructions in order to rebuild the classifier and reproduce our results. If you would like to just use the trained classifier, see above.


### Download the raw data ###
The first step is to download the FASTQ data, using European Nucleotide Archive (ENA) Browser Tools.

### Assemble the data into contigs ###
Use spades to assemble the data
```bash
spades.py -r1 reads1.fastq -r2 reads2.fastq
```
### Extract and match phenotypic data ### 
Extract the phenotypes from the ENA data and match the identifier numbers [here](https://github.com/M-Serajian/MTB-Pipeline/tree/main/src/Extract%20Phenotypes)

```bash
command line here
```

### Create feature matrix ### 

This process is does using Ascii_to_Matrix module which is a distributed processing for the output of SBWT Color Matrix. It splits the file into equal line-based chunks across multiple CPUs or processes. Each chunk is processed independently to extract binary presence/absence vectors for k-mers.

During this process, k-mers that appear in fewer samples than a minimum threshold or in more samples than a maximum threshold are filtered out. The output is saved as a NumPy `.npy` file containing the filtered binary matrix for that chunk.

**Important Notes:**
- The SBWT input file must end with a newline character (`\n`) to ensure accurate line counting.
- Use `awk 'END{print NR}' color_matrix.txt` for reliable line count.
- The number of CPUs or parallel tasks must match `--total-files`.
- Each CPU/process must be assigned exactly one file index (`--file-index`).
- Each processor will generate exactly one `.npy` file, which is why the number of CPUs and `--total-files` must be the same.
- Each process must have enough memory to load and process its chunk of the binary matrix.

---

## Input Format

Each line in the SBWT color matrix should look like:

<kmer_index> (<sample_index>:<value>) (<sample_index>:<value>) ...

---

## Usage

```bash
Usage: src/ascii_to_matrix/Ascii_to_Matrix.py [options]

Options:
  -h, --help                      Show this help message and exit

Required:
  --file-index FILE_INDEX        1-based index of the chunk assigned to this process
  --num-samples NUM_SAMPLES      Total number of samples (FASTA files)
  --color-matrix FILE_PATH       Path to the SBWT color matrix file
  --output-dir DIRECTORY         Directory to save the output `.npy` file
  --total-lines TOTAL_LINES      Total number of lines in the color matrix (use `wc -l`)
  --total-files TOTAL_FILES      Total number of chunks / CPUs
  --min-occurrence MIN           Minimum number of samples a k-mer must appear in
  --max-occurrence MAX           Maximum number of samples a k-mer can appear in
```

---

## Example

```bash
python src/ascii_to_matrix/Ascii_to_Matrix.py \
  --file-index 3 \
  --num-samples 6224 \
  --color-matrix /path/to/color_matrix.txt \
  --output-dir /path/to/output/ \
  --total-lines 700000000 \
  --total-files 100 \
  --min-occurrence 5 \
  --max-occurrence 6500
```



### Feature selection. ### 

Create five folds of the data to be further used for Chi-squared test and classification.
```bash
./mypython.py somthing.npy > output
```

Next, we perform Chi-squared test to rank the features based on their significance [here](https://github.com/M-Serajian/MTB-Pipeline/tree/main/src/Chi-Square-Kmer-Ranking).
 ```bash
./mypython.py somthing.npy > output
```
Lastly, we select the top features for each resistance class for training the classifiers [here](https://github.com/M-Serajian/MTB-Pipeline/tree/main/src/Kmer_Select).
```bash
./mypython.py somthing.npy > output
```
### Train the Classifiers ### 
The last step is to train classifiers, both the Logistic Regression and Random Forest classifiers. [here](https://github.com/M-Serajian/MTB-Pipeline/tree/main/src/Classifier).

```bash
Usage: src/classifier/classifier.py [options]

Options:
  -h, --help        Show this help message and exit

Required:
  --antibiotic_drug_name DRUG_NAME             Specify the drug name
  --total_number_of_features NUMBER            Total number of features for the model
  --feature_matrix_directory PATH              Directory containing feature matrices
  --results_directory PATH                     Directory to save the results
  --cross_validation_folds NUMBER              Number of folds for cross-validation
  --cross_validation_index INDEX               Index of the fold used for testing
  --cross_validation_indexes_directory PATH    Directory containing indexes for cross-validation
  --phenotypes_directory PATH                  Directory of the CSV file containing antibiotic drug resistance phenotypes

Optional:
  --alpha_lasso VALUE                          Alpha parameter for Lasso regularization (default: 1.0)
  --logistic_regression_lasso_threshold NUMBER Feature threshold for applying Lasso (default: 1000)
  --random_forest_trees NUMBER                 Number of trees in the random forest model (default: 150)
  --maximum_iteration NUMBER                   Maximum number of iterations for the model (default: 2500)
  --logistic_regression                        Flag to select logistic regression model
  --random_forest                              Flag to select random forest model
  --linear_regression                          Flag to select linear regression model
```
