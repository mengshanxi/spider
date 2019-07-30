from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import random

es = Elasticsearch("localhost:9200")
query = {'query': {'match': {'content': '综合'}}}

es.delete_by_query(index='http_code', body=query, doc_type='error_code')
