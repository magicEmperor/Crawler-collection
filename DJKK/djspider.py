import requests
import logging
from lxml import etree

__name__ = "六月"

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt",encoding="utf-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# logger.info("Start print log")
# logger.debug("Do something")
# logger.warning("Something maybe fail.")
# logger.info("Finish")
def run():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "UM_distinctid=17107778d15625-06b63543e6df1b-f313f6d-1fa400-17107778d16493; bdshare_firstime=1584968259888; BAIDU_SSP_lcr=https://www.baidu.com/link?url=TDdQSyUO8R4x0U3yWZR2JKvZK4Cbq91ONmP0eH6zslu&wd=&eqid=c0297c1000027d2c000000055e7c4221; CNZZDATA30033759=cnzz_eid%3D252986839-1584966576-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1585200490",
        "Host": "www.djkk.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    logger.info("开始获取网页信息")
    rsp = requests.get(url="http://www.djkk.com/", headers=headers)
    print(rsp.text)
    html = etree.HTML(rsp.text)
    logger.info("开始获取页面所有歌曲的超链接节点")
    jiedian_list = html.xpath("//ul/li/dl/dd/a")
    for i in jiedian_list:
        print(etree.tostring(i).decode("utf-8"))

if  __name__ == '六月':
    run()