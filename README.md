# MTB-plus-plus
This is the software developed to predict antimicrobial resistance (AMR) in MTB bacteria using machine learning for 13 groups of antibiotics including: Amikacin, Bedaquiline, Clofazimine, Delamanid, Ethambutol, Ethionamide Isoniazid, Kanamycin, Levofloxacin, Linezolid, Moxifloxacin, Rifampicin, Rifabutin; and 3 antibiotic families including RIA, AMG, Fluoroquinolone(FQS).


## First step: 
Downloading the raw data. The data used in this study are published by European Nucleotide Archive (ENA). The project numbers used to download the data are accessible [here](https://github.com/M-Serajian/enaBrowserTools/blob/c9ed1a39510bb976079177f2726f0a0ec9cf1275/Projects.txt).


## Second step: 
Assemble FASTQ data using [SPAdes](https://github.com/ablab/spades).

## Third step: 
Extracting the phenotypes from the ENA data and matching the identifier numbers. 

## Fourth step: 
Kmer extraction using [SBWT-kmer-counters](https://github.com/jnalanko/SBWT-kmer-counters)

