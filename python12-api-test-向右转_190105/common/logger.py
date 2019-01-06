# -*- coding:utf-8 _*-
""" 
@author:Elena
@time: 2019/1/5 23:34
@email:huimin0099@163.com
@function： 
"""
import logging
import os
import time

import HTMLTestRunnerNew
from common import contants

#定义一个日志收集器，设置级别 一般设置为DEBUG 全量收集
logger = logging.getLogger('mylogger')
logger.setLevel('DEBUG')

def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.error_handle)
    else:
        logger.addHandler(MyLog.handler)
    logger.addHandler(MyLog.ch)
    logger.addHandler(MyLog.report_handler)

def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.error_handle)
    else:
        logger.removeHandler(MyLog.handler)

    logger.removeHandler(MyLog.ch)
    logger.removeHandler(MyLog.report_handler)

def get_log_dir():
    log_dir = os.path.join(contants.logs_dir,get_current_day())
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    return log_dir

def get_current_day():
    return time.strftime('%Y%m%d', time.localtime(time.time()))




class MyLog:
    log_dir = get_log_dir()
    log_file = os.path.join(log_dir,'info.log')
    error_file = os.path.join(log_dir,'error.log')

    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')

    ch = logging.StreamHandler()
    ch.setLevel('DEBUG')
    ch.setFormatter(formatter)

    handler = logging.FileHandler(filename=log_file, encoding='utf-8')
    handler.setLevel('INFO')
    handler.setFormatter(formatter)

    error_handle = logging.FileHandler(filename=error_file, encoding='utf-8')
    error_handle.setLevel('ERROR')
    error_handle.setFormatter(formatter)

    report_handler = logging.StreamHandler(HTMLTestRunnerNew.stdout_redirector)
    report_handler.setLevel('INFO')
    report_handler.setFormatter(formatter)

    @staticmethod
    def debug(msg):
        set_handler('debug')
        logger.debug(msg)
        remove_handler('debug')

    @staticmethod
    def info(msg):
        set_handler('info')
        logger.info(msg)
        remove_handler('info')

    @staticmethod
    def error(msg):
        set_handler('error')
        logger.error(msg, exc_info=True)  # 同时输出异常信息
        remove_handler('error')

if __name__ == '__main__':
    try:
        raise AssertionError
    except AssertionError as e:
        MyLog.error('error!!!')