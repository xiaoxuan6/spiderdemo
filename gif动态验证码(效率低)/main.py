# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/18 9:53
 @File: main.py
 @Description: 
"""

'''
gif 拆分，分别识别每一帧
'''

import base64
import io
import os
import time

import requests
from PIL import Image

from base import *

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/captcha/cap2_challenge/?challenge_type=cap2_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    resp = requests.get('https://www.spiderdemo.cn/captcha/api/cap2_challenge/init/?challenge_type=cap2_challenge',
                        headers=headers, cookies=cookies).json()
    return sum(resp.get('page_data'))


def parse_captcha():
    params = {
        't': str(int(time.time() * 1000))
    }

    response = requests.get(
        'https://www.spiderdemo.cn/captcha/api/cap2_challenge/captcha_image/',
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()
    return response.get('T')


def parse_gif_frames(img_content):
    # 打开 GIF 文件
    gif = Image.open(io.BytesIO(base64.b64decode(img_content)))

    # 获取帧数
    num_frames = gif.n_frames
    # print(num_frames)

    # 跳转到最后一帧 (索引从 0 开始，所以用 num_frames - 1)
    # gif.seek(num_frames - 1)

    # 获取最后一帧的图像
    # last_frame = gif.copy()

    # 保存或显示最后一帧
    # last_frame.save("last_frame.png")  # 保存为 PNG 文件

    for i in range(num_frames):
        gif.seek(i)
        i_frame = gif.copy()
        i_frame.save(f"{i}_frame.png")

    # print(f"最后一帧已保存，总帧数：{num_frames}")

    return num_frames


def parse_img_ocr(num):
    from ddddocr import DdddOcr

    captchas = list()
    ocr = DdddOcr(show_ad=False)
    for i in range(num - 1):
        text = ocr.classification(open('%d_frame.png' % i, 'rb').read())
        if len(text) == 4:
            captchas.append(text)

        os.remove('%d_frame.png' % i)

    n_captcha = ''.join(captchas).strip()
    if len(n_captcha) != 4:
        img_content = parse_captcha()
        num = parse_gif_frames(img_content)
        return parse_img_ocr(num)

    return n_captcha


def parse_page_data(page, text):
    json_data = {
        'captcha_input': text,
        'challenge_type': "cap2_challenge",
        'page_num': page
    }
    response = requests.post('https://www.spiderdemo.cn/captcha/api/cap2_challenge/page/', json=json_data,
                             headers=headers, cookies=cookies).json()
    if not response.get('success'):
        img_content = parse_captcha()
        num = parse_gif_frames(img_content)
        text = parse_img_ocr(num)
        return parse_page_data(page, text)

    return sum(response.get('page_data'))


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print("第%d页" % page)
        img_content = parse_captcha()
        num = parse_gif_frames(img_content)
        text = parse_img_ocr(num)
        count += parse_page_data(page, text)

    print(count)
