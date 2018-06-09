import requests as rq
import getpass as gp
import re

login_url = "https://ringzer0team.com/login"
target_url = "https://ringzer0team.com/challenges/32"
ss = rq.session()

def build_session(user, passwd):
  print("Building session....")
  user_pass = dict(username=user, password=passwd)
  try:
    ss.post(login_url, data=user_pass)
    print("Login Successed!")
  except rq.exceptions.RequestException as err:
    print(err)
    sys.exit(1)

def get_text():
  print("Getting text....")
  text = ss.get(target_url).text
  # parse
  msg = text.find("BEGIN")
  s = text[msg+29:msg+70]
  r = re.search('([0-9]+) \+ (0x[a-z0-9]+) - ([0-1]+)',s) 
  first = r.group(1)
  second = r.group(2)
  third = r.group(3)
  print(s, first, second, third)
  return int(first), int(second, 16), int(third, 2)

def send_ans(a, b, c):
  ans = str(a + b - c)
  print(ans)
  res = ss.get(target_url + '/' + ans).text
  print(res)

user = 'Ice1187'
print("User: Ice1187")
#passwd = gp.getpass("Passwd: ")
passwd = 'Ice1187<ringzer0>'
print("Passwd: ")
build_session(user, passwd)
a, b, c = get_text()
send_ans(a, b, c)
    
  
