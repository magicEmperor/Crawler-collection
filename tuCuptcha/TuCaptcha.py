'''
    简单的图形验证码
    利用 OCR 技术识别图形验证码
    中国知网"http://my.cnki.net/elibregister/commonRegister.aspx"
'''
import requests
import lxml
from bs4 import BeautifulSoup as bs

HEADER = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'ASP.NET_SessionId=mfziaxbyvzecyv520n5sj34e; SID=020102',
    'Host':'my.cnki.net',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}

url = "http://my.cnki.net/elibregister/"
rsp = requests.get(url+'commonRegister.aspx#',headers=HEADER)
# print(rsp)
html = bs(rsp.text,'html.parser')
print(html.prettify())
img_code = html.find(name='img',attrs={'id':'checkcode'})
img_url = img_code.get('src')
img_data = requests.get(url+img_url,headers=HEADER)
with open('va.jpg','wb') as f:
    f.write(img_data.content)


# http://my.cnki.net/elibregister/CheckCode.aspx 验证码图片地址