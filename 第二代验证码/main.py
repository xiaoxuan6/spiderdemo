# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/17 16:02
 @File: main.py
 @Description: 第二代验证码
    webp 转 png
    图片修改大小
    识别滑块距离
"""
import base64
import os
import time

import requests
from PIL import Image
from ddddocr import DdddOcr
from base import *

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/captcha/cap4_challenge/?challenge_type=cap1_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    response = requests.get('https://www.spiderdemo.cn/captcha/api/cap4_challenge/init/?challenge_type=cap4_challenge',
                            headers=headers, cookies=cookies).json()
    return sum(response.get('page_data'))


def parse_captcha():
    params = {
        't': str(int(time.time() * 1000))
    }
    resp = requests.get('https://www.spiderdemo.cn/captcha/api/cap4_challenge/captcha_image', params=params,
                        headers=headers, cookies=cookies).json()
    # print(resp)

    # save webp
    with open('captcha.webp', 'wb') as f:
        f.write(base64.b64decode(resp.get('overlay')))

    # save png
    with open('slider.png', 'wb') as f:
        f.write(base64.b64decode(resp.get('masked')))

    # webp to png
    with Image.open('captcha.webp') as img:
        img.save('captcha.png', "PNG")

    return resp.get('captcha_id'), resp.get('slider_y')


def parse_image():
    Image.open('captcha.png').resize((378, 218)).save('captcha.png')
    Image.open('slider.png').resize((54, 45)).save('slider.png')


def parse_captcha_distance():
    det = DdddOcr(show_ad=False, det=True)
    result = det.slide_match(open('slider.png', 'rb').read(), open('captcha.png', 'rb').read(), simple_target=True)
    # print(result)
    return result['target'][0]


def parse_data(captcha_id, distance, page):
    json_data = {
        'captcha_id': captcha_id,
        'challenge_type': 'cap4_challenge',
        'container_height': 220,
        'container_width': 380,
        'distance': distance,
        'page_num': page
    }
    response = requests.post('https://www.spiderdemo.cn/captcha/api/cap4_challenge/page/', json=json_data,
                             headers=headers, cookies=cookies).json()
    # print(response)
    if not response.get('success'):
        print("验证失败，重试中……")
        captcha_id, slider_y = parse_captcha()
        parse_image()
        distance = parse_captcha_distance()
        return parse_data(captcha_id, distance, page)

    return sum(response.get('page_data'))


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print(f"第 {page} 页")
        captcha_id, slider_y = parse_captcha()
        parse_image()
        distance = parse_captcha_distance()
        count += parse_data(captcha_id, distance, page)

    print(count)

    os.remove('captcha.png')
    os.remove('captcha.webp')
    os.remove('slider.png')
