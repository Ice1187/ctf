0411 Training Web, dis_asm 筆記9
===
* 教材
    * [Simple Web Security (2017 Bamboofox社課)](https://docs.google.com/presentation/d/1wYlxRj-ixxZG93oNSw7_bQ5R_aWyDiS_ASdvmeF8d9I/edit#slide=id.g27bf3f27d6_0_78)
* 練習網站
    * [XSS game](https://xss-game.appspot.com/)

---

## Web - XSS game

### lever 1 

Search: `<script>alert('XSS')</script>`

### level 2

`<script>`不管用(不知道為啥)，改成用`<button`

Msg board: `<button onclick="alert('XSS')">click me!?</button>` 

### level 3

**Web 真的不是我擅長的領域啊啊啊啊啊QQ**

---

## dis_asm
* 教材
    * [x86 assembly & GDB (2017 Bamboofox社課)](https://drive.google.com/file/d/1HJXtYwrP6PgbhAAzKEBl-vQYRDxhJW3H/view)

### and / or / xor / test dest, src

* 清除或設定記憶體的特定bit(s)
    
    * `and`: 可用於清空特定bit(s)、判斷odd/even
        * `and dl, 11101100b(0xec)`: 與 0 and，可清空1^st^, 2^nd^, 5^th^ bits
        *  `and eax, 1`: 若回傳1，odd；否則為even
    * `or`: 可用於設定特定bit
        *  `or dl, 00100000b(0x20)`: 與 1 or，可設定6^th^
        
    * `xor`: 可用於將記憶體/暫存器歸為0
        * `xor eax, eax`: eax歸為0

    * `test`: 同`add`，但不會改變dest，可確認dest是否為0，或為odd/even
        * `test eax, eax`: 檢驗eax是否為0
        * `test AL, 01H`: 檢驗為odd/even 
                      
### call, leave, ret

* `call` == `push eip`
* `leave` == `mov esp, ebp ; pop ebp` 相對於 `push ebp ; mov ebp, esp`
* `ret` == `pop eip` 相對於 `call (push eip)`

```
main:
...
call <func>    # call == push eip

func:
push ebp
mov ebp, esp
...
leave          # mov esp, ebp ; pop ebp
ret            # pop eip
```

### System Call

* sys call number: `eax`
* 參數順序: `ebx`, `ecx`, `edx`, `esi`, `edi`
* return value: `eax`
* 觸發sys call: `int 0x80`

---

###### tags: `CTF` `Training` `web` `dis_asm`
