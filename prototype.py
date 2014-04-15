import networkx as nx
import random
import matplotlib.pyplot as plt
import time
from ete2 import Tree, TreeStyle
import json

#The Big Scary Algorithim
def partition(graph, depth=0):
        print depth
        energy = 0
        if len(graph.nodes())>3 and depth < 6: #minimum cluster size, stop deviding anythign smaller. 3,2, and 1 size clusters can still happen!
                while(nx.is_connected(graph)): #alter the graph, untill it disconnects
                        biggest = max(graph.nodes(), key=lambda x: graph.node[x]["weight"]) #go find the biggest radius node
                        energy += graph.node[biggest]["weight"]
                        peers = sorted(graph.edges(nbunch=[biggest], data=True), key=lambda x: -1* x[2]['weight']) #find that node's availible peers
                        graph.remove_edge(biggest, peers[0][1]) #cut the link with the one furthest away
                        if len(peers) >1:
                                graph.node[biggest]["weight"] = peers[1][2]["weight"] #replace it with the next-lowest radius
                        else:
                                graph.node[biggest]["weight"] = -1 #This one is now along, it's radius has no meaning

                subgraphs = nx.connected_component_subgraphs(graph) #get all the new fancy subgraphs

                recurse = [energy]
                recurse.append(map(lambda x: partition(x,depth+1),subgraphs))

                return tuple(recurse) #RECURSE
        else:
                return  str((energy,graph.nodes()))



def renderPartitionsIntoGraph(parttree):
        def renderRecurse(subset, g, depth=0):
                if depth > 3:
                        g.add_node(subset)
                        return (subset)
                else:
                        try:
                                for x in subset:
                                        g.add_node(x)
                                        for y in renderRecurse(x,g,depth+1):
                                                g.add_edge(x,y)
                                return subset
                        except TypeError:
                                print subset
                                g.add_node(subset)
                                return [subset]
        G = nx.Graph()

        renderRecurse(parttree, G,0)
        return G



#this python file generates a large random all-all graph then preforms the MST heuistic on it.

start = time.time()

G = nx.powerlaw_cluster_graph(50, 10,0.5, seed=None)
for e in G.edges_iter():
        G[e[0]][e[1]]["weight"]=random.randint(1,100)

MST = nx.minimum_spanning_tree(G,weight="weight")

RadiusGraph = MST.copy()

for n in MST.nodes():
        edges = MST.edges(nbunch=[n],data=True)
        #print edges
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


nodes = RadiusGraph.nodes()
total_radius = sum(map(lambda x: RadiusGraph.node[x]["weight"], nodes))

average_radius = total_radius/float(len(nodes))
partgraph =  partition(RadiusGraph)
print json.dumps(partgraph)


source = str(partgraph)+";"
t = Tree(source)
ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 180
t.show(tree_style=ts)
#pos = nx.spring_layout(partgraph,weight="weight")
#nx.draw(partgraph,pos)
#nx.draw(RadiusGraph,pos)
#end = time.time()
#print end-start
#plt.show()

