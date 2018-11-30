import scipy.linalg
import numpy as np
from Crypto.Random import random


def createdKey(cords, bits):
    print(cords, bits)
    equation = list()
    sum_cords = 0
    for i in range(0, len(cords)):
        equation.append(random.randint(0, 2**bits))
    
    for i in range(0, len(cords)):
        sum_cords += cords[i] * equation[i]
    
    equation.append(sum_cords)
        
    return equation

def solutionKey(cords):
    print("Cords in solutionkey\n")
    cords_len = len(cords[0]) - 1
#    fields = list()
#    field = list()
    vector = [0] * (len(cords) + 1)
    fields = [[0 for x in range(cords_len)] for y in range(len(cords))]
    print("fields", fields)
    print("dimensions {} x {}".format(len(cords), cords_len))
#    for i in range(0, len(cords)):
#        for j in range(0, cords_len):
#            field.append(0)
#        fields.append(field)

    i = 0
    j = 0
#    print("vector\n" + vector)
#    while i < len(cords):
#        while j < cords_len:
#            fields[i][j] = cords[i][j]
#            j += 1
#        i += 1
#        vector[i+1] = cords[i][cords_len - 1]
    for i in range(0, len(cords)):
        for j in range(0, cords_len):
            fields[i][j] = cords[i][j]
#            print("Type of elements" + str(type(fields[i][j])))
            print(("Fields[{}][{}] = " + str(fields[i][j])).format(i + 1, j + 1))
        
        vector[i + 1] = cords[i][cords_len - 1]

    fields_matrix = np.reshape(fields, (cords_len, cords_len)).astype(float)
    vector.pop(0)
#    print("size of vector", len(vector))
#    print("Type ", type(fields_matrix), "Shape", fields_matrix.shape)
#    vector = np.array(vector)
#    print("Type of vector " + str(type(vector[0])) + "Length of vector"  + str(vector.shape))
    
#    for r in fields_matrix:
#        for c in r:
#            print("data type ", c.dtype)
            
    vector = list(map(int, vector))
    vector = np.array(vector).astype(float)
    print(fields_matrix)
    answers = scipy.linalg.solve(fields_matrix, vector)
    print(answers, len(answers))
    
    solutions = []
    for answer in answers:
        solutions.append(int(answer))
#    byte_array = list()
    size = 0
    for solution in solutions:
        k = solution.to_bytes((solution.bit_length() + 7) // 8, 'big')
        size += len(k)
    
    pos = size - 1
    ret = bytearray(size)
    for solution in solutions:
        k = solution.to_bytes((solution.bit_length() + 7) // 8, 'big')
        for j in range(0, len(k)):
            ret[pos] = k[j]
            pos -= 1
    
    return ret

def divide(n, secret):
    print(n, secret)
    scrt = secret
    s = [0] * n
    size = len(secret) // n
    aux = bytearray(size)
    
    for i in range(0, n - 1):
        for j in range(0, size):
            index = len(secret) - (1 + (i * size) + j)
            aux[size - (j + 1)] = secret[index]
            scrt[index] = 0
        
        s[i] = int.from_bytes(aux, byteorder = 'big')
        
    
    aux = bytearray(len(secret) - (size * (n-1)))
    
    for i in range(0, len(aux)):
        aux[i] = scrt[i]
    
    s[n - 1] = int.from_bytes(aux, byteorder = 'big')

    return s            
    


n = 5
t = 3
bits = 500

secret = "Secret Sharing"
a = bytearray()
a.extend(secret.encode())
hex_secret = a
print(hex_secret)
passkey  = divide(t, hex_secret)
print("passkey", passkey)
keys = list()

for i in range(0, n):
    keys.append(createdKey(passkey, bits))

keys2 = list()

t_count = 0
for row in keys:
    for ele in row:
        print("ELEMENT " + str(ele))

print("Keys ", np.asmatrix(keys).shape)
        
for row in keys:
    if t_count < t:
        keys2.append(row)
    else:
        break
    t_count += 1
    
print("Keys2 ", np.asmatrix(keys2).shape)
b = solutionKey(keys2)
print(b)
print("string" + b.decode())
        

       
