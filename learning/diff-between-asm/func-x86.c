#include<stdio.h>

#define nop __asm__("nop");

void func1(){
  nop;
}

int func2(){
  return 1;
}

int func3(int p){
  return p+1;
}

int func4(int p, int p2){
  return p+p2;
}

int func5(int p, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9, int p10){
  return p+p2+p3+p4+p5+p6+p7+p8+p9+p10;
}

char func6(char *p){
  return *p;
}

int main(){
  func1();
  nop;
  int a = func2();
  nop;
  int b = func3(1);
  nop;
  int c = func4(1, 2);
  nop;
  int d = func5(1, 2, 3 ,4 ,5 ,6, 7, 8, 9, 10);
  nop;
  char e = func6("AAA");
  nop;

  return 0;
}
