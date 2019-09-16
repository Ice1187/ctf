#include<stdio.h>

void main(){
  int a = 1234;
  __asm__("nop");
  unsigned a2 = 1234;
  __asm__("nop");
  int a3 = -1234;
  __asm__("nop");
  int a4[10] = {1, 22, 333, 444};
  __asm__("nop");
  int a5 = a4[3];
  __asm__("nop");
  const int a6 = 1234;
  __asm__("nop");
  int a7 = 'A';
  __asm__("nop");

  short c = 1234;
  __asm__("nop");
  unsigned c2 = 1234;
  __asm__("nop");
  short c3 = -1234;
  __asm__("nop");

  long long d = 1234;
  __asm__("nop");
  unsigned long long d2 = 1234;
  __asm__("nop");
  long long d3 = -1234;
  __asm__("nop");
  
  float e = 0.1234;
  __asm__("nop");
  float e3 = -0.1234;
  __asm__("nop");
  float e4 = 0;
  __asm__("nop");
  float e5 = 1234;
  __asm__("nop");
  float e6 = 'A';
  
  double f = 0.1234;
  __asm__("nop");
  double f3 = -0.1234;
  __asm__("nop");
  double f4 = 0;
  __asm__("nop");
  double f5 = 1234;
 
  char b = 'A';
  __asm__("nop");
  unsigned b2 = 'A';
  __asm__("nop");
  char b3 = 65;
  __asm__("nop");
  char b4 = -65;
  __asm__("nop");
  const char b5 = 'A';
  __asm__("nop");
  char *b6 = "ABCD";
  __asm__("nop");
  const char *b7 = "EFGH";
  __asm__("nop");

}

