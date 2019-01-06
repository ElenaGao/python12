# -*- coding:utf-8 _*-
""" 
@author:Elena
@time: 2019/1/4 10:03
@email:huimin0099@qq.com
@function： 
"""
import hashlib
from common.mysql_util import MysqlUtil

mysql = MysqlUtil()
sql = 'SELECT * from future.member  where MobilePhone = "18602153084"'
PWD = mysql.fetch_one(sql)['Pwd']
print('PWD',PWD)

pwd = '123456'
m = hashlib.md5()
m.update(pwd.encode('utf-8'))
pwd_md5 = m.hexdigest()
pwd_md5 = pwd_md5.swapcase() # 大小写互换
print('pwd',pwd_md5)

if pwd_md5 == PWD:
    print('True')
else:
    print('false')
