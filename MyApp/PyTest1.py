from math import log2
from time import time
from bitstring import BitArray, BitStream
from numba import jit, njit

a = bytes([1,2])
@njit
def test(x):
    b = BitStream()
    b += x
    print(b)

test(a)
test(a)
# ENTROPY = -sum(p*log2(p))

# # The number of bits that correspond to the two digits.
# print(a^b)
# print(7-int(log2(a^b))) #8-int(log2(a^b)) +1