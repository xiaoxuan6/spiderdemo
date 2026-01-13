# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/11/5 19:15
 @File: main.py
 @Description: 
"""
import requests

from base import base


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://antispider.top',
            'Referer': 'http://antispider.top/challenge/13',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

    def fetch_page(self, page):
        while True:
            try:
                response = requests.get('http://antispider.top/api/common/collect', cookies=self.cookies,
                                        headers=self.headers, verify=False)
                json_data = {
                    'page': str(page),
                }

                resp = requests.post('http://antispider.top/api/challenge/13', cookies=self.cookies,
                                     headers=self.headers,
                                     json=json_data,
                                     verify=False)
                data = resp.json().get('data')
                print(data)

                if data:
                    if data.get('page', 0):
                        return sum(data.get('numbers'))
                    else:
                        print(f'{page}: {data.get('msg')}')

            except Exception as e:
                print(f"{page}: {e}")


if __name__ == '__main__':
    s = spider()
    s.run()
