from pwn import *
import gmpy2
from Crypto.Util.number import *

r = remote("isc.taiwan-te.ch", 17777)


r.recvuntil("p = 0x")
p = int(r.recvline(), 16)

r.recvuntil("q = ")
q = int(r.recvline(), 16)

r.recvuntil("e = ")
e = int(r.recvline(), 16)

r.recvuntil("c = ")
c = int(r.recvline(), 16)

n = p * q
phi = (p-1) * (q-1)
d = gmpy2.invert(e, phi)
m = long_to_bytes(pow(c, d, n))

print m


