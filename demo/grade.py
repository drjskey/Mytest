

import requests
url='http://ci.ytesting.com/api/3school/school_classes'
# 列出年级
payload = {"vcode":"00000010893537273822",
           "action":"list_classes_by_schoolgrade",
           "gradeid":None}
res = requests.get(url=url,params=payload)
print(res.json())
