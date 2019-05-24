#include<stdio.h> 
#include<string.h> 

//Ice1187$ gcc ./ret2win.c -o ret2win -fno-stack-protector 
//
// In gdb, chechsec shows that PIE is on, but it's still able to return to win(code segment?) ?

void win(){
  printf("win is here\n");
  system("/bin/sh");
}

int main(int argc, char *argv[]) 
{ 
  char buf[100]; 
  gets(buf); 
  printf("Input was: %s\n",buf); 
  return 0; 
}


