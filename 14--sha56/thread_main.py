# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2026/1/11 12:20
 @File: thread_main.py
 @Description: 
"""
import hashlib
import random
import time

import requests

from base import base


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'http://antispider.top',
            'Referer': 'http://antispider.top/challenge/14',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

    def fetch_page(self, page):
        while True:
            try:
                time.sleep(random.uniform(0, 0.6))
                timestamp = str(int(time.time() * 1000))
                json_data = {
                    'page': str(page),
                    'timestamp': timestamp,
                    'sign': hashlib.sha256(timestamp.encode()).hexdigest(),
                }
                response = requests.post(
                    'http://antispider.top/api/challenge/14',
                    headers=self.headers,
                    cookies=self.cookies,
                    json=json_data,
                    verify=False
                ).json()
                print(response)

                data = response.get('data', {})
                if not data:
                    print(response.get('msg'))
                else:
                    return sum(data.get('numbers', []))

            except:
                print(f"第 {page} 页获取数据失败，重试中……")

if __name__ == '__main__':
    s = spider()
    s.run()
