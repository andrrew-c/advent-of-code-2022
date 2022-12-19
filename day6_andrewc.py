# Update the day number
dayN = 'day6'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

with open(data_path) as f: line = f.read()

def getStartofMessage(line, packetSize):

    """ Loop through string until previous packetSize chars are unique"""

    # Init boolean
    keepGoing = True

    i = 1
    while keepGoing:

        packet = line[i-1:i-1+packetSize]

        if len(set(packet))==packetSize:
            return i-1+packetSize          
            keepGoing=False
        else:
            i+=1 
if __name__=="__main__":

   # Part 1: 4 characters
   
   p1 = getStartofMessage(line, 4)
   print(f"Part 1 answer: {p1}")

   # Part 2: 4 characters

   p2 = getStartofMessage(line, 14)
   print(f"Part 2 answer: {p2}")
