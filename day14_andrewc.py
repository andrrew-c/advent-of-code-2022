
import pygame
import re
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Update the day number
dayN = 'day14'

# Day N data
data_path = f'data/{dayN}_input.txt'

# Regex to extract coords
rgxXY = re.compile(r'[0-9]+(?:,)[0-9]+')

with open(data_path, 'r') as f: lines = f.readlines()

# Get rocks in entire file
coords = [rgxXY.findall(line) for line in lines]
coordsTuples = []

# Create a list of tuples
for coord in coords:
    # tuples = []
    tuples = [tuple(c.split(',')) for c in coord]
    tuples = [(int(tup[0]), int(tup[1])) for tup in tuples]
    coordsTuples.append(tuples)

class Sand():

    """ A a unit of sand """

    def __init__(self, grid, startPos=(500, 0), verbose=False, part2=False):

        """A unit of sand has a starting position (tuple)
            A unit of sand belongs to a grid
            A unit of sand has a list of positions it has taken
            A unit of sand has a currentPos

            By default - sand is NOT considered to be falling into the abyss (abyss = False)
            A unit of sand has the atRest property (boolean)
            A unit of sand moves (not atRest) until it cannot anymore (atRest = True)
            
            If a unit of sand falls below the lowest rock on the grid - it is considered 'falling into the abyss = True)
            

        """
        
        self.grid = grid
        # Boolean for at rest and in abyss
        self.abyss = False
        self.atRest = False

        # Get starting position and record in list of movements
        self.currentPos = startPos
        self.positions = [self.currentPos]

        # Cell below
        self.cellBelow = self.getCellBelow()

        self.verbose = verbose

    def getCellBelow(self):

        return self.currentPos[0], self.currentPos[1]+1

    def getCellDLDR(self, DL=True):

        """Get position for downleft (DL) or downright (DL=False)"""

        if DL:
            return self.currentPos[0]-1, self.currentPos[1]+1
        else:
            return self.currentPos[0]+1, self.currentPos[1]+1

    def canMove(self, newPos):

        """ Return True if cell below is free"""


        # If cell below is already in 
        if newPos in self.grid.rocks.union(self.grid.sands):
            return False
        else:
            return True

    def updatePos(self, part2=False):

        """ Update sand position by one"""

        if self.atRest:
            # print(f"I am at rest - i cannot move D, L or R")
            return None

        # Init newCell as current
        newCell = self.currentPos

        # Check if can move down one
        if self.canMove(self.cellBelow):
            if self.verbose: print(f"Can move down from {self.currentPos} to {self.cellBelow}")
            newCell = self.cellBelow
        # Can we move down left?
        elif self.canMove(self.getCellDLDR()):
            if self.verbose: print(f"Can move down left from {self.currentPos} to {self.getCellDLDR()}")
            newCell = self.getCellDLDR()

        # Can we move down right
        elif self.canMove(self.getCellDLDR(False)):
            if self.verbose: print(f"Can move down right from {self.currentPos} to {self.getCellDLDR(False)}")
            newCell = self.getCellDLDR(False)

        # We cannot move down, left or right.  We are now at rest
        else:
            if self.verbose: print(f"Cell at {self.currentPos} is now at rest")
            self.atRest=True
            return None
        # If new cell is different
        if newCell != self.currentPos:

            # Is the new cell the start of the abyss?
            if self.inAbyss(newCell):
                self.abyss = True
                if self.verbose: print("This move would move this sand into the abyss")
            if not self.abyss:
                # If not in the abyss - let's update position
                self.currentPos = newCell
                self.cellBelow = self.getCellBelow()
                self.positions.append(self.currentPos)

        # Else, the new cell is at rest
        else:
            self.atRest=True
            
            self.currentPos = self.cellBelow
            self.cellBelow = self.getCellBelow()
            self.positions.append(self.currentPos)

    def inAbyss(self, newpos):

        """ if the sand is going to fall below the rocks - then it is falling into the abyss
            Retrun true

        """
        # print(self.grid.furthestRock())
        if newpos[1] >= self.grid.furthestRock(minn=False)[1]:
            
            return True
        else:
            return False
            # This sand would fall into the abyss
    
class Grid():

    def __init__(self, coords, part2=False):

        # Keep a note of the individual coordinates provided - each element represents tuples in a single line of the input
        self.coords = coords

        # Generate all cells that represent rocks  (flatten list)
        self.points = self.generate_all_points(self.coords)

        # Flatten out list of rocks
        self.rocks = set([item for sublist in self.points for item in sublist])

        # Keep a record of the sand objects
        # self.sandlist = set([])
        # Keep a record of latest position of all sands sand that has fallen/is falling
        self.sands = set()

        self.numAtRest = 0
        # Initialise boolean - keep simulation running
        self.keepGoing = True

    def getCurrentPopulated(self):

        pass
    def generate_all_points(self, coords):

        """ Generate all points from a "list of list" of tuples"""

        # Initiate
        points = []
        for coord in coords:
            # print(f"coord ={coord}")
            for c in range(len(coord)-1):
                # print(f"c={c}")
                newPoints = self.generate_points(coord[c], coord[c+1])
                points.append(newPoints)
        return points

    def generate_points(self, p1, p2):


        """ Given two tuples - calcualte the points between
            Assumes only X or Y changes
        """
        
        # If moving in x
        if p1[0]!=p2[0]:
            x = np.linspace(p1[0], p2[0], abs(p2[0]-p1[0])+1, dtype='int')
            points = [(xi, p1[1]) for xi in x]
        
        # If moving in y
        if p1[1]!=p2[1]:
            y = np.linspace(p1[1], p2[1], abs(p2[1]-p1[1])+1, dtype='int')
            points = [(p1[0], yi) for yi in y]
        return points

    def furthestRock(self, minn=True):

        """ X or Y coordinate of lowest rock"""

        if minn:

            ### X coordinate of the lowest rock
            # X = min([r[0] for r in self.rocks])
            Y = min([r[1] for r in self.rocks])
            # print(minX, minY)
        else:
            # X = max([r[0] for r in self.rocks])
            Y = max([r[1] for r in self.rocks])
        X = [r[0] for r in self.rocks if r[1] == Y]
        return X, Y
        
    def XYRange(self):

        """ Return min and max of grid"""

        # Get lowest rock
        minn = self.furthersRock()
        # Get highest rock
        maxx = self.furthersRock(False)
        return minn, maxx


    def dropSand(self):


        verbose=False
        if self.numAtRest > 913: verbose=True
        
        # Init some sand
        sand = Sand(self, verbose=verbose)

        # While latest piece of sand is not at rest
        while not sand.atRest:
            
            # Update position of sand
            sand.updatePos()
            # self.sands[-1] = sand.currentPos
            if sand.abyss:
                print("This sand is in the abyss!")
                self.keepGoing=False
                break
        # print(f"Sand is at rest! {sand.atRest} - sand pos = {sand.currentPos}")

        # Add 1 to 'at rest'
        self.numAtRest+=1
        self.sands.add(sand.currentPos)
        # print(self.sands)
            
    def runSimulation(self):

        i=0
        while self.keepGoing:

            # Update index counter
            i+=1

            # Print what we're doing
            if i%10==0: 
                print(f"Dropping sand number {i:,}")
                # print(f"self.keepGoing = {self.keepGoing}")
                # print(f"Latest sand was at rest at {list(self.sands)[-1]}")

            # Drop next piece of sand
            self.dropSand()

# Init grid
grid = Grid(coordsTuples)
# grid.runSimulation()

#############
## Part 1
#############

print(f"Part 1: We dropped {len(grid.sands)-1:,} pieces of sand")
