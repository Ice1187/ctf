0405 Learning dis_asm, s/ltrace 筆記3
===

## dis_asm

* 教材
    * [basis.cpp](https://github.com/Ice1187/ctf/blob/master/learning/dis_asb/basis.cpp)
    * [Reverse 0x01(2018 Bamboofox社課)](https://docs.google.com/presentation/d/1h_3tut9dSVhjhAajK8atCy5CNXChoOFK213ZFh21BjM/edit#slide=id.p)

---

0. `basis.cpp`
```cpp
int a = 3;
int b = 9;
b = a * b;
a = b / a;
```

1. 查看<main>
```b
    11ba:       c7 45 fc 03 00 00 00    mov    DWORD PTR [rbp-0x4],0x3
    11c1:       c7 45 f4 09 00 00 00    mov    DWORD PTR [rbp-0xc],0x9
    11c8:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    11cb:       0f af 45 fc             imul   eax,DWORD PTR [rbp-0x4]
    11cf:       89 45 f4                mov    DWORD PTR [rbp-0xc],eax
    11d2:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    11d5:       99                      cdq    
    11d6:       f7 7d fc                idiv   DWORD PTR [rbp-0x4]
    11d9:       89 45 fc                mov    DWORD PTR [rbp-0x4],eax
    11dc:       b8 00 00 00 00          mov    eax,0x0
    11e1:       c9                      leave  
    11e2:       c3                      ret    
```

2. 分析

* [CWD/CDQ/CQO](https://www.felixcloutier.com/x86/cwd:cdq:cqo)
* [組合語言指令介紹](http://masm1215.myweb.hinet.net/2-base/5-point.htm)
```b
mov    DWORD PTR [rbp-0x4],0x3    # a = 3
mov    DWORD PTR [rbp-0xc],0x9    # b = 9
mov    eax,DWORD PTR [rbp-0xc]    # eax = b
imul   eax,DWORD PTR [rbp-0x4]    # eax = eax * a [eax作為Accumulation]
mov    DWORD PTR [rbp-0xc],eax    # b = eax
mov    eax,DWORD PTR [rbp-0xc]    # eax = b
cdq                               # edx = eax
idiv   DWORD PTR [rbp-0x4]        # edx / a，eax = 商，edx = 餘
mov    DWORD PTR [rbp-0x4],eax    # a = eax
mov    eax,0x0
leave  
ret    
```
* cdq(Convert Double word to Quad word)
    * 動作：將`EAX`中的資料加以擴充轉換後，分成兩組存入`EDX`與`EAX`中，變成`EDX:EAX (64 bits)` 
* idiv
    * 動作：有號的`AX/DX:AX/EDX:EAX`除以來源，商放入`AL/AX/EAX`，餘數放入`AH/DX/EDX`

3. 加上function

```cpp
int func(int n, int x = 0){
  if(n > x)
    return 1;
  else
    return 0;
}

int main(){
a = 5;
b = -3;
a = func(a);
b = func(b, 3);

return 0;
}
```
disasm:
```b
0000000000001155 <_Z4funcii>:
    1155:       55                      push   rbp
    1156:       48 89 e5                mov    rbp,rsp
    1159:       89 7d fc                mov    DWORD PTR [rbp-0x4],edi
    115c:       89 75 f8                mov    DWORD PTR [rbp-0x8],esi
    115f:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
    1162:       3b 45 f8                cmp    eax,DWORD PTR [rbp-0x8]
    1165:       7e 07                   jle    116e <_Z4funcii+0x19>
    1167:       b8 01 00 00 00          mov    eax,0x1
    116c:       eb 05                   jmp    1173 <_Z4funcii+0x1e>
    116e:       b8 00 00 00 00          mov    eax,0x0
    1173:       5d                      pop    rbp
    1174:       c3                      ret    

0000000000001175 <main>:
...
...
...
    11fc:       c7 45 fc 05 00 00 00    mov    DWORD PTR [rbp-0x4],0x5
    1203:       c7 45 f4 fd ff ff ff    mov    DWORD PTR [rbp-0xc],0xfffffffd
    120a:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
    120d:       be 00 00 00 00          mov    esi,0x0
    1212:       89 c7                   mov    edi,eax
    1214:       e8 3c ff ff ff          call   1155 <_Z4funcii>
    1219:       89 45 fc                mov    DWORD PTR [rbp-0x4],eax
    121c:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    121f:       be 03 00 00 00          mov    esi,0x3
    1224:       89 c7                   mov    edi,eax
    1226:       e8 2a ff ff ff          call   1155 <_Z4funcii>
    122b:       89 45 f4                mov    DWORD PTR [rbp-0xc],eax
    122e:       b8 00 00 00 00          mov    eax,0x0
    1233:       c9                      leave  
    1234:       c3                      ret 
```
4. 分析

* [Reverse(2017 Bamboofox社課)](https://drive.google.com/file/d/12ZWTQQbi6xxqfctlIxher6SpQ_JqQZUz/view)

```b
<_Z4funcii>:
        push   rbp                        
        mov    rbp,rsp                    
        mov    DWORD PTR [rbp-0x4],edi    # n = edi
        mov    DWORD PTR [rbp-0x8],esi    # x = esi
        mov    eax,DWORD PTR [rbp-0x4]    # eax = n
        cmp    eax,DWORD PTR [rbp-0x8]    # 比較 eax 和 x
        jle    116e <_Z4funcii+0x19>      # jle(Jump if Less or Equal)，
        mov    eax,0x1                    # eax = 1
        jmp    1173 <_Z4funcii+0x1e>      # jump 
<+0x19> mov    eax,0x0
<+0x1e> pop    rbp
        ret    

<main>:
mov    DWORD PTR [rbp-0x4],0x5           # a = 5 
mov    DWORD PTR [rbp-0xc],0xfffffffd    # b = -3
mov    eax,DWORD PTR [rbp-0x4]           # eax = a
mov    esi,0x0                           # esi = 0  ，esi為func的第二個參數，此做預設處理(int x = 0)
mov    edi,eax                           # edi = eax，edi為func的第一個參數
call   1155 <_Z4funcii>                  # call function
mov    DWORD PTR [rbp-0x4],eax           # a = eax(func的return)
mov    eax,DWORD PTR [rbp-0xc]           # eax = b
mov    esi,0x3                           # func的第二參數 = 3
mov    edi,eax                           # func的第一參數 = eax
call   1155 <_Z4funcii>
mov    DWORD PTR [rbp-0xc],eax           # b = eax(func的return)
mov    eax,0x0
leave  
ret    
```

---

## system call

* 教材
    * [系統呼叫 wiki](https://zh.wikipedia.org/wiki/%E7%B3%BB%E7%BB%9F%E8%B0%83%E7%94%A8)

    * [调试工具ltrace strace ftrace的使用](http://lzz5235.github.io/2013/11/22/ltrace-strace-ftrace.html)
    * [Lniux syscalls ref](https://syscalls.kernelgrok.com/)
    * [Linux 共享庫指南](http://liaoph.com/linux-shared-libary/)

0. `trace.cpp`
```cpp
#include <stdio.h>
using namespace std;

int main(){
  char text[] = "hello world!\n";

  printf("%s",text);

  return 0;
}
```

1. `strace ./trace.cpp`

```
execve("./trace", ["./trace"], 0x7fffe21cbef0 /* 42 vars */) = 0
# execute program，調用execve()函數載入程式執行 

brk(NULL)                               = 0x55b8e8431000
# change data segment size，allocate new space to load the infomation of programmer

access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
# check user's permissions for a file，讀入一些library的內容(?

openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
# open and possibly create a file，讀入另一些library內容(?

fstat(3, {st_mode=S_IFREG|0644, st_size=121893, ...}) = 0
# get file status，查看file的狀態，包含rwx等

mmap(NULL, 121893, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f5f2f250000
# 把ELF頭載入virtual adress

close(3)                                = 0
# close a file descriptor，

openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libstdc++.so.6", O_RDONLY|O_CLOEXEC) = 3
# 載入libstdc++.so函式庫

read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\260\304\10\0\0\0\0\0"..., 832) = 832
# read from a file descriptor

fstat(3, {st_mode=S_IFREG|0644, st_size=1570256, ...}) = 0

mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f5f2f24e000
mmap(NULL, 1585184, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f5f2f0ca000
mprotect(0x7f5f2f153000, 962560, PROT_NONE) = 0
# set protection on a region of memory

mmap(0x7f5f2f153000, 704512, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x89000) = 0x7f5f2f153000
mmap(0x7f5f2f1ff000, 253952, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x135000) = 0x7f5f2f1ff000
mmap(0x7f5f2f23e000, 49152, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x173000) = 0x7f5f2f23e000
mmap(0x7f5f2f24a000, 12320, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f5f2f24a000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p\322\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=1579448, ...}) = 0
mmap(NULL, 1581384, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f5f2ef47000
mmap(0x7f5f2ef54000, 651264, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xd000) = 0x7f5f2ef54000
mmap(0x7f5f2eff3000, 872448, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0xac000) = 0x7f5f2eff3000
mmap(0x7f5f2f0c8000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x180000) = 0x7f5f2f0c8000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libgcc_s.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\3402\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=100712, ...}) = 0
mmap(NULL, 103472, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f5f2ef2d000
mprotect(0x7f5f2ef30000, 86016, PROT_NONE) = 0
mmap(0x7f5f2ef30000, 69632, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x3000) = 0x7f5f2ef30000
mmap(0x7f5f2ef41000, 12288, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x14000) = 0x7f5f2ef41000
mmap(0x7f5f2ef45000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x17000) = 0x7f5f2ef45000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\260A\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1824496, ...}) = 0
mmap(NULL, 1837056, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f5f2ed6c000
mprotect(0x7f5f2ed8e000, 1658880, PROT_NONE) = 0
mmap(0x7f5f2ed8e000, 1343488, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x22000) = 0x7f5f2ed8e000
mmap(0x7f5f2eed6000, 311296, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x16a000) = 0x7f5f2eed6000
mmap(0x7f5f2ef23000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1b6000) = 0x7f5f2ef23000
mmap(0x7f5f2ef29000, 14336, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f5f2ef29000
close(3)                                = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f5f2ed6a000
arch_prctl(ARCH_SET_FS, 0x7f5f2ed6af40) = 0
# set architecture-specific thread state

mprotect(0x7f5f2ef23000, 16384, PROT_READ) = 0
mprotect(0x7f5f2ef45000, 4096, PROT_READ) = 0
mprotect(0x7f5f2f0c8000, 4096, PROT_READ) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f5f2ed68000
mprotect(0x7f5f2f23e000, 40960, PROT_READ) = 0
mprotect(0x55b8e7be2000, 4096, PROT_READ) = 0
mprotect(0x7f5f2f295000, 4096, PROT_READ) = 0
munmap(0x7f5f2f250000, 121893)          = 0
brk(NULL)                               = 0x55b8e8431000
brk(0x55b8e8452000)                     = 0x55b8e8452000
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}) = 0
write(1, "hello world!\n", 13hello world!
)          = 13
# 寫入

exit_group(0)                           = ?
+++ exited with 0 +++
```

###### tags: `CTF` `dis_asm` `s/ltrace`

