# import numpy as np
import pandas as pd
import string

# Day 3 data
data_path = 'andrewc_2022/data/day3_input.txt'

# Read data
df = pd.read_csv(data_path)

# a-z/A-z mapping from 1-52
letters = string.ascii_letters
priority = {l:i+1 for l,i in zip([l for l in letters], [i for i in range(len(letters))] )}

def calculate_score(s):

    """ Cut the string in half - return two objects"""

    fh = s[:int(len(s)/2)]
    sh = s[int(len(s)/2):]

    # Find commonn letter (problem assumes 1 common)
    common = list(set(fh).intersection(sh))[0]

    # Map to priority score 
    score = priority[common]
    return score  

# Get first/second half of string
df['priority_score'] = df.rucksack.apply(lambda x: calculate_score(x))

#############################
# Part 1: Total of scores
#############################

# Column sum
print(f"Part 1: Total is {df.priority_score.sum():,}")

#########################################
# Part 2: Total of scores across N groups
#########################################

# Create groups
ngroups = 3
# Group each row of N (3)
df['group'] = pd.Series(df.index/ngroups).astype(int)+1 

# Get row number 1-N
df['rownum']  = df.reset_index().groupby('group').transform('rank')['index']

# Get variable name before unstack
df['bag'] = 'bag_'+df['rownum'].astype('int').astype('str')

# Create three columns - for each rucksack
df_ = df.set_index(['group', 'bag'])['rucksack'].unstack()
df_.columns = [c for c in df_.columns]
def common_3(col1, col2, col3):

    """ Across three strings - what is the one commong letter (case sensitive) """

    # What is shared across all three?
    common = list(set(col1).intersection(set(col2)).intersection(col3))[0]

    # Map to scoring system
    score = priority[common]
    return score 

df_['score'] = df_.apply(lambda row: common_3(row['bag_1'], row['bag_2'], row['bag_3']), axis=1)
print(f"Part 2: Total is {df_.score.sum():,}")