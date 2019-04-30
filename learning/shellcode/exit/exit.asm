section .text
  global _start

_start:
  xor eax, eax
  xor ebx, ebx
  mov al, 60
  syscall
