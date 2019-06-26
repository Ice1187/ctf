[Misc] looooong
===

## Description

I heard you have some "delusions of grandeur" about your typing speed. How fast can you go at shell2017.picoctf.com:51091?
* HINTS
	* Use the nc command to connect!
	* I hear python is a good means (among many) to generate the needed input.
	* It might help to have multiple windows open

## Solution

Write a python script to solve it!

``` 
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
```

And, we get the flag.

