from pwn import *

r = remote("140.110.112.29", 5123)
r.recvlines(1)
for i in range(0,100):
  s = ''
  r.recvuntil("word by ")
  ele = r.recv(1)
  shift = r.recvuntil(" ")[:-1]
  r.recvuntil(": ")
  string = r.recvline()[:-1]
  print(ele, shift, string)
  for j in range(0, len(string)):
    if string[j].isalpha():
      if ele=='+':
				s += chr(65+((ord(string[j])-65+int(shift))%26))
      else:
        s += chr(65+((ord(string[j])-65+26-int(shift))%26))
    else:
      s += string[j]
  print(s)
  r.sendline(s)

r.interactive()
