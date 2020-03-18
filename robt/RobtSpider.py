'''
    爬取公司后台外呼数据
'''

import json
import requests
from requests.exceptions import RequestException
import re

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

data = {
    'currentPage': 1,
    'pageSize': 10,
    'taskNature': 1
}
def get_TK():
    d = {"username":"SHmanage01","password":"sh556677"}
    rsp = requests.post('http://47.101.64.78:7090/api/home/loginUser',data=d,headers=headers)
    aztion = json.loads(rsp.text)['data']['token']
    headers['Authorization'] = str(aztion)
    return headers

class robtSpider():
    def __init__(self):
        self.headers = get_TK()
        self.data = data

    # 获取单个页面的数据
    def get_pages_one(self):
        try:
            # 获取页面的Response
            response = requests.get(url = 'http://47.101.64.78:7090/api/task/searchTaskList', headers=self.headers, data=self.data)
            # print(response.text)
            # print(type(response.text))
            # 整理返回数据
            data = json.loads(response.text)
            print(data)
            items = data.get("data")['pageInfo'].get("list")
            print(items)
            result = re.sub('},', '}\n', str(items))
            for item in items:
                print(item)

            return result

        except RequestException:
            return requests.status_codes

    # 将数据写入文本
    def write_to_file(self, items):
        with open("任务数据.txt", 'a', encoding='utf-8') as f:
            f.write(items+'\n')
            f.close()

    def run(self):
        data = self.get_pages_one()
        self.write_to_file(str(data))


if __name__ == '__main__':
    spider = robtSpider()
    spider.run()
