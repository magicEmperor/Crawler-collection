'''
    简单的图形验证码
    利用 OCR 技术识别图形验证码
    中国知网"http://my.cnki.net/elibregister/commonRegister.aspx"
'''
from _md5 import md5
from PIL import Image
import requests
import os
import tesserocr

from bs4 import BeautifulSoup as bs
import time

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
# print(html.prettify())
img_code = html.find(name='img',attrs={'id':'checkcode'})
img_url = img_code.get('src')
img_data = requests.get(url+img_url,headers=HEADER)

# if  not os.path.exists('picture'):
#     os.mkdir(os.getcwd()+'\picture')
path = os.getcwd()+'\picture'
# path+'\img.jpg'
# filename = '{0}{1}'.format(md5(img_data.content).hexdigest(),'jpg')
with open(path+'.jpg','wb') as f: # str(time.strftime('%m-%d-%y',time.localtime(time.time())))
    f.write(img_data.content)
print('图片保存成功。。。')

img = Image.open('picture.jpg')
# info = tesserocr.image_to_text(img)
# print(info)
# 图片进行灰度处理
img = img.convert('L')
# img.show()
# 图片进行二值处理
threshold = 150
table = []
for i in range(256):
    if i<threshold:
        table.append(0)
    else:
        table.append(1)
img = img.point(table,'1')
# img = img.convert('1')
img.show()

# http://my.cnki.net/elibregister/CheckCode.aspx 验证码图片地址