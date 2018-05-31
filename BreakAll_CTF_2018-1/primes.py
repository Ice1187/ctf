from pwn import *


r = remote("140.110.112.29", 5131)
r.recvlines(9)

n = 15000000

pri = [0]*n
#print(pri)
for i in xrange(2,n):
  if pri[i]==0:
    for j in range(i+i,n, i):
        pri[j] = 1
  pri[i] = str(pri[i])
'''
for i in xrange(1, 1500):
  print(i, pri[i])
'''
dt = {}
for i in xrange(2,n):
  if pri[i]=='0':  
    l = str(len(str(i)))
    dt.setdefault(l, i)

print(dt)
#for i in xrange(1,1500):
#  print(i, dt[str(3)])

'''
for i in range(0,100):
  r.recvuntil(" = ")
  num = r.recvline()[:-1]


r.interactive()
'''
