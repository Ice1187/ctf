#!/usr/bin/python -u
import random,string

encflag = "BNZQ:20380043pc5p8u861tcy650q8xn8mf5d"
decflag = ""
# print flag
random.seed("random")

"""
for i in range(0,10):
    print random.randrange(0,26)
"""

for c in encflag:
  if c.islower():
    #rotate number around alphabet a random amount
    decflag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    decflag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    decflag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    decflag += c
print "Flag: "+decflag

