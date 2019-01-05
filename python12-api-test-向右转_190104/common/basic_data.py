__author__ = 'ghm'

import re

class DoRegex:

    @staticmethod
    def replace(target):  # 查找并且替换
        pattern = '\$\{(.*?)\}'
        while re.search(pattern,target):
            m = re.search(pattern,target)
            key = m.group(1)
            from common.basic_data import Context
            user = getattr(Context,key)
            target = re.sub(pattern,user,target,count=1) # count=0 合部匹配并替换，count=1只匹配一个
        return target


from common.config import ConfigLoader
class Context:
    config = ConfigLoader()
    normal_user = config.get('basic','normal_user')
    normal_pwd = config.get('basic','normal_pwd')
    normal_member_id = config.get('basic','normal_member_id')

    admin_user = config.get('basic','admin_user')
    admin_pwd = config.get('basic','admin_pwd')

    loan_member_id = config.get('basic','loan_member_id')
    unnormal_member_id = config.get('basic','unnormal_member_id')

    # def __init__(self,a,b):
    #     self.a = a # 成员变量
    #     self.b = b

if __name__ == '__main__':
    c = getattr(Context,'normal_user') # 获取属性的值
    d = getattr(Context,'pwd')
    print(c,d)

    # setattr(Context,'admin','abc')
    # admin = getattr(Context,'admin')
    # print(admin)

    # if hasattr(Context,'admin'):
    #     delattr(Context,'admin')
    # else:
    #     print('has no this attr')
    # print(admin)

    # context = Context(1,2)
    # a = getattr(Context,'a')  error 类名不能直接调用成员变量
    # a = getattr(context,'a')    #对象可以调用成员变量
    # print(a)


