[Master] Lazy Dev
===

## Description

I really need to login to this [website](http://shell2017.picoctf.com:46677/), but the developer hasn't implemented login yet. Can you help?

* HINTS
    * Where does the password check actually occur?

    * Can you interact with the javascript directly?

## Solution

先試一下網站回應

![](https://i.imgur.com/iHshHdM.png)

再看看SourceCode
```javascript=
//Validate the password. TBD!
function validate(pword){
  //TODO: Implement me
  return false;
}
```
無論我們輸入甚麼都會是false，那就自己改成true吧 :3
```javascript=
//Validate the password. TBD!
function validate(pword){
  //TODO: Implement me
  return true;
}
```
回去網站隨便輸入就得flag
![](https://i.imgur.com/1boPzM1.jpg)

