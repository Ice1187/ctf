[Forensics] Special Agent User
===
## Description
We can get into the Administrator's computer with a browser exploit. But first, we need to figure out what browser they're using. Perhaps this information is located in a network packet capture we took: [data.pcap](https://webshell2017.picoctf.com/static/80c0964ceb0bd2c879a4c213775715ac/data.pcap). Enter the browser and version as "BrowserName BrowserVersion". NOTE: We're just looking for up to 3 levels of subversions for the browser version (ie. Version 1.2.3 for Version 1.2.3.4) and ignore any 0th subversions (ie. 1.2 for 1.2.0)
* HINTS

    * Where can we find information on the browser in networking data? Maybe try [reading up on user-agent strings](http://www.useragentstring.com./).

## Solution

wireshark 搜尋設定 「Packet details / String / User-Agent」
![](https://i.imgur.com/WvCgLja.png)

檔頭可知User-Agent為 Chrome/40.0.2214.93
```
GET / HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36
Accept: */*
Host: 10.0.0.1
Connection: Keep-Alive
```
