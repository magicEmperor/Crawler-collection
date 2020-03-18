'''
    爬取猫眼电影TOP100榜单电影信息
'''
import json
from multiprocessing import Pool

import requests
from requests.exceptions import RequestException
import re


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}

# 请求榜单首页，并获取页面信息
def get_one_page(url):
    # 捕获请求异常
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return response.status_code
    # 抛出异常状态码
    except RequestException:
        return response.status_code

# 获取页面信息
def parser_page_source(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?<p class="name".*?title="(.*?)".*?</p>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>',
        re.S)
    data = re.findall(pattern, html)
    # print(data)
    # 制作生成器
    for i in data:
        yield {
            'index': i[0],
            'name': i[1],
            'actor': i[2].strip()[3:],
            'datetime': i[3].strip()[5:]
        }

# 将数据写入文件
def write_to_file(i):
    with open('moveis.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(i, ensure_ascii=False) + '\n')
        f.close()


def run(num):
    url = "https://maoyan.com/board/4?offset=" + str(num)
    html = get_one_page(url)
    data = parser_page_source(html)
    # print(data)
    for i in data:
        print(i)
        write_to_file(i)


if __name__ == '__main__':
    # 可用多进程实现快速抓取
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])
    pool.map(run, [i for i in range(0, 100, 10)])
