# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/19 17:01
 @File: main.py
 @Description: 
"""
import base64
import os
import time

import requests
from PIL import Image

from captcha_api import captcha_identify
from base import *

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/captcha/cap3_challenge/?challenge_type=cap3_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    resp = requests.get('https://www.spiderdemo.cn/captcha/api/cap3_challenge/init/?challenge_type=cap3_challenge',
                        cookies=cookies, headers=headers).json()
    return sum(resp.get('page_data'))


def merge_captcha_image():
    img = Image.new('RGB', (150, 50), 'white')

    for i in range(50):
        img_filename = '%d_c.png' % i
        img.paste(Image.open(img_filename), (i * 3, 0))
        os.remove(img_filename)
    img.save('captcha.png')


def parse_captcha():
    params = {
        't': str(int(time.time() * 1000)),
    }

    response = requests.get(
        'https://www.spiderdemo.cn/captcha/api/cap3_challenge/captcha_image/',
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()

    for i, resp in enumerate(response.get('data')):
        with open('%d_c.png' % i, 'wb') as f:
            f.write(base64.b64decode(resp))


def parse_captcha_operation():
    text = captcha_identify(is_show=False).operation(open('captcha.png', 'rb').read())
    print('识别结果:', text)
    if text is None:
        parse_captcha()
        merge_captcha_image()
        return parse_captcha_operation()

    return text


def parse_captcha_verify(page, text):
    json_data = {
        'captcha_input': text,
        'challenge_type': 'cap3_challenge',
        'page_num': page
    }
    resp = requests.post('https://www.spiderdemo.cn/captcha/api/cap3_challenge/page/', json=json_data, headers=headers,
                         cookies=cookies).json()
    if not resp.get('success'):
        parse_captcha()
        merge_captcha_image()
        return parse_captcha_verify(page, parse_captcha_operation())

    return sum(resp.get('page_data'))


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print("第 %d 页" % page)
        parse_captcha()
        merge_captcha_image()
        count += parse_captcha_verify(page, parse_captcha_operation())

    print(count)
