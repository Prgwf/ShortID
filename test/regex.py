import re

urls = [
    'www.baidu.com',
    'http://baidu.com',
    'http://www.baidu.com',
    'https://baidu.com',
    'https://www.baidu.com'
]

pattern = re.compile(r'://')
for i in urls:
    t=pattern.split(i)
    if len(t)>1:
        print(t[1])
    else:
        print(t[0])