#!/usr/bin/python3
#
# [!] Use python3 [!]
#
# Ice1187$ wc -l pusheen.txt 
# 6527 pusheen.txt
#
# Add a newline to the end of pusheen.txt
#
# Ice1187$ wc -l pusheen.txt
# 6528 pusheen.txt
# 
# So that every 16 lines is a pusheen
#
import re
import codecs

f = open('./pusheen.txt', 'r')

b = ''
flag = 0

for i in range(408):        # 6528 / 16 = 408
    flag = 0
    for j in range(0, 16):
        lin = f.readline()
        lin = ''.join(lin)
        lin = lin.strip().replace(' ','')
        lin = str.encode(lin)                   # convert str to bytes
        lin = str(codecs.encode(lin, 'hex'))    # convert lin from hex to bytes(to deal with '\x', then convert back to str
        if 'e29692' in lin:
            flag = 1
    if flag==1:
        b += '1'    # white
    elif flag==0:
        b += '0'    # black
    else:
        print("Error")
        exit()

print(b)
f.close()

