190520 RCTF 2019 - babyre1 (reverse)
===

## Description

> It's just a baby...
> 
> There are multiple answers, please ensure MD5(rctf{your answer}) == 5f8243a662cf71bf31d2b2602638dc1d
> 
> wrap your answer in rctf{}
> 
> [File](https://adworld.xctf.org.cn/media/uploads/task/8049616e02cc44b2a2b1d2ced35c8bfa.zip)

## Got as far as I could

- I used `gdb` attaching to the process to debug, and `radare2` to see the assmbly code.
- All the functions' names were based on what `radare2` showed to me.

0. Playing around it, I discovered the input must be 16 characters.

1. After analyzing, `sub.malloc_c00` functions liked this.
```py
in_str = input()    # in_str = AAAAAAAABBBBBBBB
sub.malloc_c00 (&in_str, 0x10, a piece of memory):
  for i in range(0, 8):
    fcn.00000be0(in_str[2*i])    # `fcn.00000be0` converted in_str to lowercase automatically , so nice :)
    fcn.00000be0(in_str[2*i+1])

  if (in_str is in 'a'~'f'):
    mem* = malloc(8 byte)
    mem* = 0xaaaaaaaabbbbbbbb
    else:
    print 'wrong'
    exit()
```

2. `sub.malloc_1180`
```py
sub.malloc_1180 (mem, 0x8, 0xc6f1d3d7, 0x10, rsp+0x4):
  mem2* = malloc(9 byte)
  memcpy(mem2*, mem*, 0x8)
  fcn.00000ce0(mem, -2, 0xc6f1d3d7e0c7e0c7)    # I got stuck here.
  ...
...

```

3. `fcn.00000ce0` seemed to be used to do some caculations (or crypto ?), and I was unable to pass it. The caculation looked like this.
```
# in_str = 0xaaaaaaaabbbbbbbb
a = 0xaaaaaaaa

b = (a<<4)^(a>>3) + (a<<2) ^ (a>>5)
c = (a^0xc6ef3729) + (a^0xc6f1d3d7)
d = b ^ c
e = (a<<2) ^ (a>>5) - d
key_h = e    # The higher 8 bits) of the key

f = (e>>3)^(e<<4) + (e*4) ^ (e>>5)
i = (e^0xc6ef3720) + (e^0xe0c7e0c7)
j = i ^ f
k = 0xc6ef3720 - j
key_l = k    # The lower 8 bits of the key

```

4. Unable to solve, so sad.

---

###### tags: `CTF` `Training` `RCTF` `writeup` `reverse`
