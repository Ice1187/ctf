#!/usr/bin/python

from pwn import *

"""

arr = []

for i in range(10, 27):
  r = remote('2018shell.picoctf.com', 31123)
  print r.recvuntil('report: ')
  padding = 'A'*i
  print "[%d] padding: " % (i) + padding
  r.sendline(padding)
  arr.append(r.recvline())
  r.close()

print arr
"""
# 'A' * (9 + 16)
# arr = "4d6276d172d79a9b7da9098f69e9b403024a64082b1f2cdfa32d27d78ca83236e30cf5302c3f000ff2cb7b8a7106351c68c9c72023aa23806854da080342f3dfac86e58c81273090424d85406ecc90cfc35695e499c759ae5006ea87846dd1030c859821edc4a53c12c5a72d294d3c20cff9f2f47f8da92f5da61d134dea56446916c59406b4b66d23e2a0219618b5698b051c9f3d699965da6a616406ed854db4cc148af3e53ce59570d4cadb345951"

# A * (9 + 15)
arr =   '4d6276d172d79a9b7da9098f69e9b403024a64082b1f2cdfa32d27d78ca83236e30cf5302c3f000ff2cb7b8a7106351c68c9c72023aa23806854da080342f3df8a7952c2019b844e7208f9edc7486b62ea9703c1a94e25010889862315d5f63e7d9d2d6518e78ef0bfd1fc2d6637b6cd371d1f79045a8473be811ddfd5c8c297dd40fd6618bd7542803e752cbfda961ec5272006c0696c81287695fdadc198ed36c10e38bb6ad50728b160404f41b786'

# A * (9 + 14)
# arr =   '4d6276d172d79a9b7da9098f69e9b403024a64082b1f2cdfa32d27d78ca83236e30cf5302c3f000ff2cb7b8a7106351c68c9c72023aa23806854da080342f3df82884a538fcd8c4df9cb0a2430b3268fcb2cfcd1f2c3b6cdef94b721348db6921a0826f66d9887f5ea6dcdddcf3d16fc6683c1d1464deac63202a312838926fb13b5344ad69ceede5925ffa70f4f42714ed93a8a9bff6cfa09d8e5a00b2ca098f677546a42c63764cce6db262291e57d'

# f = open('arr_15', 'a')
# f.write(arr_15 + '\n'


for i in range(0, 128):
  if i==0x0a:
    continue
  r = remote('2018shell.picoctf.com', 31123)
#  print r.recvuntil('report: ')
  pad = 'A'*(9+15)
  word =  chr(0 + i)
  print "[%d] pad = " % (i) + pad + word
  r.sendline(pad+word)
  rec = r.recvline()
  # rec = r.recvline().strip('\n')
  # f.write(rec + '\n')
  rec = rec[0:130]
  arr = arr[0:130]
#  print rec
#  print arr
  if rec == arr:
    print "Find char: " + word
    break

# X
