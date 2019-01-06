# -*- coding:utf-8 _*-
"""
@author:Elena
@time: 2019/1/5 12:07
@email:huimin0099@163.com
@function：
"""
import unittest
import json
from common.request import Request
from ddt import ddt,data
from common.do_excel import DoExcel
from common.basic_data import DoRegex,Context
from common import contants
from common.mysql_util import MysqlUtil

do_excel = DoExcel(contants.case_file)
cases = do_excel.get_cases('generateRepayments')


@ddt
class TestgenerateRepayments(unittest.TestCase):
    #准备测试数据--
    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()

        # 查询标的statue为1（非竞标） 和 5（满标）最大标的
        global not_generate_loan_id,max_loan_id
        select_1 = 'SELECT	* from future.loan where `Status` = "1" ORDER BY Amount DESC LIMIT 1'
        # select_5 = 'SELECT	* from future.loan where `Status` = "5" ORDER BY Amount DESC LIMIT 1'
        select_max = 'SELECT * from future.loan ORDER BY Id DESC LIMIT 1'
        not_generate_loan_id = mysql.fetch_one(select_1)['Id'] # 获取到非5\6标的
        # full_loan_id = mysql.fetch_one(select_5)['Id'] # 获取到竞标中的标的
        max_loan_id = mysql.fetch_one(select_max)['Id'] # 最大标的

    @data(*cases)
    def test_generateRepayments(self,case):
        setattr(Context,'not_generate_loan_id',str(not_generate_loan_id))
        # setattr(Context,'full_loan_id',str(full_loan_id))
        setattr(Context,'not_exist_loan_id',str(int(max_loan_id)+2)) # 跑用例之前最大id，运行完之后id+1，保证不存在需再加1
        data = DoRegex.replace(case.data) # 正则匹配，用配置文件的基础数据替换正则表达式代替的内容
        data = json.loads(data) # str反序列化为dict
        # 判断是否有cookies，解决数据依赖
        if hasattr(Context,'cookies'):
            cookies = Context.cookies
        else:
            cookies = None
        # 发起request请求
        resp = Request(method=case.method,url=case.url,data=data,cookies=cookies)
        print("用例名称：",case.title)
        #请求成功后，返回response
        resp_dict = resp.get_json()
        print(resp.get_text())
        # 优化对excel中expected和实际返回结果作断言
        expectVal = case.expected
        if (expectVal is None) or (str(expectVal).strip().strip('\n') is ''): # 对空单元格异常处理
            expectVal = ''
        self.assertEqual(str(expectVal), resp_dict['code'])

        # 判断response中是否有cookies，反射方法写到Context类中
        if resp.get_cookies():
            setattr(Context,'cookies',resp.get_cookies())
        if resp_dict['msg'] =='登录成功':
            try:
                self.assertEqual(case.expected,eval(resp_dict['code']))
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
                raise e
        # 当创建标的成功时，根据借款人ID查看数据库loan表是否与添加数据
        if resp_dict['msg'] == '加标成功':
            select_loan = 'select * from future.loan where memberId = {0} ' \
                          'order by createtime desc limit 1'.format(Context.loan_member_id)
            loan = mysql.fetch_one(select_loan) #查询到投标金额
            if loan is not None:
                self.assertEqual(data['amount'],loan['Amount']) # 实际加标金额与数据库加标金币是否一致
                self.assertEqual(data['loanRate'],str(loan['LoanRate']))
                self.assertEqual(data['loanTerm'],loan['LoanTerm'])
                self.assertEqual(data['loanDateType'],loan['LoanDateType'])
                self.assertEqual(data['repaymemtWay'],loan['RepaymemtWay'])
                self.assertEqual(data['biddingDays'],loan['BiddingDays'])
                # 将创建成功的标的ID写入到上下文中，用于之后投资用
                setattr(Context,'loan_id',str(loan['Id']))  # 放一个str类型的进去，以备后面正则替换
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
                raise AssertionError

            # 当审核成功，需校验数据库loan表中status字段更改，自己添加
        if resp_dict['msg'] == '更新状态成功：竞标开始，当前标为竞标中状态':
            select_loan = 'select * from future.loan where memberId = {0} order by createtime desc limit 1'.format(Context.loan_member_id)
            loan = mysql.fetch_one(select_loan) #查询到投标金额
            if loan is not None:
                self.assertEqual(data['status'],loan['Status'])
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        elif resp_dict['status'] == 0:
            try:
                self.assertEqual(str(case.expected),resp_dict['code'])
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
                raise e
        # 生成回款计划 校验数据库
        select_invest = 'SELECT * FROM future.invest a inner join future.repayment b on a.id = b.investid  where MemberID = {0} order by investid desc'.format(Context.normal_member_id)
        invest = mysql.fetch_one(select_invest) #查询回款记录
        if resp_dict['msg'] == '生成回款计划成功':
            if invest is not None:
                self.assertEqual(resp_dict['data'][0]['investId'],str(invest['InvestId']))
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        elif resp_dict['code'] != 10001:
            if invest is not None:
                self.assertEqual(str(case.expected),resp_dict['code'])
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('generateRepayments',case.case_id,resp.get_text(),TestResult)

    @classmethod
    def tearDownClass(cls):
        mysql.close()

if __name__ == '__main__':
    unittest.main()
