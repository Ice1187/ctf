0427 Shellcoding 筆記11
===

* 教材
    * [Linux Shellcoding (0x00SEC)](https://0x00sec.org/t/linux-shellcoding-part-1-0/289)
    * [Introduction to 8086 Assembly Language](https://www.shsu.edu/~csc_tjm/spring2005/cs272/intro_to_asm.html)

---

## Memory Segments 

---`high`---

* Stack segment (For function calls (dynamic)). 
* Heap segment (For dynamicly allocating memory).
* Data segment (assigned Variables).
* Bss segment (no assigned Variables).
& Text segment (Set of instructions (The actual code)).

---`low`---

## Reserving space for variables

### Define
```a
[name] [(might be) lables] [value]

section .data 
numRows    DB 25 
numColumns DB ? 
videoBase  DW 0800h
```
* DB and DW are common directives (define byte) and (define word). The symbols associated with variables are called `labels`.
* Strings may be declared using the DB directive:
`aTOm DB "ABCDEFGHIJKLM"`

### Program Data and Storage
* Pseudo-ops to define data or reserve storage
    * DB - byte(s)
    * DW - word(s)
    * DD - doubleword(s)
    * DQ - quadword(s)
    * DT - tenbyte(s)

### Defining Data
* Numeric data values
	* 100 - decimal
	* 100b - binary
	* 100h - hexadecimal
	* '100' - ASCII
	* "100" - ASCII
* Use the appropriate `DEFINE` directive (byte, word, etc.)
* A list of values may be used - the following creates 4 consecutive words: `DW 40Ch,10b,-13,0`

* A `?` represents an uninitialized storage location: 
`DB 255,?,-128,'X'`

## syscall into kernel mode

* `syscall` is default way of entering kernel mode on x86-64. This instruction is not available in 32 bit modes of operation on Intel processors.
* `sysenter` is an instruction most frequently used to invoke system calls in 32 bit modes of operation. It is similar to syscall, a bit more difficult to use though, but that is kernel's concern.
* `int 0x80` is a legacy way to invoke a system call and should be avoided.

> So, ==stop using `int 0x80`==. Use `syscall` in x86_64 and `sysenter` in x86

* 參考
    * [What is better? int-0x80 or syscall](https://stackoverflow.com/questions/12806584/what-is-better-int-0x80-or-syscall)
## A simple assembly program (cp from 教材)

* This sample is based on x86, but it somehow works well on my x86-64 Kali. Maybe `nasm` & `ld` have the ability to cover this misusing.

```a
section .data
  msg db '/bin/sh', 0 ; db stands for 【define byte】, msg will now be a string pointer.
 
section .text
  global _start   ; Needed for compiler, comparable to int main()
 
_start:
  mov eax, 11     ; eax = 11, think of it like this mov [destination], [source], 11 is execve
  mov ebx, msg    ; Load the string pointer into ebx
  mov ecx, 0      ; no arguments in exc
  int 0x80        ; syscall
 
  mov eax, 1      ; exit syscall
  mov ebx, 0      ; no errors
  syscall
  ```

----
  
###### tags: `CTF` `Learning` `Shellcode`
