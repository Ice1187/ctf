section .text
  global _start

_start:
  xor eax, eax
  push 0x0
  push 0x68732f2f
  push 0x6e69622f
  mov edi, esp
  mov esi, 0
  mov edx, 0
  syscall


