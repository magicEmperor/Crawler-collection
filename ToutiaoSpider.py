import json

import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException

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
            'timestamp': 1582523983867,
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
        return response.text

    # 获取首页信息
    def parse_page_index(self):
        html = self.get_page_index()
        urldata = json.loads(html)
        return urldata

    # 获取详情页的Url集合
    def get_urls(self, data):
        # print(urldata.get('data'))
        items = data.get('data')
        # print(items)
        for item in items:
            if item.get('article_url') != None:
                yield item.get('article_url')  # 构造一个生成器
                # print(item.get('article_url'))


if __name__ == '__main__':
    spider = Spider(0, "街拍")
    data = spider.parse_page_index()
    # print(data.get('data'))
    # print(spider.get_urls(data))
