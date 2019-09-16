import sympy
import binascii
from Crypto.PublicKey import RSA

e = 0x10001
flag = open('flag', 'rb').read()
getTwinPrime = lambda n: int(open('twinPrime' + str(n), 'r').read())

def genkey():
	global e
	p = getTwinPrime(1)
	q = getTwinPrime(2)
	r = getTwinPrime(3)
	n1 = p * q
	n2 = (p + 2) * (q + 2)
	n3 = r * r
	print('public key 1')
	print(str(RSA.construct((n1, e)).exportKey(), 'utf-8'))
	print('public key 2')
	print(str(RSA.construct((n2, e)).exportKey(), 'utf-8'))
	print('public key 3')
	print(str(RSA.construct((n3, e)).exportKey(), 'utf-8'))
	return n1, n2, n3

def key_flag():
	n1, n2, n3 = genkey()
	c = int(binascii.hexlify(flag), 16)
	c = pow(c, e, n1)
	c = pow(c, e, n2)
	c = pow(c, e, n3)
	print('encrypted flag')
	print(hex(c))

if __name__ == '__main__':
	while True:
		print('1) print key and flag')
		print('2) print server code')
		print('0) exit')
		n = input('Enter: ').strip('\n').strip()
		if n == '0': exit()
		elif n == '1': key_flag()
		elif n == '2': print(open(
