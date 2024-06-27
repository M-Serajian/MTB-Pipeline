This code is designed to train a classifier based on the data processed in the previous [step](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Kmer_Select). Two types of basic classifiers are designed, Logistic regression (LR) and Random Forest (RF) are trained. The saved models will be further used as the input to the main MTB++ software
```bash
Usage: 
  -h,--help  show this help message and exit
  --antibiotic_drug_name "Penicillin"  # Specify the drug name (required)
  --total_number_of_features "100"     # Total number of features for the model (required)
  --feature_matrix_directory "/path/to/feature_matrices"  # Directory containing feature matrices (required)
  --results_directory "/path/to/results"  # Directory to save the results (required)
  --cross_validation_folds 5            # Number of folds for cross-validation (required)
  --cross_validation_index 0            # Index of the fold used for testing (required)
  --cross_validation_indexes_directory "/path/to/cv_indexes"  # Directory containing indexes for cross-validation (required)
  --phenotypes_directory "/path/to/phenotypes"  # Directory of the CSV file containing antibiotic drug resistance phenotypes (required)
  --alpha_lasso 1.0                     # Alpha parameter for Lasso regularization in logistic regression (optional, default: 1.0)
  --logistic_regression_lasso_threshold 1000  # Feature threshold for applying Lasso (optional, default: 1000)
  --random_forest_trees 150             # Number of trees in the random forest model (optional, default: 150)
  --maximum_itteration 2500             # Maximum number of iterations for the model (optional, default: 2500)
  --logistic_regression                 # Flag to select logistic regression model (optional)
  --random_forest                       # Flag to select random forest model (optional)
  --linear_regression                   # Flag to select linear regression model (optional)
```