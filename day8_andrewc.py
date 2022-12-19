import pandas as pd
import numpy as np

# Update the day number
dayN = 'day8'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

grid = np.genfromtxt(data_path, delimiter=1)

# Init answer grid at one
answer = np.ones(shape=grid.shape)
answer2 = np.zeros(shape=grid.shape)

# For each row
for r in range(1,grid.shape[0]-1):

    # For each column
    for c in range(1,grid.shape[1]-1):

        # Current cell
        cell = grid[r,c]

        # Look up, down, left and right
        slcUp = grid[:r,c][::-1]
        slcDown = grid[r+1:, c]
        slcLeft = grid[r,:c][::-1]
        slcRight = grid[r,c+1:]

        # Bring together slices (up,down,left,right)
        slices = [slcUp, slcDown, slcLeft, slcRight]
        
        # Each element is a True/False array
        checks = [cell>slice for slice in slices]

        ################################################
        # Part 1:
        ################################################

        # Check that each tree is fully visible in each direction
        visp1 = [sum(check)==len(check) for check in checks]

        # If all trees are blocking, answer is 0
        if sum(visp1)==0:
            answer[r,c]=0
        
        ################################################
        # Part 2: How much can each tree see?
        ################################################

        visp2 = [np.argmin(check)+1 if sum(check)<len(check) else len(check) for check in checks]
        
        # Calculate scenic score
        answer2[r,c] = np.prod(visp2)
        
## Part 1: Needs to be fully visible in a row/column
print(f"Part 1 answer: {answer.sum()}")
print(f"Part 2 answer: {answer2.max()}")