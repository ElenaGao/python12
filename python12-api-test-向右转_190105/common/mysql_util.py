__author__ = 'ghm'
'''
如何参数化
1. 连接数据库，查询数据，得到返回-->写一个数据库操作类
2. 测试数据更换 -- 字符串查找并替换
3. 再去请求
'''
'''
1. 连接数据库
2. 编写一个sql
3. 建一个游标cursor
4. execute
'''
import pymysql
from common.config import ConfigLoader
class MysqlUtil():
    def __init__(self):
        config = ConfigLoader()
        host = config.get('mysql','host')
        port = config.getint('mysql','port')
        user = config.get('mysql','usr')
        password = config.get('mysql','pwd')
        #自行添加异常处理
        try:
            self.mysql = pymysql.connect(host=host, user=user, password=password,
                                         port=port,cursorclass=pymysql.cursors.DictCursor) #建立连接
            print('数据库连接成功！')
        except AssertionError as e:
            print('数据库连接失败！',e)
            raise e

    def fetch_one(self,sql): # 根据sql语句，查询一条数据并返回
        cursor = self.mysql.cursor()
        cursor.execute(sql)
        return cursor.fetchone()

    def fetch_all(self,sql): # 根据sql语句，查询一条数据并返回
        cursor = self.mysql.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def close(self):
        self.mysql.close()

if __name__ == '__main__':
    sql='select mobilephone from future.member where \
    mobilephone != " " order by mobilephone desc limit 1'
    print(sql)
    mysql_util = MysqlUtil()
    # result = mysql_util.fetch_one(sql) # 返回的为元组
    # print(result['mobilephone'])
    # max_mobile = int(result[0]) + 1
    max_mobile = mysql_util.get_mobilephone(sql)
    print(max_mobile)
    print(type(max_mobile))
    # sql = 'select leaveamount from future.member where mobilephone ="${normal_user}"'
    # from common.basic_data import DoRegex
    # sql = DoRegex().replace(sql)
    # mysql_util = MysqlUtil()
    # result = mysql_util.fetch_one(sql) # 返回的为元组
    # print(result['leaveamount'])

