from random import randint
from numpy import dtype, uint, asarray, uint8
from compression_methods.DC2 import DC2_decode_arr, DC2_encode, DC2_encode_arr
from compression_methods.RLE import RLE_decode_arr, RLE_encode_arr
from compression_methods.huffman import get_frequencies, huffman_decode, huffman_encode

# Usable
# from DC2 import DC2_decode_arr, DC2_encode, DC2_encode_arr
# from RLE import RLE_decode_arr, RLE_encode_arr
# from huffman import get_frequencies, huffman_decode, huffman_encode

def RLE_H_encode(data, progress_bar=None):
    return huffman_encode(RLE_encode_arr(data))
def DC_H_encode(data, progress_bar=None):
    return huffman_encode(DC2_encode_arr(data))
def DC_RLE_H_encode(data, progress_bar=None):
    a = DC2_encode_arr(data)
    b = RLE_encode_arr(a)
    return huffman_encode(b)


def RLE_H_decode(data, progress_bar=None):
    return RLE_decode_arr(huffman_decode(data))
def DC_H_decode(data, progress_bar=None):
    return DC2_decode_arr(huffman_decode(data))
def DC_RLE_H_decode(data, progress_bar=None):
    return DC2_decode_arr(RLE_decode_arr(huffman_decode(data)))

def Test():
    test = []
    test2 = [3, 7]
    for i in range(1000000):
        test.append(randint(0, 255))
        test2.append(randint(0, 255))
    e1 = DC_H_encode(test)
    e2 = DC_H_encode(test2)
    d = DC_H_decode(e1 + e2)
    print(d == test + test2)
# Test()

def variety_test(data=[]):
    test = []
    if len(data) > 0:
        test = data
    else:
        for i in range(100000):
            test.append(randint(0, 255))
    test = asarray(test, dtype=uint8)
    e1 = RLE_encode_arr(test)
    e2 = DC2_encode_arr(test)
    e3 = RLE_encode_arr(e2)
    print('Varietat de símbols a la imatge: ')
    print(f'raw: ', len(get_frequencies(test)))
    print(f'RLE: ', len(get_frequencies(e1)))
    print(f'DC: ', len(get_frequencies(e2)))
    print(f'RLE + DC: ', len(get_frequencies(e3)))
    # print(get_frequencies(e2))
    print(RLE_decode_arr(e1) == test, sum(DC2_decode_arr(e2)==test) == len(test), len(test) == sum(DC2_decode_arr(RLE_decode_arr(e3)) == test))
# variety_test()