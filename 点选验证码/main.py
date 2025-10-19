# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/13 11:31
 @File: main.py
 @Description: 
"""
import time

import execjs
import requests
from loguru import logger

import base

headers = {
    "referer": "https://www.spiderdemo.cn/captcha/cap8_challenge/?challenge_type=cap8_challenge",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}
cookies = {
    "sessionid": base.config['Session']['value']
}


def fetch_captcha_img():
    url = "https://www.spiderdemo.cn/captcha/api/cap8_challenge/click_captcha_image/"
    params = {
        "t": str(int(time.time() * 1000))
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params).json()
    # print(response)
    return response.get('captcha_id'), response.get('background_pic')


def identify_captcha(img_base64):
    payload = {
        "img": img_base64,
        "type": "30009"
    }

    response = requests.post("http://127.0.0.1:8000/api/v1/img/identify", json=payload).json()
    # pprint.pprint(response)

    if response.get('status') != 200:
        print(response.get('msg'))
        return ''

    if response.get('data').get('code') != 0:
        print(response.get('data'))
        return ''

    axis = list()
    for item in response.get('data').get('data').split('|'):
        x, y = item.split(',')
        axis.append([int(x), int(y)])  # 坑点：必须转为 int 否则加密之后的数据错误

    return axis


def captcha_verify(captcha_id, axis, page):
    data = {
        "click_positions_encoded": execjs.compile(open('code.js', encoding='utf-8').read()).call('encrypt', axis),
        "page_num": page,
        "challenge_type": "cap8_challenge",
        "captcha_id": captcha_id
    }
    # pprint.pprint(data)

    response = requests.post("https://www.spiderdemo.cn/captcha/api/cap8_challenge/click_page/", headers=headers,
                             cookies=cookies, json=data).json()
    print(response)


if __name__ == '__main__':
    '''
    仅获取第 2 页数据
    '''
    captcha_id, img_base64 = fetch_captcha_img()
    axis = identify_captcha(img_base64)
    logger.info('文字坐标：' + str(axis))

    captcha_verify(captcha_id, axis, 2)
    # 返回结果：{'success': True, 'data_type': 'page', 'page_data': [7763, 6725, 3217, 7716, 2111, 7794, 7888, 6189, 1931, 9828], 'current_page': 2, 'total_pages': 100, 'challenge_type': 'cap8_challenge', 'message': '点选验证成功，获取第2页数据'}
