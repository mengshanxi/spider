# from elasticsearch import Elasticsearch
# from src.config.config_load import host
# from src.config.config_load import es_index
# from src.config.config_load import es_port
#
# """
# Elasticsearch 工具类
# """
#
#
# class EsUtil:
#     def __init__(self, host=host, port=es_port):
#         self.host = host
#         self.port = port
#         try:
#             self.es = Elasticsearch(host + ":" + port)
#         except Exception as e:
#             print(e)
#
#     def index_monitor_baike(self, website_id, url, http_res):
#         body = {"website_id": website_id,
#                 "url": url,
#                 "http_res": http_res}
#         self.es.index(index=es_index, doc_type="monitor_baike", body=body)
#
#     def index_monitor_bc(self, merchant_name, http_res):
#         body = {"merchant_name": merchant_name,
#                 "http_res": http_res}
#         self.es.index(index=es_index, doc_type="monitor_bc", body=body)
#
#     def index_monitor_third(self, type, website_name, title, url):
#         body = {"type": type,
#                 "website_name": website_name,
#                 "title": title,
#                 "url": url}
#         self.es.index(index=es_index, doc_type="monitor_third", body=body)
#
#     def index_monitor_weburl(self, weburl_id, url, http_res):
#         body = {"weburl_id": weburl_id,
#                 "url": url,
#                 "http_res": http_res}
#         self.es.index(index=es_index, doc_type="monitor_url", body=body)
#
#     def search(self, doc_type, keyword):
#         if self.es.indices.exists(index=es_index) is not True:
#             self.es.indices.create(index=es_index)
#         params = {'size': 1000}
#         res = self.es.search(index=es_index, doc_type=doc_type,
#                              body={"query": {"query_string": {"query": keyword}}}, params=params)
#         return res
#
#     def delete(self, doc_type):
#         res = self.es.delete(index=es_index, doc_type=doc_type)
#         return res
