190519 RCTF 2019 - printer (misc)
===

## Description

> The supermarket bought a new printer last night. I hacked into their computer and captured the USB traffic on it. Could you help me steal the secret?
> 
> Flag format: `flag{0-9a-z_}` (Convert uppercase to lowercase)
>
> [File](https://adworld.xctf.org.cn/media/uploads/task/c3f62efbf7a94e2c8d8e0b351de08194.zip)

## Solve

- I use `wireshark` to analyze the pcap.

0. In `Control response data` of packet[475], there was some information.

```
2MFG:4BARCODE;CMD:TSPL2;MDL:3B-363B;CLS:PRINTER;
```

After googling, it came out that the printer might be Barcode Printer, and the info was TSPL/TSPL2 commands, a programming language using by printers. [TSPL/TSLP2 programming manual (en)](https://www.mediaform.de/fileadmin/support/handbuecher/Armilla/Handbuecher/TSC_TSPL_TSPL2_Programming.pdf) / [(cn)](https://github.com/lokingwei/tspl-printer-php/blob/master/document/%E6%9D%A1%E7%A0%81%E6%9C%BA%E4%B8%AD%E6%96%87%E7%BC%96%E7%A8%8B%E6%89%8B%E5%86%8C.pdf)

1. In `Leftover Capture Data` of packet[673, 674], it showed the info about printing. It is able to extract the data in `wireshark by simply `select the packet -> right click the layer(ex: Leftover Capture Data) -> copy -> Value`
```
SIZE 47.5 mm, 80.1 mm
GAP 3 mm, 0 mm
DIRECTION 0,0
REFERENCE 0,0
OFFSET 0 mm
SET PEEL OFF
SET CUTTER OFF
SET PARTIAL_CUTTER OFF
SET TEAR ON
CLS
BITMAP 138,75,26,48,1,
...    # the data of BITMAP
BITMAP 130,579,29,32,1,
...    # the data of BITMAP
BAR 348, 439, 2, 96
BAR 292, 535, 56, 2
BAR 300, 495, 48, 2
BAR 260, 447, 2, 88
BAR 204, 447, 56, 2
BAR 176, 447, 2, 96
BAR 116, 455, 2, 82
BAR 120, 479, 56, 2
BAR 44, 535, 48, 2
BAR 92, 455, 2, 80
BAR 20, 455, 72, 2
BAR 21, 455, 2, 40
BAR 21, 495, 24, 2
BAR 45, 479, 2, 16
BAR 36, 479, 16, 2
BAR 284, 391, 40, 2
BAR 324, 343, 2, 48
BAR 324, 287, 2, 32
BAR 276, 287, 48, 2
BAR 52, 311, 48, 2
BAR 284, 239, 48, 2
BAR 308, 183, 2, 56
BAR 148, 239, 48, 2
BAR 196, 191, 2, 48
BAR 148, 191, 48, 2
BAR 68, 191, 48, 2
BAR 76, 151, 40, 2
BAR 76, 119, 2, 32
BAR 76, 55, 2, 32
BAR 76, 55, 48, 2
BAR 112, 535, 64, 2
BAR 320, 343, 16, 2
BAR 320, 319, 16, 2
BAR 336, 319, 2, 24
BAR 56, 120, 24, 2
BAR 56, 87, 24, 2
BAR 56, 88, 2, 32
BAR 224, 247, 32, 2
BAR 256, 215, 2, 32
BAR 224, 215, 32, 2
BAR 224, 184, 2, 32
BAR 224, 191, 32, 2
BAR 272, 311, 2, 56
BAR 216, 367, 56, 2
BAR 216, 319, 2, 48
BAR 240, 318, 2, 49
BAR 184, 351, 2, 16
BAR 168, 351, 16, 2
BAR 168, 311, 2, 40
BAR 152, 351, 16, 2
BAR 152, 351, 2, 16
PRINT 1,1
```

2. `BITMAP` can be used to draw bitmap images, and `BAR` to bar. The definitions of these commands are in the manual mentioned above. So, I use `wireshark` to extract the data and write `draw.py` to draw the graph. Thank tangerine1202 for helping me write this script. Without him, I definitely can't make it.

3. The graph is the flag. Get flag.

## Files

- `c3f62efbf7a94e2c8d8e0b351de08194.zip`: The file gotten from RCTF, the zip of `Printer.pcapng`
- `Printer.pcapng`: The file of this challenge, unzip from `c3f...zip`
- `leftover`: The data of first `BITMAP`
- `leftover.bin`: `leftover` in binary
- `bar`: The parameters of the `BAR` commands
- `draw.py`: Draw the graph
- `flag.png`: The flag

---

###### tag: `CTF` `Training` `RCTF` `writeup` `misc`
