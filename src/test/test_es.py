from src.search.es_util import EsUtil


class TestEs(object):
    if __name__ == "__main__":
        aa=[]
        aa.append('购物')
        aa.append('销售')
        bb= ' '.join(aa)
        print(bb)
        es = EsUtil()
        json_dic = es.search('error_code',bb)
        print(json_dic)
        a = json_dic['hits']['total']
        for i in range(a):
            b = json_dic['hits']['hits'][i]['_source']['name']
            print(b )

        exist = json_dic['hits']['total']
        if exist > 0:
            print("傻逼 exist: true")
        else:
            print("傻逼 exist: false")



