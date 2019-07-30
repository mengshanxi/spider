from elasticsearch import Elasticsearch

conn = Elasticsearch('127.0.0.1:9200', timeout=3.5)  # 连接ES


def set_mapping(es, index_name="content_engine", doc_type_name="en"):
    my_mapping = {
        "en": {
            "properties": {
                "content": {
                    "type": "string"
                },
                "url": {
                    "type": "string"
                }
            },
            "_all": {"analyzer": "whitespace"}
        }
    }

    # 创建Index和mapping
    create_index = es.indices.create(index=index_name, body=my_mapping)  # {u'acknowledged': True}
    mapping_index = es.indices.put_mapping(index=index_name, doc_type=doc_type_name,
                                           body=my_mapping)  # {u'acknowledged': True}
    if create_index["acknowledged"] != True or mapping_index["acknowledged"] != True:
        pass