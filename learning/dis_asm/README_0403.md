0403 Learning dis_asm 筆記1
===
* 教材
    * [basis.cpp](https://github.com/Ice1187/ctf/blob/master/learning/dis_asb/basis.cpp)
    * [Reverse 0x01(2018 Bamboofox社課)](https://docs.google.com/presentation/d/1h_3tut9dSVhjhAajK8atCy5CNXChoOFK213ZFh21BjM/edit#slide=id.p)
---

0. `basis.cpp`
```c++
int main(){
  int a;
  a = 0;
  a++;
  int b = 1;
  b = a + b;
  printf("%d\n",b);
  return 0;
}
```

1. 用`objdump`開啟查看disasb。
```bash
Ice1187: objdump -M intel -d basis
# -M 切換到intel syntax
# -d 表示disasb反組譯
```
2. 查看<main>
```b
0000000000001030 <printf@plt>:
    1030:       ff 25 e2 2f 00 00       jmp    QWORD PTR [rip+0x2fe2]        # 4018 <printf@GLIBC_2.2.5>
    1036:       68 00 00 00 00          push   0x0
    103b:       e9 e0 ff ff ff          jmp    1020 <.plt> 

0000000000001155 <main>:
    1155:       55                      push   rbp
    1156:       48 89 e5                mov    rbp,rsp
    1159:       48 83 ec 10             sub    rsp,0x10
    115d:       c7 45 fc 00 00 00 00    mov    DWORD PTR [rbp-0x4],0x0
    1164:       83 45 fc 01             add    DWORD PTR [rbp-0x4],0x1
    1168:       c7 45 f8 01 00 00 00    mov    DWORD PTR [rbp-0x8],0x1
    116f:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
    1172:       01 45 f8                add    DWORD PTR [rbp-0x8],eax
    1175:       8b 45 f8                mov    eax,DWORD PTR [rbp-0x8]
    1178:       89 c6                   mov    esi,eax
    117a:       48 8d 3d 84 0e 00 00    lea    rdi,[rip+0xe84]        # 2005 <_ZStL19piecewise_construct+0x1>
    1181:       b8 00 00 00 00          mov    eax,0x0
    1186:       e8 a5 fe ff ff          call   1030 <printf@plt>
    118b:       b8 00 00 00 00          mov    eax,0x0
    1190:       c9                      leave  
    1191:       c3                      ret   
```

3. 分析
* [基本知識](http://karosesblog.blogspot.com/2016/10/cmu-buffer-overflow-attack.html)
* %rbp：Frame pointer，用來指到目前stack frame的開頭
* %rsp：stack pointer，用來指到目前stack的top，也是尾巴
* x86的stack是從高位往低位長的
* mov byte [rcx], 0x61		// byte = 8 bits
mul word [rax], 0x87		// word = 2 bytes
inc dword [rbp]				// dword = 2 words
not qword [rsp]				// qword = 2 dwords
```b
<printf@plt>:
jmp    QWORD PTR [rip+0x2fe2]     # 4018 <printf@GLIBC_2.2.5>
push   0x0
jmp    1020 <.plt>

<main>:
push   rbp                        # stack放入rbp    
mov    rbp,rsp                    # 將rsp移到rbp
sub    rsp,0x10                   # 將rsp往低位減出16個bytes
mov    DWORD PTR [rbp-0x4],0x0    # 第一個local變數[位址rbp-0x4]，就是a，a=0
add    DWORD PTR [rbp-0x4],0x1    # a++ 
mov    DWORD PTR [rbp-0x8],0x1    # 第二個local變數[位址rbp-0x8]，就是b，b=1
mov    eax,DWORD PTR [rbp-0x4]    # 將a的值放入eax
add    DWORD PTR [rbp-0x8],eax    # 將eax的值加到b，b = b + eax(a的值) 
mov    eax,DWORD PTR [rbp-0x8]    # eax - b
mov    esi,eax                    # rsi放func(此為printf)的第二個參數，esi = eax
lea    rdi,[rip+0xe84]            # rdi放func(此為printf)的第一個參數，rdi = &(rip+0xe84)
mov    eax,0x0                    # 設定vector register(?)，eax = 0
call   1030 <printf@plt>          # call <printf@plt>
mov    eax,0x0
leave  
ret
```

4. 加上loop
```c++
for(int i=0; i<5; i++)
  a = a + i;
printf("%d\n", a);
```
disasm:
```b
1155 <main>:
...
...
...
==> <main+0x?>根據main的起始位址和四位數的指令位址換算
Ex: 0x1192 - 0x1155 = 0x3d，所以<main+0x3d>在1192那行。
每行佔多少長度，根據第二欄的hex數量來看
Ex: 0x118b + 7 = 1192

    118b:       c7 45 f8 00 00 00 00    mov    DWORD PTR [rbp-0x8],0x0
    1192:       83 7d f8 04             cmp    DWORD PTR [rbp-0x8],0x4
    1196:       7f 0c                   jg     11a4 <main+0x4f>
    1198:       8b 45 f8                mov    eax,DWORD PTR [rbp-0x8]
    119b:       01 45 fc                add    DWORD PTR [rbp-0x4],eax
    119e:       83 45 f8 01             add    DWORD PTR [rbp-0x8],0x1
    11a2:       eb ee                   jmp    1192 <main+0x3d>
    11a4:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
    11a7:       89 c6                   mov    esi,eax
    11a9:       48 8d 3d 55 0e 00 00    lea    rdi,[rip+0xe55]        # 2005 <_ZStL19piecewise_construct+0x1>
    11b0:       b8 00 00 00 00          mov    eax,0x0
    11b5:       e8 76 fe ff ff          call   1030 <printf@plt>
    11ba:       b8 00 00 00 00          mov    eax,0x0
    11bf:       c9                      leave  
    11c0:       c3                      ret    
```
5. 分析(變數位址跟上方3.不同)
```
# [rbp-0x4] = a
# [rbp-0xc] = b
# [rbp-0x8] = i
```
```b
main:
...
...
...

        mov    DWORD PTR [rbp-0x8],0x0    # i = 0
<+0x3d> cmp    DWORD PTR [rbp-0x8],0x4    # 比較i與4，設定flags
        jg     11a4 <main+0x4f>           # jg(jump if greater)，據cmp的flags結果，較大則跳到<main+0x4f>
        mov    eax,DWORD PTR [rbp-0x8]    # eax = i
        add    DWORD PTR [rbp-0x4],eax    # a = a + eax
        add    DWORD PTR [rbp-0x8],0x1    # i++
        jmp    1192 <main+0x3d>           # 跳回<main+0x3d>處
<+0x4f> mov    eax,DWORD PTR [rbp-0x4]    # eax = a
        mov    esi,eax                    # esi放func(此為printf)的第二個參數，esi = eax 
        lea    rdi,[rip+0xe55]            # rdi放func(此為printf的第一個參數)，此處參數為"%d"，rdi(%d) = [rip+0xe55]的位址
        mov    eax,0x0                    # 設定vector register(?)，eax = 0
        call   1030 <printf@plt>          # call printf
        mov    eax,0x0
        leave  
        ret    
```
* [關於printf前eax=0的問題，和vector register(有看沒懂)](https://stackoverflow.com/questions/6212665/why-is-eax-zeroed-before-a-call-to-printf)




###### 參考資料
* [What does @plt mean here? (StackOverflow)](https://stackoverflow.com/questions/5469274/what-does-plt-mean-here)

---
###### tags: `CTF` `dis_asm`








