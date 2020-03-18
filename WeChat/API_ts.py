import requests
import json
ac_tk = '31_gAQBnCX7a2-inYJO0LZIxJcRiNJnPYXjQtXDeRi-zjRhqhDRxWgANdaS6yruzYw62fLUCzve3a5fBG3N6LkBd6Qb3lDZqqXpKSelXQVihKc6pDMOkPOWuK3aoulvyjy-C-V9REULQsB-jNr6DJBfAIAKQI'
rsp = requests.get('https://api.weixin.qq.com/cgi-bin/tags/create?access_token={}'.format(ac_tk),data=json.dumps({   "tag" : {     "name" : "广东"  } } ))
print(rsp.text)