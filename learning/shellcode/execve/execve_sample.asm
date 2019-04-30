section .data
msg db '/bin/sh'

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
