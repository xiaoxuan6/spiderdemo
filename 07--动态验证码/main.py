# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/21 13:01
 @File: main.py
 @Description: 
"""
import base64
import glob
import io

import requests

from base import base


def parse_captcha(response):
    from PIL import Image

    img = Image.open(io.BytesIO(base64.b64decode(response.get('data').get('image').split(',')[-1])))
    num_frames = img.n_frames

    from ddddocr import DdddOcr

    text = glob
    ocr = DdddOcr(show_ad=False)
    for i in range(num_frames):
        img.seek(i)
        i_frame = img.copy()
        text = ocr.classification(i_frame)
        if len(text) == 4:
            break

    return text


class spider(base):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Referer": "http://antispider.top/challenge/07",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        # self.max_page = 2
        self.re = requests.session()

    def fetch_page(self, page):
        print('第 %d 页' % page)
        while True:
            try:
                url = "http://antispider.top/api/captcha/gif"
                response = self.re.get(url, headers=self.headers, cookies=self.cookies, verify=False).json()
                # print(response)

                text = parse_captcha(response)
                # print('text：' + text)
                token = self.parse_captcha_verify(response.get('data').get('captchaId'), text)
                if token is not None:
                    return self.parse_data(token, page)

                print('第 %d 页 验证失败，重试……' % page)
            except Exception as e:
                print(f"{page}: {e}")


    def parse_captcha_verify(self, captchaId, text):
        data = {
            'captchaId': captchaId,
            'text': text
        }
        resp = self.re.post('http://antispider.top/api/captcha/gif/verify', headers=self.headers, cookies=self.cookies,
                             json=data)
        print(f"验证结果：{resp.text}")
        if resp.json().get('code') == 0:
            return resp.json().get('data').get('token')

        return None

    def parse_data(self, token, page):
        data = {
            'token': token,
            'page': str(page)
        }
        resp = self.re.post('http://antispider.top/api/challenge/07', headers=self.headers, cookies=self.cookies,
                             json=data)

        print(resp.text)
        return sum(resp.json().get('data').get('numbers'))

    def main(self):
        count = 0
        for page in range(1, 101):
            count += self.fetch_page(page)
        print(count)


if __name__ == '__main__':
    s = spider()
    # s.main()
    # 线程
    s.run()
