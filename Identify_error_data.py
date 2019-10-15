import collections
import csv
from datetime import datetime
from typing import List, Tuple

def check_file_data(file_path: str) -> List[Tuple[datetime, float, str]]:
    outlier_check_period = 5
    date_data = collections.deque(maxlen=outlier_check_period)
    value_data = collections.deque(maxlen=outlier_check_period)
    missing_values = []
    stale_values = []
    outliers = []
    with open (file_path) as raw_data:
        reader = csv.reader(raw_data)
        next(reader)    #skip the header
        for count, row in enumerate(reader):
            date_data.append(row[0])
            value_data.append(row[1])
            missing_values = check_for_missing_value(date_data, value_data, missing_values)
            stale_values = check_for_stale_value(date_data, value_data, stale_values)
            if count % outlier_check_period == 0:
                outliers = check_for_outliers(date_data, value_data, outliers)
    return stale_values

def check_for_missing_value(date_data, value_data, missing_values):
    if value_data[-1] == "":
        missing_values.append((date_data.pop(), value_data.pop(), 'missing value'))
    return missing_values

def check_for_stale_value(date_data, value_data, stale_values):
    week_days = 7
    format_str = '%d/%m/%Y' # The format
    for counter in range(len(value_data)-1, -1, -1):
        if value_data[counter] != value_data[-1] or counter == 0:
            if (datetime.strptime(date_data[counter], format_str) - datetime.strptime(date_data[-1], format_str)).days >= week_days:
                stale_values.append((date_data.pop(), float(value_data.pop()), 'stale value'))
            break
    return stale_values




def check_for_outliers(date_data, value_data, outliers):
    return []
    
def main(path_to_csv_file: str):
    error_data = check_file_data(path_to_csv_file)
    return error_data

if __name__ == '__main__':
    path_to_csv_file = "Equity_history_raw.csv"
    error_data = main(path_to_csv_file)
    print(error_data)