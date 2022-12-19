import os
os.chdir('/home/jovyan/ds-risk-team-adventofcode/')

from datetime import datetime

# import numpy as np
import pandas as pd

# Day 1 data
data_path = 'andrewc_2022/data/day1_input.txt'


def print_time_taken(start):
    
    """ Simple function to print out how long the process took """
    
    print(f"Process took: {datetime.now()-start}")
    
def print_result(calories_list):
    
    """ Print results for different attempts """
    
    # Some print statements for submission
    print(f"There were {len(calories_list):,} elves")
    print(f"The maximum number of calories for one elf was {max(calories_list):,}")


def attempt_1_loop():
    
    """ Attempt 1: Using a loop """
    
    # Make a not of the start of the process
    start = datetime.now()

    # Get lines to iterate over
    with open(data_path, 'rt') as f: lines = f.readlines()
    
    # Init list of calorie counts
    cal_list = []

    # Init cal_count (reset within loop)
    cal_count = 0
    last_max = 0
    
    # Iterate over lines in input
    for line in lines:

        # Strip whitespace (removal of \n at end of line)
        line = line.strip()

        # If line has some data
        if line != '':

            # Add up calories to cumulative count
            cal_count += int(line)

        else:
            # Append latest calorie count
            cal_list.append(cal_count)
            
            # Keep a note of maximum calorie
            max_cl = max(cal_list)
            
            # Check if maximum has changed
            if max_cl != last_max:
#                 print(f"New max = {max_cl}")
                last_max = max_cl

            # Reset calories
            cal_count = 0

    # Print out the results
    print_result(cal_list)
    
    # How long did this take?
    print_time_taken(start)
    
def attempt_2_pandas():
    
    """ Using pandas with groupb """
    
    # Make a note of when this started
    start = datetime.now()
    
    # No header and keep blank lines
    df = pd.read_csv(data_path, header=None, skip_blank_lines=False)

    # Rename default column
    df.rename(columns={0:'calories'}, inplace=True)
    
    # Get index of missing lines
    idx = df[df['calories'].isna()].index
    
    # Create integers from 1 to n (keep index as original)
    idx_row_number = pd.DataFrame(data=range(len(idx)), index=idx).rename(columns={0:'elf_num'})
    
    # Add back to original df
    df = df.merge(idx_row_number, how='left', left_index=True, right_index=True)
    
    # Initialise first row to 0
    df.iloc[0, 1] = 0
    
    # Populate all elf numbers using 'back fill' - to repeat the previous non-missing value
    df.elf_num.fillna(method='bfill', inplace=True)
    
    # Remove missing calories
    df = df[df.calories.notnull()]
    
    # Calculate total number of calories by elf
    sum_cals = df.groupby('elf_num')['calories'].sum()
    
   # Some print statements for submission
    print_result(sum_cals)

    # How long did this take?
    print_time_taken(start)
    
    return sum_cals

def sum_over_top_N(series, topN = 3):
    
    """Returns the sum total over the topN largest numnbers """
    
    # Turn series to df
    series = series.to_frame()
    
    # Add rank to series
    series['rank'] = series.rank(ascending=False)
    
    # Sort data and keep top N
    series.sort_values(by='rank', inplace=True)
    topOfList = series.iloc[:3, :]
    
    # Get sum
    sumCal = topOfList['calories'].sum()

    # print it oot!
    print(f"Total calories for the top {topN} reindeers was {sumCal:,}")

if __name__ == "__main__":
    
    ########################################
    # Part 1: Who is carrying the most?
    ########################################

    # Attempt 1: Used a loop
#     attempt_1_loop()
    
    # Attempt 2: Using index to groupby
    sum_cals = attempt_2_pandas()

    ########################################
    # Part 2: Top N total
    ########################################
    
    sum_over_top_N(sum_cals)
    
