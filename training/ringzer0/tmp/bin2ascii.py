# parse bin 
# cipher = "01001001 01100110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01100001 00100000 01100111 01100101 01101110 01110100 01101100 01100101 00100000 01101000 01100001 01100011 01101011 01100101 01110010 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01110111 01100101 01101100 01100011 01101111 01101101 01100101 00100000 01110100 01101111 00100000 01100100 01101111 01110111 01101110 01101100 01101111 01100001 01100100 00100000 01100110 01101001 01101100 01100101 01110011 00101110 00100000 01001001 01100110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01100001 00100000 01100110 01110101 01100011 01101011 01101001 01101110 01100111 00100000 01100010 01101111 01110100 00100000 01110100 01101000 01100001 01110100 00100000 01110011 01100011 01100001 01101110 00100000 01110100 01101000 01100101 00100000 01001001 01101110 01110100 01100101 01110010 01101110 01100101 01110100 00100000 01110101 01110011 01101001 01101110 01100111 00100000 01110011 01110100 01110101 01110000 01101001 01100100 00100000 01101000 01100101 01110101 01110010 01101001 01110011 01110100 01101001 01100011 00100000 01110010 01110101 01101100 01100101 01110011 00100000 01110100 01101000 01100001 01110100 00100000 01110011 01110101 01100011 01101011 01110011 00100000 01110100 01101000 01100101 01101110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01101110 01101111 01110100 00100000 01110111 01100101 01101100 01100011 01101111 01101101 01100101 00101110 00100000 01010011 01101001 01101110 01100011 01100101 01110010 01100101 01101100 01111001 00101100 00100000 01001101 01110010 00101110 01010101 01101110 00110001 01101011 00110000 01100100 00110011 01110010 "
cipher = "01001001 01100110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01100001 00100000 01100111 01100101 01101110 01110100 01101100 01100101 00100000 01101000 01100001 01100011 01101011 01100101 01110010 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01110111 01100101 01101100 01100011 01101111 01101101 01100101 00100000 01110100 01101111 00100000 01100100 01101111 01110111 01101110 01101100 01101111 01100001 01100100 00100000 01100110 01101001 01101100 01100101 01110011 00101110 00100000 01001001 01100110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01100001 00100000 01100110 01110101 01100011 01101011 01101001 01101110 01100111 00100000 01100010 01101111 01110100 00100000 01110100 01101000 01100001 01110100 00100000 01110011 01100011 01100001 01101110 00100000 01110100 01101000 01100101 00100000 01001001 01101110 01110100 01100101 01110010 01101110 01100101 01110100 00100000 01110101 01110011 01101001 01101110 01100111 00100000 01110011 01110100 01110101 01110000 01101001 01100100 00100000 01101000 01100101 01110101 01110010 01101001 01110011 01110100 01101001 01100011 00100000 01110010 01110101 01101100 01100101 01110011 00100000 01110100 01101000 01100001 01110100 00100000 01110011 01110101 01100011 01101011 01110011 00100000 01110100 01101000 01100101 01101110 00100000 01111001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01101110 01101111 01110100 00100000 01110111 01100101 01101100 01100011 01101111 01101101 01100101 00101110 00100000 01010011 01101001 01101110 01100011 01100101 01110010 01100101 01101100 01111001 00101100 00100000 01001101 01110010 00101110 01010101 01101110 00110001 01101011 00110000 01100100 00110011 01110010 "
cipher = cipher.split(' ')

# convert bin to ascii
ans = []
for i in range(0, 9*22):
	ans.append(chr(int(cipher[i],2)))

# print
# for j in range(0, 9):
#		for i in range(0, 22):
for i in range(0, 22):
	for j in range(0, 9):	
		print(ans[i*9+j],end='')
	print('\n')
