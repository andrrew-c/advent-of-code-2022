import pandas as pd
from scipy.spatial.distance import euclidean

import numpy as np

# Update the day number
dayN = 'day9'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

class Knot():

    """ A knot

        Starts out with coordinates as specified 

        updatePos: You can update their position to a specific x,y
        getUniqueCoords: All coords touched at least once (unique)
        getUniqueMoves: Count of unique coords
        makeSingleMove: Calcualte the updated coords given a direction
        touching: Return boolean - True if touching the other knot provided (euclidean distance < 2)
        moveTowards: Move towards a given knot - one step
    """

    def __init__(self, start):

        """ Init head object with x, y coords and init list of coords"""

        self.currentPos = (start[0], start[1])

        # Init list of coords
        self.coords = [self.currentPos]


    def updatePos(self, x, y):

        self.currentPos = x, y
        # Add coordinate to list
        self.coords.append(self.currentPos)
        
    
    def getUniqueCoords(self):

        """ Returns a set of unique coords landed on"""

        return set(self.coords)

    def getUniqueMoves(self):

        """ Returns an integer - unique"""

        return len(self.getUniqueCoords())

    def makeSingleMove(self, dir):

        """ Move the knot one step in the given direction """
        x, y = self.currentPos

        if dir == 'L':
            y -= 1
        elif dir== 'R':
            y += 1
        elif dir == 'U':
            x += 1
        elif dir == 'D':
            x -= 1

        self.updatePos(x,y)

    def touching(self, otherKnot):

        """ Returns True if touching other knot"""
        return euclidean(self.currentPos, otherKnot.currentPos) < 2
        
    def moveTowards(self, otherKnot):

        """ Updates position of self by one, towards otherKnot"""
        # print(f"self.currentpos = {self.currentPos}")
        # Calculate difference in coords
        coordDiff = tuple(map(lambda i,j: (i-j)/2, otherKnot.currentPos, self.currentPos))

        # If any of the coord movements are 0.5 - we need to increase to 1 (a diag move)
        coordDiff = tuple([i*2 if abs(i) == 0.5 else i for i in coordDiff])
        # print(f"coorddiff after mult = {coordDiff}")

        # Move knot
        x, y= tuple(map(lambda i, j: (i+j), self.currentPos, coordDiff))
        self.updatePos(x, y)

class Game():

    """ Let's play the simulation/game
        Initialise with an integer - number of knots
        printPositions: Output all the coords of all knots
        processMove: Given a single input - process the entire simulation/game by one 'move'
    """

    def __init__(self, numKnots):
        
        # Init start position, h and t positions
        self.start = (0,0)

        # Initialise all the knots
        self.knots = [Knot(self.start) for i in range(numKnots)]
      
    def printPositions(self):


        for k in range(len(self.knots)):
            print(f"Knot {i}: {self.knots[k].coords}")

    def processMove(self, dir, num):

        """ Move the head in a certain direction by a number of steps"""

        # For each move
        for i in range(num):
            
            # Move the 'head'
            self.knots[0].makeSingleMove(dir)
            
            # For each tail n+1, check if touching n
            for k in range(1, len(self.knots)):
            
                if not self.knots[k].touching(self.knots[k-1]):
                    
                    # Move knot (k) towards knot (k-1)
                    self.knots[k].moveTowards(self.knots[k-1])  

if __name__ == "__main__":

    # Initialise game
    game = Game(numKnots=10)

    i = 0
    with open(data_path, 'r') as f: lines = f.readlines()
    for line in lines:
        i+=1
        line = line.replace('\n', '').split()
        
        game.processMove(line[0], int(line[1]))

# Part 1/2
print(f"Answer with {len(game.knots)} knots: {game.knots[len(game.knots)-1].getUniqueMoves()}")

