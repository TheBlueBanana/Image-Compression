from random import randint
from bitstring import BitArray, BitStream
from concurrent.futures import thread, ThreadPoolExecutor
from math import log2

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

def DC_decode(data):
    print('decoding DC')
    data = BitStream(data)
    result = []
    with ThreadPoolExecutor() as executor:
        threads = []
        while data.pos < len(data):
            section_lenght = int.from_bytes(data.read(8*4).tobytes(), byteorder='big') 
            threads.append(executor.submit(decode_chunk, data=data.read(section_lenght*8)))
        
        for i in threads:
            result.extend(i.result())
    return result
    
def decode_chunk(data):
    chunk_length = int.from_bytes(data.read(8*4).tobytes(), byteorder='big') 
    last_num = data.read(8)
    result = [last_num.uint]
    for i in range(chunk_length-1):
        eq_bits = data.read(3).uint
        new_num = data.read(8-eq_bits)
        last_num = last_num[:eq_bits] + new_num
        result.append(last_num.uint) #BitStream(f'0b{last_num}')
    return result

def Test():
    a = b = []
    for i in range(10000):
        a.append(randint(0, 255))
        b.append(randint(0, 255))
    e = DC_encode(a)
    e2 = DC_encode(b)
    d = DC_decode(e + e2)
    print(e)
    print(d)
    print(a+b == d)