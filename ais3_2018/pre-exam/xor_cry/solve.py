#!/usr/bin/env python3
import random
'''
with open('flag', 'rb') as data:
    flag = data.read()
    assert(flag.startswith(b'AIS3{'))
'''

def xor(X, Y):
    return bytes([x ^ y for x, y in zip(X, Y)])

#plain = flag + key
#cipher = xor(plain, key)

f = open('flag-encrypted', 'rb').read()
print(f[:5])
