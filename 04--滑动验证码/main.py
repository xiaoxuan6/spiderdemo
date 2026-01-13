# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/21 12:25
 @File: main.py
 @Description: 
"""
import base64
import pprint

import requests
from ddddocr import DdddOcr

from base import base


# se = requests.session()
# headers = {
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "Cache-Control": "no-cache",
#     "Pragma": "no-cache",
#     "Proxy-Connection": "keep-alive",
#     "Referer": "http://antispider.top/challenge/04",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
# }
# cookies = {
#     "sessionId": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiN2ZmNzc3ZmQtNzE4Ni00ZDg1LThiNjctNWRhYjQyMGVjMjgwIiwiSUQiOjgsIlVzZXJuYW1lIjoiMTUyNjU5MjYxNzgiLCJCdWZmZXJUaW1lIjo4NjQwMCwiaXNzIjoicW1QbHVzIiwiYXVkIjpbIkFOVEkiXSwiZXhwIjoxNzY4NzA3OTU1LCJuYmYiOjE3NjgxMDMxNTV9.xh1MXgi0FKlaUNyDI9hBWc-nt_IH38jVNKHpxXbpgXo"
# }
# url = "http://antispider.top/api/captcha/slide"
# response = se.get(url, headers=headers, cookies=cookies, verify=False).json()
# pprint.pprint(response)
#
# open('captcha.png', 'wb').write(base64.b64decode(response.get('data').get('bgImage').split(',')[-1]))
# open('s_captcha.png', 'wb').write(base64.b64decode(response.get('data').get('sliderImage').split(',')[-1]))
#
# det = DdddOcr(show_ad=False, det=True)
# result = det.slide_match(
#     base64.b64decode(response.get('data').get('sliderImage').split(',')[-1]),
#     base64.b64decode(response.get('data').get('bgImage').split(',')[-1]),
#     simple_target=True
# )
#
# # recognizer = Recognizer()
# # result = recognizer.identify_gap(base64.b64decode(response.get('data').get('bgImage').split(',')[-1]), is_single=True)
#
# print(result)
# distance = result['target'][0]
# # print(distance)
#
# resp = se.post('http://antispider.top/api/captcha/slide/verify', headers=headers, cookies=cookies, json={
#     'captchaId': response.get('data').get('captchaId'),
#     'distance': distance
# }).json()
# print(resp)
#
# if resp.get('data', {}).get('token', ''):
#     url = "http://antispider.top/api/challenge/04"
#     data = {
#         "page": "1",
#         "token": resp.get('data').get('token')
#     }
#     response = se.post(url, headers=headers, cookies=cookies, json=data, verify=False)
#
#     print(response.text)
#     print(response)


class spider(base):
    def __init__(self):
        super().__init__()
        self.se = requests.session()
        self.det = DdddOcr(show_ad=False, det=True)
        self.headers = {
            "Referer": "http://antispider.top/challenge/04",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        # self.max_page = 2

    def fetch_captcha(self):
        response = self.se.get("http://antispider.top/api/captcha/slide", headers=self.headers, cookies=self.cookies,
                               verify=False).json()
        # pprint.pprint(response)
        return response

    def parse_captcha(self, response: dict):
        result = self.det.slide_match(
            base64.b64decode(response.get('data').get('sliderImage').split(',')[-1]),
            base64.b64decode(response.get('data').get('bgImage').split(',')[-1]),
            simple_target=True
        )

        return result['target'][0]

    def verify_captcha(self, distance, response: dict):
        resp = self.se.post('http://antispider.top/api/captcha/slide/verify', headers=self.headers,
                            cookies=self.cookies,
                            json={
                                'captchaId': response.get('data').get('captchaId'),
                                'distance': distance
                            }).json()
        # print(resp)

        data = resp.get('data', {})
        if data:
            return data.get('token')
        else:
            raise Exception(resp.get('msg'))

    def fetch_data(self, page, token: str):
        url = "http://antispider.top/api/challenge/04"
        data = {
            "page": str(page),
            "token": token
        }
        # pprint.pp(data)
        response = self.se.post(url, headers=self.headers, cookies=self.cookies, json=data, verify=False).json()
        # print(response)

        data = response.get('data', {})
        if data:
            return sum(data.get('numbers', []))
        else:
            raise Exception(response.get('msg'))

    def fetch_page(self, page):
        while True:
            try:
                response = self.fetch_captcha()
                return self.fetch_data(page, self.verify_captcha(self.parse_captcha(response), response))
            except Exception as e:
                print(f"{page}: {e}")

    def main(self):
        for page in range(1, self.max_page):
            self.count += self.fetch_page(page)

        print("计算总和：", self.count)


if __name__ == '__main__':
    s = spider()
    s.run()
    # s.main() # 5641283
