# MTB++



## Introduction
MTB++ is a software developed to predict antimicrobial resistance in MTB bacteria using machine learning for 13 groups of antibiotics including Amikacin, Bedaquiline, Clofazimine, Delamanid, Ethambutol, Ethionamide, Isoniazid, Kanamycin, Levofloxacin, Linezolid, Moxifloxacin, Rifampicin, Rifabutin; and 3 antibiotic families including Rifampin, Aminoglycosides, Fluoroquinolone. This README contains instructions on how to run the trained classifier or to rebuild the classifier from raw data.

[Rebuilding](https://github.com/M-Serajian/MTB-plus-plus#classifying-data-using-mtb) is an advanced use-case.  We expect most users to only run the trained classifier.   This software is maintained by Ali Serajian (ma.serajian@gmail.com).  Please post an Issue onto GitHub if there are any issues with these instructions.

## Citation ##
This software is under GNU license.  If you use the software please cite the following paper:   

## Installation ##
Two methods of installation are considered for MTB++ according to the user's preference. [Automatic Installation](https://github.com/M-Serajian/MTB-plus-plus#automatic-installation), and [Manual Installation](https://github.com/M-Serajian/MTB-plus-plus#manual-installation). In case your system supports the "module load" environment, you can your the Automatic Installation, otherwise, Manual Installation is recommended. 

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
git clone https://github.com/M-Serajian/MTB-plus-plus.git
cd MTB-plus-plus
sh setup.sh
```

### Manual Installation ###

If the setup script is not applicable to your system (for example, if your system does not support the "module load" environment), follow these manual installation steps:

1. **Cloning MTB++ getting into the project:**
```bash
git clone https://github.com/M-Serajian/MTB-plus-plus.git
cd MTB-plus-plus
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
Mtb++.py can be located at the MTB-plus-plus directory (the root on the cloned directory).
 
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
    <img src="https://github.com/M-Serajian/MTB-plus-plus/blob/main/images/Pipeline_transparent_backgrounds.png" alt="MTB++ Image" style="width: 100%;">
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
Extract the phenotypes from the ENA data and match the identifier numbers [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Extract%20Phenotypes)

```bash
command line here
```

### Create feature matrix ### 
The first step is to extract the k-mers using the SBWT.  The `fasta_filenames.txt` is a list with all the names of the fasta files.  
```bash
./sbwt build --in-file fasta_filenames.txt -k 31 -o index.sbwt -t 8 -m 10 --temp-dir temp
./counters index.sbwt fasta_filenames.txt > index_file.txt
```

From the above command, you should have an index file outputted from SBWT (`index_file.txt`).  Next, we transform this index file to a feature matrix that can be used for training.
```bash
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
```
These commands are also available in a script. The output should be `.npy` files that we will use in the next step.  See [ascii_to_feature.sh](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Ascii_to_Feature_Matrix).


### Feature selection. ### 

Create five folds of the data to be further used for Chi-squared test and classification.
```bash
./mypython.py somthing.npy > output
```

Next, we perform Chi-squared test to rank the features based on their significance [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Chi-Square-Kmer-Ranking).
 ```bash
./mypython.py somthing.npy > output
```
Lastly, we select the top features for each resistance class for training the classifiers [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Kmer_Select).
```bash
./mypython.py somthing.npy > output
```
### Train the Classifiers ### 
The last step is to train classifiers, both the Logistic Regression and Random Forest classifiers. [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Classifier).

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