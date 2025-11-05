# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/11/5 18:23
 @File: main.py
 @Description: 
"""
import hashlib
import time

import requests

cookies = {
    'sessionId': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiN2ZmNzc3ZmQtNzE4Ni00ZDg1LThiNjctNWRhYjQyMGVjMjgwIiwiSUQiOjgsIlVzZXJuYW1lIjoiMTUyNjU5MjYxNzgiLCJCdWZmZXJUaW1lIjo4NjQwMCwiaXNzIjoicW1QbHVzIiwiYXVkIjpbIkFOVEkiXSwiZXhwIjoxNzYyNTA1MTc4LCJuYmYiOjE3NjE5MDAzNzh9.Gc0MHKVKOTAbjh1f2iH3xf9nrpm-t4PR_gXPqGNd7wY',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Origin': 'http://antispider.top',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://antispider.top/challenge/14',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}


def fetch_numbers_sum(page: int) -> int:
    timestamp = str(int(time.time() * 1000))
    json_data = {
        'page': str(page),
        'timestamp': timestamp,
        'sign': hashlib.sha256(timestamp.encode()).hexdigest(),
    }
    print(json_data)

    response = requests.post(
        'http://antispider.top/api/challenge/14',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False
    ).json()
    numbers = response.get('data', {}).get('numbers', [])
    return sum(numbers)


if __name__ == '__main__':
    total = 0
    for page in range(1, 101):
        total += fetch_numbers_sum(page)
    print(total)
