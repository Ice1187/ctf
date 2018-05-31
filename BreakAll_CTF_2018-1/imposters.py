from pwn import *

r = remote("140.110.112.29", 5129)
r.recvlines(8)
for i in range(0,100):
	r.recvuntil(" = ")
	l = int(r.recvline()[:-1])
	print(l)

r.interactive()
