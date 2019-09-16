fd
===

## Description

> Mommy! what is a file descriptor in Linux?
> 
> * try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw
> 
> ssh fd@pwnable.kr -p2222 (pw:guest)

## Explanation
```c
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
if(!strcmp("LETMEWIN\n", buf)){
    printf("good job :)\n");
    system("/bin/cat flag");
    exit(0);
}   
```
先了解一下read()函式:
```c
ssize_t read(int fd,void * buf ,size_t count);
```
read() 會把fd所指的文件傳送count個位元組到buf指標所指的記憶體中。
一般情況下，fd應該會長得像是這樣:
```c
fd = open(“/tmp/temp”,O_RDWR); // 開啟/tmp/temp檔案, 可讀寫
```

但在此題，fd傳入的則是一個int !?

在Linux中，`0`代表std_input，`1`代表std_output，`2`代表std_error_output。
所以可以透過傳入0，來控制buf的內容。

## Solution
```c
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
if(!strcmp("LETMEWIN\n", buf)){
    printf("good job :)\n");
    system("/bin/cat flag");
    exit(0);
}   
```
```shell=
fd@ubuntu:~$ echo "LETMEWIN" | ./fd 4660
```
1. 0x1234轉為十進位為4660，傳入4660，使得fd = 0
2. read() 會從 std_input 讀入資料，echo 之後 pipe 過去即可
3. 得 flag




