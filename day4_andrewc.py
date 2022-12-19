# import numpy as np
import pandas as pd

# Update the day number
dayN = 'day4'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

# Read data
df = pd.read_csv(data_path)

def overlap(p1, p2, part=1):

    """ Common function for part 1 and part 2
    """

    # Get start and end of range
    p11, p12 = map(int, p1.split('-'))
    p21, p22 = map(int, p2.split('-'))
    # Get a range object
    rng1 = range(p11, p12+1)
    rng2 = range(p21, p22+1)

    # Part 1 - whether rng1 or rng2 is a total subset of the other
    s1 = set(rng1).issubset(set(rng2))
    s2 = set(rng2).issubset(set(rng1))
    
    # Part 1 return if either is a subset
    if part==1:
        return s1 or s2

    # PArt 2 - return True if any overlap
    if part==2:
        return len(set(rng1).intersection(set(rng2)))>0

# Part 1: Total overlaps
df['overlap'] = df.apply(lambda row: overlap(row['p1'], row['p2']), axis=1)
olaps = df.overlap.sum()
print(f"Part 1: There are {olaps:,} TOTAL overlaps")

# Part 2: Any overlap
df['overlap2'] = df.apply(lambda row: overlap(row['p1'], row['p2'], part=2), axis=1)
olaps2 = df.overlap2.sum()
print(f"Part 2: There are {olaps2:,} ANY overlaps")