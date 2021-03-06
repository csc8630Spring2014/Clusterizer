import networkx as nx
from matplotlib import pyplot as plt
from json import dumps
import re, hashlib



def get_pdb_dict():
        """Takes CATH domain list and returns dictionary of PDB codes
        & their CATH families"""
        pdbs = {}
        fh = open('CathDomainList', 'r')
        lines = fh.read().split('\n')
        fh.close()
        colors_dict = {}
        for line in lines:
                #ignore comments
                if not line.startswith('#'):
                        #tokens = line.split()
                        #lines are space-delimited, so need re.split() here
                        tokens = re.split('\s+', line)
                        pdb = tokens[0][0:5].upper()
                        #split the PDB into root identifier and chain id
                        #could be more/less precise by using more/fewer columns
                        cath = '.'.join(tokens[1:5])
                        pdbs[pdb] = [cath]
                        color = "#000000"
                        color = "#"+hashlib.md5(str(cath)).hexdigest()[:6]
                        colors_dict[cath]=color
        with open("cathcolors.json","w") as fp:
                fp.write(dumps(colors_dict))
        return pdbs

get_pdb_dict()

class JSONNode():
        def __init__(self, energy, children):
                self.energy = energy
                self.children = children
        def repr(self):
                return {'name':str(int(self.energy*100))+"%", 'size':self.energy**-1,'children':self.children}


global_g = None

def fileReader(filename):
        with open(filename) as fp:
                line = fp.readline()
                yield line.split(",")
                line = fp.readline()
                while line:
                        yield line.split(",")
                        line = fp.readline()


RAWDICT = get_pdb_dict()


def ParsedGraph(fileName):

        G = nx.Graph()
        for line in fileReader(fileName):
                origin = line.pop(0).upper()
                metadata = line.pop(0)#throw away metadata
                if origin not in G.node:
                        G.add_node(origin)
                #G.node[origin]["data"] = metadata
                #print "origin", origin
                while len(line)>0:
                        other = line.pop(0)
                        dist = float(line.pop(0))

                        if dist == 0.0:
                                dist = float("inf")
                        else:
                                dist= dist**-1
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
        #if depth > 100:
        #        return graph.nodes()
        subgraphs = []
        toRecurse = []
        energy = 0.0
        done = False
        #print graph.edges(data=True)
        while not done:
                while(nx.is_connected(graph)): #alter the graph, untill it disconnects
                        print "CHOPPING"
                        biggest = max(graph.nodes(), key=lambda x: graph.node[x]["weight"]) #go find the biggest radius node
                        energy = max((energy,graph.node[biggest]["weight"]))
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
                        if len(g.nodes()) == 1:
                                subgraphs.append(g.nodes())
                        else:
                                toRecurse.append(g)
                print "HAVE ", len(toRecurse), "TO RECURSE"
                if len(toRecurse) <= 10: #we spawned an orphan, iterate
                        print "ITERATING"
                        graph = toRecurse.pop()
                elif len(toRecurse) > 10:
                        #time to bother forking!
                        done = True
                        print "RECURSING"
                        for r in toRecurse:
                                subgraphs.append(partition(r,depth+1))
                else:
                        done = True
        return (energy, subgraphs)


def partition2XML(p):
        global global_g
        def recurse(G,subp):
                
                if type(subp[0]) == type(0.0):#new node
                        G+="\n<NODE energy='"+str(subp[0])+"'/>"
                        newroot = subp[0]
                        for sub in subp[1:]:
                                G = recurse(G,sub)
                        G+="\n</NODE>"
                else:

                        if type(subp) == type(list()):
                                for n in subp:
                                        G = recurse(G,n)
                        else:
                                G+="\n<PROTEIN name='"+str(subp)+"'/>\n"+global_g.node[subp]["data"]
                                G+="\n</PROTEIN>"
                return G

        G = "<TREE/>"
        print p
        root = p[0]
        G+="\n<ROOT energy='"+str(root)+"'/>"
        for subp in p[1:]:
                G = recurse(G,subp)
        G+="\n</ROOT>"
        return G+"\n</Tree>"

def partition2JSON(p):
        global global_g
        colors_dict = {}
        def recurse(root,subp):
                global colors_dict
                try:
                        subp[0]
                except Exception:
                        if type(root) is dict:
                                return root
                        else:
                                return root.repr()
                if type(subp[0]) == type(0.0):#new node
                        newNode = JSONNode(float(subp[0])**-1,[]).repr()
                        for sub in subp[1:]:
                                root['children'].append(newNode)
                                newNode = recurse(newNode,sub)
                        return root
                else:

                        if type(subp) == type(list()):
                                for n in subp:
                                        root = recurse(root,n)
                        else:
                                color = "#000000"
                                if str(subp) in RAWDICT:
                                        cathid = RAWDICT[str(subp)]
                                        print(len(cathid), cathid)
                                        color = "#"+hashlib.md5(str(cathid)).hexdigest()[:6]
                                        colors_dict[cathid]=color
                                else:
                                        cathid = "None"

                                protein = {'name':str(subp), 'cathid':cathid, 'color':color,'size':1}

                                root['children'].append(protein)
                if type(root) is dict:
                        return root
                else:
                        return root.repr()

        print p
        root = JSONNode(float(p[0])**-1,[]).repr()
        for subp in p[1:]:
                root = recurse(root,subp)

        with open("cathcolors.json","w") as fp:
                fp.write(dumps(color_dict))


        return dumps(root,sort_keys=False,indent=4, separators=(',', ': '))



def partition2Graph(p):
        def recurse(G,root,subp):
                #print type(subp),subp
                if type(subp[0]) == type(0.0):
                        print subp
                        newroot = subp[0]
                        G.add_node(newroot)
                        G.add_edge(root, newroot)
                        for sub in subp[1:]:
                                recurse(G,newroot,sub)
                else:
                        if type(subp) == type(list()):
                                for n in subp:
                                        recurse(G,root,n)
                        else:
                                G.add_node(str(subp))
                                G.add_edge(root,str(subp))
                return G       
        G = nx.Graph()
        print p
        root = p[0]
        G.add_node(root)
        for subp in p[1:]:
                G = recurse(G,root,subp)
        print "about to return",type(G)
        return G



global_g = ParsedGraph("100_out_raw.txt")

nx.draw(global_g)
plt.show()

gprime = genMinEnergyCoverGraph(global_g)



print "graphifying"
partitions = partition(gprime.copy())
#tree_graph = partition2Graph(partitions)

# same layout using matplotlib with no labels
<<<<<<< HEAD
with open("brendan_output.json","w") as fp:
=======
with open("100_output.json","w") as fp:
>>>>>>> 724effabd505f02400a53c3c898293f60eb8b412
        fp.write(partition2JSON(partitions))

#plt.title("draw_networkx")
#nx.draw(gprime)
#plt.show()

