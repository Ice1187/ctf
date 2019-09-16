0409 Learning program_security 筆記8
===

* 教材
    * [Pwn 1 (2018 Bamboofox社課)](https://drive.google.com/file/d/16eP_DqOXdh-TljABnIHWsCByL5a0u0zF/view) 
    * [Secure Programming
Smashing the Stack (Bamboofox)](https://bamboofox.cs.nctu.edu.tw/uploads/material/attachment/8/Secure_Programming_Smashing_the_Stack.pdf)

* 參考
    * [checksec及其包含的保护机制](http://yunnigu.dropsec.xyz/2016/10/08/checksec%E5%8F%8A%E5%85%B6%E5%8C%85%E5%90%AB%E7%9A%84%E4%BF%9D%E6%8A%A4%E6%9C%BA%E5%88%B6/)
    * [printf函數leak與canary繞過原理及利用方式
](https://read01.com/zh-tw/5M24yNm.html#.XKoAIOgkvb0)

---

## 編譯程序
* [ELF檔案格式與程式的編譯連結](https://www.itread01.com/content/1549571596.html)
* [連結器linker (wiki)](https://zh.wikipedia.org/wiki/%E9%93%BE%E6%8E%A5%E5%99%A8)

* 編譯程序圖

![編譯程序](https://img-blog.csdn.net/20160123200340137)

 1. `code(.c .cpp .h)`跟`Header Files(.h)`，經過`預處理器(cpp)`預處理，生成`.i`檔案
 2. `.i`檔案，經`編譯器(cc1、cc1plus)`編譯，生成`.s`檔案
 3. `.s`檔案，經`彙編器(as)`彙編，生成`.o`檔案
 4. `.o`檔案跟`Static Library(.a)`，經`連結器(ld)`連結，生成可執行檔案。
> * gcc是對cpp、cc1(cc1plus)、as、ld這些後臺程式的包裝，它會根據不同的引數要求去呼叫後臺程式。
>   * 以hello程式為例，使用gcc -o hello hello.c時加上-v選項可觀察到詳細的步驟。也可使用gcc分別進行以上四步驟，
        1. **preprocess** 預編譯: `gcc -E hello.cpp -o hello.i` (處理#include, #defined之類的，.i file)
        2. **compilation** 編譯:　`gcc -S hello.i -o hello.s` (code 轉成 assembler source，.s file) 
        3. **assembly** 彙編:　`gcc -c hello.s -o hello.o`(asm source 轉成 binary asm，obj file)
        4. **link** 連結:　`gcc -o hello hello.o` (link 並轉成 executable)

* GCC編譯過程分解

![GCC編譯過程分解](https://img-blog.csdn.net/20160123205549808)


> 1. 以下分析一下編譯完成之後的ELF檔案：
>
> `readelf -S add.o檢視section header table`
> 
> ![](https://img-blog.csdn.net/20160125150047179)
> 
> ![](https://img-blog.csdn.net/20160125150959720)
> 
> 由section header table可推測add.c檔案程式碼中並沒有實際資料(.data的size大小為0)。add.o中共包含了11個節描述符，每個節描述符大小為40位元組(sizeof(Elf32_Shdr))，共440位元組，因此在這11個節之後還有440位元組的section header table。
>
> `readelf -S main.o檢視section header table`
>
> ![](https://img-blog.csdn.net/20160125152437005)
>
> alloc表示該section在程序地址空間中要分配空間(.text .data .bss都會有這個標誌)
>
> ![](https://img-blog.csdn.net/20160125200436445)
>
> main.o中共有14個節描述符，每個節的大小為40位元組(sizeof(Elf32_Shdr))，因此這14個節之後還有560位元組的section header table。

* 上述比較表示，link後，會做alloc

* [The Preprocessor (The C Book)](https://publications.gbdirect.co.uk/c_book/chapter7/)

---

## Static/Dynamic Linking  靜/動態連結

* 教材
    * [動態(Dynamic Linking)與靜態連結(Static Linking) (阿洲 blog)](http://monkeycoding.com/?p=876)

* 參考
    * [靜態函式庫 wiki](https://zh.wikipedia.org/wiki/%E9%9D%99%E6%80%81%E5%BA%93)
    * [Why are #ifndef and #define used in C++ header files?
](https://stackoverflow.com/questions/1653958/why-are-ifndef-and-define-used-in-c-header-files)
    * [使用 gcc 自製 C/C++ 靜態、共享與動態載入函式庫教學](https://blog.gtwang.org/programming/howto-create-library-using-gcc/)

## Program Security

* 教材
    * [Pwn 1 (2018 Bamboofox社課)](https://drive.google.com/file/d/16eP_DqOXdh-TljABnIHWsCByL5a0u0zF/view) 
    * [Shared Library 中 PLT 和 GOT 的使用機制](http://brandon-hy-lin.blogspot.com/2015/12/shared-library-plt-got.html)

<iframe src="https://drive.google.com/file/d/16eP_DqOXdh-TljABnIHWsCByL5a0u0zF/preview" width="640" height="480"></iframe>

### Lazy binding & GOT和PLT

* [Lazy binding](https://rafaelchen.wordpress.com/2017/09/25/pwn%E7%9A%84%E4%BF%AE%E7%85%89%E4%B9%8B%E8%B7%AF-lazy-binding/)

* [Global Offset Table (GOT) and Procedure Linkage Table (PLT) (Liveoverflow)](https://www.youtube.com/watch?v=kUk5pw4w0h4)

---

###### tags: `CTF` `Learning` `program_secrity`
