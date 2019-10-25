import http.client

url = "http://lanhongc.cn"
conn = http.client.HTTPSConnection("lanhongc.cn", timeout=10)
try:
    conn.request('GET', url)
    resp = conn.getresponse()
    print(resp.code)
except Exception as e:
    print(e)
    print(str(e).find("getaddrinfo failed"))
