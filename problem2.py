""" 1) Make a tree first
    2) Figure out how to print in Newick format
    3) Find distance
"""

from collections import defaultdict
import sys
import pprint

def tree():
    return defaultdict(tree)

def insert(tree, nodes):
    for node in nodes:
        tree = tree[node]

#Converts to standard dicts
def dicts(t):
    return {k: dicts(t[k]) for k in t}

def print_tree(t):
    pp = pprint.PrettyPrinter()
    pp.pprint(dicts(t))


def main():
    newick = tree()
    
    #for line in sys.stdin:
    #    print(line)
if __name__ == '__main__':
    main()
