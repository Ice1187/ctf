0405 Learning dis_asm 筆記2
===
* 教材
    * [x86 wiki](https://zh.wikipedia.org/wiki/X86)

---
0. wiki

## x86 簡介
> * x86泛指一系列由英特爾公司開發處理器的架構，這類處理器最早為1978年面市的「Intel 8086」CPU，後續包含80386, 80486, 80686
> * 8086是16位元處理器；直到1985年32位元的80386的開發，這個架構都維持是16位元。接著一系列的處理器表示了32位元架構的細微改進，推出了數種的擴充，直到2003年AMD對於這個架構發展了64位元的擴充，並命名為AMD64。後來英特爾也推出了與之相容的處理器，並命名為Intel 64。兩者一般被統稱為x86-64或x64，開創了x86的64位元時代。

## x86 暫存器

* [x86 CPU暫存器](http://finalfrank.pixnet.net/blog/post/22992166-x86-cpu-%E6%9A%AB%E5%AD%98%E5%99%A8-register-%E5%A4%A7%E5%85%A8)
* [Intel x86 Architecture](https://www.csie.ntu.edu.tw/~cyy/courses/assembly/10fall/lectures/handouts/lec12_x86arch.pdf)
* [x86 定址模式Adressing mode 大全](http://finalfrank.pixnet.net/blog/post/22995822)
* [Intel 64, rsi and rdi registers (StackOverflow)](https://stackoverflow.com/questions/23367624/intel-64-rsi-and-rdi-registers)
* [Why are x86 registers named the way they are? (StackOverflow)](https://stackoverflow.com/questions/892928/why-are-x86-registers-named-the-way-they-are)
* [Introduction to x64 Assembly (Intel.com)](https://software.intel.com/en-us/articles/introduction-to-x64-assembly)
* [程式設計師的自我修養 Ch10 記憶體 ](https://www.slideshare.net/shuyufu/chapter-10-13179267)
* [Purpose of ESI & EDI registers?
 (StackOverflow)](https://stackoverflow.com/questions/1856320/purpose-of-esi-edi-registers)


### General Purpose Registers 通用暫存器

* RAX(64bits) -> EAX(32bits) -> AX(16bits) -> AH/AL(8bits)

* `AX`, `BX`, `CX`, `DX`為通用目的，但各自都有附加目的
    * AX(Accumulator)
        * 執行乘/除法時，結果將記錄在`AX`
    * BX(Base)
    * CX(Counter)
        * loop計數器
    * DX(Data)
* 可以被當成兩個分開的位元組存取
    * `AX`的高位元可以被當成`AH`，低位元則可以當成`AL`
* 64位元下，還有`R8`~`R15`，16個通用暫存器

### Segment Registers 區段暫存器

* 16bits

* `CS`、`DS`、`SS`、`ES`、`FS`、`GS`用來紀錄記憶體的絕對位址
    * CS = Code Segment
        * 指一個程式是從哪個位址開始
        * 程式從000A，則`CS`裡面就會記載000A
        * 常搭配`IP`使用，程式目前執行位置由`(CS)0 + IP`決定，如果跑到程式第一行，`IP`就是0，如果跑到第三行，`IP`就是2。在實體記憶體實際上的位址就分別是000A0和000A2  
    
    * DS = Data Segment
        * 指資料從記憶體的哪個位址開始
        * 常搭配其他暫存器使用，例如`BX`、`CX`
        * 假如在組語中要求使用[BX]位址的資料 ，而BX = 3，則其實找到的是在記憶體位置`(DS)0 + BX`位址的資料 ，即是000A3這個位址的資料 (假如DS=000A)
    
    * SS = Stack Segment
        * 指堆疊( Stack )的底部位置
        * 常搭配`SP`使用
        * `SS + SP`就是目前Stack(堆疊)頂端的位址 ( TOS，Top of Stack )。如果把一筆資料送入堆疊( PUSH ) ，則`SP`就會-2；反之，若把一筆資料從堆疊中拿出( POP )，則`SP`就會+2
        * Intel x86中，Stack由高位址往低位址疊(?
    * ES = Extra Segment
        * 額外的區段暫存器，`FS`、`GS`也是

#### Pointer Registers 指標暫存器  (屬 通用暫存器)

* RBP(64bits) -> EBP(32bits) -> BP(16bits) -> BPL(8bits, 64-bit mode only)

* BP、SP用來記錄Stack堆疊的底部及頂部；IP用來紀錄目前執行指令位址
    * BP = Base Pointer 
        * 指向Stack堆疊的底部，或記憶體的其它地方(通用功能)
    * SP = Stack Pointer
        * 指向Stack堆疊的頂部
    * IP = Instruction Pointer
        * 指向目前執行指令的位址

#### Index Registers 索引暫存器 (屬 通用暫存器)

* RDI(64bits) -> EDI(32bits) -> DI(16bits) -> DIL(8bits, 64-bit mode only)

* SI、DI用來指向陣列的內部
    * SI = Source Index
    * DI = Destination Index
        * 組語中，`MOV AX,BX`是將`BX`的資料複製到 `AX`，則`SI`就要指向`BX`，`DI`就要指向`AX`

> 1. used for high-speed memory transfer instructions
> 2. These are operations that work on a bunch of bytes at a time, and they kind of put the CPU in automatic.
 
 * => 似乎與加速運算有關，不是很懂 

#### Status Register (FLAGS) 旗標暫存器

* 16bits (32位元下)

* FLAGS用來記錄狀態，比如進位、溢位、結果為零...
    * CF = Carry Flag
        * 如果指令的運作中，使得資料產生了Carry，那麼CF就會變成 1 (set)，反之就是 0 (reset)
        * 例如 1000000000000000 + 1000000000000000 = ==1==0000000000000000，第17位為1就紀錄`CF = 1` 
    * ZF = Zero Flag
        * 如果計算結果為0，`ZF = 1`，反之`ZF = 0`
    * SF = Sign Flag
        * 如果計算結果有負號，那麼`SF = 1`，反之`SF = 0`
    * TF = Trap Flag
        * 如果`TF = 1`，那麼電腦的程式會逐行執行 (用於除錯等用途)
    * DF = Direction Flag
        * 決定字串的讀取是由「高位讀到低位」(small endian)還是「低位讀到高位」(big endian)
        * X86的設計，預設是small endian
        * `DF = 0`時，為small endian
        * 在small endian下，位址`00`資料為`34`，位址`01`資料為`12`，則這個字串讀起來就是 `1234`
    * OF = Overflow Flag
        * 如果計算結果產生溢位(overflow)，`OF = 1`，反之`OF = 0`


###### tags: `CTF` `Learning` `dis_asm`
