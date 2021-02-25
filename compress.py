#!/usr/bin/env python

from compression_utility import *

def compress(string, spacer, depth=inf):
    mappings, condition_depth = getMappings(string, depth)
    tree = {key:huffmanTree(mappings[key]) for key in mappings}
    inverse_tree = {key:{tree[key][key2]:key2 for key2 in tree[key]} for key in tree}
    
    bin_string1 = convert('compress', string, tree, condition_depth)
    compressed = asciiIt(bin_string1)
    
#    print strProbs(percentify(getCounts(string, condition_depth)))

    pickled = pickle.dumps(inverse_tree)
    total_string = spacer.join([pickled, compressed, str(condition_depth), str(len(string))])
    
    return total_string

def main():
    ''' main '''
    
    string = sys.stdin.read()
    
    depth = inf
    spacer = '$$$spacer5000$$$'

    compressed = compress(string, spacer, depth)
            
    sys.stdout.write(compressed)
    
    
if __name__=='__main__':
#    import doctest
#    doctest.testmod()
    ### For some reason doctests ruin i/o stuff
    main()