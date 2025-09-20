# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/18 19:44
 @File: main.py
 @Description: 
"""

'''
pip install fonttools
'''
import base64

import requests
from fontTools.ttLib import TTFont

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
        'challenge_type': 'font_anti_challenge',
    }

    response = requests.get(
        'https://www.spiderdemo.cn/font_anti/api/challenge/init/',
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()
    return sum(response.get('page_data'))


def parse_captcha(page):
    resp = requests.get(
        f'https://www.spiderdemo.cn/font_anti/api/font_anti_challenge/page/{page}/?challenge_type=font_anti_challenge',
        headers=headers,
        cookies=cookies).json()
    # print(resp)

    with open('a.woff2', 'wb') as f:
        f.write(base64.b64decode(resp.get('b64Font')))

    return resp


def parse_data_count(resp, newmap):
    data_list = list()
    for data in resp.get('page_data'):
        num = ''
        for i in list(data):
            num += newmap[i]

        data_list.append(int(num))

    return sum(data_list)


def woff_font():
    '''获取字体真实对应关系'''
    newmap = {}
    font = TTFont('a.woff2')  # 读取woff数据

    # 这个woff字体文件前面两个无用字符去掉，用不到
    lis = font.getGlyphOrder()[1:]
    # print(lis)

    glyf = font['glyf']  # 获取请求到的字体形状

    # 建立基础的字体和字体形状的对应关系
    base_font_map = {}
    for index, name in enumerate(lis):
        base_font_map[index] = glyf[name]

    cmap = font.getBestCmap()  # 获取字体对应关系
    font.close()
    for code, name in cmap.items():
        codestr = str(code - 48)  # 根据分析结果需要减去48
        current_shape = glyf[name]  # 根据name获取字体形状
        for number, shape in base_font_map.items():  # 遍历基础字体形状对应关系
            if shape == current_shape:  # 判断，如果两个字体形状相等
                newmap[codestr] = str(number)  # 将字体编码和字体添加到字典

    # print(newmap)
    return newmap


if __name__ == '__main__':
    count = parse_page()
    for page in range(2, 101):
        print("第 %d 页" % page)
        resp = parse_captcha(page)
        newmap = woff_font()
        count += parse_data_count(resp, newmap)

    print(count)
