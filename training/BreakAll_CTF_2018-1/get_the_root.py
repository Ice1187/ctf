from pwn import *
import numpy as np
import math

r = remote("140.110.112.29", 5122)
r.recvlines(6)
for i in range(0,100):
  r.recvuntil("al : ")
  rc = r.recvline()[:-1]
  ls = rc.split(' ')
  print(rc)
  print(ls)
  root =  int(round(float(np.roots(ls)[0])))
  print(root)
  r.sendline(str(root))

r.interactive()
