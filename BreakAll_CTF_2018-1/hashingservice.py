from pwn import *
import hashlib as hl

r = remote("140.110.112.29", 4112)
r.recvuntil("Me:")
plain = r.recvline()[:-1]
print(plain)
h = hl.sha512()
h.update(str(plain))
ans = str(h.hexdigest())
print(ans)
r.sendline(ans)

r.interactive()
