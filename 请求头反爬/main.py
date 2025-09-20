# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/17 9:04
 @File: main.py
 @Description:
"""

'''
1、请求头顺序反爬
2、使用了 http2
'''
from curl_cffi import requests

from base import base


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            "sec-ch-ua-platform": "\"Windows\"",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.spiderdemo.cn/sec1/header_check/",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cookie": "sessionid=ob8ssjwg5kjtowva80gknrkz8b8t70zm",
            "priority": "u=1, i"
        }

    def fetch_page(self, page):
        print("第 %d 页" % page)
        params = {
            "challenge_type": "header_check"
        }

        resp = requests.get('https://www.spiderdemo.cn/sec1/api/challenge/page/%d' % page, headers=self.headers,
                            cookies=self.cookies, params=params).json()
        return sum(resp['page_data'])


if __name__ == '__main__':
    s = spider()
    s.run()
