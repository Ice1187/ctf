0406 Learning dis_asm 筆記6
===

* 教材
    * [Reverse 0x02(2018 Bamboofox社課)](https://docs.google.com/presentation/d/1DzZOlyOr_aUSL9volIrAuNhXgGEr7pkqj-sZSQeEBmg/edit#slide=id.g46e515a023_0_43)

---

0. 安裝peda, Pwngdb
    * [peda](https://github.com/longld/peda)
    * [Pwngdb](https://github.com/scwuaptx/Pwngdb)
```
$ git clone https://github.com/longld/peda.git ~/peda
$ echo "source ~/peda/peda.py" >> ~/.gdbinit
$ git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb
$ cp ~/Pwngdb/.gdbinit ~/

# 路徑按自身需求修改，記得.gdbinit裡也要改
```

1. GDB指令

指令|說明|例子
-|-|-
break / b|設定`Breakpoint`斷點|break <func> / <*address>
delete [Num] / d| 刪除斷點(預設為全部，可依據Num刪除) | delete <br> delete 3
run|執行程式
step / s|執行下一個指令(會追進function)
next / n|執行下一個指令(不追進function)
continue / c|繼續執行
finish|執行至結束
jump|跳轉| jump <*adress>
print|印出暫存器的值| print <$register>
x|印出記憶體的值|x <memory address>
set|改變暫存器的值|set <$register>=<value>
set|改變記憶體的值|set {size}<memory address>=<value>
info breakpoints| 查看斷點

* Breakpoint
    * 沒加`*`視為func_name，加`*`視為address
```b
$ break <function>        # use func_name
$ break main
Breakpoint 1 at 0x1179

$ break <*address>         # use *address
$ break <*0x011f5>
Breakpoint 2 at 0x11f5

$ break 0x011f5           # 沒加*，視為func_name
Function "0x011f5" not defined.
```

* run
```gdb
[----------------------------------registers-----------------------------------]
RAX: 0x555555555175 (<main>:	push   rbp)
RBX: 0x0 
RCX: 0xa0 
RDX: 0x7fffffffe298 --> 0x7fffffffe584 ("SHELL=/bin/bash")
RSI: 0x7fffffffe288 --> 0x7fffffffe563 ("/root/ctf/learning/dis_asm/basis")
RDI: 0x1 
RBP: 0x7fffffffe1a0 --> 0x5555555552a0 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffe1a0 --> 0x5555555552a0 (<__libc_csu_init>:	push   r15)
RIP: 0x555555555179 (<main+4>:	sub    rsp,0x10)
R8 : 0x7ffff7c8ad80 --> 0x0 
R9 : 0x0 
R10: 0xfffffffffffff51b 
R11: 0x7ffff7b082d0 (<__cxa_atexit>:	lea    rcx,[rip+0x181441]        # 0x7ffff7c89718)
R12: 0x555555555070 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe280 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555555174 <func(int, int)+31>:	ret    
   0x555555555175 <main>:	push   rbp
   0x555555555176 <main+1>:	mov    rbp,rsp
=> 0x555555555179 <main+4>:	sub    rsp,0x10
   0x55555555517d <main+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x555555555184 <main+15>:	add    DWORD PTR [rbp-0x4],0x1
   0x555555555188 <main+19>:	mov    DWORD PTR [rbp-0xc],0x1
   0x55555555518f <main+26>:	mov    eax,DWORD PTR [rbp-0x4]
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe1a0 --> 0x5555555552a0 (<__libc_csu_init>:	push   r15)
0008| 0x7fffffffe1a8 --> 0x7ffff7af209b (<__libc_start_main+235>:	mov    edi,eax)
0016| 0x7fffffffe1b0 --> 0xffffffffffffff90 
0024| 0x7fffffffe1b8 --> 0x7fffffffe288 --> 0x7fffffffe563 ("/root/ctf/learning/dis_asm/basis")
0032| 0x7fffffffe1c0 --> 0x1f7ee79e0 
0040| 0x7fffffffe1c8 --> 0x555555555175 (<main>:	push   rbp)
0048| 0x7fffffffe1d0 --> 0x0 
0056| 0x7fffffffe1d8 --> 0x510b4532685db929 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0000555555555179 in main ()
```

其中出現`<address> --> <value>`的部分，前面為address；後面為value。
```
$ x 0x7fffffffe1a0
0x7fffffffe1a0:	0x00005555555552a0
$ print $eax
$1 = 0x55555175
```
EFLAGS 亮起紅色粗體者表示<font  color=red>**true**</font>，綠色表示<font color=green>false</font>

2. 練習
    * Bamboofox: [add](https://bamboofox.cs.nctu.edu.tw/courses/6/challenges/116), [guess](https://bamboofox.cs.nctu.edu.tw/courses/6/challenges/117)
    * picoCTF 2018: [be-quick-or-be-dead-1](https://2018shell.picoctf.com/static/1a796b0425170aa031a6ad476c64bf75/be-quick-or-be-dead-1), 

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

###### tags: `CTF` `Learning` `dis_asm`
