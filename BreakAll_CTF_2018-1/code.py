# code.py
#!/usr/bin/env python
from Crypto.Util import number 
import libnum
import random
import itertools
flag = libnum.s2n(open("flag.txt",'rb').read())
e = 65537
n_size = 2048
prime_list = []
n_list = []

for _ in range(50):
	prime_list.append(number.getStrongPrime(n_size, e))

for i in itertools.combinations(prime_list, 2):
	n_list.append(i[0] * i[1])
random.shuffle(n_list)

result = ""
for n in n_list:
	result += str(pow(flag,e,n)) + "\n"
with open("ciphertext.txt","w") as f:
	f.write(result)

