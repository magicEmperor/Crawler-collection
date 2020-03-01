"""
    根据期号爬取对应双色球序列和开奖日期
    使用mongoDB存储数据
"""
import json
from urllib.parse import urlencode

import pymongo
import requests
from config import *


class CP():
    def __init__(self, name):
        self.data = {
            'name': name,
            'issueCount': 30,   # 最大数值只能到最近100期
        }
        self.url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?" + urlencode(self.data)

    # 获取页面信息
    def get_page_num(self):
        response = requests.get(self.url, headers=HEADERS)
        # print(response.text)
        return self.parser_page(response)

    # 解析返回数据
    def parser_page(selef, response):
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
    def save_to_mongo(self, data):
        client = pymongo.MongoClient(MONGO_URL)
        db = client['CP']
        if data:
            db[data.get('name')].insert_one(dict(data))
            print(data, "数据插入成功！")
        else:
            return "数据插入失败！"


def run(name):
    cp = CP(name)
    generator = cp.get_page_num()
    for i in generator:
        cp.save_to_mongo(i)

if __name__ == '__main__':
    run("qlc")
