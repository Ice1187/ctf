#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>


char buf[80];

int main (int argc, char **argv)
{

  unsigned int filler0 = 0x70115011;
  unsigned int filler1 = 0x70077011;
  unsigned int key     = 0x00000000;
  unsigned int filler2 = 0x50115075;
  unsigned int filler3 = 0x70117117;
  unsigned int filler4 = 0x70075110;
  unsigned int filler5 = 0x71171075;

  unsigned int red = read(STDIN_FILENO,buf,80);
  printf("%d\n", red);
	buf[red] = '\x00';
	printf(buf);
}
