from random import randint
from compression_methods.DC2 import DC2_decode_arr, DC2_encode, DC2_encode_arr
from compression_methods.RLE import RLE_decode_arr, RLE_encode_arr
from compression_methods.huffman import huffman_decode, huffman_encode, huffman_DC_decode, huffman_DC_encode

# from DC2 import DC2_decode_arr, DC2_encode, DC2_encode_arr
# from RLE import RLE_decode_arr, RLE_encode_arr
# from huffman import huffman_decode, huffman_encode, huffman_DC_decode, huffman_DC_encode

def RLE_H_encode(data, progress_bar=None):
    return huffman_encode(RLE_encode_arr(data))
def DC_H_encode(data, progress_bar=None):
    return huffman_encode(DC2_encode_arr(data))
def DC_RLE_H_encode(data, progress_bar=None):
    return huffman_encode(RLE_encode_arr(DC2_encode_arr(data)))


def RLE_H_decode(data, progress_bar=None):
    return RLE_decode_arr(huffman_decode(data))
def DC_H_decode(data, progress_bar=None):
    return DC2_decode_arr(huffman_decode(data))
def DC_RLE_H_decode(data, progress_bar=None):
    return DC2_decode_arr(RLE_decode_arr(huffman_decode(data)))

def Test():
    test = []
    for i in range(100000):
        test.append(randint(0, 255))
    e1 = huffman_encode(RLE_encode_arr(DC2_encode_arr(test)))
    d = DC2_decode_arr(RLE_decode_arr(huffman_decode(e1)))
    print(d == test)
# Test()