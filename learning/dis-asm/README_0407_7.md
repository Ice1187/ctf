0407 Learning dis_asm 筆記7
===
* 教材
    * [Pwn 1 (2018 Bamboofox社課)](https://drive.google.com/file/d/16eP_DqOXdh-TljABnIHWsCByL5a0u0zF/view)

* 參考
    * [ELF格式文件符号表全解析及readelf命令使用方法](https://blog.csdn.net/freeking101/article/details/78270487)
    * [ELF格式文件详细分析](https://blog.csdn.net/xuehuafeiwu123/article/details/72963229)
    * [目的檔格式 (ELF)](http://ccckmit.wikidot.com/lk:elf)

---

## Stack

<iframe src="https://drive.google.com/file/d/16eP_DqOXdh-TljABnIHWsCByL5a0u0zF/preview" width="640" height="480"></iframe>

<br>
<br>
<br>

0. `call <func>`時，會自動push原先下一個指令的記憶體位址
```b
[-------------------------------------code-------------------------------------]
   0x555555555227 <main+157>:	mov    edi,eax
=> 0x555555555229 <main+159>:	call   0x555555555155 <func(int, int)>
   0x55555555522e <main+164>:	mov    DWORD PTR [rbp-0x4],eax
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0     # rsp
0008| 0x7fffffffe1b8 --> 0x500000005 
0016| 0x7fffffffe1c0 --> 0x5555555552b0         # rbp 
```
`gdb: step`
```b
[-------------------------------------code-------------------------------------]
=> 0x555555555155 <func(int, int)>:	push   rbp
   0x555555555156 <func(int, int)+1>:	mov    rbp,rsp
   0x555555555159 <func(int, int)+4>:	mov    DWORD PTR [rbp-0x14],edi
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)    # rsp，原先的下一行指令位址被psuh到stack
0008| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0 
0016| 0x7fffffffe1b8 --> 0x500000005 
0024| 0x7fffffffe1c0 --> 0x5555555552b0     # rbp
```

1. `push rbp`將原先的rbp推進stack
```b
[-------------------------------------code-------------------------------------]

   0x555555555155 <func(int, int)>:	push   rbp
=> 0x555555555156 <func(int, int)+1>:	mov    rbp,rsp
   0x555555555159 <func(int, int)+4>:	mov    DWORD PTR [rbp-0x14],edi
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a0 --> 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # rsp，原本的rbp被push進stack(此時rbp還沒改變)
0008| 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)
0016| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0 
0024| 0x7fffffffe1b8 --> 0x500000005 
0032| 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # rbp
```

2. 將rbp更新到stack頂端(rsp處)
```b
[-------------------------------------code-------------------------------------]
   0x555555555156 <func(int, int)+1>:	mov    rbp,rsp
=> 0x555555555159 <func(int, int)+4>:	mov    DWORD PTR [rbp-0x14],edi
   0x55555555515c <func(int, int)+7>:	mov    DWORD PTR [rbp-0x18],esi
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a0 --> 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # rsp，也是現在的rbp
0008| 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)    # call <func> 之前的下一行指令，也是此func走完ret之後的下一行指令
0016| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0 
0024| 0x7fffffffe1b8 --> 0x500000005 
0032| 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # 原本的rbp(已改變)
```


3. 放入傳入的參數和區域參數到stack
```b
[-------------------------------------code-------------------------------------]
   0x555555555159 <func(int, int)+4>:   mov    DWORD PTR [rbp-0x14],edi
   0x55555555515c <func(int, int)+7>:   mov    DWORD PTR [rbp-0x18],esi
   0x55555555515f <func(int, int)+10>:  mov    DWORD PTR [rbp-0x4],0x0
   0x555555555166 <func(int, int)+17>:  mov    DWORD PTR [rbp-0x8],0x1
   0x55555555516d <func(int, int)+24>:  mov    DWORD PTR [rbp-0xc],0x2
```
stack|value|explame
-|-|-
rbp-0x18|esi |傳入的第二個參數
rbp-0x14|edi |傳入的第一個參數
rbp-0xc|2 |第三個宣告的區域變數
rbp-0x8|1 |第二個宣告的區域變數
rbp-0x4|0 |第一個宣告的區域變數 (照順序放入)

4. `pop`將`rbp`復原為call func前的`rbp`
```b
[-------------------------------------code-------------------------------------]
   0x555555555183 <func(int, int)+46>:	mov    eax,0x0   
=> 0x555555555188 <func(int, int)+51>:	pop    rbp
   0x555555555189 <func(int, int)+52>:	ret    

[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a0 --> 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # 1.時psuh的「進入func前，原先的rbp」
0008| 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)
```
`gdb: step`
```b
[----------------------------------registers-----------------------------------]
RBP: 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)    # rbp復原為call func前的rbp
RSP: 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)
RIP: 0x555555555189 (<func(int, int)+52>:	ret)
[-------------------------------------code-------------------------------------]
   0x555555555188 <func(int, int)+51>:	pop    rbp
=> 0x555555555189 <func(int, int)+52>:	ret    
   0x55555555518a <main>:	push   rbp
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a8 --> 0x55555555522e (<main+164>:	mov    DWORD PTR [rbp-0x4],eax)
0008| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0 
0016| 0x7fffffffe1b8 --> 0x500000005 
```

5. `ret`使`位於stack top`的`return address`放入`rip`，然後`pop`掉
```b
[----------------------------------registers-----------------------------------]
RBP: 0x7fffffffe1c0 --> 0x5555555552b0 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe1b0 --> 0xfffffffdffffe2a0       # rsp pop掉一個
RIP: 0x55555555522e (<main+164>:	mov        # rip =  return address
[-------------------------------------code-------------------------------------]
   0x555555555229 <main+159>:	call   0x555555555155 <func(int, int)>
=> 0x55555555522e <main+164>:	mov    DWORD PTR [rbp-0x4],eax
   0x555555555231 <main+167>:	mov    eax,DWORD PTR [rbp-0xc]
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1b0 --> 0xfffffffdffffe2a0 
0008| 0x7fffffffe1b8 --> 0x500000005 
0016| 0x7fffffffe1c0 --> 0x5555555552b0 
```

---

###### tags: `CTF` `Learning` `dis_asm`




