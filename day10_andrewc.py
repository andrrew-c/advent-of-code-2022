import numpy as np 
import pandas as pd

# Update the day number
dayN = 'day10'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

###################
# Set up constants
###################

numCycles = {'noop':1, 'addx':2}

# Answer indices
idx_start = 20
idx_end = 220
idx_step = 40

# Go from start to end (inclusive) by step amounts
idx_answer = [i for i in range(idx_start, idx_end+idx_step, idx_step)]

# Initial state
initState = 1

####
## Part 2 constants

numCols = 40
numRows = 6
crt = np.zeros(numRows*numCols)

def updateSpriteArray(sa, X):

    """ Update sprite array given a position X"""

    sa = np.zeros(sa.shape())
    sa[X-1:X+2] = 1
    return sa


if __name__ == "__main__":

    ###############
    ## Part 1
    ###############
        
    # Read in data - fill missing with zero
    df = pd.read_csv(data_path, header=None, sep=' ',names='instruction,amount'.split(',')).fillna(0)

    # Add initial state to first amount
    df.loc[0, 'amount'] += initState

    # Calculate individual cycle increments
    df['cycleincr'] = df['instruction'].map(numCycles)

    # End cycle (from each instruction)
    df['cycle'] = df['cycleincr'].cumsum()

    # Calculate rolling amount
    df['amountsum'] = df['amount'].cumsum()

    # Calculate new index with no missing cycles
    new_index = pd.Series(range(1,df['cycle'].max()+1)).rename('cycle')

    # Create new dataframe
    df = df.merge(new_index, how='right', left_on='cycle', right_on='cycle')
    df = df.fillna(method='ffill')

    # Calculate amount X during the cycle
    df['X'] = df['amountsum'].shift(1)
    
    # Set first cycle of X to 1
    df.loc[0,'X'] = 1
    df['X'].fillna(method='ffill', inplace=True)

    # Calculate signals
    df['signal'] = df['cycle'] * df['X']

    # For part2 - the pixel col
    df['col'] = ((df['cycle']-1)%40)+1

    # Get cycles of interest
    df_p1_cycles = df[df['cycle'].isin(idx_answer)]

    # Calculate sum
    print(f"Part 1 answer: {df_p1_cycles['signal'].sum()}")

    # Determine wether we need to draw a pixel
    df['pixel'] = df.apply(lambda row: '#' if (row['X']-1)<=row['col']-1<=(row['X']+1) else '.', axis=1)


    f = open('day10.txt', 'wt') 
    # df.f.write(df.iloc[0:40]['pixel'].to_string())
    for i in range(numRows):

        # Tuple of indexes
        idx0, idx1 = i*numCols, (i+1)*numCols

        # String
        st = df.iloc[idx0:idx1]['pixel'].to_string(index=False).replace('\n', ' ')

        # Write series on single line - no index and replace new line chars with space - end line with new line
        f.write(f"{st}\n")

    # Close text file
    f.close() 
        