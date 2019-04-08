#include <iostream>
#include <cstring>
using namespace std;

int main(){
  string table, cipher;
  printf("table: ");
  cin >> table;
  printf("cipher: ");
  cin >> cipher;
  for(int i = 0; i < table.length(); i++){
    printf("\n");
    for(int j =0; j < cipher.length(); j++){
      char c = cipher[j];
      for(int k=0; k < table.length(); k++)
        if(c == table[k]){
          char r = table[k+i];
	  printf("%c", r);
	  break;
	}
    }
  }    

   return 0;
} 
