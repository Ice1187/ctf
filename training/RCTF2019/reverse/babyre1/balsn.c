#include <dlfcn.h>
#include <string.h>
#include <openssl/md5.h>

char* data="0123456789abcdef";
unsigned char out[MD5_DIGEST_LENGTH];

int main(int argc,char** argv){
    char** handle=dlopen("./babyre",RTLD_LAZY);
    char* code = *handle;
    void (*change)(char*,int,char*);        
    change = code+0xce0;
    unsigned char buf[]="Bingo!\x00\x00";
    for(int i=0,e=strlen(buf);i<e;i++){
        buf[i]^=0x17;
    }
    buf[6] = 0x2; // bruteforce 0~255 to match md5
    buf[7] = 0x2;
    change(buf,2,code+0x202010);
    char sol[0x17]="rctf{aaaaaaaaaaaaaaaa}";
    for(int i=0;i<8;i++){
        int a = buf[i]>>4;
        int b = buf[i]&0xf;
        sol[5+i*2+0]=data[a];
        sol[5+i*2+1]=data[b];
    }
    MD5_CTX c;
    MD5_Init(&c);
    MD5_Update(&c,sol,0x16);
    MD5_Final(out, &c);
    puts(sol);

    // MD5 match 5f8243a662cf71bf31d2b2602638dc1d
    for(int n=0; n<MD5_DIGEST_LENGTH; n++)
        printf("%02x", out[n]);

    puts("");

}
