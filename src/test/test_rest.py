from urllib import request, parse

try:
    url = "http://localhost/ims/open/api/v1/agent/monitor_bc"
    data_json = {"batchNum": "1", "websiteId": 1, "taskId": 2}
    data = bytes(parse.urlencode(data_json), encoding="utf8")
    new_url = request.Request(url, data)
    res = request.urlopen(new_url).read().decode('utf-8')

    url = "http://localhost/ims/views/system/qichacha.jsp?merchantNum="
    data_json = {"data": res}
    data = bytes(parse.urlencode(data_json), encoding="utf8")
    new_url = request.Request(url, data)
    request.urlopen(new_url)
except Exception as e:
    print(e)
