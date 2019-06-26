[Crypto] Hash101
===

## Description

Prove your knowledge of hashes and claim a flag as your prize! Connect to the service at shell2017.picoctf.com:63004
UPDATED 16:12 EST 1 Apr.

* HINTS

    * All concepts required to complete this challenge, including simple modular math, are quickly found by googling :)

## Solution
```
ice1187:~$ nc shell2017.picoctf.com 63004
```
nc過去，本題皆可用python解，也可上網查工具。

**第一題**
```
-------- LEVEL 1: Text = just 1's and 0's --------
All text can be represented by numbers. To see how different letters translate to numbers, go to http://www.asciitable.com/

TO UNLOCK NEXT LEVEL, give me the ASCII representation of 011100000111011101101110011010010110111001100111
```
```python
>>> import binascii
>>> s = '0111000001101100011000010110100101100100'
>>> d = int(s,2)
482854660452
>>> h = hex(d)
>>> h
'0x706c616964'
>>> '706c616964'.decode("hex")
'plaid'
```
**第二題**
```
------ LEVEL 2: Numbers can be base ANYTHING -----
Numbers can be represented many ways. A popular way to represent computer data is in base 16 or 'hex' since it lines up with bytes very well (2 hex characters = 8 binary bits). Other formats include base64, binary, and just regular base10 (decimal)! In a way, that ascii chart represents a system where all text can be seen as "base128" (not including the Extended ASCII codes)

TO UNLOCK NEXT LEVEL, give me the text you just decoded, plaid, as its hex equivalent, and then the decimal equivalent of that hex number ("foo" -> 666f6f -> 6713199
```
hex,dec 剛剛第一題的時候就出現過，直接複製貼上
```
hex> 706c616964
dec> 482854660452
```
**第三題**
```
----------- LEVEL 3: Hashing Function ------------
A Hashing Function intakes any data of any size and irreversibly transforms it to a fixed length number. For example, a simple Hashing Function could be to add up the sum of all the values of all the bytes in the data and get the remainder after dividing by 16 (modulus 16)

TO UNLOCK NEXT LEVEL, give me a string that will result in a 12 after being transformed with the mentioned example hashing function
```
尋找一個每位數字加總模16之後，會等於12的數字，12+16=28，28平分成7777
```
> 7777
```
**第四題**
```
--------------- LEVEL 4: Real Hash ---------------
A real Hashing Function is used for many things. This can include checking to ensure a file has not been changed (its hash value would change if any part of it is changed). An important use of hashes is for storing passwords because a Hashing Function cannot be reversed to find the initial data. Therefore if someone steals the hashes, they must try many different inputs to see if they can "crack" it to find what password yields the same hash. Normally, this is too much work (if the password is long enough). But many times, people's passwords are easy to guess... Brute forcing this hash yourself is not a good idea, but there is a strong possibility that, if the password is weak, this hash has been cracked by someone before. Try looking for websites that have stored already cracked hashes.

TO CLAIM YOUR PRIZE, give me the string password that will result in this MD5 hash (MD5, like most hashes, are represented as hex digits):
e9e39bbf56f17b4b9ea35945fc7aa015
```
直接丟[md5 decrypto online](http://www.md5online.org/)
```
> s1m14
```
