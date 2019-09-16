from pwn import *
from brute import brute

# enc_hash = "CD04302CBBD2E0EB259F53FAC7C57EE2"
enc_hash = "cd04302cbbd2e0eb259f53fac7c57ee2"
counter = 0

for i in brute(length=5, letters=True, numbers=True, symbols=False):
  m1 = util.hashes.md5sumhex(i)
  m2 = util.hashes.md5sumhex(m1)
  m3 = util.hashes.md5sumhex(m2)
  m4 = util.hashes.md5sumhex(m3)
  m5 = util.hashes.md5sumhex(m4)
  m6 = util.hashes.md5sumhex(m5)
  m7 = util.hashes.md5sumhex(m6)
  m8 = util.hashes.md5sumhex(m7)
  m9 = util.hashes.md5sumhex(m8)
  m10 = util.hashes.md5sumhex(m9)
  if (counter%100000) == 0:
    print "[*] counter: " + str(counter)
    print "[+] " + i
    print "[-] " + m10
  if m10 == enc_hash:
    print "[!] flag: " + i
    break
  counter += 1

