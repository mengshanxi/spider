from datetime import datetime
from elasticsearch import Elasticsearch

#https://www.cnblogs.com/muniaofeiyu/p/5616316.html
#https://blog.csdn.net/xiaoxinwenziyao/article/details/49471977
es = Elasticsearch("localhost:9200")
body = {"url": "1111",
        "content": '京东JD.COM-专业的综合网上购物商城，销售超数万品牌、4020万种商品，囊括家电、手机、电脑、母婴、服装等13大品类。秉承客户为先的理念，京东所售商品为正品行货、全国联保、机打发票。'}
es.index(index="content_engine", doc_type="en", body=body)
