190523 SecurityFestCTF 2019 - baby1 (pwn)
===

## Description

> When Swordfish came out, these were considered some state of the art techniques. Let's see if you have what it takes.
> 
> Service: `nc baby-01.pwn.beer 10001`
> File: [baby1.tar.gz](https://s3-eu-west-1.amazonaws.com/dl.securityfest.2019/cc0dcec1dd6b34bc02e08bc5e52a854d2741b55ceec40983080c5f918c9b5f11/baby1.tar.gz)

## My first ROP

There was a function called `win`, which would call `system`. According to `win`, we should set `rdi` to "/bin/sh", return to `win`, and get shell.

```b
Ice1187@kali$ readelf -s ./baby1
...
    58: 0000000000400730   101 FUNC    GLOBAL DEFAULT   13 __libc_csu_init
    **59: 0000000000400698    27 FUNC    GLOBAL DEFAULT   13 win**
    60: 0000000000602030     0 NOTYPE  GLOBAL DEFAULT   23 _end

gdb-peda$ disas win
Dump of assembler code for function win:
   0x0000000000400698 <+0>:	push   rbp
   0x0000000000400699 <+1>:	mov    rbp,rsp
   0x000000000040069c <+4>:	sub    rsp,0x10
   0x00000000004006a0 <+8>:	**mov    QWORD PTR [rbp-0x8],rdi**
   0x00000000004006a4 <+12>:	**mov    rax,QWORD PTR [rbp-0x8]**
   0x00000000004006a8 <+16>:	**mov    rdi,rax**
   0x00000000004006ab <+19>:	**call   0x400560 <system@plt>**
   0x00000000004006b0 <+24>:	nop
   0x00000000004006b1 <+25>:	leave  
   0x00000000004006b2 <+26>:	ret    
End of assembler dump. 
...

Since ASLR was on, we could only use the gadgets in `./baby1`. 
I found "/bin/sh" in `./baby1` actually, but it was somehow unusable (Don't trust `find` when using gdb!!!). I then turned to use `gets` to input the command.

Returned to `win`, got shell, and got my first flag of ROP.

> *Thanked lys0829 for helping me debug the payload, he helped me a lot.* 
