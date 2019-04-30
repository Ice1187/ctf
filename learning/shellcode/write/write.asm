section .data
  msg db '/bin/sh' ; db stands for defind byte, so now msg is a pointer pointing to the string '/bin/sh'.

section .text 
  global _start    ; Just like that in C you would need a int main(), in asm it is _start

_start:           
  mov eax, 59      ; In x64, syscall 59 is execve
  mov edi, msg     ; Load the string pointer into edi
  mov esi, 0       ; No argumests
  mov edx, 0       ; No envp
  int 0x80

  mov eax, 1       ; In x64, syscall 1 is write
  mov edi, 1       ; Set fd to standard output
  mov esi, msg     ; Set output string
  mov edx, 7       ; Set the size of output string
  int 0x80

  mov eax, 60
  mov edi, 0
  int 0x80
