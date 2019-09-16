from pwn import *

r = remote('crypto.chal.csaw.io', 1003)

print r.recv(2048)

res = "\x0f" * 0xf

r.sendline(res)

r.interactive()

