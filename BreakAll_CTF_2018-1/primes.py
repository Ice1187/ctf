from pwn import *

r = remote("140.110.112.29", 5130)
r.recvlines(7)
for i in range(0,100):
  r.recvuntil(" = ")
  num = r.recvline()[:-1]


r.interactive()
