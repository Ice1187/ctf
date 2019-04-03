from pwn import *

r = remote("140.110.112.29", 5127)
r.recvlines(5)
for i in range(0,100):
	r.recvuntil("heit : ")
	f = r.recvline()[:-1]
#	print(f)
	c = str((int(f)-32)*5)
	ans = c + '/9'
	r.sendline(ans)

r.interactive()
