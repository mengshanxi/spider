from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import random

es = Elasticsearch("localhost:9200")
res = es.search(index="content_engine", params={},
                body={"query": {"match_phrase": {"content": "综网  电脑"}}})
