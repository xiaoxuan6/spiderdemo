# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/11 19:34
 @File: main.py
 @Description: 
"""
import base64
import time

import requests
from ddddocr import DdddOcr

import base

headers = {
    "referer": "https://www.spiderdemo.cn/captcha/cap6_challenge/?challenge_type=cap6_challenge",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": base.config['Session']['value']
}

response = requests.get('https://www.spiderdemo.cn/captcha/api/cap6_challenge/init/?challenge_type=cap6_challenge',
                        headers=headers, cookies=cookies).json()
count = sum(response.get('page_data'))
print(count)

det = DdddOcr(show_ad=False, det=True)

for page in range(2, 101):
    print('第 %d 页' % page)

    while True:
        slider1 = 0
        slider2 = 0
        load_img = True

        try:
            url = "https://www.spiderdemo.cn/captcha/api/cap6_challenge/captcha_image/"
            params = {
                "t": str(int(time.time() * 1000))
            }
            response = requests.get(url, headers=headers, cookies=cookies, params=params).json()

            # with open('a.webp', 'wb') as f:
            #     f.write(base64.b64decode(response.get('overlay')))
            #
            # with Image.open('a.webp') as img:
            #     img.save('captcha.png', "PNG")

            distance = det.slide_match(base64.b64decode(response.get('sliders')[0].get('masked')),
                                       base64.b64decode(response.get('overlay')))
            slider1 = int(distance['target'][0] * 378 / 840)
            # print(distance, slider1)

            distance = det.slide_match(base64.b64decode(response.get('sliders')[1].get('masked')),
                                       base64.b64decode(response.get('overlay')))
            slider2 = int(distance['target'][0] * 378 / 840 - 12)
            # print(distance, slider2)
        except:
            load_img = False
            print("获取滑块失败")

        if load_img:
            url = "https://www.spiderdemo.cn/captcha/api/cap6_challenge/page/"
            data = {
                "distances": {
                    "slider1": slider1,
                    "slider2": slider2
                },
                "page_num": page,
                "challenge_type": "cap6_challenge",
                "captcha_id": response.get('captcha_id'),
                "container_width": 380,
                "container_height": 220
            }
            resp = requests.post(url, headers=headers, cookies=cookies, json=data).json()
            print(resp)
            # break

            if resp.get('success'):
                count += sum(resp.get('page_data'))
                break

print(count)
