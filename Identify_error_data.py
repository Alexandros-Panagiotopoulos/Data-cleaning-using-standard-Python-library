import collections
import csv
from datetime import datetime
from typing import List, Tuple

def check_file_data(file_path: str) -> List[Tuple[datetime, float, str]]:
    date_data = collections.deque(maxlen=28)
    value_data = collections.deque(maxlen=28)
    missing_values = []
    stale_values = []
    outliers = []
    outlier_check_period = 28
    with open (file_path) as raw_data:
        reader = csv.reader(raw_data)
        next(reader)    #skip the header
        for count, row in enumerate(reader):
            missing_values = check_for_missing_value(date_data, value_data, row, missing_values)
            stale_values = check_for_stale_value(date_data, value_data, row, stale_values)
            if count % outlier_check_period == 0:
                outliers = check_for_outliers(date_data, value_data, row, outliers)
    return ['temporary output']

def check_for_missing_value(date_data, value_data, row, missing_values):
    return []

def check_for_stale_value(date_data, value_data, row, stale_values):
    return []

def check_for_outliers(date_data, value_data, row, outliers):
    return []
    
def main(path_to_csv_file: str):
    error_data = check_file_data(path_to_csv_file)
    return error_data

if __name__ == '__main__':
    path_to_csv_file = "Equity_history_raw.csv"
    error_data = main(path_to_csv_file)
    print(error_data)