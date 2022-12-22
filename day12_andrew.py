import string 
import networkx as nx
from pyvis.network import Network

# Update the day number
dayN = 'day12' ; data_path = f'data/{dayN}_input.txt'

with open(data_path, 'r') as f: lines = f.readlines()


# Set grid (2-d) and flat version of it
grid = [[w for w in line if w != '\n'] for line in lines]; flatGrid = [item for g in grid for item in g]

def visualiseNetwork(G, fname='outputs/day12_network.html', directed=True):

    """ Use pyvis to visualise network"""

    net = Network(directed=True)
    # Visualise networka
    net.from_nx(G)
    print(f"Export visualisation to '{fname}'")
    net.show(fname)


def getEdges(grid):

    letters = string.ascii_letters
    letterMap = {letters[i]:i for i in range(len(letters))}

    # Start end positions have 0 and Z respectively
    letterMap.update(dict(S=0,E=25))

    # List of tuples
    edges = []
    
    # Keep a note of the node we're processing
    nodeNum = -1
    for row in range(len(grid)):

        for col in range(len(grid[row])):

            nodeNum += 1
            # print(f"---> nodeNum = {nodeNum}")

            cell = letterMap[grid[row][col]]
            
            # print(f"row={row}, col={col}")
            # print(f"cell={cell} value = {flatGrid[nodeNum]}")

            # Check down
            if row < len(grid)-1: 
                down = letterMap[grid[row+1][col]]
                if (cell >= down) or down-cell==1:
                    edges.append((nodeNum, nodeNum+len(grid[row])))
            # Check up
            if row > 0:
                up = letterMap[grid[row-1][col]]
                if (cell >= up) or up-cell==1:
                    edges.append((nodeNum, nodeNum-len(grid[row])))
                    
            # Check left
            if col > 0:
                left = letterMap[grid[row][col-1]]
                if (cell >= left) or left-cell==1:
                    edges.append((nodeNum, nodeNum-1))
            # Check right
            if col < len(grid[row])-1:
                right = letterMap[grid[row][col+1]]
                if (cell >= right) or right-cell==1:
                    edges.append((nodeNum, nodeNum+1))
    return edges

# Get edges from input (directed)
edges = getEdges(grid)

# Create graph object
G = nx.DiGraph()
G.add_nodes_from( [(i, dict(title=flatGrid[i])) for i in range(len(flatGrid))])

# Get start/end nodes
snode, enode = zip([node[0] for node in G.nodes(data=True) if node[1]['title'] in ['S', 'E']])
snode, enode = snode[0], enode[0]
# Change colour for 2
attrs = {snode:dict(color='blue')}
attrs.update({enode:dict(color='red')})
nx.set_node_attributes(G, attrs)

# Add edges
G.add_edges_from(edges)
# Visualise network
visualiseNetwork(G)

########################################
# Part 1 - shortest path from S to E
########################################
p1_shortest = nx.shortest_path(G, snode, enode)

# Remove the starting node - that isn't a step
p1_shortlength = len(p1_shortest) - 1

print(f"Part 1 answer: {p1_shortlength}")


