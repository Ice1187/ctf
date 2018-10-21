from pwn import *
import hashlib as hl


r = remote('104.199.235.135', 20000)
print(r.recvlines(2))

r.recvuntil("x[:6] == ")
plain = r.recv(6)
r.recvuntil("x = ")

#plain = raw_input('x[:6]: ')
ext = 'A'

alpha = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
m = hl.sha256(plain+ext)
ans = m.hexdigest()
print(plain, ans)

for i in xrange(0, len(alpha)):
  ext = alpha[i]
  ans = hl.sha256(plain+ext).hexdigest()
  if ans[:6] == '000000':
    print(alpha[i], ans)
    r.sendline(plain+ext)
    print(r.recvline())

while 1:
  for h in xrange(0, len(ext)):
    if ext[0] == 'Z':
      ext = '0' * (len(ext)+1)
     # print(ext)
    elif ext[h] == 'Z':
      c = ext
      if len(ext) != 2:
        ext = c[0:h-1] + alpha[alpha.find(ext[h-1])+1] + '0'*(len(c)-h)
  #      print(c[0:h-2], h, c, ext)
      else:
        ext = alpha[alpha.find(ext[h-1])+1] + '0'*(len(c)-h)
  for i in xrange(0,len(alpha)):
    c = ext
    ext = ext[:-1] + alpha[i]
    ans = hl.sha256(plain+ext).hexdigest()
    #print(ext, ans[:6], m.hexdigest()[0:6])
    if ans[0:6] == '000000':
      print(plain+ext, ans)
      r.sendline(plain+ext)
      #r.interactive()
      res = r.recvline()
      print(res)
