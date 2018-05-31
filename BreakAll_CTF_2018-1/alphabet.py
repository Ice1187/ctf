from pwn import *

r = remote("140.110.112.29", 5128)
r.recvlines(3)
for i in range(0,100):
  count = 0
  r.recvuntil("many ")
#  print(le)
  alpha = r.recv(1)
  r.recvuntil(" in ")
  string = r.recvline()[:-1]
  print(alpha, string)
  for j in range(0, len(string)):
    if string[j] == alpha:
      count += 1
  r.sendline(str(count))

r.interactive()
