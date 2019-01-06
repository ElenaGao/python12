# -*- coding:utf-8 _*-
""" 
@author:Elena
@time: 2019/1/5 23:50
@email:huimin0099@163.com
@function： 
"""
import unittest

import HTMLTestRunnerNew

from common import contants
from testcases.test_login import TestLogin
from testcases import test_register
# suite = unittest.TestSuite()  # 测试用例集合
# loader = unittest.TestLoader()  # 加载用例
# suite.addTest(loader.loadTestsFromTestCase(TestLogin))
# suite.addTest(loader.loadTestsFromModule(test_register))

# 自动查找testcases目录下，以test开头的.py文件里面的测试类
discover = unittest.defaultTestLoader.discover(contants.testcases_dir, pattern="test*.py", top_level_dir=None)
#
with open(contants.reports_html, 'wb') as file:
    # 执行用例
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              title='API',
                                              description='API测试报告',
                                              tester='Elena')
    runner.run(discover)  # 执行查找到的用例