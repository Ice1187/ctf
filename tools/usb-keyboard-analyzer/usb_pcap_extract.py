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

"""
usb_codes = {  # upper
    0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
    0x0A:"gG", 0x0B:"hH", 0x0C:"iI", 0x0D:"jJ", 0x0E:"kK", 0x0F:"lL",
    0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
    0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1A:"wW", 0x1B:"xX",
    0x1C:"yY", 0x1D:"zZ", 0x1E:"1!", 0x1F:"2@", 0x20:"3#", 0x21:"4$",
    0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
    0x2C:"  ", 0x2D:"-_", 0x2E:"=+", 0x2F:"[{", 0x30:"]}",  0x32:"#~",
    0x33:";:", 0x34:"'\"",  0x36:",<",  0x37:".>", 0x4f:">", 0x50:"<"
}
"""

usb_codes = {  # lower
    0x04:"aA", 0x05:"bB", 0x06:"cC", 0x07:"dD", 0x08:"eE", 0x09:"fF",
    0x0a:"gG", 0x0b:"hH", 0x0c:"iI", 0x0d:"jJ", 0x0e:"kK", 0x0f:"lL",
    0x10:"mM", 0x11:"nN", 0x12:"oO", 0x13:"pP", 0x14:"qQ", 0x15:"rR",
    0x16:"sS", 0x17:"tT", 0x18:"uU", 0x19:"vV", 0x1a:"wW", 0x1b:"xX",
    0x1c:"yY", 0x1d:"zZ", 0x1e:"1!", 0x1f:"2@", 0x20:"3#", 0x21:"4$",
    0x22:"5%", 0x23:"6^", 0x24:"7&", 0x25:"8*", 0x26:"9(", 0x27:"0)",
    0x2c:"  ", 0x2d:"-_", 0x2e:"=+", 0x2f:"[{", 0x30:"]}",  0x32:"#~",
    0x33:";:", 0x34:"'\"",  0x36:",<",  0x37:".>", 0x38:"/?", 0x4f:">", 
    0x50:"<"
}
# output lines
lines = ["","","","",""]

count = 1
pos = 0 
file = sys.argv[1]
for x in open(file,"r").readlines():
    code = int(x[6:8],16)  # get the key typed (in 3rd block)

    # didn't type any button
    if code == 0:
        print 'count:' + str(count)
        count += 1 
        continue
    elif code == 0x2a:
        lines[pos] = lines[pos][0:len(lines[pos])-1]
        continue
    # down arrow / move down or newline
    elif code == 0x51 or code == 0x28:
        pos += 1
        continue
    # up arrow - move up
    elif code == 0x52:
        pos -= 1
        continue
    # not complete, need more operate!!!
    elif int(x[0:2],16) == 1 or int(x[0:2]) == 0x10:
        continue
    # select the character based on the L/R Shift key
    elif int(x[0:2],16) == 2 or int(x[0:2],16) == 0x20:
        lines[pos] += usb_codes[code][1]  # Shift + code
    else:
        print 'count:' + str(count)
        count += 1 
        lines[pos] += usb_codes[code][0]  # code
        print usb_codes[code][0]


for x in lines:
   print x

