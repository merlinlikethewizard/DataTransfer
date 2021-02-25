# DataTransfer
A compressing, error correcting data transfer protocall I made for a class. I implemented Huffman coding and Hamming codes. Here's the original assignment description:

>For an end-of-semester project, implement a quasi-real data transmission consisting of (compression, error encoding, error simulation,corrected, uncompressed) pipeline. More specifically,
>
>```
>I)   start an ascii text file       original.txt      
> 
>II)  compress it to                 compressed.xxx  |
>                                                     | prepare 
>III) error-correct encode to        encoded.yyy     |
> 
>IV)  simulate transmission errors   transmitted.yyy
>     by flipping random bits with
>     probability e. (For a really
>     good time, you could put in
>     burst errors or malicious errors.)
> 
>V)   correct errors                 decoded.xxx     |
>                                                    | restore
>VI)  uncompress                     final.txt       |  
>```
