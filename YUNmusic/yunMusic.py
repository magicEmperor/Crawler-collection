from urllib.parse import urlencode
from lxml import etree
from config import HEADER
import requests
import pymongo
import re

MONGO_URL = 'localhost'
MONGO_DB = 'MusicDB'
MONGO_TABLE = 'MusicTb'
g_url = 'https://music.163.com'

# 获取专辑页面
def music_index(ID):
    data = {
        'id' : ID
    }
    url = g_url+'/artist/album?'+urlencode(data)
    rsp = requests.get(url,headers=HEADER)
    # print(rsp.text)
    html = etree.HTML(rsp.text)
    items = html.xpath('//ul[@id="m-song-module"]/li')
    for item in items:
        # print(etree.tostring(item).decode('utf-8'))
        str_data = etree.tostring(item).decode('utf-8')
        patImg = re.compile('<img src="(.*?)"')
        patUrl = re.compile('<a href="(.*?)"')
        str_img = patImg.search(str_data,re.S).group(1)
        str_url = patUrl.search(str_data,re.S).group(1)
        yield {
            'img': str_img,
            'url': str_url
        }

# 拼接Url链接
def music_detail_url(items):
    urls = []
    for item in items:
        # data = json.loads(item)
        urls.append(g_url+item.get('url'))
    return urls

# 获取专辑歌曲信息
def get_music_detail(url):
    rsp = requests.get(url,headers=HEADER)
    for cookie in rsp.cookies:
        print(cookie.value)
    html = etree.HTML(rsp.text)
    mname = html.xpath('//ul[@class="f-hide"]/li/a')
    name_list = [etree.tostring(name).decode('utf-8') for name in mname]
    for jname in name_list:
        pat = re.compile('<a href="(.*?)">(.*)</a>',re.S)
        href = pat.search(jname).group(1)
        zname = pat.search(jname).group(2)
        tname = re.sub('&#','',zname)
        # print(href,tname)
        shuzi = re.findall('\d+|[\(\)a-zA-Z]',tname)
        # print(shuzi)
        shuzi_list=[]
        for i in shuzi:
            if i=='(' or i==')' or 'a'<=i<='z' or 'A'<=i<='Z':
                shuzi_list.append(i)
                # 处理英文空格
                # if 'A'<=i<='Z':
                #     shuzi_list.append(" "+i)
                # else:
                #     shuzi_list.append(i)
            elif int(i)<=65535:
                shuzi_list.append(chr(int(i)))
            else:
                print("失败")
            # else:
            #     shuzi_list.append(chr(int(i)))
        # print(shuzi_list)
        zzname = "".join(shuzi_list)
        # print(href,zzname)
        xname = zzname
        yield {
            'url': href,
            'name': xname
        }


    # data = etree.tostring(mname[0]).decode('utf-8')
    # with open('xx.txt','w') as f:
    #     f.write(str(data))
    # Qdata = re.search('>([.*])<',data,re.S)
    # print(Qdata)

# 保存数据到MongoDB
def save_to_mongo(music_data):
    client = pymongo.MongoClient(MONGO_URL, connect=False)
    db = client[MONGO_DB]
    if music_data != None:
        if db[MONGO_TABLE].insert(music_data):
            print("数据插入成功", music_data)
            return True
        return False

def run():
    items = music_index(ID=11127)
    urls = music_detail_url(items)
    for i in urls:
        data_info = [i for i in get_music_detail(i)]
        # print(type(data_info))
        save_to_mongo(data_info)




