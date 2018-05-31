from pwn import *

r = remote("140.110.112.29", 5124)
r.recvlines(12)
func = {
'0': lambda x: 3*x**2 + x + 3,
'1': lambda x: 5*x**2 + 8,
'2': lambda x: 4*x**3 + 6*x + 6,
'3': lambda x: 7*x**3 + 5*x**2,
'4': lambda x: x**2 + 4*x + 3
}
for i in range(0,100):
  r.recvuntil("tion : ")
  f = r.recvline()[:-1]
  r.recvuntil("x = ")
  x = r.recvline()[:-1]
  print(f, x)
  ans = func[f](int(x))
  print(ans)
  r.sendline(str(ans))

r.interactive()
