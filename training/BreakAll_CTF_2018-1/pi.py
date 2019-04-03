from pwn import *

r = remote("140.110.112.29", 5130)
r.recvlines(5)
pi = "3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 70679 82148 08651 32823 06647 09384 46095 50582 23172 53594 08128 48111 74502 84102 70193 85211 05559 64462 29489 54930 38196".replace(' ','')
for i in range(0,100):
  s = ''
  r.recvuntil(" = ")
  l = int(r.recvline()[:-1])
  s = int(pi[2:l+1])
  print(int(pi[l+1]))
  if int(pi[l+1])>4 and l!=31:
    s += 1
  ans = str('3.'+str(s))
  print(l, ans, len(ans)) 
  r.sendline(ans) 

r.interactive()
