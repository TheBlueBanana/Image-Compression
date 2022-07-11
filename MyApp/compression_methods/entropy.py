from base64 import encode
from concurrent.futures.process import EXTRA_QUEUED_CALLS
import encodings
from itertools import count
from math import log2
from random import randint
from bitstring import BitArray, BitStream
from numpy import byte
from compression_methods.DC2 import DC2_encode_arr
from compression_methods.RLE import RLE_encode_arr
from compression_methods.huffman import  get_frequencies, huffman_encode

# from DC2 import DC2_encode_arr
# from RLE import RLE_encode_arr
# from huffman import  get_frequencies, huffman_encode

#We want entropies to be low, as they represent the minimun size for a file
def get_all_entropies(data):
    dc = DC2_encode_arr(data)[1:]
    return get_entropy(data), get_entropy(RLE_encode_arr(data), 'RLE'), get_entropy(dc, 'DC'), get_entropy(RLE_encode_arr(dc), 'DC + RLE')

def get_entropy(encoded_data, method="raw"):
    frequency_dict = get_frequencies(encoded_data)
    # print(f'#símbols {method}: {len(frequency_dict)}')
    entropy = 0
    for v in frequency_dict.values():
        p = v/len(encoded_data)
        entropy += p * log2(p)
    return -entropy * len(encoded_data)

# def get_huffman_entropy(data):
#     encoded_data = huffman_encode(data)[4:]
#     dict_length = int.from_bytes(encoded_data[:2], byteorder='big', signed=False)
#     encoded_data = BitStream(encoded_data[2+dict_length:])
#     one_count = encoded_data.count(1)
#     return get_entropy({1:one_count, 0:len(encoded_data)-one_count}, len(encoded_data))

def test():
    test = ([10] * 130) *40
    # for i in range(100000):
    #     test.append(randint(0, 255))
    print(get_all_entropies(test))
    print((len(huffman_encode(test))*8, 8*len(huffman_encode(RLE_encode_arr(test))), 8*len(huffman_encode(DC2_encode_arr(test)))))
# test()