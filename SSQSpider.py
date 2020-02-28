"""
    根据期号爬取对应双色球序列和开奖日期
    使用mongoDB存储数据
"""
import json
from urllib.parse import urlencode

import pymongo
import requests
from config import *

data = {
    'name': 'ssq',
    'issueCount': 30,
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'www.cwl.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
    'Cookie': 'Sites=_21; UniqueID=yorWRXPQeuPxdful1582852216903; _ga=GA1.3.1738058863.1580821227; _gid=GA1.3.2125694018.1582852217; _Jo0OQK=4C6441CCBD5084F567BE774821EC1D3628E5F49893E73A67E04E3C172197E31770D331988DC7B0F714BD8A56E197075B6DB408A06281124A025EE643D8CFF4C65E0F1B3C19C5B2FC5F8E6E66EDA7420CD4BE6E66EDA7420CD4B0843FEEF9AD95C656011E4DFAAE0DD7EGJ1Z1Qg==; _gat_gtag_UA_113065506_1=1; 21_vq=26',
    'X-Requested-With': 'XMLHttpRequest',
}


# 获取页面信息
def get_page_num():
    url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?" + urlencode(data)
    print(url)
    response = requests.get(url, headers=headers)
    # print(response.text)
    return parser_page(response)


# 解析返回数据
def parser_page(response):
    result = json.loads(response.text).get('result')
    for item in result:
        yield {
            'name': item['name'],
            'code': item['code'],
            'date': item['date'],
            'red': item['red'],
            'blue': item['blue'],
        }


# 数据保存到MongoDB
def save_to_mongo(data):
    client = pymongo.MongoClient(MONGO_URL)
    db = client['SSq']
    if data:
        db['SSq_table'].insert_one(dict(data))
        print("数据插入成功！")
    else:
        return "数据插入失败！"


def run():
    generator = get_page_num()
    for i in generator:
        save_to_mongo(i)


if __name__ == '__main__':
    run()
