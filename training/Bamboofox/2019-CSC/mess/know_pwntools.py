from pwn import *

context.log_level = 'debug'

r = remote('bamboofox.cs.nctu.edu.tw', 6002)

for i in range(1, 1001):
	r.recv()
	r.sendline(str(i))

r.recv()
