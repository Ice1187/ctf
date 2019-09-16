from pwn import *
import binascii as ba

def init_info():
	msg = ba.unhexlify('%x' % (int(r.recvline().strip(), 2)))
	print msg
	r.recvline()
	msg = ba.unhexlify('%x' % (int(r.recvline().strip(), 2)))
	print msg
	r.recvline()
	msg = ba.unhexlify('%x' % (int(r.recvuntil("(").strip()[:-3], 2)))
	print msg + ": "
	N = int(r.recvuntil(",").strip()[:-1], 2)
	print "N: " + str(N)
	e = int(r.recvuntil(")").strip()[:-1], 2)
	print "e: " + str(e)
	msg = ba.unhexlify('%x' % (int(r.recvuntil(":").strip()[:-1], 2)))
	print msg + ": "
	c = int(r.recvline().strip(), 2)
	print "c: " + str(c)
	return N, e, c
	

r = remote("chall2.2019.redpwn.net", 5001)
N, e, c = init_info()



