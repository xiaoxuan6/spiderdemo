# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/13 9:44
 @File: main.py
 @Description: 
"""
import base64
import time

import requests
from PIL import Image
from ddddocr import DdddOcr

import base

headers = {
    "referer": "https://www.spiderdemo.cn/captcha/cap5_challenge/?challenge_type=cap5_challenge",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": base.config['Session']['value']
}


def parse_page():
    response = requests.get('https://www.spiderdemo.cn/captcha/api/cap5_challenge/init/?challenge_type=cap5_challenge',
                            headers=headers, cookies=cookies).json()
    return sum(response.get('page_data'))


def parse_captcha(count):
    det = DdddOcr(show_ad=False, det=True)

    for p in range(2, 101):
        while True:
            try:
                print('第 %d 页' % p)
                url = "https://www.spiderdemo.cn/captcha/api/cap5_challenge/captcha_image/"
                params = {
                    "t": str(int(time.time() * 1000))
                }
                response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
                # # print(response)

                open('captcha.webp', 'wb').write(base64.b64decode(response.get('overlay')))
                Image.open('captcha.webp').save('captcha.png')

                result = det.slide_match(base64.b64decode(response.get('masked')), open('captcha.png', 'rb').read(),
                                         simple_target=True)
                distance = result['target'][0] * 378 / 840
                # print(distance)

                url = "https://www.spiderdemo.cn/captcha/api/cap5_challenge/page/"
                data = {
                    "distance": int(distance),
                    "page_num": p,
                    "challenge_type": "cap5_challenge",
                    "container_width": 380,
                    "container_height": 220
                }
                response = requests.post(url, headers=headers, cookies=cookies, json=data).json()
                # print(response)
                count += sum(response.get('page_data'))
                break
            except:
                print('识别失败，重试')

    print(count)


if __name__ == '__main__':
    parse_captcha(parse_page())
