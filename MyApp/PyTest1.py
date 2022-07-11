from math import log2, log
from random import randint
import numpy as np
from time import sleep, time
from bitstring import BitArray, BitStream
  
def DC_encode(data, progress_bar=None):
    print('encoding DC')
    data = list(data)
    chunk_size = int.to_bytes(len(data), length=4, byteorder='big')
    last_num = data.pop(0)
    result = BitStream(chunk_size) + BitStream(f'uint:8={last_num}')
    for i in data:
        num_xor = i^last_num
        eq_bits = 7 if num_xor == 0 else 7-int(log2(num_xor))
        result += BitStream(f'uint:3={eq_bits}')
        result += BitStream(f'uint:8={i}')[eq_bits-8:]
        last_num = i
    return int.to_bytes(len(result.tobytes()), length=4, byteorder='big') + result.tobytes()


def DC_encodeN(data, progress_bar=None):
    print('encoding DC')
    data = np.asarray(data)
    chunk_size = int.to_bytes(len(data), length=4, byteorder='big')
    result = BitStream(chunk_size) + BitStream(f'uint:8={data[0]}')
    calculs = calculation(data)
    for i in range(len(calculs)):
        result += BitStream(f'uint:3={calculs[i]}') if i % 2 == 0 else BitStream(f'uint:8={calculs[i]}')[calculs[i-1]-8:]
        
    return int.to_bytes(len(result.tobytes()), length=4, byteorder='big') + result.tobytes()

def calculation(data):
    result = []
    last_num = data[0]
    l2=log(2)
    for i in range(1, len(data)):
        num_xor = data[i]^last_num
        eq_bits = 7 if num_xor == 0 else 7-int(log(num_xor)/l2)
        result.append(eq_bits)
        result.append(data[i]) #BitStream(f'uint:3={eq_bits}')
                         #BitStream(f'uint:8={i}')[eq_bits-8:]
        last_num = data[i]
    return result
calculation(np.arange(5))

test = []
for i in range(10000):
    test.append(randint(0, 255))

DC_encodeN(test)
t = time()
DC_encodeN(test)
DC_encodeN(test)
DC_encodeN(test)
DC_encodeN(test)
print(time()-t)
# print(DC_encodeN(test) == DC_encode(test))


# a = np.arange(10)
# print(np.unique(a, return_counts=True))