import urllib.request


class TestCookie(object):
    if __name__ == "__main__":
        header = {
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'cookie': '1zg_did=%7B%212d1id%22%3A%20%221641330d61764'
        }
        word = urllib.parse.quote("测试")
        url = 'http://www.qichacha.com/search?key=%s' % word
        try:
            req = urllib.request.Request(url, headers=header)
            res = urllib.request.urlopen(req).read()
            res = res.decode('UTF-8')
            print(res)
        except Exception as e:
            print(1)
            print(e)
