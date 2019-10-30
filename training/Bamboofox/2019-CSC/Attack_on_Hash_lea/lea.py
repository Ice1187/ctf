from pwn import *
from hashpumpy import hashpump

r = remote('bamboofox.cs.nctu.edu.tw', 30000)

r.recvuntil(': ')

r.recvline().strip()

r.recvuntil(': ')

auth = r.recvline().strip()

# input

msg = 'user=someone'
append_str = 'user=admin'
hmac = auth
len_of_key = 40

result = hashpump(auth, msg, append_str, 40)

r.recvuntil(': ')

r.sendline(b64e(result[1]))

r.recvuntil(': ')

r.sendline(result[0])

print r.recv(4096)


