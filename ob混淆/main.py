# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/23 10:28
 @File: main.py
 @Description: 
"""
import threading

from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.headless()
co.incognito()

dp = ChromiumPage(co)
dp.get("https://www.spiderdemo.cn/authentication/ob1_challenge/?challenge_type=ob1_challenge")

import base
import requests

lock = threading.Lock()

cookies = {
    'sessionid': base.config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/authentication/ob1_challenge/?challenge_type=ob1_challenge',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

params = {
    'challenge_type': 'ob1_challenge',
}


def parse_page():
    response = requests.get(
        'https://www.spiderdemo.cn/authentication/api/ob1_challenge/init/',
        params=params,
        cookies=cookies,
        headers=headers,
    ).json()
    return sum(response.get('page_data'))


def parse_page_data(page):
    print(f"第 {page} 页")
    params.update({
        'signature': dp.run_js("return O0o0O0O0()")
    })
    resp = requests.get('https://www.spiderdemo.cn/authentication/api/ob1_challenge/page/%d/' % page, headers=headers,
                        params=params, cookies=cookies).json()
    return sum(resp.get('page_data'))


def ThreadPool(count):
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(parse_page_data, range(2, 101))
        with lock:
            for page_sum in results:
                count += page_sum

    print('count', count)


def Thread(count):
    thread = threading.Thread(target=ThreadPool, args=(count,), daemon=True)
    thread.start()
    thread.join()


'''
线成
'''
count = parse_page()
Thread(count)

'''
基础 5510938
'''
# count = parse_page()
# for page in range(2, 101):
#     print(f"第 {page} 页")
#     signature = dp.run_js("return O0o0O0O0()")
#     # print(signature)
#
#     params.update({
#         'signature': signature
#     })
#     resp = requests.get('https://www.spiderdemo.cn/authentication/api/ob1_challenge/page/%d/' % page, headers=headers,
#                         params=params, cookies=cookies).json()
#     print(resp)
#     count += sum(resp.get('page_data'))
# print(count)

dp.close()
dp.quit()
