# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2026/1/27 17:00
 @File: main.py
 @Description: 
"""
import re

import requests

import base

cookies = {
    'sessionid': base.config['Session']['value']
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'referer': 'https://www.spiderdemo.cn/captcha/api/challenge/init/?challenge_type=slide_puzzle_challenge'
}


def init():
    resp = requests.get(
        'https://www.spiderdemo.cn/captcha/api/challenge/init/?challenge_type=slide_puzzle_challenge',
        headers=headers, cookies=cookies).json()

    return sum(resp.get('page_data'))


def load_data(count):
    for page in range(2, 101):
        print('第 %d 页' % page)

        # 1
        response = requests.get('https://www.spiderdemo.cn/captcha/api/slide_puzzle_challenge/captcha', headers=headers,
                                cookies=cookies).json()

        # 2
        payload = {
            "verify_idf_id": "83",
            'words': str(response.get('data').get('y')),
            "img_str": str(response.get('data').get('bg')).replace('data:image/png;base64,', '')
        }
        result = requests.post('http://127.0.0.1:8000/api/v3/img/identify', json=payload).json()
        print(result)
        res_str = result.get('data').get('res_str')
        result = re.findall(r'\d+', res_str)[0]

        # 3
        resp = requests.post('https://www.spiderdemo.cn/captcha/api/slide_puzzle_challenge/verify', json={
            "distance": int(result),
            "captchaId": response.get('data').get('captchaId')
        }, headers=headers, cookies=cookies).json()

        # 4
        resp = requests.get(
            f'https://www.spiderdemo.cn/captcha/api/slide_puzzle_challenge/page/{page}/?challenge_type=slide_puzzle_challenge&token={resp.get('data').get('token')}',
            cookies=cookies, headers=headers).json()
        print(resp)
        count += sum(resp.get('page_data'))
        break

    print('总和：%d' % count)


if __name__ == '__main__':
    '''
    仅获取第 2 页数据
    '''
    load_data(init())
