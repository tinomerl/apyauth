import requests as rq

url = 'http://httpbin.org/'
print(url)
resp = rq.get(url)
resp
resp.status_code
resp.headers['content-type']
resp.text