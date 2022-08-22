from random import randint
import sys
import numpy as np

def RLE_encode(data):
    arr = RLE_encode_arr(data)
    arr = (i if i>= 0 else int.from_bytes(int.to_bytes(i, length=1, byteorder='big', signed=True), byteorder='big', signed=False) for i in arr)
    return bytearray(arr)

# DECODE..................................
def RLE_decode(data):
    print('decoding RLE')
    result = []
    c = 0
    for i in data:
        if c == 0: # el següent numero és un comptador
            n = to_negative_encoding(i)
            c = n if n<0 else (n+3)
        elif c > 0: # aplicar el comptador
            result.extend([i] * c)
            c = 0
        else: # c < 0; aplicar el comptador negatiu
            result.append(i)
            c+= 1
    return result

def to_negative_encoding(num):
    """Transforma un byte sense signe a un amb signe"""
    return int.from_bytes(bytes([num]), 'big', signed=True)

def RLE_encode_arr(data, progress_bar=None):
    print('encoding RLE arr')
    result = []
    last_digit = [] # ultims digits
    c = 0 # contador
    cp = 0 # contador parcial
    progress_cont = 0 # progress counter
    for i in data:
        #progress handling
        progress_cont+=1
        if progress_bar!=None and progress_cont % 10000 == 0:
            progress_bar.setValue(int(progress_cont/len(data)*100))

        if len(last_digit) == 0: # si no hi ha digit anterior, passa
            last_digit.append(i) 
            continue
        if i == last_digit[-1]: 
            if c>0: # si el comptador ja està iniciat (+3 repeticions)
                c+=1
                if c>=127: # si el comptador és major de 127
                    c = 0
                    result.append(127)
                    result.append(last_digit[0])
                    last_digit = []
            else: # si el comptador no està iniciat (<=3 repeticions)
                cp+=1
                if cp==2 and c<0: # si tenim només 3 repeticions però ja hi havia un comptador negatiu
                    result.append(-len(last_digit[:-1]))
                    result.extend(last_digit[:-1])
                    c = 0
                    last_digit = [i]
                if cp >= 3: # 3 repeticions, activem el comptador principal
                    c = 1
                    cp = 0
        elif cp > 0: # si hi havia repeticions al comptador parcial
            if cp == 2:
                cp = 0
                result.append(0)
                result.append(int(last_digit[0]))
                last_digit = [i]
            else: #cp = 1
                c -= cp + 1 # cp=1=> dos numeros seguits, per tant el comptador ha d'augmentar 1 mes
                last_digit.extend([last_digit[-1]])
                cp = 0
                if c == -126: # diferents casuístiques al actualitzar quan surts d'una quasi-repetició
                    last_digit.append(i)
                    c = 0
                    result.append(-127)
                    result.extend(last_digit)
                    last_digit = []
                elif c == -127:
                    c = 0
                    result.append(-127)
                    result.extend(last_digit)
                    last_digit = [i]
                elif c == -128:
                    result.append(-127)
                    result.append(last_digit[:-1])
                    c = -1
                    last_digit = [last_digit[-1], i]
                else: # si no hi ha cap cas especial
                    last_digit.append(i)
        elif c > 0: # si el comptador hi era en marxa, escriure-ho i tornar a començar de 0
            result.append(c)
            result.append(int(last_digit[0]))
            c = 0
            last_digit = [i]
        else: # si el comptador negatiu ja compta, actualitzar-lo fins a 127
            c-=1
            last_digit.append(i)
            if len(last_digit) >= 127:
                result.append(-127)
                result.extend(last_digit)
                last_digit = []
                c = 0
    if len(last_digit) != 0: # per acabar d'escriure els dígits que s'han quedat en el bucle, si s'escau
        if cp == 2:
            result.append(0)
            result.extend(last_digit)
        elif cp>0:
            result.append(c + -cp-1)
            last_digit.append(last_digit[-1])
            result.extend(last_digit)
        else:
            result.append(c if c>0 else c-1)
            result.extend(last_digit)
    return result

# DECODE..................................
def RLE_decode_arr(data):
    print('decoding RLE arr')
    result = []
    c = 0 # comptador
    for i in data:
        if c == 0: # el següent numero és un comptador
            c = i if i<0 else (i+3)
        elif c > 0: # aplicar el comptador
            result.extend([i] * c)
            c = 0
        else: # c < 0; aplicar el comptador negatiu
            result.append(i)
            c+= 1
    return result

def RLE_encode_arrV2(data):
    print('V2', min(data), max(data))
    data = RLE_encode_arr(data)
    cont = 0
    for i in range(len(data)):
        if cont == 0:
            cont = -data[i] if data[i] < 0 else 1
            data[i] += 127
        else:
            cont-=1
    return data

def RLE_decode_arrV2(data):
    print('V2')
    cont = 0
    for i in range(len(data)):
        if cont == 0:
            data[i] -= 127
            cont = -data[i] if data[i] < 0 else 1
        else:
            cont-=1
    return RLE_decode_arr(data)


def test_arr():
    # RLE_decode_arr(RLE_encode_arr([np.arange(100)]))

    test=[]
    for i in range(10000):
        test.append(randint(0, 255))
    # test = np.array(test)
    te = RLE_encode_arrV2(test)
    print(min(te), max(te))
    td = RLE_decode_arrV2(te)
    # print(td)
    print(td == test)
test_arr()