"""
    实现今日头条街拍图集抓取

"""
import json
import os
import re
from hashlib import md5
from multiprocessing.pool import Pool

import pymongo
from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
# 导入配置文件所有参数
from config import *

# 创建MongoDB连接对象
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
# 当前目录下创建photo文件夹
if not os.path.exists("photo"):
    os.mkdir('photo')
# 构造必要的请求头参数
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'tt_webid=6796876210003592711; s_v_web_id=verify_k7006qe3_cjfE8ez2_r9Ld_4H7G_8u19_R6vgNKCgnNU8; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6796876210003592711; ttcid=7a6427be702a4fe7b485588c5d77c6a441; __tasessionId=255yyf17z1582521075292; csrftoken=6fe6d283b2faef38ee1ae12f8db02091; tt_scid=3TjZ-tGLZeT3GoUHjhAD8FnvF2xIYQD9Zyn3fgUEiTlY2aElVFG7uFWRHGAZkNIQb835',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


class Spider():
    # 初始化对象属性
    def __init__(self, offset, keyword):
        self.url = "https://www.toutiao.com/api/search/content/?"
        self.headers = headers
        self.data = {
            'aid': 24,
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': keyword,
            'autoload': 'true',
            'count': 20,
            'en_qc': 1,
            'cur_tab': 1,
            'from': 'search_tab',
            'pd': 'synthesis',
            'timestamp': 1582612780633,
        }

    # 获取详情页返回的数据
    def get_page_index(self, detail_url=""):
        # 做一个简单的复用构造
        if detail_url == "":
            url = self.url + urlencode(self.data)
        else:
            url = detail_url
        try:
            response = requests.get(url, headers=self.headers)
        except RequestException:
            return response.status_code
        return response

    # 获取首页信息
    def parse_page_index(self):
        html = self.get_page_index()
        urldata = json.loads(html.text)
        return urldata

    # 获取详情页的Url集合
    def get_urls(self, data):
        items = data.get('data')
        for item in items:
            if item.get('article_url') != None:
                yield item.get('article_url')  # 构造一个生成器

    # 针对详情页链接获取图片页面信息
    def get_img_parser(self, url):
        html = self.get_page_index(url)
        soup = bs(html.text, 'lxml')
        title = soup.select("title")[0].get_text()
        img_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
        img_info = re.search(img_pattern, html.text)
        if img_info:
            # 调整数据结构，使其变成json格式
            info = re.sub(r'\\\"', '"', str(img_info.group(1)))
            json_img_info = json.loads(info)
            img_url_items = json_img_info.get("sub_images")
            urls_item = [item.get("url") for item in img_url_items]
            # 将链接格式成有效链接
            str_urls_item = re.sub("\\\\", "", str(urls_item))
            dict_info = {
                'title': title,
                'url': url,
                'images': eval(str_urls_item)
            }
            self.save_to_mongo(dict_info)
            self.download_img(eval(str_urls_item))

    # 将数据写入到MongoDB中
    def save_to_mongo(self, image_info):
        if image_info != None:
            if db[MONGO_TABLE].insert(image_info):
                print("数据插入成功", image_info)
                return True
            return False

    # 下载图片信息
    def download_img(self, img_urls):
        for url in img_urls:
            img_detail = self.get_page_index(url)
            self.save_img(img_detail.content, url)

    # 保存图片到当前位置的photo文件夹
    def save_img(self, img_detail, url):
        filePath = "{0}\{1}\{2}.{3}".format(os.getcwd(), 'photo', md5(img_detail).hexdigest(), 'jpg')
        if filePath:
            with open(filePath, 'wb') as f:
                f.write(img_detail)
                f.close()
            print("正在下载:", url)


def run(num):
    spider = Spider(num, KEYWORD)
    data = spider.parse_page_index()
    urls = spider.get_urls(data)
    for url in urls:
        spider.get_img_parser(url)


if __name__ == '__main__':
    pool = Pool()
    pool.map(run, [i * 20 for i in range(START_NUM, END_NUM + 1)])
