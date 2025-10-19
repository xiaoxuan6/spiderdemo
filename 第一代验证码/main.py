# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/17 12:00
 @File: main.py
 @Description: 
"""
import os
import time

import ddddocr
import requests

from base import *

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/captcha/cap1_challenge/?challenge_type=cap1_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    params = {
        'challenge_type': 'cap1_challenge',
    }

    response = requests.get(
        'https://www.spiderdemo.cn/captcha/api/cap1_challenge/init/',
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()
    return sum(response.get('page_data'))


def parse_captcha():
    params = {
        't': str(int(time.time() * 1000))
    }
    content = requests.get('https://www.spiderdemo.cn/captcha/api/cap1_challenge/captcha_image', params=params,
                           headers=headers, cookies=cookies).content

    with open('captcha.png', 'wb') as f:
        f.write(content)

    # Image.NEAREST（最近邻插值，速度快但质量较低）
    # Image.BILINEAR（双线性插值，质量中等）
    # Image.BICUBIC（三次插值，质量较高，推荐）
    # Image.LANCZOS（Lanczos 插值，质量最佳但计算较慢）
    # Image.open('captcha.png').resize((300, 100), Image.LANCZOS).save('captcha.png')

    from PIL import Image
    img = Image.open('captcha.png')
    crop_box = (53, 20, 95, 36)
    cropped_img = img.crop(crop_box)
    scale_factor = 2
    width, height = cropped_img.size
    resized_img = cropped_img.resize((width * scale_factor, height * scale_factor), Image.LANCZOS)
    resized_img.save("resized.png")


def parse_captcha_identify():
    return ddddocr.DdddOcr(show_ad=False).classification(open('resized.png', 'rb').read())


def parse_captcha_verify():
    result = ''
    identify_result = False
    while not identify_result:
        parse_captcha()
        result = parse_captcha_identify()
        if len(result) == 4:
            identify_result = True

    print('识别结果：', result)
    return result


def parse_page_data(page, captcha_input):
    json_data = {
        'captcha_input': captcha_input,
        'challenge_type': 'cap1_challenge',
        'page_num': page
    }
    resp = requests.post('https://www.spiderdemo.cn/captcha/api/cap1_challenge/page/', json=json_data, headers=headers,
                         cookies=cookies).json()
    # print(resp)

    if not resp.get('success'):
        text = parse_captcha_verify()
        return parse_page_data(page, text)
    else:
        return sum(resp.get('page_data'))


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print(f"第 {page} 页")
        text = parse_captcha_verify()
        count += parse_page_data(page, text)

    print(count)
    os.remove('captcha.png')
    os.remove('resized.png')
