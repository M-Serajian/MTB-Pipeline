This code is designed to train a classifier based on the data processed in the previous [step](https://github.com/M-Serajian/MTB-plus-plus/tree/main/src/Kmer_Select). Two types of basic classifiers are designed, Logistic regression (LR) and Random Forest (RF) are trained. The saved models will be further used as the input to the main MTB++ software
```bash
Usage: src/classifier/classifier.py [options]

Options:
  -h, --help        Show this help message and exit

Required:
  --antibiotic_drug_name ANTIBIOTIC_DRUG_NAME             Specify the drug name
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