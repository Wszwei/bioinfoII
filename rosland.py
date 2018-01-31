# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
import re

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


def dna2rna(infile: str):
    """Translates dna to rna"""
    with open(infile) as filep:
        dna = filep.read()
        rna = re.sub("T", "U", dna)
        print(rna)
def rc_seq(infile: str):
    """Translates dna to rna"""
    nt_dict = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }
    with open(infile) as filep:
        dna = filep.read()
        rc_seq = []
        for nt in dna[::-1]:
            if nt in nt_dict:
                rc_seq.append(nt_dict[nt])
        print("".join(rc_seq))

def mendel(infile: str) -> None:
    with open(infile) as filep:
        counts = filep.readline()
        nums = [int(cnt) for cnt in counts.split()]
        homo_d = nums[0]
        homo_r = nums[1]
        hyb = nums[2]
        total = homo_d + homo_r + hyb
        prob_res = (1/4*hyb*(hyb-1) + hyb*homo_r + homo_r*(homo_r-1))/(total*(total -1))
        prob = 1 - prob_res
        print (prob)

def test_build_print_newicktree(infile):
    """Test to build and print newick tree."""
    with open(infile) as filep:
        n_tree = NewickTree()
        for line in filep:
            entry = line.split()
            if not entry:
                continue
            n_tree.add_node(entry[0], entry[1])
            n_tree.print_tree()
        n_tree.print_tree()

def main():
    """Main func for Rosland"""
    args = sys.argv[1:]
    if len(args) != 2:
        print("%s [input_file] [output_prefix]" %sys.argv[0])
        return
    infile = args[0]
    prefix = args[1]
    # dna2rna(infile)
    # rc_seq(infile)
    # mendel(infile)
    test_build_print_newicktree(infile)

if __name__ == '__main__':
    main()