#!/usr/bin/env python

from compression_utility import *
from numpy import matrix
    
H = matrix([[1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]])

def getFlippedBit(word):
    '''
    Takes a 7-word, returns the position of the flipped bit (-1 if none have flipped)
    
    >>> getFlippedBit([0,0,0,0,0,0,0])
    -1
    >>> getFlippedBit([1,0,0,0,0,0,0])
    0
    >>> getFlippedBit([0,1,0,0,0,0,0])
    1
    >>> getFlippedBit([0,0,1,0,0,0,0])
    2
    >>> getFlippedBit([0,0,0,1,0,0,0])
    3
    >>> getFlippedBit([0,0,0,0,1,0,0])
    4
    >>> getFlippedBit([0,0,0,0,0,1,0])
    5
    >>> getFlippedBit([0,0,0,0,0,0,1])
    6
    '''
    
    word_matrix = matrix([[n] for n in word]) ### Turn the word into a 1x7 matrix
    
    code = H * word_matrix                    ### get the dot product of H and the word matrix
    code = code.flatten().tolist()[0][::-1]   ### flatten the result
    code = [n % 2 for n in code]              ### make math binary
    
    flipped_bit = eval('0b' + ''.join([str(n) for n in code])) - 1 ### convert binary to decimal
    
    return flipped_bit

def decode(string):
    '''
    Takes an encoded (and possibly fuzzed) message and de-fuzzes using Hamming 7, 4.
    1 error correcting.
    
    Witout errors:
    >>> decode(asciiIt('110011001010101100110011110011001101101001110011011100000000000101101000'))
    'blah\\n'
    
    With errors:
    >>> decode(asciiIt('110010001010101110110011110111001101001001110011111100000001000101101001'))
    'blah\\n'
    '''
    binary_string = unAsciiIt(string)
    
    word_length = 7
    data_length = word_length - (int(log2(word_length))+1) ### (i.e. 4)
    
    decoded_list = [None] * (len(binary_string) / 7 * 4)
    
    for i in xrange(0, len(binary_string), word_length):
        word = [int(n) for n in binary_string[i:i+word_length]]
        
        if len(word) != 7:
            break
        
        flipped_bit = getFlippedBit(word)
        
        if flipped_bit > -1:
            word[flipped_bit] = (word[flipped_bit] + 1) % 2
#            print i, code, flipped_bit
        
        data = [word[2], word[4], word[5], word[6]]
        
        for j in xrange(data_length):
            decoded_list[i/7*4 + j] = data[j]
            
    decoded_string = ''.join([str(n) for n in decoded_list])
    
    ascii_string = asciiIt(decoded_string)
    
    if ascii_string[-1] == '\x00':
        ascii_string = ascii_string[:-1]
    
    return ascii_string
#    return decoded_string

def main():
    string = sys.stdin.read()
    
    decoded = decode(string)
    
    sys.stdout.write(decoded)

if __name__ == '__main__':
#    import doctest
#    doctest.testmod()
    main()