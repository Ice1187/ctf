section .text
  global _start

_start:
  
  jmp short ender
  
  starter:
    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx

    mov edi, 1
    pop rsi    ; the size of stack is 64-bit, so the reg must be 64-bit, too.
    mov edx, 12
    mov al, 1
    syscall
  
    xor eax, eax
    xor ebx, ebx
    mov al, 60
    syscall

  ender:
    call starter
    db "Hello world!"
