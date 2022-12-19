import pandas as pd
import re
import math

# Update the day number
dayN = 'day5'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

# Regular expression to extract boxes from string
rgx_box = re.compile("[A-Z]{1}")
rgx_moveline = re.compile("^move")
rgx_moves = re.compile('[0-9]+')

# Open file
with open(data_path, 'rt') as f: lines = f.readlines()

#########################
## Initial configuation
#########################

def get_stacks(lines):

    """ Load up the initial crate configuration """
    # Init crate object
    stacks = {}

    for line in lines:
        # Extract crates
        crates = list(rgx_box.finditer(line))
        if len(crates)==0:
            break
        else:
            # Get stack numbers for each crate
            stacknums = [math.ceil((c.span()[0]+1)/4) for c in crates]

            # Update the stacks, given teh crates
            for sn in range(len(stacknums)):
                # Get current stack
                currentStack = stacks.get(stacknums[sn])

                # Get crate value
                crate = crates[sn].group()

                # If stack empty then initialise
                if currentStack is None:
                    stacks.update({stacknums[sn]:[crate]})
                else:
                    
                    currentStack.append(crate)
                    stacks.update({stacknums[sn]:currentStack})
    return stacks

def getTop(stacks):

    """ Get the first item from each 'stack'"""

    stacks_ = stacks.copy()
    """ Return top item of each stack"""
    top = []
    for k in sorted(stacks_):
        top.append(stacks_[k][0])
    return top

def processMoves(stacks, lines, part1=True):

    """ Process the entire text file
        Only process lines that start with 'move'
    """

    # Make copy
    stacks_ = stacks.copy()
    # Process file - 
    for line in lines:

        # If this line is a 'move'
        if len(rgx_moveline.findall(line))>0:
            
            # Next move is....
            nextMove = [int(move) for move in rgx_moves.findall(line)]
            
            stacks_ = makeMove(stacks_, *nextMove, part1=part1)
            
    return stacks_

def makeMove(stacks, amnt, source, target, part1=True):

    """
        Make a single move
        With an amount (amnt), move items from source column to target.  
        Return updates stack object (stacks)
    """
    
    # Make copy
    stacks__ = stacks.copy()

    # Find source stack
    src = stacks__[source]

    # Find target stack
    trgt = stacks__[target]

    # Get crates 
    crate_ = src[:amnt]

    # Update source list
    src_new = src[amnt:]
    stacks__.update({source:src_new})

    # Part 2 - Retain order
    if not part1:
        crate_ = crate_[::-1]
    # Add each item to new (target) stack
    for elm in crate_:
        trgt.insert(0, elm)

    # Update the target stack
    stacks__.update({target:trgt})
    return stacks__
    
if __name__=="__main__":

    # Stacks: Load up initial configuration
    stacks = get_stacks(lines)
    print(stacks)

    ################################################
    # Part 1: Crate moves them 'one by one'
    ################################################

    stacks_p1 = processMoves(stacks, lines)

    # Part 1: Get top 
    top_p1 = ''.join(getTop(stacks_p1))
    print(f"Part 1: Top = {top_p1}")
    
    ################################################
    # Part 2: Cratemove 9001 - retains order
    ################################################

    stacks_p2 = processMoves(get_stacks(lines), lines, part1=False)
    top_p2 = ''.join(getTop(stacks_p2))
    print(f"Part 2: Top = {top_p2}")
