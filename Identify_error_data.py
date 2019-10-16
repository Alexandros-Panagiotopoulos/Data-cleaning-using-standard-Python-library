import collections
import csv
import statistics
from datetime import datetime
from typing import List, Tuple

def check_file_data(file_path: str) -> List[Tuple[datetime.date, float, str]]:
    outlier_check_period = 30
    date_data = collections.deque(maxlen=outlier_check_period)
    value_data = collections.deque(maxlen=outlier_check_period)
    missing_values = []
    stale_values = []
    outliers = []
    with open (file_path) as raw_data:
        reader = csv.reader(raw_data)
        next(reader)    #skip the header
        for count, row in enumerate(reader):
            add_row_to_deques(date_data, value_data, row)
            missing_values = check_for_missing_value(date_data, value_data, missing_values)
            stale_values = check_for_stale_value(date_data, value_data, stale_values)
            if (count+1) % outlier_check_period == 0:
                outliers = check_for_outliers(date_data, value_data, outliers)
    return outliers + stale_values + missing_values

def add_row_to_deques(date_data, value_data, row):
    format_str = '%d/%m/%Y' # The format
    date_data.append(datetime.date(datetime.strptime(row[0], format_str)))
    if row[1]:
        value_data.append(float(row[1]))
    else:
        value_data.append(None)

def check_for_missing_value(date_data, value_data, missing_values):
    if value_data[-1] == None:
        missing_values.append((date_data.pop(), value_data.pop(), 'missing value'))
    return missing_values

def check_for_stale_value(date_data, value_data, stale_values):
    week_days = 7
    for counter in range(len(value_data)-1, -1, -1):
        if value_data[counter] == value_data[-1] or counter == 0:
            if (date_data[counter] - date_data[-1]).days >= week_days:
                stale_values.append((date_data.pop(), value_data.pop(), 'stale value'))
        else:
            break
    return stale_values

def check_for_outliers(date_data, value_data, outliers):
    # Set upper and lower limit to 3 standard deviation
    outlier_found = True
    while outlier_found:
        outlier_found = False
        lower_limit, upper_limit = find_acceptable_value_range(date_data, value_data)
        for counter, value in enumerate(value_data):
            if value > upper_limit or value < lower_limit:
                outliers.append((date_data[counter], value, 'outlier'))
                del date_data[counter]
                del value_data[counter]
                outlier_found = True
                break
    return outliers

def find_acceptable_value_range(date_data, value_data):
    value_data_std = statistics.pstdev(value_data)
    value_data_mean = statistics.mean(value_data)
    outlier_cut_off = value_data_std * 2.6
    lower_limit  = value_data_mean - outlier_cut_off 
    upper_limit = value_data_mean + outlier_cut_off
    return lower_limit, upper_limit
    
def main(path_to_csv_file: str):
    error_data = check_file_data(path_to_csv_file)
    return error_data

if __name__ == '__main__':
    path_to_csv_file = "Equity_history_raw.csv"
    error_data = main(path_to_csv_file)
    print(len(error_data))
    path_to_csv_file = "FX_history_raw.csv"
    error_data = main(path_to_csv_file)
    print(len(error_data))
    path_to_csv_file = "InterestRate_history_raw.csv"
    error_data = main(path_to_csv_file)
    print(len(error_data))
    print(error_data)