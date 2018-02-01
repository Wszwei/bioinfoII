import argparse
import sys
import re
from rosland import NewickTree, NewickNode


def displaymatch(match):
    if match is None:
        print('nahfam')
    print( '<Match: %r, groups=%r>' % (match.group(), match.groups()))
    

def read_tree(tree):
    n_tree = NewickTree()
    
    print(tree)
    print()
    find_root = re.compile('\((?P<content>.+)\)(?P<root>.+);')
    find_children = re.compile('\((?P<content>.+)\)(?P<child>.+),?')
    #'(\(.+\).+;){1}')
    
    #check if right format    
    t = re.match('(\(.+\).+;){1}', tree)
    if t:
        t = t.group()       
        
        print('find root')
        tr = find_root.match(t)
        displaymatch(tr)
        print(tr.group(1))
        t = tr.group(1)
        print()
        
        print('first child')
        tr = find_children.match(t)
        displaymatch(tr)
        print(tr.group(1))
        t = tr.group(1)
        print()
        
        print('second children')
        tr = find_children.match(t)
        displaymatch(tr)
        print(tr.group(1))
        t = tr.group(1)
        print()
        
        #t.group()
    else:
        sys.stderr('Newick tree is of incorrect format (forgot semicolon?)\n')
    
    #find_root.match(tree))
    

def main(tree, nodes):
    """Main func for Rosland"""
    read_tree(tree)
#    infile = sys.stdin
#    if len(sys.argv)>1:
#        if len(args) != 2:
#            print("%s [optional_input_file]" %sys.argv[0], file=sys.stderr)
#            return
#        else:
#            infile = open(sys.argv[1])
    #test_build_print_newicktree(infile)


if __name__ == '__main__':
    #main()    
    parser = argparse.ArgumentParser(description='problem 2b',
             prog='2b.py')
    parser.add_argument('newick_tree', type=str, 
                        help='tree in newick format')
    parser.add_argument('node_tuple', type=str, 
                        help='two node names in tuple form e.g. :3,6')
    args = parser.parse_args()
    main(args.newick_tree, args.node_tuple)