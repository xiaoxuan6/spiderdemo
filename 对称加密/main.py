# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/11 17:59
 @File: main.py
 @Description: 
"""
import execjs
import requests

import base

cookies = {
    'sessionid': base.config['Session']['value']
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'referer': 'https://www.spiderdemo.cn/authentication/symmetry_challenge/?challenge_type=symmetry_challenge'
}


def init():
    resp = requests.get(
        'https://www.spiderdemo.cn/authentication/api/symmetry_challenge/init/?challenge_type=symmetry_challenge',
        headers=headers, cookies=cookies).json()

    return sum(resp.get('page_data'))


def load_data(count):
    params = {
        'challenge_type': 'symmetry_challenge'
    }

    for page in range(2, 101):
        print('第 %d 页' % page)
        result = execjs.compile(open('code.js', encoding='utf-8').read()).call('encrypt', page)
        params.update({
            'aes_sign': result['p'],
            'des_sign': result['f'],
            't': result['s']
        })

        headers.update({
            'x-aes-token': result['aes_token'],
            'x-des-token': result['des_token']
        })
        resp = requests.get(f'https://www.spiderdemo.cn/authentication/api/symmetry_challenge/page/{page}/',
                            params=params, cookies=cookies, headers=headers).json()
        print(resp)
        count += sum(resp.get('page_data'))

    print('总和：%d' % count)


if __name__ == '__main__':
    load_data(init())
