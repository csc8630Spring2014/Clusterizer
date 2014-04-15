import random

def GenerateCluster(num_of_clusters, num_of_nodes):
        assert num_of_clusters <= num_of_nodes
        output = ""
        distances = {}
        for i in range(0,num_of_nodes):
                output+=str(i)+",blah"
                for j in range(0,num_of_nodes):
                        if i == j:
                                break
                        output+=","+str(j)
                        clusteri = i % num_of_clusters
                        clusterj = j % num_of_clusters
                        if clusteri == clusterj:
                                distances[(i,j)] = 1.0*random.random()
                        else:
                                distances[(i,j)] = 10.0*random.random()
                        output+=","+str(distances[(i,j)])
                output+="\n"
        return output

with open("test_input.csv","w") as fp:
        fp.write(GenerateCluster(2,100))

