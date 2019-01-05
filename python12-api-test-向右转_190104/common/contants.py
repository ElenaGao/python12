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
# print(reports_dir)