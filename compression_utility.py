'''
compression_utility.py
'''

from numpy import log2, inf
import pickle
import sys
from time import time

def entropy(probabilities):
    return -1 * sum([a * log2(b) for a,b in probabilities])

def getCounts(string, condition_depth=0, include_blanks=True):
    ''' Returns a dictionary of {condition : dictionary-of-characters}
        with the dictionary-of-characters being of {char : probability}.
        
    >>> getCounts('10100', 0)
    {'': {'1': 2, '0': 3}}
    
    >>> getCounts('10100', 1, False)
    {'1': {'0': 2}, '0': {'1': 1, '0': 1}}
    
    >>> getCounts('10100', 1, True)
    {'1': {'0': 2}, '0': {'1': 1, '0': 1}, '_': {'1': 1}}
    '''
    probabilities = {}
    for i in xrange({False:condition_depth, True:0}[include_blanks], len(string)):
        ch = string[i]
        condition = ''
        for offset in xrange(condition_depth, 0, -1):
            if 0 <= i - offset < len(string):
                condition += string[i - offset]
            else:
                condition += '_'
        if not condition in probabilities:
            probabilities[condition] = {}
        if not ch in probabilities[condition]:
            probabilities[condition][ch] = 0
        probabilities[condition][ch] += 1
    return probabilities

def percentify(probabilities):
    ''' Makes a probabilities dict in percent format
    
    >>> percentify({'1': {'0': 2}, '0': {'1': 1, '0': 1}})
    {'1': {'0': 1.0}, '0': {'1': 0.5, '0': 0.5}}
    '''
    new_probabilities = {key:{} for key in probabilities}
    for key1 in probabilities:
        values_sum = sum(probabilities[key1].values())
        for key2 in probabilities[key1]:
            new_probabilities[key1][key2] = float(probabilities[key1][key2]) / values_sum
    return new_probabilities

def strProbs(probabilities):
    ''' Returns a list of probabilities '''
    
    s = ''
    for key1 in probabilities:
        if key1 == '':
            s += '\nProbability of characters:'
        else:
            s += '\nProbability of characters following {}:'.format(key1)

        for key2 in probabilities[key1]:
            s += '\n  {}: {:.2f}%'.format(key2, probabilities[key1][key2]*100)
            
    return s + '\n'
                    
def huffmanTree(probabilities):
    ''' Takes probabilities dict, returns dict of encoding rules...
    
    >>> huffmanTree({'a':0.4, 'b':0.3, 'c':0.15, 'd':0.08, 'e':0.07})
    {'a': '0', 'c': '110', 'b': '10', 'e': '1110', 'd': '1111'}
    
    >>> huffmanTree({'a':0.6, 'b':0.1, 'c':0.1, 'd':0.1, 'e':0.1})
    {'a': '1', 'c': '001', 'b': '000', 'e': '011', 'd': '010'}
    '''
    
    tree = [(probabilities[key], key) for key in probabilities]
    while len(tree) > 1:
        tree.sort()
        tree = [(tree[0][0] + tree[1][0], (tree[0][1], tree[1][1]))] + tree[2:]
    
    tree = {tree[0][1]: ''}
    
    exit = False
    while not exit:
        exit = True
        tree_append = {}
        tree_del = []
        for key in tree:
            if type(key) == tuple:
                tree_append.update({key[0]:tree[key] + '0', key[1]:tree[key] + '1'})
                tree_del += [key]
                exit = False
        for key in tree_del:
            del(tree[key])
        tree.update(tree_append)
                
    return tree

def getMappings(string, force_depth=inf, depth_max=False, verbose=False):
    str_len = len(string)
    
    last_probabilities = percentify(getCounts(string))
    probabilities_list = [last_probabilities['']]
    
    adjust = len(pickle.dumps(last_probabilities)) / 1.25
    
    real_entropy_values = [entropy([(value, value) for value in probabilities_list[-1].values()])]
    entropy_values = [(real_entropy_values[0] * str_len/8) + adjust]
    
    depth = 0
    while depth < force_depth:
        depth += 1
        probabilities = percentify(getCounts(string, depth))
        
        entropy_set = []
        
        expanded_probability = {}
        for key in probabilities_list[-1]:
            if '_' in key:
                key_prob = 0
            else:
                key_prob = probabilities_list[-1][key]
            
            if key in probabilities:
                for key2 in probabilities[key]:
                    prob_value = probabilities[key][key2]

                    entropy_set += [(key_prob * prob_value, prob_value)]
                    expanded_probability[key + key2] = key_prob * prob_value

        # this is the value to compensate for a larger pickeled dictionary at the head of a file
        math = (((2**(-(depth-1)/3.7586987453764))/3.46687265) + 1)
        adjust = int(len(pickle.dumps(probabilities)) / math)
        
        new_real_entropy = entropy(entropy_set)
        new_entropy = (new_real_entropy * str_len/8) + adjust
        if not (force_depth == inf or depth_max) or entropy_values[-1] > new_entropy * 1.1:
            real_entropy_values += [new_real_entropy]
            entropy_values += [new_entropy]
            probabilities_list += [expanded_probability]
            last_probabilities = probabilities
        else:
            depth -= 1
            break
    
    if verbose:
        print '\nUnweighted:'
        for i in xrange(len(real_entropy_values)):
            print 'Entropy at depth {}: {}'.format(i, real_entropy_values[i]/8)
        print '\nWeighted:'
        for i in xrange(len(entropy_values)):
            print 'Compression ratio at depth {}: {}'.format(i, entropy_values[i]/1202470)
            
    return last_probabilities, depth

def convert(mode, string, tree, condition_depth, out_len=0):
    if not mode in ['compress', 'decompress']:
        raise Exception("mode arg must be either 'compress' or 'decompress'")
    converted = ''
    i = 0
    str_len = len(string)
    while True:
        condition = ''
        for offset in xrange(condition_depth, 0, -1):
            if mode == 'compress':
                if 0 <= i - offset < len(string):
                    condition += string[i - offset]
                else:
                    condition += '_'
            else:
                if 0 <= len(converted) - offset < len(converted):
                    condition += converted[len(converted) - offset]
                else:
                    condition += '_'
        if not condition in tree:
            break
        if mode == 'compress':
            converted += tree[condition][string[i]]
            i += 1
            if i >= str_len:
                break
        else:
            table = tree[condition]
            j = 0
            while True:
                if string[i:i+j] in table:
                    converted += table[string[i:i+j]]
                    break
                j += 1
            i += j
            if len(converted) >= out_len:
                break
                
    return converted

def asciiIt(string):
    ''' Takes a string of '1's and '0's and makes it into ascii text by pairs of 8
        (sticks '0's on the end to make it a multiple of 8)
    
    >>> asciiIt('0110010001110101011000110110101101110')
    'duckp'
    '''
    
    newstring = ''
    string += '0' * (8 - (len(string) % 8))
    len_str = len(string)
    for i in xrange(0, len(string), 8):
        newstring += chr(eval('0b' + string[i:i+8]))
        
    return newstring

def unAsciiIt(string):
    ''' Takes a string and turns it into a string of '1's and '0's
    
    >>> unAsciiIt('duckp')
    '0110010001110101011000110110101101110000'
    '''
    
    newstring = ''
    for ch in string:
        newstring += bin(ord(ch))[2:].zfill(8)
        
    return newstring