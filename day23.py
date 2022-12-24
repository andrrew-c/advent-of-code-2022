# Update the day number
dayN = 'day23'

# Day N data
data_path = f'data/{dayN}_input.txt'

# Read file and init elves
with open(data_path, 'r') as f: lines = f.readlines(); lines = [line.replace('\n', '') for line in lines]

maxX, maxY = len(lines)-1, len(lines[0])-1
print(maxX, maxY)
moves = dict( N  = (-1, 0)
            , E  = (0, 1)
            , S  = (1, 0)
            , W  = (0, -1)
            , NW = (-1, -1)
            , NE = (-1, 1)
            , SW = (1, -1)
            , SE = (1, 1)
            )

class Elf():

    def __init__(self, startpos):

        self.pos = startpos
        self.posOrder = ['N', 'S', 'W', 'E']

    def Surrounded(self, positions):

        """ Return True if there is at least one elf nearby (surrounding 8)"""

        # If no elf is in the surrounding 8 cells
        # return len(positions.difference(self.pos).intersection([(i,j) for i in range(self.pos[0]-1,self.pos[0]+2) for j in range(self.pos[1]-1,self.pos[1]+2) if (i,j) != self.pos and 0<=i<=maxX and 0<=j<=maxY])) > 0
        
        # surround =  [t for t in [tuple(sum(x) for x in zip (self.pos, moves[m])) for m in moves] if 0 <= t[0] <= maxX and 0 <= t[1] <= maxY]
        surround =  [t for t in [tuple(sum(x) for x in zip (self.pos, moves[m])) for m in moves]]
        return len(positions.difference(self.pos).intersection(surround)) > 0 
         

    def PosFree(self, positions, direction='N'):

        """ N if N, NE, NW are free
            S if S, SE, SW are free
            E if E, NE and SE are free
            S if S, SE, SW are free
        """
        

        othPositions = positions.difference(self.pos)
        # addx0, addx1, addy0, addy1 = -1, 2, -1, 2
        if direction == 'N':
            addx1 = 0
            return len(othPositions.intersection([(i,j) for i in range(self.pos[0]-1,self.pos[0]) for j in range(self.pos[1]-1,self.pos[1]+2) if (i,j) != self.pos]))==0
        elif direction == 'S':
            addx0 = 1
            return len(othPositions.intersection([(i,j) for i in [self.pos[0]+1] for j in range(self.pos[1]-1,self.pos[1]+2) if (i,j) != self.pos ]))==0
        elif direction == 'W':
            return len(othPositions.intersection([(i,j) for i in range(self.pos[0]-1, self.pos[0]+2) for j in [self.pos[1]-1] if (i,j) != self.pos ]))==0
        elif direction == 'E':
            return len(othPositions.intersection([(i,j) for i in range(self.pos[0]-1,self.pos[0]+2) for j in [self.pos[1]+1] if (i,j) != self.pos ]))==0
        else:
            return False

    def getProposal(self, positions):
        
        # Update the order
        oldOrder = self.posOrder.copy()
        self.posOrder = self.posOrder[1:] + [self.posOrder[0]]
        # Init dir variable
        dir = None

        # If not surrounded - do nothing
        if not self.Surrounded(positions):
            return self.pos
        elif self.PosFree(positions, oldOrder[0]): dir = oldOrder[0]
        elif self.PosFree(positions, oldOrder[1]): dir = oldOrder[1]
        elif self.PosFree(positions, oldOrder[2]): dir = oldOrder[2]
        elif self.PosFree(positions, oldOrder[3]): dir = oldOrder[3]
        if dir is None: return self.pos
        else: return tuple(sum(x) for x in zip(self.pos, moves[dir]))

if __name__ == "__main__":

    def doRound(elves, part2=False, running=False):

        # Get positions
        positions = set([e.pos for e in elves])

        if part2:
            if sum([e.Surrounded(positions) for e in elves]) == 0:
                # print(f"There have been {:,} rounds until elves stopped moving")
                return elves, False
            else:
                if iRound%10 ==0: print(f"Round number {iRound:,}: There are {len(elves)} elves and {sum([not e.Surrounded(positions) for e in elves])} didn't move")

        # Get proposals
        proposals = [e.getProposal(positions) for e in elves]

        # Check proposals and update accordingly
        for p in range(len(proposals)):
            if proposals.count(proposals[p]) ==1:
                elves[p].pos = proposals[p]
        if not part2: return elves
        else: return elves, running



    numRounds = 10

    # Get elves
    elves = [Elf(pos) for pos in [(row, col) for row in range(len(lines)) for col in range(len(lines[row])) if lines[row][col]=='#']]
    
    # Part 1
    for r in range(numRounds):

        # Do a round
        elves = doRound(elves)

        # Get positions
        positions = set([e.pos for e in elves])

    # Get positions (list)
    positions = [e.pos for e in elves]
    
    ###############
    # Part 1: Number of empty cell
    ###############

    # Grid min/max
    gminX, gmaxX = min([p[0] for p in positions]), max([p[0] for p in positions])
    gminY, gmaxY = min([p[1] for p in positions]), max([p[1] for p in positions])

    empty_cells = len([cell+1 for cell in [j for i in range(gminX, gmaxX+1) for j in range(gminY, gmaxY+1)]])-len(elves)
    print(f"Part 1 answer = {empty_cells}")

    # Part 2:

    running = True
    iRound = 0
    elves = [Elf(pos) for pos in [(row, col) for row in range(len(lines)) for col in range(len(lines[row])) if lines[row][col]=='#']]
    while running:
        iRound += 1
        elves, running = doRound(elves, part2=True, running=running)

    print(iRound)