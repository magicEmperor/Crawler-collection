import requests



rsp = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%('wx27c0e6ef6a7f0716','6e29e232daf462652f66ee8acc11838b'))
print(rsp.text)