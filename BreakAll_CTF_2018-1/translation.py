from pwn import *

r = remote("140.110.112.29", 5125)
r.recvlines(5)
for i in range(0,100):
	count = 0
	r.recvuntil("string : ")
	s = r.recvline()[:-1]
	#print(s)
	for j in range(len(s)-1, -1, -1):
		count += ord(s[j]) * (256**(len(s)-1-j))
		print(count)
	r.sendline(str(count))

r.interactive()
