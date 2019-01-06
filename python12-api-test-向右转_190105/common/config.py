__author__ = 'ghm'

import configparser
from common import contants
import os
# 创建实例
#加载配置文件
#根据section options来取到配置项的值

class ConfigLoader:

    def __init__(self):
        self.conf = configparser.ConfigParser()
        file_name = os.path.join(contants.configs_dir,'global.conf') # global.conf用来配置测试环境的选取 -- 开关，为bool型
        self.conf.read(filenames=file_name,encoding='UTF-8')
        if self.getboolean('switch','on'): #必须为bool型
            online = os.path.join(contants.configs_dir,'online.conf')
            self.conf.read(filenames=online,encoding='UTF-8')
        else:
            test = os.path.join(contants.configs_dir,'test.conf')
            self.conf.read(filenames=test,encoding='UTF-8')

            # read方法 返回的为字符串类型   源文件中的说明Return list of successfully read files. list？？？？

    def get(self,section,option): # 返回str类型
        return self.conf.get(section,option)

    def getint(self,section,option):
        return self.conf.getint(section,option)

    def getboolean(self,section,option): # 返回bool型
        return self.conf.getboolean(section,option)

    def getfloat(self,section,option): # 返回float型
        return self.conf.getfloat(section,option)



if __name__ == '__main__':
    config = ConfigLoader()
    url_pre = config.get('api','url_pre')
    print(url_pre)
    print(type(url_pre))
