After trying, I found that when gave it more than 39 chars, it got 'Seg fault'.

Found there was a strange function called 'reply' and it contained the flag. 
```shell=bash
Ice1187$ r2 -d mail
> aaa
> afl
....
0x00400796    1 145          sym.reply
...
> s sym.reply
> pdf
...
|           0x004007a8      bf5b094000     mov edi, str.Here_is_your_reply: ; 0x40095b ; "Here is your reply: "
|           0x004007ad      b800000000     mov eax, 0
|           0x004007b2      e879feffff     call sym.imp.printf         ; int printf(const char *format)
|           0x004007b7      be70094000     mov esi, 0x400970
|           0x004007bc      bf72094000     mov edi, str.flag.txt       ; 0x400972 ; "flag.txt"
...
```

Write some payload, try to get the flag. [See payload.py]
