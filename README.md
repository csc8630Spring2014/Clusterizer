Clusterizer
==========

Given: a graph 
Generate: clusters

##TODO
Standardize input and output formats for graphs
Implement MST greedy heuristic
Use results of greedy heuristic as seed for a GA or annealing technique

Hack the above together in python and networkX to prove it works

re-write in java or go becuase python is problematically slow.


##
         |--------|
graph -> |   ?    | ->  clusters
         |--------|
         
    
         |--------------------|    |----------------------------------------------|
graph -> |  min energy cover  | -> |  lower radius, repeat, stop when got a tree? | ->  tree of clusters
         |____________________|    |______________________________________________| 
        
         
         
