import numpy as np
import re

class Monkey():

    """
    Each monkey has several attributes:

        Starting items lists your worry level for each item the monkey is currently holding in the order they will be inspected.
        Operation shows how your worry level changes as that monkey inspects an item. (An operation like new = old * 5 means that your worry level after the monkey inspected the item is five times whatever your worry level was before inspection.)
        Test shows how the monkey uses your worry level to decide where to throw an item next.
        If true shows what happens with an item if the Test was true.
        If false shows what happens with an item if the Test was false.

    After each monkey inspects an item but before it tests your worry level, your relief that the monkey's inspection didn't damage the item causes your worry level to be divided by three and rounded down to the nearest integer.

    The monkeys take turns inspecting and throwing items. On a single monkey's turn, it inspects and throws all of the items it is holding one at a time and in the order listed. Monkey 0 goes first, then monkey 1, and so on until each monkey has had one turn. The process of each monkey taking a single turn is called a round.

    When a monkey throws an item to another monkey, the item goes on the end of the recipient monkey's list. A monkey that starts a round with no items could end up inspecting and throwing many items by the time its turn comes around. If a monkey is holding no items at the start of its turn, its turn ends.
    """


    def __init__(self, mnum, items, operation, divisor, monkeyTrue, monkeyFalse, verbose, boredomFactor):

        """Initialise attributes of monkey
            mnum: Integer - monkey index number
            item: List of integers - worry levels of items
            operation: String defining the mathematical function of the monkey
            divisor: Integer to check which monkey to throw to 
            monkeyTrue: Integer - number of monkey to throw to if True
            monkeyFalse: Integer - number of monkey to throw to if False
        """

        # Keep a tab on monkey index number
        self.mnum = mnum

        # Items (worry levels) 
        self.items = items

        # Init count of the number of times a monkey inspects an item
        self.inspectedItems = 0

        # Add divisor (integer)
        self.divisor = int(divisor)

        # True/False (depending on divisor 'test')
        self.monkeyTrue = monkeyTrue 
        self.monkeyFalse = monkeyFalse 

        # Monkey's boredom factor (currently all have the same)
        self.boredomFactor = boredomFactor
        
        # Worry level operation - Derive method
        self.operation = operation
        opString = self.operationMaker(self.operation)
        # print(opString)

        # Execute the function definition
        exec(opString, globals())

        # Add function to class
        self.updateWorryLevel = updateWorryLevel


        # Whether monkey prints out information
        self.verbose = verbose
        
    def operationMaker(self, operation, varprefix='old'):
        
        """ Base version of Monkey operation to be modified by decorator

        """

        # Split arguments (e.g. "old + 1" -> "old", '+' and '1')
        val1, oper, val2 = operation.split(' ')

        # Init bored string
        bored = "boredom"
        # Define the function we need
        # operationStr = f"""def updateWorryLevel({varprefix}): return {val1} {oper} {val2}"""
        if oper == "+": 
            modCheck = "v1+v2"
        else:

            modCheck = "v1*v2"
            # Are we squaring it?
            if self.boredomFactor == 1:
                if val1 == val2:
                    val2 = 1
                else:
                    pass
                    # val1 = val1%self.divisor
                    # val2 = val2%self.divisor
                    # bored = 'boredom%divisor'
            
            modCheck = "v1*v2"
                  
        operationStr = f"""
def updateWorryLevel({varprefix}, boredom, divisor): 
    v1 = {val1} #%divisor
    v2 = {val2} #%divisor
    b = boredom #%divisor
    return int(({modCheck})/b)
    
    
"""
        print(operationStr)
        return operationStr
 
    def decideMonkey(self, item):

        """ Decide which monkey gets the item next
         - based on current worry level of item
         """
        if item%self.divisor == 0:
        # if self.checkMonkey(item, self.boredomFactor, self.divisor):
            # print("Ran self checkMonkey, item = {item}, self.checkMonkey(item, self.divisor) {self.checkMonkey(item, self.divisor)}")
            return self.monkeyTrue
        else:
            return self.monkeyFalse
        
    def inspectItem(self, item):
        pass

    def throw(self, item, monkey):

        """ Throw object to monkey number 
        """

        if self.verbose: print(f"\tProcess item is {item} going to monkey {monkey}")

        # Append the item to the other monkey's list
        self.game.monkeys[monkey].items.append(item)
            
    def processItem(self, item):

        """
            For a given item:
            
            Worry level is updated as per self.updateLevels (Monkey's individual operation)
            Monkey gets bored with item. Worry level is divided by Game's parameter for deprec.
            Check which monkey gets the item (based on self.divisor)
            Remove item from current monkey and add item to other monkey
    
        """
        # if self.boredomFactor > 1:
            # Update worry level
            # itemUp = int(self.updateLevels(item))

            # Monkey gets bored
            # itemUp = int(itemUp//self.boredomFactor)
    
        # Decide which monkey gets it next (returns index of monkey)
        itemUp = self.updateWorryLevel(item, self.boredomFactor, self.divisor)
        nextMonkey = self.decideMonkey(itemUp)

        # Throw item to that monkey
        self.throw(itemUp, nextMonkey)

    def processMove(self):

        """ process each item for Monkey"""
        if self.verbose: print(f"Processing monkey: {self.mnum}")
        # For each item in Monkey
        for item in self.items:

            self.inspectedItems += 1
            # Process item
            self.processItem(item)

        # Remove all items from Monkey
        self.items = []


class Game():

    """ Play 'monkey in the middle' """

    def __init__(self, inputFile, boredomFactor = 3, verbose=False):

        # Init regular expressions
        self.initRegEx()

        # Process input file
        self.input = self.readInput(inputFile)

        # Get number of monkeys
        self.nMonkeys = len(self.rgxMonkeys.findall(self.input))

        ######################################################
        ## Process input 
        ## into lists which we can then initialise the 'monkeys'
        ######################################################

        # Get starting items (list of integers)
        items = [[int(i) for i in i.split(',')] for i in self.rgxItems.findall(self.input)]

        # Get operations (e.g. "old + 1")
        operations = self.rgxOperation.findall(self.input)

        # Divisors for test (e.g. True if divsible by 13)
        divisors = self.rgxTest.findall(self.input)

        # List of monkeys to send to if True/False
        MTrues = [int(i) for i in self.rgxMTrue.findall(self.input)]
        MFalse = [int(i) for i in self.rgxMFalse.findall(self.input)]
        
        ####################
        # Initialise monkeys
        ####################

        self.monkeys = [ Monkey(m, items[m], operations[m], divisors[m], MTrues[m], MFalse[m], verbose, boredomFactor) for m in range(self.nMonkeys)]
        
        # Add self to each monkey so we can get back
        for monkey in self.monkeys:
            monkey.game = self

    def initRegEx(self):

        """ Initialise regular expressions"""
        
         # Regex to get number of monkeys
        self.rgxMonkeys = re.compile(r'^Monkey', re.MULTILINE)

        # Starting items
        self.rgxItems = re.compile("(?<=  Starting items: ).+", re.MULTILINE)

        # Operation string
        self.rgxOperation = re.compile("(?<=  Operation: new = ).+", re.MULTILINE)
        
        # Test and where to send it
        self.rgxTest = re.compile("(?<=  Test: divisible by )\d+", re.MULTILINE)
        self.rgxMTrue = re.compile("(?<=    If true: throw to monkey )\d+", re.MULTILINE)
        self.rgxMFalse = re.compile("(?<=    If false: throw to monkey )\d+", re.MULTILINE)

    def readInput(self, inputFile):

        """ Take input file from puzzle and return """

        # Now open file
        with open(inputFile) as f: input = f.read()
        
        return input

    def processRound(self, numRounds=1):

        # Process numRound times
        for i in range(numRounds):
            # For each monkey - process their individual move
            for monkey in self.monkeys:
                monkey.processMove()

    def printItems(self):
        """ Print out list for each monkey"""

        for monkey in self.monkeys:
            print(monkey.items)

    def printNInspected(self):
        """ Number of times monkey had inspected any item"""

        for monkey in self.monkeys:
            print(monkey.inspectedItems)
            
    def getMonkeyBusiness(self, n=2):

        """Return the monkeyBusiness value
            Calculated as the product of the two largest counts of inspected items
        """

        # Get a list of the number of inspected items
        inspectList = [monkey.inspectedItems for monkey in self.monkeys]

        # N largest values
        inspectList.sort()
        largestVals = np.array(inspectList[-n::])

        # Calcualte product of N largest values
        monkeyBusiness = largestVals.prod()
        return monkeyBusiness

# Update the day number
dayN = 'day11'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

game = Game(data_path, verbose=True)

game.processRound(20)

game.printItems()
game.printNInspected()

##############
# Part 1
##############

p1_answer = game.getMonkeyBusiness()
print(f"Part 1: {p1_answer}")

##########################################
# Part 2 - boredom no longer affects
##########################################

game2 = Game(data_path, boredomFactor=1)
game2.processRound(20)
game2.printItems()
game2.printNInspected()

p2_answer = game2.getMonkeyBusiness()
print(f"Part 2: {p2_answer}")

def updateWorryLevel(old, boredom, divisor): 
    v1 = old%divisor
    v2 = 19%divisor
    b = boredom%divisor
    print(f"v1, v2, b = {v1}, {v2}, {b}")
    return int((v1*v2)/b)