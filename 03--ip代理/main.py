# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/10/31 16:47
 @File: main.py
 @Description: 
"""

import loguru
import requests

cookies = {
    'sessionId': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiN2ZmNzc3ZmQtNzE4Ni00ZDg1LThiNjctNWRhYjQyMGVjMjgwIiwiSUQiOjgsIlVzZXJuYW1lIjoiMTUyNjU5MjYxNzgiLCJCdWZmZXJUaW1lIjo4NjQwMCwiaXNzIjoicW1QbHVzIiwiYXVkIjpbIkFOVEkiXSwiZXhwIjoxNzYyNTA1MTc4LCJuYmYiOjE3NjE5MDAzNzh9.Gc0MHKVKOTAbjh1f2iH3xf9nrpm-t4PR_gXPqGNd7wY',
}

headers = {
    'Origin': 'http://antispider.top',
    'Referer': 'http://antispider.top/challenge/03',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

for page in range(1, 6):
    print('第 %d 页' % page)
    try:
        while True:
            proxy = requests.get('https://269900.xyz/fetch_random', headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}).text

            loguru.logger.info(f'代理ip: {proxy}')
            if proxy.startswith('http', 0, -1):
                response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
                if response.status_code == 200:
                    break

        proxies = {
            'http': proxy,
            'https': proxy,
        }

        # 获取IP代理的API接口，返回格式为json
        # api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=odb8cskdnp4w6j1nzfcc&signature=t2h6uykokdzsu0pntiqf22dhkkfi202k&num=1&pt=1&format=json&sep=1"
        # # # 用户名密码认证(私密代理/独享代理)
        # username = "d2299983745"
        # password = "e8g8y8o2"
        #
        # # 获取API接口返回的代理IP
        # proxy_ip = requests.get(api_url).text
        # loguru.logger.info(f'代理ip: {proxy_ip}')
        #
        # proxies = {
        #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
        # }

        # break

        json_data = {
            'page': str(page),
        }

        response = requests.post('http://antispider.top/api/challenge/03', cookies=cookies, headers=headers,
                                 json=json_data, proxies=proxies, verify=False).json()
        print(response)
    except Exception as e:
        print(e)
