import requests as rq

url = 'http://104.199.235.135:31332/_hidden_flag_.php'
ss = rq.session()
c = dict(c=100000)
r = ss.post(url, data=c)
print(r.header)
