import json

import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if str(args) in self.cache:
         return self.cache[str(args)]
      else:
         value = self.func(*args)
         self.cache[str(args)] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)


output = {}

names = []

def traverse_names(local_root):
        global names
        if "children" in local_root.keys():
                for x in local_root["children"]:
                        traverse_names(x)
        else:
                names.append(str(local_root["name"]))


@memoized
def flatten(root):
        output = []
        global names
        if "children" in root.keys():
                for x in root["children"]:
                        output+=flatten(x)
        else:
                return [str(root["name"])]
        return output

nodeOutput = {}
leafOutput = {}
nodeid = 0
def top_down_generate(root):
        global nodeid
        global leafOutput
        global nodeOutput
        myid = nodeid
        nodeid+=1
        nodeOutput[myid] = []
        height = root["size"]
        flat = flatten(root)
        for i in flat:
                nodeOutput[myid].append(i)
                leafOutput[i][height] = myid
                        
        for subtree in root["children"]:
                if "children" in subtree.keys():
                        top_down_generate(subtree)

with open("test_output.json") as fp:
        tree = json.load(fp)

for n in flatten(tree):
        leafOutput[n] = {}

top_down_generate(tree)

for p in leafOutput.keys():
        print p
        for s in leafOutput[p].keys():
                leafOutput[p][s] = nodeOutput[leafOutput[p][s]]

with open("out.json","w") as fp:
        json.dump(leafOutput,fp)
