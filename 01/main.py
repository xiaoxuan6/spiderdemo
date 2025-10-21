# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/21 11:14
 @File: main.py
 @Description: 
"""
import requests

from base import base


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Origin": "http://antispider.top",
            "Referer": "http://antispider.top/challenge/01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        # self.max_page = 2

    def fetch_page(self, page):
        while True:
            try:
                url = "http://antispider.top/api/challenge/01"
                data = {
                    "page": str(page)
                }
                response = requests.post(url, headers=self.headers, cookies=self.cookies, json=data,
                                         verify=False).json()
                print(response)

                return sum(response.get('data').get('numbers'))
            except:
                print("第 %d 页 获取失败，重试中……" % page)


if __name__ == '__main__':
    s = spider()
    s.run()
