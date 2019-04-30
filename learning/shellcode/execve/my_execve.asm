section .text
  global _start
  msg db '/bin/sh'

_start:
  xor rax, rax
  mov rdi, msg
  mov rsi, rax
  mov rdx, rax 
  mov al, 0x3b
  syscall
