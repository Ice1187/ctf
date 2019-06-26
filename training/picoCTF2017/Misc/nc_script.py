#!/usr/bin/python
#
# History:
# 	18/04/11
# CTF:
#	picoCTF2017
#
# Description:
#	nc to a server using python script.
 
import socket

# Build and connect to server ( Open socket)
s = socket.socket()
s.connect(('shell2017.picoctf.com', 51091))

# Recieve information from server
ser_inf = s.recv(4096).decode('utf-8')

# Parse information
muti_letter = ser_inf[ser_inf.find('the')+5]
time =  int(ser_inf[ser_inf.find('char')+11] + ser_inf[ser_inf.find('char')+12] + ser_inf[ser_inf.find('char')+13])
sgl_letter =  ser_inf[ser_inf.find('single')+8]

# Build reply
rep = time * muti_letter + sgl_letter + "\n"

# Send reply to server
s.send(rep.encode('utf-8'))

# Recieve the flag
flag =  s.recv(4096).decode('utf-8')
print flag

s.close()

