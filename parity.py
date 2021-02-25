#!/usr/bin/env python

from compression_utility import *
from numpy import matrix
    
G = matrix([[1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]])

def getCodeWord(data):
    '''
    Takes four bits of data, returns the corresponding code word.
    
    >>> getCodeWord([0,0,0,0])
    [0, 0, 0, 0, 0, 0, 0]
    >>> getCodeWord([1,0,1,0])
    [1, 0, 1, 1, 0, 1, 0]
    >>> getCodeWord([0,1,0,1])
    [0, 1, 0, 0, 1, 0, 1]
    >>> getCodeWord([1,1,0,1])
    [1, 0, 1, 0, 1, 0, 1]
    >>> getCodeWord([1,1,1,1])
    [1, 1, 1, 1, 1, 1, 1]
    '''
    
    code = data * G              ### get the dot product of data and G
    code = code.tolist()[0]      ### flatten the result
    code = [n % 2 for n in code] ### make math binary
    
    return code

def encode(string):
    '''
    Takes a string, adds redundancy using Hamming 7, 4.
    1 error correcting
    
    >>> unAsciiIt(encode('blah'))
    '1100110010101011001100111100110011011010011100110111000000000000'
    >>> unAsciiIt(encode('hello'))
    '110011011100001100110010010111001100111100110011001111001100110111111100'
    >>> unAsciiIt(encode('world'))
    '000111100011111100110111111100011110101010110011001111001100110100110000'
    '''
    binary_string = unAsciiIt(string)
#    binary_string = string
    
    word_length = 7
    data_length = word_length - (int(log2(word_length))+1) ### (i.e. 4)
    
#    zero_tail_filler = -len(binary_string) % data_length
#    binary_string += '0' * zero_tail_filler
#    binary_string += bin(zero_tail_filler)[2:].zfill(data_length)
    
    assert len(binary_string) % data_length == 0
    
    encoded_list = [None] * (len(binary_string) / 4 * 7)
    
    for i in xrange(0, len(binary_string), data_length):
        data = [int(n) for n in binary_string[i:i+data_length]]
        
        code = getCodeWord(data)
        
        for j in xrange(word_length):
            encoded_list[i/4*7 + j] = code[j]
            
    encoded_string = ''.join([str(n) for n in encoded_list])
    
    return asciiIt(encoded_string)

def main():
    string = sys.stdin.read()
    
    encoded = encode(string)
    
    sys.stdout.write(encoded)

if __name__ == '__main__':
    ### For some reason doctests ruin i/o stuff
#    import doctest
#    doctest.testmod()
    main()