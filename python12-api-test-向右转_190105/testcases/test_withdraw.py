# -*- coding:utf-8 _*-
""" 
@author:Elena
@time: 2019/1/5 22:35
@email:huimin0099@163.com
@function： 
"""

import unittest
import json
import re

from ddt import ddt,data
from common.request import Request
from common.do_excel import DoExcel
from common import contants
from common.mysql_util import MysqlUtil
from common.basic_data import DoRegex,Context

do_excel = DoExcel(contants.case_file)
cases = do_excel.get_cases(sheet_name='withdraw') # 返回cases列表

# 登录接口的测试类
@ddt
class TestWithdraw(unittest.TestCase):

    @classmethod
    def setUpClass(cls): #每个测试函数运行前运行
        global mysql,max_phone
        mysql = MysqlUtil()
        sql = 'select mobilephone from future.member where ' \
              ' mobilephone != ""  order by mobilephone desc limit 1 '
        max_phone = mysql.fetch_one(sql)['mobilephone']

    def setUp(self):
        # 取现之前的账户余额
        global select_before,before_leaveamount
        select_before = 'select * from future.member where mobilephone = "{0}"'.format(Context.normal_user)
        before_leaveamount = mysql.fetch_one(select_before)['LeaveAmount']

    @data(*cases)
    def test_login(self,case):
        register = int(max_phone)+1
        data = re.sub(pattern='\#\{(.*?)\}', repl=str(register),string=case.data) # 使用正则匹配替换excel中的数据
        data = DoRegex.replace(data)
        print('data:',data)
        data = json.loads(data) #将str反序列化为字典
        if hasattr(Context,'cookies'):
            cookies = Context.cookies
        else:
            cookies = None

        resp = Request(method=case.method,url=case.url,data=data,cookies=cookies)
        print("响应结果：",resp.get_status_code())
        resp_dict = resp.get_json()
        if resp.get_cookies():
            setattr(Context,'cookies',resp.get_cookies())
        resp_text = resp.get_text()
        print(resp_text)

        #优先判断期望结果与实现结果
        self.assertEqual(str(case.expected),resp_dict['code'])

        if resp_dict['msg'] == "登录成功": # 登录成功的数据校验，判断数据库有这条数据
            sql = 'select * from future.member where mobilephone = "{0}"'.format(Context.normal_user)
            member = mysql.fetch_one(sql)
            if member is not None: # 正常注册成功就不应该返回None
                self.assertEqual(data['mobilephone'],member['MobilePhone'])
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('withdraw',case.case_id,resp.get_text(),TestResult)
            else: # 返回None则代表注册成功之后但是数据库里面没有插入数据
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('withdraw',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        elif resp_dict['msg'] == '取现成功':
            select_amount = 'select * from future.member where mobilephone = "{0}"'.format(Context.normal_user)
            leaveamount = mysql.fetch_one(select_amount)
            if leaveamount is not None: # 取现成功，校验数据库，余额 = 取现前 - 取现金额
                expected = float(before_leaveamount) - float(data['amount'])
                actual = leaveamount['LeaveAmount']
                self.assertEqual(expected,actual)
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('withdraw',case.case_id,resp_text,TestResult)
        elif resp_dict['code'] != 0: # 取现失败，余额不变
            try:
                select_amount = 'select * from future.member where mobilephone = "{0}"'.format(Context.normal_user)
                leaveamount = mysql.fetch_one(select_amount)
                expected = float(before_leaveamount)
                actual = float(leaveamount['LeaveAmount'])
                self.assertEqual(expected,actual)
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('withdraw',case.case_id,resp_text,TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('withdraw',case.case_id,resp_text,TestResult)
                raise e

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        mysql.close()

if __name__ == '__main__':
    unittest.main()







