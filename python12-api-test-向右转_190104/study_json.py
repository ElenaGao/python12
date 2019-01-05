#-*- coding:utf-8 _*-  
""" 
@author:mongo
@file: study.py 
@version:
@time: 2018/12/17 
@email:3126972006@qq.com
@function： 
"""

import json
dict_obj = {"status": 0, "code": "20111", "data": None, "msg": "用户名或密码错误"}
str_obj = json.dumps(dict_obj,ensure_ascii=False,indent=4)
# print(str_obj)



str_test = '{"status": 0, "code": "20111", "data": null, "msg": "用户名或密码错误"}'
str2 = '{"a":[1,2],"b":["c","d"]}' # json是一个跨语言的数据类型，python，Java，C
dict_test =json.loads(str2)
# print(dict_test['msg'])
# print(type(dict_test))
# print(type(dict_test))

# #load 将文件里面的json 反序列成str
# f = open('datas/data.json')
# s = json.load(f)
# print(type(s))

#dump 将dict写入到文件
dict_obj={'a':1,'b':2}
f = open('datas/data.json','w+')
json.dump(dict_obj,fp=f)

#load 将文件里面的json 反序列成str
f = open('datas/data.json')
# s = json.load(f)
print(type(f.read()))