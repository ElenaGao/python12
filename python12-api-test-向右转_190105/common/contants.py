__author__ = 'ghm'

import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取当前文件的根路径

# print(base_dir)

configs_dir = os.path.join(base_dir,'configs')
# print(configs_dir)

datas_dir = os.path.join(base_dir,'datas')
case_file = os.path.join(datas_dir,'cases.xlsx')
# print(datas_dir)

logs_dir = os.path.join(base_dir,'logs')
# print(logs_dir)

reports_dir = os.path.join(base_dir,'reports')
reports_html = os.path.join(reports_dir, 'reports.html')  # reports文件夹路径
# print(reports_dir)

logs_dir = os.path.join(base_dir, 'logs')  # logs文件夹路径
logs_file = os.path.join(logs_dir, 'logs.log')  # logs文件夹路径
error_file = os.path.join(logs_dir, 'error.log')  # logs文件夹路径

testcases_dir = os.path.join(base_dir, 'testcases')  # logs文件夹路径