__author__ = 'ghm'

import re

# s = 'www.lemonban.com'
# p = '(w)(ww)'
# m = re.search(p,s)
# print(m)
# print(m.group()) # Return one or more subgroups of the match.
# print(m.group(1))
# print(m.group(2))

s1 = '{"mobilephone":"${normal_user}","pwd":"${pwd}"}'
p = '\$\{(.*?)\}'
while re.search(p,s1):
    m = re.search(p,s1)
    key = m.group(1)
    from common.basic_data import Context
    user = getattr(Context,key)
    s1 = re.sub(p,user,s1,count=1) # count=0 合部匹配并替换，count=1只匹配一个
print(s1)




