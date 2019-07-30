import json


class ResponseObj:
    def __init__(self, **kwargs):
        '''
        self.code = kwargs["code"]
        self.message = kwargs["message"]
        self.mobile = kwargs["mobile"]
        self.taskId = kwargs["taskId"]
        '''
        self.__dict__.update(kwargs)


class Result(object):
    def __init__(self, **kwargs):
        if kwargs["response"] is None:
            kwargs["response"] = []
        self.code = kwargs["code"]
        self.message = kwargs["message"]
        self.response = kwargs["response"]


test_str = '{"code":200,"message":"发送成功","response":[{"code":2,"message":"xxxxxxxx","mobile":"xxxxxx","taskId":null},{"code":2,"message":"xxxxxx","mobile":"xxxxxx","taskId":null}]}'

result = Result(**json.loads(test_str))
policys_length = len(result.response)
res = []
for i in range(policys_length):
    policy = ResponseObj(**result.response[i])
    res.append(policy)
print(res)
print()
