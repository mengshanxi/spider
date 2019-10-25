import http.client

url = "http://shailuoa.cn"
conn = http.client.HTTPSConnection("shailuoa.cn",timeout=10)
conn.request('GET', url)
resp = conn.getresponse()
print(resp.code)
url = "http://2019zgzymr.medmeeting.org/cn/ddd/"
aaa=url[url.find("/")+2:]
print(aaa)
# start = domain_name.index("/")
# dns = domain_name[0:start]
start = "shailuoa.cn".find("/")
print(start)