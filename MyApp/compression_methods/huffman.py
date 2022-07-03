# Huffman algorythm
import math as math
import json
from random import randint
from bitstring import BitArray, BitStream
from concurrent.futures import thread, ThreadPoolExecutor


# INTRODUCE LOADING BAR!!!!!!!!!!!!!!


# 1. Get frequencies and generate huffman Tree
def huffman_encode(data, progress_bar=None):
    print('encoding huffman')
    result = bytes()
    data = list(data)
    data.append(256) # the end of input mark
    
    frequency_dict = get_frequencies(data.copy())
    
    pixel_dict = create_huffman_tree(frequency_dict).visualize() # we get the byte to number dict
    bin_dict = json.dumps(pixel_dict).encode('utf-8') #codifiquem el diccionari obtingut
    # 2. Code the Tree (len + tree)

    result += int.to_bytes(len(bin_dict), length=2, byteorder='big')
    result += bin_dict
    
    # 3. Code every digit
    pixel_dict = invert_dict(pixel_dict) # to get the number to byte dict
    result += encode_pixels(pixel_dict, data, progress_bar)
    return int.to_bytes(len(result), length=4, byteorder='big') + result

# Decode:
# 1. Get frequencies from the tree
def huffman_decode(data):
    print('decoding huffman')
    bin_data = BitStream(data) # create the bit representation
    result = []
    with ThreadPoolExecutor() as executor:
        threads = []
        while bin_data.pos < len(bin_data):
            section_lenght = int.from_bytes(bin_data.read(32).tobytes(), byteorder='big') 
            # result.extend(decode_section(bin_data=bin_data.read(section_lenght*8)))#section lenght is in bytes, we read in bits
            threads.append(executor.submit(decode_section, bin_data=bin_data.read(section_lenght*8)))
        
        for i in threads:
            result.extend(i.result())
    return result

def decode_section(bin_data):
    dict_lenght = int.from_bytes(bin_data.read(8*2).tobytes(), byteorder='big') # each dict takes 2 bytes of space 
    binDict = bin_data.read(dict_lenght*8).tobytes() # dict lenght is in bits
    huffman_dict = json.loads(binDict.decode('utf-8')) # get the lenght of the dict and translate to json (bit to int) dict
    # 2. Start reading
    return decode_pixels(huffman_dict, bin_data.read(len(bin_data) - bin_data.pos)) #decode the rest of the string

def sort_dict(d, reverse=False):
    """odrdena un dicrtionari de menor a major"""
    return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse)) # ordena el diccionari en funció dels valors de frequencies
  
def get_frequencies(arr):
    arr = list(arr)
    frequency_dict = {}
    while len(arr) != 0:
        v = arr[0]
        frequency_dict.update({v: arr.count(v)})
        arr = list(filter(v.__ne__, arr))
    return frequency_dict

class node:
    """Un node d'un arbre binari"""
    def __init__(self, next_node_a, next_node_b):
        self.next_node = ['', '']
        self.next_node[0] = next_node_a or 0
        self.next_node[1] = next_node_b or 0
    
    def get(self, value):
        return self.next_node[value or 0]
    
    def visualize(self, prev = ''):
        dct = {}
        for i in range(2):
            if type(self.next_node[i]) is node:
                dct.update(self.next_node[i].visualize(prev + f'{i}'))
            else :
                dct[prev + f'{i}'] = self.next_node[i]
        return dct

def create_huffman_tree(pixels):
    """Retorna un arbre de huffman en base al diccionari de freqüències d'entrada"""
    # the keys of a dict mustn't be an object
    pixels = dict((str(k),v) for k,v in pixels.items()) # we make the initial keys to be strings
    node_list = []
    while len(pixels) > 1:
        pixels = sort_dict(pixels) # sorts by the lowest frequency first
        pixel_key_list = list(pixels) # returns a list of the keys (pixel value)
        n1 = node_list[pixel_key_list[0]] if isinstance(pixel_key_list[0], int) else int(pixel_key_list[0])
        n2 = node_list[pixel_key_list[1]] if isinstance(pixel_key_list[1], int) else int(pixel_key_list[1])
        pixels[len(node_list)] = pixels[pixel_key_list[0]] + pixels[pixel_key_list[1]] # Es sumen les freqüències dels dos nodes anteriors i es posicionen últims a la llista
        node_list.append(node(n1, n2)) 
        del pixels[pixel_key_list[0]]
        del pixels[pixel_key_list[1]]
    return node_list[-1]

def encode_pixels(dct, data, progress_bar):
    output = BitArray()
    progress_cont = 0
    for i in data:
        output += f'0b{dct[i]}'
        if progress_bar!= None:
            progress_cont+=1
            progress_bar.setValue(0.3 + 0.7*progress_cont/len(data))
    return output.tobytes()

def decode_pixels(dct, data):
    output = []
    current_string = BitStream()
    while data.pos < len(data):
        current_string += data.read(1)
        if current_string.bin in dct:
            if dct[current_string.bin] == 256:
                if len(data) - data.pos < 8:
                    break
                data.read(data.pos % 8)
            else:
                output.append(dct[current_string.bin])
            current_string = BitStream()
    return output

def invert_dict(dct):
    tuples = []
    for i in dct.items():
        tuples.append((i[1], i[0]))
    return dict(tuples)
 #res = dict((v,k) for k,v in a.items()), siendo a el diccionario original

def huffman_DC_encode(data):
    data = list(data)
    first = int.to_bytes(data.pop(0), length=4, byteorder='big')
    return first + huffman_encode(data)

def huffman_DC_decode(data): # change!!!!!! => lenHuffman -> lenDC (decode separately ->)
    print('decoding huffman')
    bin_data = BitStream(data) # create the bit representation
    result = []
    DC_first = []
    with ThreadPoolExecutor() as executor:
        threads = []
        while bin_data.pos < len(bin_data):
            DC_first.append(int.from_bytes(bin_data.read(32).tobytes(), byteorder='big'))
            section_lenght = int.from_bytes(bin_data.read(32).tobytes(), byteorder='big') 
            # result.extend(decode_section(bin_data=bin_data.read(section_lenght*8)))#section lenght is in bytes, we read in bits
            threads.append(executor.submit(decode_section, bin_data=bin_data.read(section_lenght*8)))
        
        for i in threads:
            result.append(DC_first.pop(0))
            result.extend(i.result())
    return result
    first = int.from_bytes(data[:3], byteorder='big')
    return first + huffman_decode(data[4:])


def test():
    test = []
    test2 = []
    for i in range(100000):
        test.append(randint(-127, 255))
        test2.append(randint(-127, 255))
    # test[1290] = 256
    # test = [1, 21, 4, 5]
    encoded = huffman_encode(test.copy())
    encoded2 = huffman_encode(test2.copy())
    decoded = huffman_decode(encoded + encoded2)
    # print(test)
    # print(encoded)
    print(decoded)
    print(test + test2 == decoded)
# test()