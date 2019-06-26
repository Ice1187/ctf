[Crypto] keyz
===

## Description

While webshells are nice, it'd be nice to be able to login directly. To do so, please add your own public key to ~/.ssh/authorized_keys, using the webshell. Make sure to copy it correctly! The key is in the ssh banner, displayed when you login remotely with ssh, to shell2017.picoctf.com

* HINTS
    * There are plenty of tutorials out there. This one covers key generation: https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html

    * Then, use the web shell to copy/paste it, and use the appropriate tool to ssh to the server using your key

## Solution

先在local端設置ssh公鑰，公鑰預設放在~/.ssh/ida_rsa.pub
```bash
ssh-keygen
```

到websell建立~/.ssh/authorized_keys，將剛剛的公鑰貼進去，然後連線過去即可
```
ssh shell2017.picoctf.com
```


