from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import random

import urllib.request
#https://blog.csdn.net/YHYR_YCY/article/details/78882011


url = "http://hebca.com/"
data = urllib.request.urlopen(url, timeout=10).read()
data = data.decode('UTF-8')



es = Elasticsearch("localhost:9200")
package = []
for i in range(1):
    row = {
        "@timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
        "http_code": "404",
        "count": data
    }
    package.append(row)

actions = [
    {
        '_op_type': 'index',
        '_index': "http_code",
        '_type': "error_code",
        '_source': d
    }
    for d in package
]

elasticsearch.helpers.bulk(es, actions)
