# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/19 18:38
 @File: main.py
 @Description: 
"""
import base64
import re

import requests
from PIL import Image
from ddddocr import DdddOcr

from base import *

ocr = DdddOcr(show_ad=False)

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/font_anti/font_sprites_challenge/?challenge_type=font_sprites_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    resp = requests.get(
        'https://www.spiderdemo.cn/font_anti/api/font_sprites_challenge/init/?challenge_type=font_sprites_challenge',
        cookies=cookies, headers=headers).json()
    return sum(resp.get('page_data'))


def parse_img():
    img = Image.open('captcha.png')
    # 如果是 RGBA 模式，处理透明背景
    if img.mode == 'RGBA':
        # 创建白色背景
        width, height = img.size
        white_bg = Image.new('RGBA', (width, height), (255, 255, 255, 255))  # 白色不透明

        # 粘贴原图片（透明区域会显示白色背景）
        white_bg.paste(img, (0, 0), img)

        # 转换为 RGB（移除透明通道）
        img = white_bg.convert('RGB')
    else:
        # 非 RGBA 图片，直接转换为 RGB
        img = img.convert('RGB')

    img.save('captcha.png')


def parse_font_img(page):
    resp = requests.get(
        'https://www.spiderdemo.cn/font_anti/api/font_sprites_challenge/page/%d/?challenge_type=font_sprites_challenge' % page,
        cookies=cookies, headers=headers).json()
    # print(resp)

    with open('captcha.png', 'wb') as f:
        f.write(base64.b64decode(resp.get('sprite')))

    # 背景改为白色，方便 ocr 识别文字
    parse_img()

    return resp.get('css_code'), resp.get('page_data')


def parse_css_code(css_data):
    result = re.findall(r'.class(\d+){background-position: -(\d+)px', css_data)
    return {
        k: v
        for k, v in result
    }


def parse_captcha(key):
    img = Image.open('captcha.png')
    cropped_img = img.crop((key, 0, key + 25, 50))
    # img_bytes = img.tobytes()
    cropped_img.save('a.png')

    text = ocr.classification(open('a.png', 'rb').read())
    # print(text)
    return text


def parse_page_data(img_keys, page_data):
    count = 0
    for data in page_data:
        result = re.findall(r'class(\d+)', data)

        num = ''
        for key in result:
            i = int(img_keys[key])
            # 可以优化，先查询是否存在，不存在在执行 parse_captcha，可以提高效率
            num += parse_captcha(i)

        count += int(num)

    return count


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print("第 %d 页" % page)
        css_code, page_data = parse_font_img(page)
        img_keys = parse_css_code(css_code)
        count += parse_page_data(img_keys, page_data)

    print(count)
