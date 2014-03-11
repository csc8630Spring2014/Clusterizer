import networkx as nx
import random
import matplotlib.pyplot as plt
import time

#this python file generates a large random all-all graph then preforms the MST heuistic on it.

start = time.time()

G = nx.complete_graph(1000)
for e in G.edges_iter():
        G[e[0]][e[1]]["dist"]=random.randint(1,100)

MST = nx.minimum_spanning_tree(G,weight="dist")
"""
for n in MST.nodes():
        edges = MST.edges(nbunch=[n],data=True)
        r = max(edges,key=lambda())
"""
pos = nx.spring_layout(MST,weight="dist")

nx.draw(MST,pos)
end = time.time()
print end-start
plt.show()