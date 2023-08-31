This code is designed to train a classifier based on the data processed in the previous [step](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Kmer_Select). Two types of basic classifiers are designed, Logistic regression (LR) and Random Forest (RF).

Usage: 
  -h,--help  show this help message and exit
  -1 ARG1     Drug name group
  -2 ARG2     The address to the top kmers selected for
              classification on previous step
  -3 ARG3     Results address
  -4 ARG4     Cross validation folds (5 in our study)
  -5 ARG5     Cross validation index
  -6 ARG6     Address of index of folds of cross-validation
  -7 ARG7     Model address
  -8 ARG8     Alpha lasso parameter for LR
  -9 ARG9     Number of RF trees
  -10 ARG10   Phenotypes address