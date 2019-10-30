from pwn import *

context.log_level = 'debug'

r = remote("bamboofox.cs.nctu.edu.tw", 30002)

r.recvuntil('A.')
