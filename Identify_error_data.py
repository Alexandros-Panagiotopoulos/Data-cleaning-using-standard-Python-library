import collections
import csv
import statistics
from datetime import datetime
from typing import List, Tuple

def check_file_data(file_path: str) -> List[Tuple[datetime.date, float, str]]:
    """read the CSV file and add the error values in a list"""
    outlier_check_period = 30   #only a small sample is being used to find the outliers to better match a normal distribution
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
            if (count+1) % outlier_check_period == 0:   #Check for outliers every few rows (samples)
                outliers = check_for_outliers(date_data, value_data, outliers)
        outliers = check_for_outliers(date_data, value_data, outliers)
    return missing_values  + stale_values + outliers

def add_row_to_deques(date_data:list, value_data:list, row:tuple):
    format_str = '%d/%m/%Y'
    date_data.append(datetime.date(datetime.strptime(row[0], format_str))) #converts the date string into datetime.date type
    if row[1]:
        value_data.append(float(row[1]))
    else:
        value_data.append(None) #in case of missing value a none type is added

def move_error_data(error_list:list, date_data:list, value_data:list, message:str, position:int=-1):
    error_list.append((date_data[position], value_data[position], message))
    del date_data[position]
    del value_data[position]

def check_for_missing_value(date_data:list, value_data:list, missing_values:list):
    if value_data[-1] == None:
        move_error_data(missing_values, date_data, value_data, 'missing value')
    return missing_values

def check_for_stale_value(date_data:list, value_data:list, stale_values:list):
    week_days = 7
    for counter in range(len(value_data)-1, -1, -1):
        if value_data[counter] == value_data[-1]:
            if (date_data[counter] - date_data[-1]).days >= week_days:
                move_error_data(stale_values, date_data, value_data, 'stale value')
        else:
            break
    return stale_values

def check_for_outliers(date_data:list, value_data:list, outliers:list):
    """ Finds the outliers based on the normal distribution principle that 99%
     of the values are within range of 2.6 standard deviations from the mean value"""
    no_of_standard_deviations_acceptale = 2.6
    #With 2.6 standard deviations range it is expected about 1% of values to be false positive as outliers or about 20 in 2000 entries
    outlier_found = True
    #series contains extreme outliers which are unrelated values and also outliers of smaller offsets
    #extreme outliers greatly affect the std of the sample and so after removing an outlier the std is recalculated
    #and outliers are being searched from the beginning of the sample
    while outlier_found:
        outlier_found = False
        lower_limit, upper_limit = find_acceptable_value_range(date_data, value_data, no_of_standard_deviations_acceptale)
        for counter, value in enumerate(value_data):
            if not lower_limit < value < upper_limit:
                move_error_data(outliers, date_data, value_data, 'outlier', counter)
                outlier_found = True
                break
    return outliers

def find_acceptable_value_range(date_data:list, value_data:list, no_of_standard_deviations_acceptale:float):
    value_data_std = statistics.pstdev(value_data)
    value_data_mean = statistics.mean(value_data)
    outlier_cut_off = value_data_std * no_of_standard_deviations_acceptale
    lower_limit  = value_data_mean - outlier_cut_off 
    upper_limit = value_data_mean + outlier_cut_off
    return lower_limit, upper_limit
    
def main(path_to_csv_file: str):
    error_data = check_file_data(path_to_csv_file)
    return error_data

if __name__ == '__main__':
    path_to_csv_file = "Equity_history_raw.csv"
    error_data = main(path_to_csv_file)