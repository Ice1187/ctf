[Misc] Yarn
===

## Description

I was told to use the linux strings command on [yarn](https://webshell2017.picoctf.com/static/9adb6ebf01d8755201564dba69bc1a92/yarn), but it doesn't work. Can you help? I lost the flag in the binary somewhere, and would like it back

* HINTS
    * What does the strings command use to determine if something is a string?
    * Is there an option to change the length of what strings considers as valid?

## Soluiton

```bash
Ice11187@Misc$ strings yarn
/lib/ld-linux.so.2
U^TR
libc.so.6
```
沒有看見flag，man一下strings，可能有有用的參數
```bash
Ice1187@Misc$ man strings
...(略)

-min-len
       -n min-len
       --bytes=min-len
           Print sequences of characters that are at least min-len characters long, instead of the default 4.
```
列出strings之後，嘗試尋找flag，因為default為4時沒有列出flag，猜測flag可能被拆成兩三段
```bash
Ice1187@Misc$ strings -1 yarn | grep -n 'fl'
Ice1187@Misc$ strings -1 yarn | grep 'ag'
171:lag  # Bingo~~
229:.note.ABI-tag
Ice1187@Misc$ 
```
約在160~170行處，重組得flag
