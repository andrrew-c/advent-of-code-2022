import json
# Update the day number
dayN = 'day13'

# Day N data
data_path = f'data/{dayN}_input.txt'

# Read entire file
with open(data_path, 'r') as f: lines = f.readlines()

# Lists from file
lists = [json.loads(line) for line in lines if line !='\n']

# Pairs (list of tuples)
pairs = [(i, i+1) for i in range(0, len(lists), 2)]

# Dictionary of pairs (i.e. 0:(0,1))
dpairs = {i:pairs[i] for i in range(len(pairs))}


""" Scenarios

L = R: Keep checking
L < R: Inputs in right order
L > R: Inputs are NOT in right order
L runs out: Inputs in right order
R runs out: Inputs are NOT in right order

"""

a = [1, [[2,3]]]
b = [[1,2], [3,4]]


def compare_lists(L, R):

    if L is None and R is not None:
        return True
    if R is None and L is not None:
        return True

    if isinstance(L, int) and isinstance(R, int):

        if L < R:
            return True
        if L > R:
            return False

    elif isinstance(L, int) and

def recurList(lst):
    
    if isinstance(lst, int): 
        return int
    if isinstance(lst[0], list):
        if len(lst[0]) >0:
            return recurList(lst[0])
        else:
            return None
    else:
        return lst

ordered = None

# Who has more items L or R?
moreItems = None

def whoHasMore(a, b):
    moreItems = None
    if isinstance(a, int) and isinstance(b, int):
        return moreItems
    if len(a) > len(b): 
        moreItems = 'L'
    if len(b) > len(a):
        moreItems = 'R'

    return moreItems

pair = 6
p1 = lists[pairs[pair-1][0]]
p2 = lists[pairs[pair-1][1]]


checkPairs(p1, p2)

def checkPairs(p1, p2):
        
    for ai, bi in zip(p1, p2):

        if recurList(ai) is None:
            moreItems = 'R'
            return True
            
        elif recurList(bi) is None:
            moreItems = 'L'
            return False

        if isMixedTypes(ai, bi):
            print("Mixed types")
            ai, bi = convertTypes(ai,bi) 
        elif isinstance(ai, int) and isinstance(bi, int):
            print(f"Both int: ai={ai}, bi={bi}")
            if ai < bi: 
                return True
            elif ai > bi: 
                return False
            else:
                continue
        print(f"ai:{ai} bi:{bi}")

            

        print(f"ai:{ai} bi:{bi}")
       
        moreItems = whoHasMore(ai,bi)
        print("..",ai,bi)
        for aj, bj in zip(recurList(ai), recurList(bi)):

            if aj is None:
                moreItems = 'R'
                return True
                
            elif bj is None:
                moreItems = 'L'
                return False
            print(f"\taj={aj}\n\tbj={bj}")
        
            if aj < bj:
                print("ordered!")
                return True
                break
            if aj > bj:
                print("Not ordered!")
                return False
                break
        
        if ordered is None: 
            print("No decision on order")
            print(f"{moreItems} has more items")
            break
        
    print(f"Ordered = {ordered}")
    return ordered





recurList(a[1])



def convertToList(item):

    """ If not list - convert to one"""
    if isinstance(item, int): item = [item]
    return item

def convertTypes(p1, p2):

    p1 = convertToList(p1)
    p2 = convertToList(p2)
    return p1, p2

def isMixedTypes(p1,p2):

    i1 = type(p1)
    i2 = type(p2)

    # If mixed type
    if i1 != i2:
        return True

def checkPair(p1, p2):

    # Init boolean
    rightOrder = False

    for a, b in zip(p1, p2):
        print(f"a:{a}\nb:{b}")   

        for i, j in zip(a, b):
            print(f"\ti:{i}\n\tj:{j}")
        
            if isMixedTypes(i, j):

                # Convert types
                i, j = convertTypes(i,j)
                print("Convert types")
                print(f"\ti:{i}\n\tj:{j}")


       
            if i==j:
                print(f'i==j: Keep going...')
            if i<j:
                # Update
                rightOrder=True 
                print(f"Pair in right order")
                break
        if rightOrder: 
            break
        
    print(f"Right order= {rightOrder}")
    if rightOrder ==False and len(p1)<len(p2):
        print(f"LHS < RHS")
        rightOrder=True

    print(f"**** rightOrder={rightOrder}")
    return rightOrder
        
pairsInRightOrder = []
for p, idx in dpairs.items():


    print(p, idx)

    print(f"Pair: {p}")
    p1 = lists[idx[0]]
    p2 = lists[idx[1]]
    if checkPairs(p1, p2):
        
        pairsInRightOrder.append(p+1)

p1_sum = sum(pairsInRightOrder)
print(f"Part 1 answer: {p1_sum}")

    