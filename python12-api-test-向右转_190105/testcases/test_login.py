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
import hashlib

from ddt import ddt,data
from common.request import Request
from common.do_excel import DoExcel
from common import contants
from common.basic_data import DoRegex
from common.mysql_util import MysqlUtil

class HashLib:
    @staticmethod
    def md5_key(arg):
        hash = hashlib.md5()
        hash.update(arg.encode('utf-8')) # #参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
        return hash.hexdigest()

do_excel = DoExcel(contants.case_file)
cases = do_excel.get_cases(sheet_name='login') # 返回cases列表

# 登录接口的测试类
@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global mysql
        mysql = MysqlUtil()
        sql_max = 'select mobilephone from future.member where ' \
              ' mobilephone != ""  order by mobilephone desc limit 1 '
        global max_phone
        max_phone = mysql.fetch_one(sql_max) # 从数据库中查找出最大的手机号码用来测试非注册用户登录用例

    @data(*cases)
    def test_login(self,case):

        data = DoRegex.replace(case.data) #用正则匹配替换
        data = json.loads(data) #将str反序列化为字典
        resp = Request(method=case.method,url=case.url,data=data)

        print("响应结果：",resp.get_status_code())
        resp_dict = resp.get_json()
        resp_text = json.dumps(resp_dict, ensure_ascii=False, indent=4)
        print('response: ', resp_text)  # 打印响应
        expect = json.loads(case.expected)
        mobilephone =  data['mobilephone']
        sql_mobile = 'select * from future.member where mobilephone = {0}'.format(mobilephone)
        self.assertEqual(expect['code'],resp_dict['code'])
        if resp_dict['msg'] == '登录成功': # 如果登录成功，校验数据库登录密码是否正确 没必要做这步 为了研究下MD5加密
            member = mysql.fetch_one(sql_mobile)
            if member is not None: # 如果数据库中存在，判断登录密码是否正确
                # 明天接着写
                #思路：针对登录失败 要判断
                # 1.手机号未注册 -- 即查询不在数据库中
                # 2. 密码与数据库中密码不匹配 研究下密码MD5加密处理
                # 3. 其他失败场景不需校验数据库
                sql_pwd = 'SELECT * from future.member  where MobilePhone = {0}'.format(mobilephone)
                Pwd = mysql.fetch_one(sql_pwd)['Pwd'] # 查询该用户数据库中的密码为md5加密非明文密码
                pwd_md5 = HashLib.md5_key(data['pwd']) # 获取传入明文密码进行md5加密
                pwd_md5 = pwd_md5.swapcase() # 因数据库为大写，这里需要进行大小写互换
                if pwd_md5 == Pwd:
                    TestResult = 'PASS'
                    do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
                else: # 密码不匹配，登录成功-- 异常场景
                    TestResult = 'Fail'
                    do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)

            else: # 返回None则代表登录成功之后但是数据库里面没有插入数据，抛出异常
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        elif resp_dict['msg'] == '重复注册': # 重复注册-->查询数据库有记录则pass，否则fail
            member = mysql.fetch_one(sql_mobile)
            if member is not None:
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
            else:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
                raise AssertionError
        else: # 其他异常不需数据库校验
            try:
                self.assertEqual(case.expected,resp.get_text())
                TestResult = 'PASS'
                do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
            except AssertionError as e:
                TestResult = 'Fail'
                do_excel.write_result_by_case_id('login',case.case_id,resp.get_text(),TestResult)
                raise e

    @classmethod
    def tearDownClass(cls):
        mysql.close()

if __name__ == '__main__':
    unittest.main()








