[Forensics] Digital Camouflage
===
## Description
We need to gain access to some routers. Let's try and see if we can find the password in the captured network data: [data.pcap](https://webshell2017.picoctf.com/static/1836a8ab819664a77ff4d8a754f91d92/data.pcap).
* HINTS
    * It looks like someone logged in with their password earlier. Where would log in data be located in a network capture?
    * 
    * If you think you found the flag, but it doesn't work, consider that the data may be encrypted.

## Solution

查看data.pcap，因為要找password，先關注http協定的封包
![](https://i.imgur.com/K84JnoE.png)

包不多，直接翻一翻
![](https://i.imgur.com/vJL07zQ.png)

看來是base64呢 :3 
```python=
import base64
s = "dEo2NFpxYmRMdw=="
print base64.b64decode(s)
```