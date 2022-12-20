import re
import networkx as nx
from pyvis.network import Network
import itertools

from datetime import datetime
# Update the day number
dayN = 'day16'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

# Time left in minutes
maxTime = 30

# All valves
rgx_valves = re.compile(r'[A-Z]{2}')
rgx_flows = re.compile(r'(?<==)[0-9]+')
startPoint = 'AA'

class Valve():

    """
        A valve has a name (e.g. AA)
        A value as a flow rate (flowR) - integer
        A valve has one or more child valves
    """

    def __init__(self, name, flowR, children=None):

        self.name = name
        self.flowR = flowR
        self.children = children

        # Each valve started closed
        self.open = False

class Person():

    """ """

    def __init__(self, startValve):

        # What valve am I being initiated at?
        self.currentValv = startValve

    def moveValv(self):

        """Move from one valve to another 
            Time passes
            Update current valve
        """

        pass

class Simulation():

    allValves = []

    def __init__(self, path, maxTime):
     
        # Parse file input - list of valves
        self.valves = self.parseInput(path)
        
        # Get graph object
        self.G = self.createNetwork()
        
        # What nodes are worth turning on?
        self.flowsWorth = {n:v['flow'] for n,v in self.G.nodes(data=True) if v['flow'] > 0}

        # Permutations of valves to open
        self.valvePerms = itertools.permutations(self.flowsWorth)

        self.maxTime = maxTime
 
    def parseInput(self, path):

        """ Parse all input"""

        # print(f"Path = {path}")
        with open(path, 'r') as f: lines = f.readlines()

        # Init list of valvs
        valveList = []
        # First initiate the valves with no children
        for line in lines:

            # Get all valves/flows in line
            valves, flow = self.parseLine(line)
            # print(f"valves, flows = {valves}, {flow}")

            nextValve = Valve(name=valves[0], flowR=flow[0], children=valves[1:])
        
            valveList.append(nextValve)
            
        return valveList

    def parseLine(self, line):

        # Valve names
        vs = rgx_valves.findall(line)

        # Flow rates
        flows = [int(flow) for flow in rgx_flows.findall(line)]
        return vs, flows

    def printValves(self):

        """Return names of valves loaded"""
        return [v.name for v in self.valves]

    def getValve(self, vname):

        """ Return valve object that matches the name given by vname"""

        return [v for v in self.valves if v.name==vname][0]

    def createNetwork(self):

        G = nx.Graph()
        
        # Edge data
        edges = [(v.name,child) for v in self.valves for child in v.children]

        # Add nodes
        # G.add_nodes_from([v.name for v in sim.valves], size=[v.flowR for v in sim.valves])
        G.add_nodes_from([(v.name, {'size':v.flowR+2, 'flow':v.flowR, 'title':f"{v.name}: {v.flowR}"}) for v in self.valves], color='blue')
        # Add edges
        G.add_edges_from([edge for edge in edges])

        # G.nodes['AA']['color'] = 'red'
        nx.set_node_attributes(G, {'AA':'red'}, 'color')
        return G
        
    def visauliseNetwork(self, fname='day16_network.html'):

        """ Use pyvis to visualise network"""

        net = Network()
        # Visualise networka
        net.from_nx(self.G)
        print(f"Export visualisation to '{fname}'")
        net.show(fname)

    def processPermutation(self, perm):

        # Get route we need to follow
        mustStops = list((startPoint,) + perm)

        # Create dictionary of order to open valves
        mustStopsOrder = {mustStops[i]:i for i in range(1,len(mustStops))}
        
        # Get fastest route given the valves
        route = self.getFastestRoute(mustStops)

        pressure = self.calcPressure(route, mustStopsOrder)
        
        return pressure
    def getFastestRoute(self, mustStops):

        """ Given the nodes to hit - what are the fastest routes between
            mustStops = iterable of (string) nodes to hit
        """

        # List of tuples - of points (A-B)
        route = []      

        # Full (quickest) route between each pair (i.e. A-A1-A2-B)
        fullRoute = []
        
        # What points do we need to stop at?
        for n in range(len(mustStops)-1):
            # print(n)
            route.append((mustStops[n], mustStops[n+1]))
        # print(f"len route {len(route)}")

        # With the pairs - what is the fastest route?        
        for p in range(len(route)): 
            # print(f"p={p}")
            # Get shortest path between pair
            routes = nx.shortest_path(self.G, route[p][0], route[p][1])
            # print(routes)
            # Remove duplicate nodes (i.e. A-A-B can become A-B)
            if p > 0:
                routes = routes[1:len(routes)]
            
            fullRoute.extend(routes)

        return fullRoute

    def calcPressure(self, route, mustStopsOrder):

        """ Calculate the amount of pressure released by traversing over route 
            You need to stop on each mustStop
            Each valve must be opened only in the order they were specified in mustStopsOrder (dict)
        """

        # What is the shortest route - going through each node
        # route = self.getFastestRoute(perm)

        # init constants
        timeAvail = self.maxTime  
        iNumOpen = 0
        pressures = []
        latestPressure = 0

        # Initialise number on route at -1
        routen = -1

        # Whilst there is time
        while timeAvail > -1:

            # Add pressure amount before update
            pressures.append(latestPressure)

            # Decrement time
            timeAvail -= 1

            # Move up the route map
            routen += 1

            # Check if steps are left
            routen = min(len(route)-1, routen)

            # Get next move
            move = route[routen]

            # print(f"routen={routen}, move={move}")

            # If the current move is in the 'must stops'
            if move in mustStopsOrder:

                # print(f".. Valve {move} is a mustStop")
                # print(f"mustStopsOrder[move]==iNumOpen + 1 = {mustStopsOrder[move]} {iNumOpen + 1}")

                # If this valve shall be opened in this order
                if mustStopsOrder[move]==iNumOpen + 1:

                    pressures.append(latestPressure)
                    # Update number of open valves
                    iNumOpen+=1

                    # Update time available - by another minute due to 'opening the valve'
                    timeAvail -= 1

                    # Update pressure released
                    latestPressure += self.G.nodes[move]['flow']
                    # print(f"Latest pressure = {latestPressure}")
        
        return sum(pressures)

    def runOverCombos(self):

        iIterations = 0
        maxPressure = 0
        
        # Iterate
        for perm in self.valvePerms:

            iIterations += 1
            if iIterations%10000==0:
                print(f"Iteration: {iIterations:,} time: {datetime.now()}")

            # With a given permuation (route order) - calculate the pressure
            newPressure = self.processPermutation(perm)

            if newPressure > maxPressure: 
                print(f'We have new pressure!')
                # print(f"Old pressure = {maxPressure} new pressure = {newPressure}")
                maxPressure = newPressure
        return maxPressure

# Start simulation
sim = Simulation(data_path, maxTime=maxTime)

#######################
# Part 1 answer
#######################

p1_answer = sim.runOverCombos()
start = datetime.now()
print(f"Part 1 answer: {p1_answer}")
print(f"Process took: {datetime.now()-start}")