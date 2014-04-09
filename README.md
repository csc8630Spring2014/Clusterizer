# Clusterizer
==========

Given: a graph; 

Generate: clusters

## TODO
* Standardize input and output formats for graphs
* Implement MST greedy heuristic
* Use results of greedy heuristic as seed for a GA or annealing technique

* Hack the above together in python and networkX to prove it works

* re-write in java or go becuase python is problematically slow.


## Flowcharts

graph -> |   ?    | ->  clusters

Ways to do that:

1)
we can use K-means approach:
"+" no need to generate graph
"-" hard to decide on k
"+/-" specialized way of deciding on centroids, may use [kGem idea](http://alan.cs.gsu.edu/NGS/?q=content/kgem)

2) 
graph -> |  min energy cover  | -> |  lower radius, repeat, stop when got a tree? | ->  tree of clusters

        
--------------
I know now why you don't want to use XML

1) you are doing it wrong.
2) you are doing it wrong.

Please see any of the numerous samples on how to describe a tree using XML such as: http://www.w3schools.com/xml/xml_tree.asp
         
