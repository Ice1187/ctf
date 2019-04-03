#include<iostream>
using namespace std;

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
  return 0;
}
