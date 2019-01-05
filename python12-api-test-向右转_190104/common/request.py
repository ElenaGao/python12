#-*- coding:utf-8 _*-  
""" 
@author:mongo
@file: request.py 
@version:
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""

import requests
from common.config import ConfigLoader

class Request:

    def __init__(self,method,url,data=None,cookies=None,headers=None):
        config = ConfigLoader()
        url_pre = config.get('api','url_pre')
        try:
            if method == 'get':
                self.resp = requests.get(url=url_pre+url, params=data, cookies=cookies, headers=headers)
            elif method == 'post':
                self.resp = requests.post(url=url_pre+url, data=data, cookies=cookies, headers=headers)
            elif method == 'delete':
                self.resp = requests.delete(url=url_pre+url, data=data, cookies=cookies, headers=headers)
        except Exception as e:
            raise e


    def get_status_code(self):
        return self.resp.status_code

    def get_text(self):
        return self.resp.text

    def get_json(self):
        return self.resp.json()

    def get_cookies(self,key=None):
        if key is not None:
            return self.resp.cookies[key]
        else:
            return self.resp.cookies
