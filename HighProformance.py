import networkx as nx
from matplotlib import pyplot as plt
def fileReader(filename):
        with open(filename) as fp:
                line = fp.readline()
                yield line.split(",")
                line = fp.readline()
                while line:
                        yield line.split(",")
                        line = fp.readline()





def ParsedGraph(fileName):
        G = nx.Graph()
        for line in fileReader(fileName):               
                origin = line.pop(0)
                metadata = line.pop(0)#throw away metadata
                if origin not in G.node:
                        G.add_node(origin)
                #print "origin", origin
                while len(line)>0:
                        other = line.pop(0)
                        dist = float(line.pop(0))
                        #print other, dist
                        if other not in G.node:
                                G.add_node(origin)
                        G.add_edge(origin,other,{"weight":dist})
        return G


def genMinEnergyCoverGraph(G):
        MST = nx.minimum_spanning_tree(G,weight="weight")
        RadiusGraph = MST.copy()
        for n in MST.nodes():
                edges = MST.edges(nbunch=[n],data=True)
                ##print edges
                farthest = max(edges, key=lambda x: x[2]['weight']  )
                r = farthest[2]["weight"]
                MST.node[n]["weight"] = r
                RadiusGraph.node[n]["weight"] = r
                old_edges = G.edges(nbunch=[n],data=True)
                for e in old_edges:
                        to = e[1]
                        dist = e[2]["weight"]
                        if dist < r:
                                RadiusGraph.add_edge(n, to, weight=dist )
        return RadiusGraph

def partition(graph, depth=0):
        #reduce the radius of the largest node
        #cut resulting edge
        #check and see if we partitioned the graph
        #if the size of split is < 3 iterate
        #if the size of split is > 3 recurse
        #dont go more than 6 levels deep
        if depth > 6:
                return (0.0, graph)
        subgraphs = []
        toRecurse = []
        energy = 0.0
        done = False
        #print graph.edges(data=True)
        while not done:
                while(nx.is_connected(graph)): #alter the graph, untill it disconnects
                        print "CHOPPING"
                        biggest = max(graph.nodes(), key=lambda x: graph.node[x]["weight"]) #go find the biggest radius node
                        energy += graph.node[biggest]["weight"]
                        peers = sorted(graph.edges(nbunch=[biggest], data=True), key=lambda x: -1* x[2]['weight']) #find that node's availible peers
                        graph.remove_edge(biggest, peers[0][1]) #cut the link with the one furthest away
                        if len(peers) >1:
                                graph.node[biggest]["weight"] = peers[1][2]["weight"] #replace it with the next-lowest radius
                        else:
                                graph.node[biggest]["weight"] = -1 #This one is now along, it's radius has no meaning
                #we must have managed to partition the graph
                #lets insepect the sub-graphs
                print "PARTITONED!"
                tmpsubgraphs = nx.connected_component_subgraphs(graph) #get all the new fancy subgraphs
                print "GOT SUBGRAPHS", subgraphs
                for g in tmpsubgraphs:
                        if len(g.nodes()) <= 3:
                                subgraphs.append(g.nodes())
                        else:
                                toRecurse.append(g)
                print "HAVE ", len(toRecurse), "TO RECURSE"
                if len(toRecurse) == 1: #we spawned an orphan, iterate
                        print "ITERATING"
                        graph = toRecurse.pop()
                elif len(toRecurse) > 1:
                        #time to bother forking!
                        done = True
                        print "RECURSING"
                        for r in toRecurse:
                                subgraphs.append(partition(r,depth+1))
                else:
                        done = True
        return (energy, subgraphs)




g = ParsedGraph("test_input.csv")

gprime = genMinEnergyCoverGraph(g)

print partition(gprime.copy())

nx.draw_spring(gprime, weight="weight")
plt.show()

