# -*- coding: utf-8 -*-
#!/usr/bin/python3
import sys
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
                print("Cannot have duplicated node as %s" %node, file=sys.stderr)
                return
            newnode = NewickNode(parent_name, None)
            self.root = newnode
            self.node_dict[parent_name] = newnode
            newchild = newnode.add_child(node_name)
            self.node_dict[node_name] = newchild
            return
        if parent_name not in self.node_dict and self.root:
            print("Node_Parent %s not in the tree" %parent_name, file=sys.stderr)
            return
        if node_name in self.node_dict:
            print("Node %s already in the tree" % node_name, file=sys.stderr)
            return
        parent_node = self.node_dict[parent_name]
        childnode = parent_node.add_child(node_name)
        self.node_dict[node_name] = childnode

    def add_raw_node(self, parent_name, node_name):
        if node_name == parent_name:
            print("Cannot have duplicated node as %s" %node, file=sys.stderr)
            return
        if parent_name not in self.node_dict:
            newnode = NewickNode(parent_name, None)
            self.node_dict[parent_name] = newnode
        if node_name not in self.node_dict:
            newnode = NewickNode(node_name, None)
            self.node_dict[node_name] = newnode
        if self.node_dict[node_name].parent:
            print ("Node %s cannot be assigned to both %s and %s" %(
                node_name, parent_name, self.node_dict[node_name].parent.name),
                file=sys.stderr)
            return
        self.node_dict[parent_name].child_list.append(self.node_dict[node_name])
        self.node_dict[node_name].parent = self.node_dict[parent_name]

    def print_tree(self):
        """Print tree"""
        cur_node = self.root
        if not cur_node:
            print("Empty Tree", file=sys.stderr)
        children_content = self.print_children(cur_node)
        print(children_content)

    def load_tree(self, raw_tree: str):
        """Load the Newick tree from the parentheses form."""
        # Remove spaces/tabs
        raw_tree = "".join(raw_tree.split())
        # Use depth dict to store the raw tree
        cur_node_ch = []
        orphans = {}
        cur_depth = 0
        for ch in raw_tree:
            if ch == "(" :
                cur_depth += 1
            elif ch == ",":
                node = "".join(cur_node_ch)
                cur_node_ch = []
                orphans.setdefault(cur_depth, [])
                orphans[cur_depth].append(node)
                # Add the child of current node if exists
                if cur_depth + 1 in orphans:
                    for child in orphans[cur_depth + 1]:
                        self.add_raw_node(node, child)
                    del orphans[cur_depth + 1]
            elif ch == ")":
                node = "".join(cur_node_ch)
                cur_node_ch = []
                orphans.setdefault(cur_depth, [])
                orphans[cur_depth].append(node)
                # Add the child of current node if exists
                if cur_depth + 1 in orphans:
                    for child in orphans[cur_depth + 1]:
                        self.add_raw_node(node, child)
                    del orphans[cur_depth + 1]
                cur_depth -= 1
            else:
                cur_node_ch.append(ch)
        # Add the child of the root node
        root = "".join(cur_node_ch)
        if 1 in orphans:
            for child in orphans[1]:
                self.add_raw_node(root, child)
        self.root = self.node_dict[root]

    def get_distance(self, nodename_a, nodename_b):
        """Get the distance between two nodes."""
        try:
            assert nodename_a in self.node_dict
        except:
            print("%s is not in the tree" %nodename_a, file=sys.stderr)
        try:
            assert nodename_b in self.node_dict
        except:
            print("%s is not in the tree" %nodename_b, file=sys.stderr)

        node_a = self.node_dict[nodename_a]
        node_b = self.node_dict[nodename_b]
        trans_a = [nodename_a]
        trans_b = [nodename_b]

        cur_node = node_a
        while cur_node.parent:
            cur_node = cur_node.parent
            trans_a.append(cur_node.name)
        cur_node = node_b
        while cur_node.parent:
            cur_node = cur_node.parent
            trans_b.append(cur_node.name)


        for depth_a, node_name in enumerate(trans_a):
            if node_name in trans_b:
                depth_b = trans_b.index(node_name)
                break

        return depth_a + depth_b

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

def build_print_newicktree(infile):
    """Test to build and print newick tree."""
    n_tree = NewickTree()
    count = 0
    for line in infile:
        count = count + 1
        entry = line.split()
        if not entry: #empty line
            continue        
        elif len(entry) != 2:
            print("Line must be of format <node_1> <node_2>. Line %i skipped." % count, \
                  file=sys.stderr)
            continue
        n_tree.add_node(entry[0], entry[1])
    n_tree.print_tree()

def dist_newicktree(infile):
    """Load Newick Tree in parentheses format."""
    entry = infile.read().split(":")
    if len(entry) != 2:
        print("Wrong input format")
        return
    raw_tree = entry[0]
    nodes = entry[1].split(",")
    if len(nodes) != 2:
        print("Require two Nodes to calculate distance")
        return
    node_a = nodes[0].strip()
    node_b = nodes[1].strip()


    n_tree = NewickTree()
    n_tree.load_tree(raw_tree)
    print(n_tree.get_distance(node_a, node_b))


def main(infile):
    """Main func for Rosland"""
    build_print_newicktree(infile)

if __name__ == '__main__':
    #main()
    parser = argparse.ArgumentParser(description='Computes newick tree',
             prog='problem2.A.py')
    parser.add_argument('--infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='Default input is stdin. Also \
                        accepts a filename.')
    args = parser.parse_args()
    main(args.infile)
