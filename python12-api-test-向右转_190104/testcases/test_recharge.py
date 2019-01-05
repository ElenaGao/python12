__author__ = 'ghm'

# 基础数据放入配置文件>> context （反射）>> 通过从类里取出，用正则匹配excel中 >>
# request >> context 添加cookies >>recharge 取context的cookies

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
cases = do_excel.get_cases(sheet_name='recharge') # 返回cases列表

# 登录接口的测试类
@ddt
class TestRecharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("准备最大手机号码")
        global mysql
        mysql = MysqlUtil()
        sql = 'select mobilephone from future.member where ' \
              ' mobilephone != ""  order by mobilephone desc limit 1 '
        global max_phone
        max_phone = mysql.fetch_one(sql)['mobilephone']

    def setUp(self): # 因有些用例执行前需要检查充值前余额
        #充值前账户余额
        self.select_member = 'select * from future.member where mobilephone = {0}'.format(Context.normal_user)
        self.before_amount = mysql.fetch_one(self.select_member)['LeaveAmount']

    @data(*cases)
    def test_recharge(self,case):
        #参数化
        register = int(max_phone)+1
        data = DoRegex.replace(case.data) #正则 查找并替换$表达式
        data = re.sub(pattern='\#\{(.*?)\}', repl=str(register),string=data) # 使用正则匹配替换#表达式register
        data = json.loads(data)#将str反序列化为字典
        #处理cookies
        if hasattr(Context,'cookies'):
            cookies = getattr(Context,'cookies')
        else:
            cookies = None
        resp = Request(method=case.method,url=case.url,data=data,cookies=cookies)
        #判断有没有cookies，动态获取cookies
        if resp.get_cookies():
            setattr(Context,'cookies',resp.get_cookies())

        print("请求响应结果：",resp.get_status_code())
        resp_dict = resp.get_json()
        resp_text = json.dumps(resp_dict, ensure_ascii=False, indent=4)
        print('response: ', resp_text)  # 打印响应
        # 请求完后后，优先判断返回code
        self.assertEqual(case.expected,int(resp_dict['code']))
        actural = mysql.fetch_one(self.select_member)['LeaveAmount'] # 查询数据库中该用户的实际余额

        if resp_dict['msg'] == '登录成功':
            try:
                self.assertEqual(case.expected,eval(resp_dict['code']))
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
                raise e
        # 充值需要校验数据库,查询数据库中的 leaveamount是否与实际金额一致
        elif resp_dict['msg'] == '充值成功':
            expected = self.before_amount + int(data['amount']) # 充值成功余额 = 充值前+充值金额
            self.assertEqual(expected,actural)
            TestResult = 'PASS'
            do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
        elif resp_dict['msg'] == '此手机号对应的会员不存在':
            sql_member = 'select * from future.member where mobilephone = {0}'.format(register)
            member = mysql.fetch_one(sql_member)
            if member is  None: # 如果数据中不存在，表示未被注册，无法充值
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
        else: # 其他异常场景也需要校验数据库
            try:
                expected = self.before_amount # 充值失败 = 充值前
                self.assertEqual(expected,actural)
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('recharge',case.case_id,resp.get_text(),TestResult)
                raise e
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        mysql.close()

if __name__ == '__main__':
    unittest.main()
