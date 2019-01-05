# -*- coding:utf-8 _*-
""" 
@author:Elena
@time: 2019/1/3 17:15
@email:huimin0099@qq.com
@function： 
"""

import unittest
import json

from ddt import ddt,data
from common.mysql_util import MysqlUtil
from common.basic_data import DoRegex,Context
from common.do_excel import DoExcel
from common.request import Request
from common import contants

do_excel = DoExcel(contants.case_file)
cases = do_excel.get_cases('add')

@ddt
class TestAdd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil() # check the loan's args after adding successfully

    @data(*cases)
    def test_add(self,case):
        data = DoRegex.replace(case.data)
        data = json.loads(data)
        if hasattr(Context,'cookies'):
            cookies = Context.cookies
        else:
            cookies = None
        #请求成功后，返回response
        resp = Request(method=case.method,url=case.url,data=data,cookies=cookies)
        if resp.get_cookies(): # 将cookies动态写入上下文管理器中
            setattr(Context,'cookies',resp.get_cookies())
        print("用例名称：",case.title)
        resp_dict = resp.get_json()
        print(resp.get_text())
        self.assertEqual(str(case.expected),resp_dict['code']) # check the response code firstly

        # Check that the login case is successful
        if case.title == '管理员正常登录':
            try:
                self.assertEqual(str(case.expected),resp_dict['code'])
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
                raise e
        # Check Check that the add case is successful , need to check the database
        else:
            select_loan = 'select * from future.loan where memberId = {0} ' \
                          'order by createtime desc limit 1'.format(Context.loan_member_id)
            loan = mysql.fetch_one(select_loan)
            if resp_dict['msg'] =='加标成功':
                if loan is not None:
                    self.assertEqual(data['title'],loan['Title'])
                    self.assertEqual(data['amount'],int(loan['Amount'])) # 实际加标金额与数据库加标金币是否一致
                    self.assertEqual(data['loanRate'],str(loan['LoanRate']))
                    self.assertEqual(data['loanTerm'],int(loan['LoanTerm']))
                    self.assertEqual(data['loanDateType'],int(loan['LoanDateType']))
                    self.assertEqual(data['repaymemtWay'],int(loan['RepaymemtWay']))
                    self.assertEqual(data['biddingDays'],int(loan['BiddingDays']))
                    TestResult = 'PASS'
                    do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
                else:
                    TestResult = 'Fail'
                    do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
                    raise AssertionError
            else:
                try:
                    self.assertEqual(str(case.expected),resp_dict['code'])
                    TestResult = 'PASS'
                    do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
                except AssertionError as e:
                    TestResult = 'Fail'
                    do_excel.write_result_by_case_id('add',case.case_id,resp.get_text(),TestResult)
                    raise e

    @classmethod
    def tearDownClass(cls):
        mysql.close()

if __name__ == '__main__':
    unittest.main()





