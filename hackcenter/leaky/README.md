HackCenter: https://hackcenter.com/

#Description:
	Leak the key from memory. Source is available at leaky.c, and the binary's running on enigma2017.hackcenter.com:14410.
	
	* HINTS
		* man 3 printf
		* What does printf do if it receives a format specifier like %x, but has no more args?
		* Where is the key allocated in memory? (heap, stack, text, etc)
		* The solution is *8* hex characters	
