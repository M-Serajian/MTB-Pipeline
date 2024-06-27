#!/usr/bin/env python3
import unittest
import sys
import os
from unittest.mock import patch
import numpy as np

sys.path.insert(0, os.path.abspath('../../'))

from src.classifier.classifier import (
    remove_ambiguous_phenotype_isolates,
    create_train_test_indices, parse_arguments
)





class TestParseArguments(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_with_logistic_regression(self, mock_parse_args):
        """Test parsing arguments when --logistic_regression is provided."""
        # Setup mock return values
        mock_args = mock_parse_args.return_value
        mock_args.antibiotic_drug_name = 'test_drug'
        mock_args.total_number_of_features = '100'
        mock_args.feature_matrix_directory = '/path/to/features'
        mock_args.results_directory = '/path/to/results'
        mock_args.cross_validation_folds = 5
        mock_args.cross_validation_index = 0
        mock_args.cross_validation_indexes_directory = '/path/to/indexes'
        mock_args.phenotypes_directory = '/path/to/phenotypes'
        mock_args.alpha_lasso = 1.0
        mock_args.logistic_regression_lasso_threshold = 1000
        mock_args.random_forest_trees = 150
        mock_args.maximum_itteration = 2500
        mock_args.logistic_regression = True
        mock_args.random_forest = False
        mock_args.linear_regression = False
        
        # Execute
        args = parse_arguments()
        
        # Assert conditions
        self.assertTrue(args.logistic_regression)
        self.assertFalse(args.random_forest)
        self.assertFalse(args.linear_regression)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_without_any_model_selected(self, mock_exit, mock_parse_args):
        """Test parsing arguments when no model selection flag is provided."""
        # Setup mock return values
        mock_args = mock_parse_args.return_value
        mock_args.antibiotic_drug_name = 'test_drug'
        mock_args.total_number_of_features = '100'
        mock_args.feature_matrix_directory = '/path/to/features'
        mock_args.results_directory = '/path/to/results'
        mock_args.cross_validation_folds = 5
        mock_args.cross_validation_index = 0
        mock_args.cross_validation_indexes_directory = '/path/to/indexes'
        mock_args.phenotypes_directory = '/path/to/phenotypes'
        mock_args.alpha_lasso = 1.0
        mock_args.logistic_regression_lasso_threshold = 1000
        mock_args.random_forest_trees = 150
        mock_args.maximum_itteration = 2500
        mock_args.logistic_regression = False
        mock_args.random_forest = False
        mock_args.linear_regression = False
        
        # Execute
        parse_arguments()
        
        # Test if sys.exit was called due to no model being selected
        mock_exit.assert_called_once()



class TestRemoveAmbiguousPhenotypeIsolates(unittest.TestCase):
    def test_remove_ambiguous_phenotype_isolates(self):
        phenotype = np.array([1, 0, np.nan, 0, 2, np.nan, 1, np.nan, 1])
        indices = np.array([0, 1, 2, 3, 4, 5, 6])
        expected_indices = np.array([0, 1, 3, 4, 6])
        expected_phenotypes = np.array([1, 0, 0, 2, 1])

        filtered_indices, y_values = remove_ambiguous_phenotype_isolates(phenotype, indices)

        np.testing.assert_array_equal(filtered_indices, expected_indices)
        np.testing.assert_array_equal(y_values, expected_phenotypes)


class TestCreateTrainTestIndices(unittest.TestCase):
    @patch('numpy.load')
    def test_create_train_test_indices(self, mock_load):
        # Setup mock
        mock_load.side_effect = [
            np.array([0, 1, 2]),  # Fold 0
            np.array([3, 4, 5]),  # Fold 1
            np.array([6, 7, 8])   # Fold 2
        ]
        
        cross_validation_folds = 3
        cross_validation_index = 1
        cross_validation_indexes_directory = '/fake/directory/'
        
        expected_train_indices = np.array([0, 1, 2, 6, 7, 8])
        expected_test_indices = np.array([3, 4, 5])
        
        train_indices, test_indices = create_train_test_indices(
            cross_validation_folds, cross_validation_index, cross_validation_indexes_directory)
        
        np.testing.assert_array_equal(train_indices, expected_train_indices)
        np.testing.assert_array_equal(test_indices, expected_test_indices)


if __name__ == '__main__':
    unittest.main()
