__author__ = 'ghm'
'''
写测试用例的思路：
1. 调用DoExcel的get_cases方法，读取测试数据 --> 前置条件，需要用ConfigLoader方法及contants中的定义的case_file获取到文件
2. 取到数据后，调用request方法，发送一个http请求
3. 测试完成后，调用DoExcel的write_result_by_case_id 将实际结果和测试结果写入excel中
4. 引用DDT，将测试数据与测试用例分离，一条数据是一条测试用例
'''

import unittest
import json
import re

from ddt import ddt,data

from common.request import Request
from common.do_excel import DoExcel
from common import contants
from common.mysql_util import MysqlUtil


do_excel = DoExcel(contants.case_file)
cases = do_excel.get_cases(sheet_name='register') # 返回cases列表

# 登录接口的测试类
@ddt
class TestLogin(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls): # 必须使用@classmethod 装饰器,所有test运行前运行一次
    #     global mysql
    #     mysql = MysqlUtil()
    #     sql = 'select mobilephone from future.member where ' \
    #           ' mobilephone != ""  order by mobilephone desc limit 1 '
    #
    #     global max_phone
    #     max_phone = mysql.fetch_one(sql)['mobilephone']

    def setUp(self): #每个测试函数运行前运行
        self.mysql = MysqlUtil()
        self.sql = 'select mobilephone from future.member where ' \
              ' mobilephone != ""  order by mobilephone desc limit 1 '
        self.max_phone = self.mysql.fetch_one(self.sql)['mobilephone']

    @data(*cases)
    def test_login(self,case):
        register = int(self.max_phone)+1
        data = re.sub(pattern='\$\{(.*?)\}', repl=str(register),string=case.data) # 使用正则匹配替换excel中的数据
        print('data:',data)
        data = json.loads(data) #将str反序列化为字典
        resp = Request(method=case.method,url=case.url,data=data)
        print("响应结果：",resp.get_status_code())
        resp_dict = resp.get_json()
        resp_text = json.dumps(resp_dict, ensure_ascii=False, indent=4)
        print('response: ', resp_text)  # 打印响应
        #优先判断期望结果与实现结果
        expected = json.loads(case.expected)
        self.assertEqual(expected['code'],resp_dict['code'])
        sql = 'select * from future.member where mobilephone = "{0}"'.format(str(register))
        if resp_dict['msg'] == "注册成功": # 注册成功的数据校验，判断数据库有这条数据
            expected = int(self.max_phone) + 1
            member = self.mysql.fetch_one(sql)
            if member is not None: # 正常注册成功就不应该返回None
                self.assertEqual(expected,int(member['MobilePhone']))
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('register',case.case_id,resp.get_text(),TestResult)
            else: # 返回None则代表注册成功之后但是数据库里面没有插入数据
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('register',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        else: #注册失败的数据校验，判断数据库没有这条数据，自己写
            if resp_dict['msg'] == "手机号码已被注册":
                expected = data['mobilephone']
                mobilephone = self.mysql.fetch_one('select * from future.member where mobilephone = {0}'.format(expected))
                if mobilephone is not None: # 若数据库里有这条数据，则说明该手机号已被注册，用例pass
                    self.assertEqual(expected,mobilephone['MobilePhone'])
                    TestResult = 'PASS'
                    do_excel.write_result_by_case_id('register',case.case_id,resp_text,TestResult)
                else: # 若数据库里没有这条数据，则说明该手机号未被重复注册，用例fail
                    TestResult = 'Fail'
                    do_excel.write_result_by_case_id('register',case.case_id,resp_text,TestResult)
            else: # 其他所有注册失败用例
                expected = register
                member = self.mysql.fetch_one(sql)
                if member is None: # 查询数据库里没有这条数据，说明该手机号未被注册，用例pass
                    TestResult = 'PASS'
                    do_excel.write_result_by_case_id('register',case.case_id,resp.get_text(),TestResult)
                else:
                    TestResult = 'Fail'
                    do_excel.write_result_by_case_id('register',case.case_id,resp.get_text(),TestResult)

    # def tearDown(self):
    #     print('数据清除')

    # @classmethod
    # def tearDownClass(cls):
    #     mysql.close()
        def tearDown(self):
            self.mysql.close()

if __name__ == '__main__':
    unittest.main()









