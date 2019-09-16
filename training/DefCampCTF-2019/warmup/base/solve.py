from pwn import *

r = remote("206.81.24.129", 4441)


# hex
r.recvuntil('<<')
number = hex(int(r.recvuntil('>>')[:-2]))
r.recvuntil(': ')
r.sendline(number)


# ascii
r.recvuntil('<<')
number = r.recvuntil('>>')[:-2]
ans = ""
for i in range(0, len(number), 2):
	ans += chr(int(number[i:i+2], 16))
r.recvuntil(':')
r.sendline(ans)

# oct
r.recvuntil('<<')
number = r.recvuntil('>>')[:-2]
oct_num = number.split(' ')
ans = ""
for i in oct_num:
	ans += chr(int(i[1:], 8))
r.recvuntil(':')
r.sendline(ans)

r.interactive()

