import requests as rq
import hashlib
import getpass
import re

login_url = "https://ringzer0team.com/login"
target_url = "https://ringzer0team.com/challenges/13/"
ss = rq.session()

def build_session(username, password):
  print("Building session....")
  user_pass = dict(username=username, password=password)
  ss.post(login_url, data=user_pass)

def get_text():
  print("Getting text....")
  r = ss.get(target_url)
  text = r.text
  msg = text.find('BEGIN')
  text = text[msg+29:msg+29+1024]
  return text

def hash_sha512(text):
  m = hashlib.sha512(text)
  ans = m.hexdigest()
  return ans  

def send_ans(ans):
  r = ss.get(target_url+ans).text
  msg = r.find('FLAG-')
  print(r[msg:msg+31])
  return r[msg:msg+31]

username = raw_input("username : ")
password = getpass.getpass("password : ")
build_session(username, password)
text = get_text()
ans = hash_sha512(text)
send_ans(ans)      
