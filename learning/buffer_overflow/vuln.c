#include <stdio.h>

void vuln(){
	printf(" Wow! Stack overflow.");
	system("/bin/sh");
}

int main(){
	char buf[0x20];
	setvbuf(stdout, 0, 2, 0);
	printf("Stack overflow is e4sy.\n");
	printf("Input: ");
	read(0, buf, 100);
	return 0;
}
