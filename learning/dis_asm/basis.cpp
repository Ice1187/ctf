#include<iostream>
using namespace std;

int glob = 0;

int func(int a, int x = 0){
  int f, g, h;
  f = 0;
  g = 1;
  h = 2;
  if(a > x)
    return 1;
  else
    return 0;
}

int main(){
  int a;
  a = 0;
  a++;
  int b = 1;
  b = a + b;
  printf("%d\n", b);

  for(int i=0; i<5; i++)
    a = a + i;
  printf("%d\n", a);

  a = 3;
  b = 9;
  b = a * b;
  a = b / a;

  a = 5;
  b = -3;
  a = func(a);
  b = func(b, 3);

  return 0;
}
