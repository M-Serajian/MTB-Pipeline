#!/usr/bin/env python
import sys
import os
import time
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score, recall_score, accuracy_score,confusion_matrix
import numpy as np
import pickle
import argparse
import copy


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process arguments for drug classification/regression models.")
    
    parser.add_argument('--antibiotic_drug_name', type=str, required=True, help="Drug name group.")
    parser.add_argument('--total_number_of_features', type=str, required=True, help="The total number of features that will be used for training of the models.")
    parser.add_argument('--feature_matrix_directory', type=str, required=True, help="The directory of the feature matricies that includes the .npy files stored from previous part.")
    parser.add_argument('--results_directory', type=str, required=True, help="The ROC curves and csv files of the accuracy will be stored in this directory.")
    parser.add_argument('--cross_validation_folds', type=int, required=True, help="Total number of cross-validation folds (integer greater than 3).")
    parser.add_argument('--cross_validation_index', type=int, required=True, help="Specifies the index of the cross-validation fold to be used (ranging from 0 to k-1). This parameter determines which fold will be used for testing in the cross-validation process, while the remaining folds are used for training.")
    parser.add_argument('--cross_validation_indexes_directory', type=str, required=True, help="Directory containing the indexes for each cross-validation fold.")
    parser.add_argument('--alpha_lasso', type=float, default=1.0, help="Alpha lasso parameter for logistic regression (default: 1.0).")
    parser.add_argument('--logistic_regression_lasso_threshold', type=int, default=1000, help="If the number of features used to train the logistic regression model is more than this value, lasso shrinkage will be used (default: 1000).")
    parser.add_argument('--random_forest_trees', type=int, default=150, help="Number of random forest trees (default: 150).")
    parser.add_argument('--maximum_iteration', type=int, default=2500, help="Maximun number of itterations for the machine learning.")
    parser.add_argument('--phenotypes_directory', type=str, required=True, help="The directory of the csv file of the antibiotic drug resistance phenotypes.")
    parser.add_argument('--logistic_regression', action='store_true', help="Flag to use logistic regression model.")
    parser.add_argument('--random_forest', action='store_true', help="Flag to use random forest model.")
    parser.add_argument('--linear_regression', action='store_true', help="Flag to use linear regression model.")
    args = parser.parse_args()

    if not (args.logistic_regression or args.random_forest or args.linear_regression):
      print("\033[91mNo machine-learning model is selected!\nPlease select at least one model to run the script.\033[0m")
      sys.exit(1)
    return parser.parse_args()






def remove_ambiguous_phenotype_isolates(phenotype, indices):
    """
    Remove isolates with ambiguous (NaN) phenotype values from the given indices.

    Parameters:
    phenotype (numpy array): The phenotype array.
    indices (numpy array): The indices of the data set (training or testing).
    target (numpy array): The target array containing phenotypes for different groups.
    group (int): The group index to extract from the target array.

    Returns:
    numpy array: The filtered indices.
    numpy array: The corresponding phenotypes for this indices.
    """

    # Extract phenotype values for the given indices
    y_values = phenotype[indices]

    # Initialize a list to hold indices of non-NaN values
    non_nan_indices = []
    
    # Iterate over the y_values array to find non-NaN indices
    for i in range(len(y_values)):
        if not np.isnan(y_values[i]):
            non_nan_indices.append(i)

    # Filter the indices to only include non-NaN phenotype indices
    filtered_indices = indices[non_nan_indices]

    # Update the phenotype array to the target group's phenotypes

    # Re-extract the y_values array using the updated indices
    y_values = phenotype[filtered_indices]

    # Convert y_values to integers
    y_values = y_values.astype('int')

    return filtered_indices, y_values

# Test case



def create_train_test_indices(cross_validation_folds, cross_validation_index, cross_validation_indexes_directory):
    """
    Determine the fold number and create the test and train indices for cross-validation.

    Parameters:
    cross_validation_folds (int): Total number of cross-validation folds.
    cross_validation_index (int): Index of the fold to be used as the test set.
    cross_validation_indexes_directory. (str): Directory path containing the indexes for each cross-validation fold.

    Returns:
    tuple: A tuple containing the train indices and test indices.
    """
    # Initialize an empty list to hold the indexes of each fold
    list_indexes = []

    # Load the index of each fold into the list_indexes list
    for i in range(cross_validation_folds):
        # Construct the filename for the current fold's index file
        filename = f"{cross_validation_indexes_directory}indexes_of_fold_{i}.npy"
        
        # Load the numpy array from the file and append it to the list
        list_indexes.append(np.load(filename))

    # Choose the fold specified by cross_validation_index as the test set
    test_index = list_indexes[cross_validation_index]

    # Remove the test fold from the list to leave only the training folds
    list_indexes.pop(cross_validation_index)

    # Concatenate the remaining folds to form the training set
    train_index = np.concatenate(list_indexes)

    return train_index, test_index














def main(): 
  args=parse_arguments()
  antibiotic_resistance_phenotype_dataframe=pd.read_csv(args.phenotypes_directory)

  train_index, test_index= create_train_test_indices(args.cross_validation_folds,args.cross_validation_index, args.cross_validation_indexes_directory)
  # print("Columns in the CSV file are:",flush=True)
  # print(df.columns,flush=True)

  drug_names_list=['ERR', 'ID', 'ERS',"Amikacin",\
              "Bedaquiline", "Clofazimine",\
              "Delamanid","Ethambutol", "Ethionamide",\
              "Isoniazid", "Kanamycin","Levofloxacin",\
              "Linezolid","Moxifloxacin", "Rifampicin",\
              "Rifabutin","Rifampin","Aminoglycoside","Fluoroquinolones"]




  try:
    csv_antibiotic_index = drug_names_list.index(args.antibiotic_drug_name) # This is the index of the antibiotic inside the csv phenotypic data  
  except Exception as error:
    raise ValueError("Could not find the drug name; \
                    The drug names are: \n \
                    Amikacin ,\n \
                    Bedaquiline ,\n \
                    Clofazimine,\n \
                    Delamanid ,\n \
                    Ethambutol ,\n \
                    Ethionamide ,\n \
                    Isoniazid ,\n \
                    Kanamycin ,\n \
                    Levofloxacin ,\n \
                    Linezolid ,\n \
                    Moxifloxacin ,\n \
                    Rifampicin ,\n \
                    Rifabutin ,\n \
                    Rifampin,\n \
                    Aminoglycoside,\n\
                    Fluoroquinolones")

  print("Drug Found!",flush=True)



  csv_file_column_abbreviations=['ERR', 'ID', 'ERS',"AMI",\
              "BDQ", "CFZ",\
              "DLM","EMB", "ETH",\
              "INH", "KAN","LEV",\
              "LZD","MXF", "RIF",\
              "RFB","RIA","AMG","FQS"]


  print("Column number on CSV is {}".format(csv_antibiotic_index),flush=True)
  antibiotic_drug_name=drug_names_list[csv_antibiotic_index]
  drug_names_abbreviation=csv_file_column_abbreviations[csv_antibiotic_index]

  print("The drug is : {}".format(antibiotic_drug_name),flush=True)
  target=np.array(antibiotic_resistance_phenotype_dataframe)
  print("The shape of the target is:",flush=True)
  phenotype=target[:,csv_antibiotic_index]


  # Loading machine learning data
  feature_matrix_directory= os.path.join(args.feature_matrix_directory, antibiotic_drug_name, f"/feature_matrix_{args.total_number_of_features}_features_fold_{args.cross_validation_index}.npy")
  data=np.load(feature_matrix_directory)
  print("The data is loaded",flush=True)
  print("The shape of the used data is:{}".format(np.shape(data)))



  y_train, filtered_train_indices =remove_ambiguous_phenotype_isolates(phenotype,train_index)
  y_test,  filtered_test_indices  =remove_ambiguous_phenotype_isolates(phenotype,test_index)
  x_train=data[filtered_train_indices,:]
  x_test =data[filtered_test_indices,:]


  plt.axis("square")
  plt.xlabel("False Positive Rate",fontsize=16)
  plt.ylabel("True Positive Rate",fontsize=16)
  #plt.title(drug_names_abbreviation,fontsize=22)

  header_csv=["Model", "Kmers used","AUC(%)","F1(%)","accuracy(%)","sensitivity(%)","specificity(%)"]

  csv_file=[]
  logarithm_base=2 # 1 kmers, base kmers, base^2 kmers, base^3 kmers , ...
  list_kmers=[1* pow(logarithm_base,i) for i in range(math.ceil(math.log(((np.size(X_train,1))/1),logarithm_base)))]
  #list_kmers.append(np.size(X_train,1))

  #Logistic Regression
  if (args.logistic_regression):
    for i in list_kmers :

      if ( args.logistic_regression_lasso_threshold<i):
        model=LogisticRegression(penalty='l1', solver='liblinear', max_iter=args.maximum_iteration,C=1/args.logistic_regression_lasso_threshold)
        model_name="Logistic Regression Lasso"
      else: 
        model=LogisticRegression(max_iter=args.maximum_iteration)
        model_name="Logistic Regression"
      
      print("Training {} model with {} Kmers".format(model_name,i),flush=True) 
      # Here we select first i significant features to do the training and evaluation
      x_train_selected= x_train[:,0:i]
      x_test_selected= x_test[:,0:i]
      model.fit(x_train_selected, y_train)

      # Predict class labels for the test set
      y_prediction = model.predict(x_test_selected)

      # Calculate the AUC
      auc = roc_auc_score(y_test, y_prediction) * 100

      # Calculate the F1 score
      f1 = f1_score(y_test, y_prediction) * 100


      # Calculate the accuracy
      accuracy = accuracy_score(y_test, y_prediction) * 100

      # Calculate sensitivity and specificity using confusion matrix
      tn, fp, fn, tp = confusion_matrix(y_test, y_prediction).ravel()
      sensitivity = (tp / (tp + fn)) * 100
      specificity = (tn / (tn + fp)) * 100


      csv_file.append([model_name,i,auc,f1,sensitivity,specificity])
      




  if (args.random_forest):
    
    for i in list_kmers :
      model_name="Random forest"
      print("{} model with {} Kmers".format(model_name,i),flush=True) 
      model = RandomForestClassifier(max_depth=10, random_state=10,n_estimators=RF_trees)

      x_train_selected= x_train[:,0:i]
      x_test_selected= x_test[:,0:i]
      model.fit(x_train_selected, y_train)

      # Predict class labels for the test set
      y_prediction = model.predict(x_test_selected)

      # Calculate the AUC
      auc = roc_auc_score(y_test, y_prediction) * 100

      # Calculate the F1 score
      f1 = f1_score(y_test, y_prediction) * 100


      # Calculate the accuracy
      accuracy = accuracy_score(y_test, y_prediction) * 100

      # Calculate sensitivity and specificity using confusion matrix
      tn, fp, fn, tp = confusion_matrix(y_test, y_prediction).ravel()
      sensitivity = (tp / (tp + fn)) * 100
      specificity = (tn / (tn + fp)) * 100


      csv_file.append([model_name,i,auc,f1,sensitivity,specificity])
      
  
  csv_saving_directory=  os.path.join(args.results_directory, args.antibiotic_drug_name,\
                                      '/cross_validation{}.csv'.format(args.cross_validation_index)\
                                      ,header= header_csv)
  pd.DataFrame(csv_file).to_csv(csv_saving_directory)






   