#!/usr/bin/env python

from compression_utility import *
    
def decompress(string, spacer):
    inputs = string.split(spacer)
    inverse_tree2 = pickle.loads(inputs[0])
    bin_string2 = unAsciiIt(inputs[1])
    decompressed = convert('decompress', bin_string2, inverse_tree2, int(inputs[2]), int(inputs[3]))
    return decompressed

def main():
    ''' main '''
    
    compressed = sys.stdin.read()
    
    spacer = '$$$spacer5000$$$'
    
    epoch = time()

    decompressed = decompress(compressed, spacer)
            
    sys.stdout.write(decompressed)
    
    
if __name__=='__main__':
#    import doctest
#    doctest.testmod()
    ### For some reason doctests ruin i/o stuff
    main()