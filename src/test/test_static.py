class ClassTest(object):
    __num = 0

    @classmethod
    def addNum(cls):
        cls.__num += 1

    @classmethod
    def getNum(cls):
        return cls.__num

    # 这里我用到魔术方法__new__，主要是为了在创建实例的时候调用累加方法。
    def __new__(self):
        ClassTest.addNum()
        return super(ClassTest, self).__new__(self)


class Student(ClassTest):
    def __init__(self):
        self.name = ''

a = Student()
b = Student()
print(ClassTest.getNum())