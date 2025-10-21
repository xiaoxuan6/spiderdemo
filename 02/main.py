# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/21 12:15
 @File: main.py
 @Description: 
"""
import requests

from base import base


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Host": "antispider.top",
            "Content-Length": "12",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "http://antispider.top",
            "Referer": "http://antispider.top/challenge/02",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        # self.max_page = 2

    def fetch_page(self, page):
        while True:
            try:
                url = "http://antispider.top/api/challenge/02"
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