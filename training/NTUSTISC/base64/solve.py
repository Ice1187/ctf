import re
from pwn import *

r = remote("isc.taiwan-te.ch", 10801)

print b64d(r.recvline().strip())
print b64d(r.recvline().strip())
print b64d(r.recvline().strip())

for i in range(100):
	print r.recvuntil("100\n")
	task = b64d(r.recvline().strip())
	matchObj = re.match("(.*) (.*) (.*) = ?", task)
	first =  int(matchObj.group(1))
	op = matchObj.group(2)
	second = int(matchObj.group(3))
	if op=="+":
		ans = first + second
	elif op=="-":
		ans = first - second
	elif op=="*":
		ans = first * second
	elif op=="/":
		ans = first / second
	r.sendline(str(ans))
	print task
	print ans

flag = b64d(r.recvline().strip())
print flag
