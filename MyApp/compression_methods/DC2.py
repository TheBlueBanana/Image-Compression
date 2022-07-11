from random import randint
from re import A
from bitstring import BitArray, BitStream
from concurrent.futures import thread, ThreadPoolExecutor
from math import log2

def DC2_encode(data, progress_bar=None):
    print('encoding DC2')
    data = list(data)
    last_num = data.pop(0)
    result = BitStream(f'uint:8={last_num}')
    for i in data:
        diff = i - last_num
        result += BitStream(f'int:8={-128}') + BitStream(f'uint:8={i}') if  abs(diff) > 127 else BitStream(f'int:8={diff}') 
        last_num = i
    result = int.to_bytes(len(result.tobytes()), length=4, byteorder='big') +  result # chunk_size
    return int.to_bytes(len(result.tobytes()), length=4, byteorder='big') + result.tobytes()

def DC2_decode(data):
    print('decoding DC2')
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
    last_num = data.read(8).uint
    result = [last_num]
    full_value = False
    for i in range(chunk_length-1):
        n = data.read(8)
        if n.int == -128 and not full_value:
            full_value = True
            continue
        else:
            last_num = n.uint if full_value else n.int + last_num
            result.append(last_num)
            full_value = False
        # result.append(last_num.uint) #BitStream(f'0b{last_num}')
    return result


def DC2_encode_arr(data, progress_bar=None):
    print('encoding DC2')
    data = list(data)
    last_num = data.pop(0)
    result = [last_num]
    for i in data:
        diff = i - last_num
        # result.extend([-128, i] if  abs(diff) > 127 else [diff])
        result.append(diff)
        last_num = i
    # result = int.to_bytes(len(result.tobytes()), length=4, byteorder='big') +  result # chunk_size
    return [len(result)] + result

def DC2_decode_arr(data):
    print('decoding DC2')
    result = []
    data = list(data)
    pointer = 0
    with ThreadPoolExecutor() as executor:
        threads = []
        while len(data)-1 >pointer:
            section_lenght = data[pointer]
            pointer +=1
            threads.append(executor.submit(decode_chunk_arr, data=data[pointer:pointer+section_lenght]))
            pointer += section_lenght
        
        for i in threads:
            result.extend(i.result())
    return result
    
def decode_chunk_arr(data):
    last_num = data.pop(0)
    result = [last_num]
    full_value = False
    for i in data:
        # if i == -128 and not full_value:
        #     full_value = True
        #     continue
        # else:
        last_num = i if full_value else i + last_num
        result.append(last_num)
        full_value = False
    return result


def Test():
    a = []
    for i in range(100000):
        a.append(randint(0, 255))
    # print(a)
    e = DC2_encode_arr(a)
    d = DC2_decode_arr(e)
    print(len(e))
    print(len(d))
    print(a == d)
# Test()