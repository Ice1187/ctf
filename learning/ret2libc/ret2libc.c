#include<stdio.h> 
#include<string.h> 

//Ice1187$ gcc ./ret2win.c -o ret2win -fno-stack-protector 

int main(int argc, char *argv[]) 
{ 
  char buf[100]; 
  gets(buf); 
  printf("Input was: %s\n",buf); 
  return 0; 
}


