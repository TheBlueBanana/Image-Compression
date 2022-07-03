from ast import Bytes
from math import log2
from bitstring import BitArray, BitStream

# Huffman
a = bytes([1, 2, 3])
st = BitStream(a)
print(st.count(0))
print(st.count(1))
b = (1, 2, 3)

# Others
# ENTROPY = -sum(p*log2(p))

# # The number of bits that correspond to the two digits.
# print(a^b)
# print(7-int(log2(a^b))) #8-int(log2(a^b)) +1