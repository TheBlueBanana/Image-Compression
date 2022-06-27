from math import log2
from bitstring import BitArray, BitStream
a = {1:2, 3:6, 9:0}

print( dict((str(k),v) for k,v in a.items()))
# a = BitStream(f'uint:8=1')
# b = 18

# # The number of bits that correspond to the two digits.
# print(a^b)
# print(7-int(log2(a^b))) #8-int(log2(a^b)) +1