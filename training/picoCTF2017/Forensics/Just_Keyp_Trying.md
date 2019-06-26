[Forensics] Just Keyp Trying
===

## Description

Here's an interesting capture of some data. But what exactly is this data? Take a look: [data.pcap](https://webshell2017.picoctf.com/static/d24295d46a581824ce7fc26026f43cb4/data.pcap)

* HINTS
    * Find out what kind of packets these are. What does the info column say in Wireshark/Cloudshark?
    * What changes between packets? What does that data look like?

    * Maybe take a look at http://www.usb.org/developers/hidpage/Hut1_12v2.pdf?

## Solution 

![](https://i.imgur.com/xlO1hY9.png)

1. USB傳送的封包，觀察之後發現重點在於 Leftover Capture Data 裡的資訊。

2. 透過 "URB_INTERRUPT in" 跟 Leftover 的資料格式可以察覺是keyboard的訊息^[2]^。

3. 可以用 tshark 單獨取出 Leftover 的資料
    * tshark [**-r** <infile>] [ **-T** <output format/fields> ] [ **-e** [<fields>]^[3]^ ]

  
```bash
ice1187$ tshark -r data.pcap -T fields -e usb.capdata
00:00:09:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:0f:00:00:00:00:00
00:00:00:00:00:00:00:00
```
4. 寫 script 取出資訊
```python=
import sys

# Reference
    # https://bitvijays.github.io/LFC-Forensics.html (CTF Series : Forensics)
    # http://www.usb.org/developers/hidpage/Hut1_12v2.pdf (USB documentation)

# leftover capture data = '00:00:09:00:00:00:00:00' [keyboard]
    # Byte 0: Keyboard modifier bits (SHIFT, ALT, CTRL etc)
        # KEY_MOD_LCTRL  0x01 
        # KEY_MOD_LSHIFT 0x02
        # KEY_MOD_LALT   0x04
        # KEY_MOD_LMETA  0x08
        # KEY_MOD_RCTRL  0x10
        # KEY_MOD_RSHIFT 0x20
        # KEY_MOD_RALT   0x40
        # KEY_MOD_RMETA  0x80
    # Byte 1: reserved
    # Byte 2-7: Up to six keyboard usage indexes representing the keys that are currently "pressed". 
    # For byte 2-7, order is not important, a key is either pressed (present in the buffer) or not pressed.

usb_codes = {
    0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
    0x0A:"gG", 0x0B:"hH", 0x0C:"iI", 0x0D:"jJ", 0x0E:"kK", 0x0F:"lL",
    0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
    0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1A:"wW", 0x1B:"xX",
    0x1C:"yY", 0x1D:"zZ", 0x1E:"1!", 0x1F:"2@", 0x20:"3#", 0x21:"4$",
    0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
    0x2C:"  ", 0x2D:"-_", 0x2E:"=+", 0x2F:"[{", 0x30:"]}",  0x32:"#~",
    0x33:";:", 0x34:"'\"",  0x36:",<",  0x37:".>", 0x4f:">", 0x50:"<"
}

# output lines
lines = ["","","","",""]

pos = 0 
file = sys.argv[1]
for x in open(file,"r").readlines():
    code = int(x[6:8],16)  # get the key typed (in 3rd block)
    # print code

    # didn't type any button
    if code == 0:          
        continue
    # down arrow / move down or newline
    if code == 0x51 or code == 0x28:
        pos += 1
        continue
    # up arrow - move up
    if code == 0x52:
        pos -= 1
        continue
    # not complete, need more operate!!!
    if int(x[0:2],16) == 1 or int(x[0:2]) == 0x10:
        continue
    # select the character based on the L/R Shift key
    if int(x[0:2],16) == 2 or int(x[0:2],16) == 0x20:
        lines[pos] += usb_codes[code][1]  # Shift + code
    else:
        lines[pos] += usb_codes[code][0]  # code


for x in lines:
   print x

```

## Reference

1. [从CTF中学USB流量捕获与解析](https://www.anquanke.com/post/id/85218)

2. [CTF Series : Forensics](https://bitvijays.github.io/LFC-Forensics.html#ctf-series-forensics "Permalink to this headline")

3. [Display Filter Reference](https://www.wireshark.org/docs/dfref/)

