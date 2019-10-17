import unittest
import datetime
from Identify_error_data import check_file_data

class IdentifyErrorDataTestCase(unittest.TestCase):
    """Test for Identify_error_data.py"""

    def test_check_file_data_for_missing_values(self):
        error_values = check_file_data ('sample_for_testing_missing_values.csv')
        expected = [(datetime.date(2017, 12, 29), None, 'missing value'),
                    (datetime.date(2017, 12, 28), None, 'missing value'),
                    (datetime.date(2017, 12, 21), None, 'missing value'),
                    (datetime.date(2017, 12, 18), None, 'missing value')]
        
        self.assertEqual(error_values, expected)

    def test_check_file_data_for_stale_values(self):
        error_values = check_file_data ('sample_for_testing_stale_values.csv')
        expected = [(datetime.date(2017, 12, 28), 7620.68, 'stale value'),
                    (datetime.date(2017, 12, 19), 7592.66, 'stale value'),
                    (datetime.date(2017, 12, 18), 7592.66, 'stale value'),
                    (datetime.date(2017, 12, 1), 7544.09, 'stale value')]
        
        self.assertEqual(error_values, expected)

    def test_check_file_data_for_outliers(self):
        error_values = check_file_data ('sample_for_testing_outliers.csv')
        expected = [(datetime.date(2017, 12, 15), 0, 'outlier'),
                    (datetime.date(2017, 12, 13), 7800, 'outlier'),
                    (datetime.date(2017, 9, 27), 732222, 'outlier'),
                    (datetime.date(2017, 9, 26), 7000, 'outlier')]
        
        self.assertEqual(error_values, expected)

    def test_check_file_data_for_various_errors(self):
        error_values = check_file_data ('sample_for_testing_varius_errors.csv')
        expected = [(datetime.date(2017, 12, 26), None, 'missing value'),
                    (datetime.date(2017, 12, 18), 7592.66, 'stale value'),
                    (datetime.date(2017, 12, 1), 8000, 'outlier')]
        
        self.assertEqual(error_values, expected)

#Many more tests should be included but ommited as they considered beyond the scope of current test

unittest.main()