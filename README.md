# MTB-plus-plus
This is the software developed to predict antimicrobial resistance (AMR) in MTB bacteria using machine learning for 13 groups of antibiotics including Amikacin, Bedaquiline, Clofazimine, Delamanid, Ethambutol, Ethionamide Isoniazid, Kanamycin, Levofloxacin, Linezolid, Moxifloxacin, Rifampicin, Rifabutin; and 3 antibiotic families including Rifampin(RIA), Aminoglycosides(AMG), Fluoroquinolone(FQS).


## First step: 
Download the raw data. The data used in this study are available at the European Nucleotide Archive (ENA). The project numbers used to download the data are accessible [here](https://github.com/M-Serajian/enaBrowserTools/blob/c9ed1a39510bb976079177f2726f0a0ec9cf1275/Projects.txt).


## Second step: 
Assemble FASTQ data using [SPAdes](https://github.com/ablab/spades).

## Third step: 
Extract the phenotypes from the ENA data and match the identifier numbers. 

## Fourth step: 
Extract Kmer  using [SBWT-kmer-counters](https://github.com/jnalanko/SBWT-kmer-counters).

## Fifth step: 
Transform the output of the previous section to a feature matrix [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Ascii_to_Feature_Matrix).

## Sixth step: 
Perform Chi-squared test to rank kmers based on their significance [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Chi-Square-Kmer-Ranking).

## Seventh step: 
Select the top kmers for each antibiotic for training a classifier [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Kmer_Select).

## Eighth step: 
Train classifiers (Logistic Regression and Random Forest) [here](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Classifier).
