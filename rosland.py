# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
import re
import argparse

class NewickTree(object):
    """Newick Tree."""
    def __init__(self):
        self.root = None
        self.node_dict = {}

    def add_node(self, parent_name, node_name):
        # First input as root
        if not self.root:
            if node_name == parent_name:
                print("Cannot have duplicated node as %s" %node)
                return
            newnode = NewickNode(parent_name, None)
            self.root = newnode
            self.node_dict[parent_name] = newnode
            newchild = newnode.add_child(node_name)
            self.node_dict[node_name] = newchild
            return
        if parent_name not in self.node_dict and self.root:
            print("Node_Parent %s not in the tree" %parent_name)
            return
        if node_name in self.node_dict:
            print("Node %s already in the tree" % node_name)
            return
        parent_node = self.node_dict[parent_name]
        childnode = parent_node.add_child(node_name)
        self.node_dict[node_name] = childnode

    def print_tree(self):
        """Print tree"""
        cur_node = self.root
        if not cur_node:
            print("Empty Tree")
        content = []
        children_content = self.print_children(cur_node)
        print(children_content)

    def print_children(self, cur_node):
        cur_children = cur_node.child_list
        if not cur_children:
            return cur_node.name
        children_content = []
        for child in cur_children:
            children_content.append(self.print_children(child))
        children_content = ",".join(children_content)
        children_content = "(%s)%s" %(children_content, cur_node.name)
        return children_content

class NewickNode(object):
    """Node of Newick Tree"""
    def __init__(self, name, parent):
        self.name = name
        self.child_list = []
        self.parent = parent

    def add_child(self, name):
        new_child = NewickNode(name, self)
        self.child_list.append(new_child)
        return new_child

def test_build_print_newicktree(infile):
    """Test to build and print newick tree."""
    n_tree = NewickTree()
    for line in infile:
        entry = line.split()
        if not entry:
            continue
        n_tree.add_node(entry[0], entry[1])
        n_tree.print_tree()
    n_tree.print_tree()

def main(infile):
    """Main func for Rosland"""
#    infile = sys.stdin
#    if len(sys.argv)>1:
#        if len(args) != 2:
#            print("%s [optional_input_file]" %sys.argv[0], file=sys.stderr)
#            return
#        else:
#            infile = open(sys.argv[1])
    test_build_print_newicktree(infile)


if __name__ == '__main__':
    #main()    
    parser = argparse.ArgumentParser(description='problem 2a',
             prog='rosland.py')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()
    main(args.infile)
    