# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/19 8:42
 @File: main.py
 @Description: 
"""

'''
报错：
    浏览器连接失败，请检查9222端口是否浏览器，且已添加"--remote-debugging-port=9222"启动项。
    地址: 127.0.0.1:9222
    
解决方法：
    1、cmd 查找端口 9222
        netstat -ano | findstr :9222
    说明：
        -a：显示所有连接和监听端口。
        -n：以数字形式显示地址和端口。
        -o：显示与每个连接关联的进程 ID (PID)。
        findstr :9222：过滤出包含 9222 端口的结果。 
    2、终止占用端口的进程
        taskkill /PID 1234 /F
    说明：
        /PID 1234：指定进程 ID。
        /F：强制终止。   
'''

import time

import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from base import *

co = ChromiumOptions()
co.headless()  # 无头模式
co.incognito()  # 匿名模式 -- 无痕模式启动浏览器

# 设置用户代理（模拟真实浏览器）
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
co.set_user_agent(user_agent)

# 禁用自动化特征
co.set_argument('--disable-blink-features=AutomationControlled')  # 禁用自动化控制标志，防止 navigator.webdriver 被设置为 true
# --no-sandbox 和 --disable-dev-shm-usage 常用于 Linux 环境或容器中，确保浏览器正常运行。
co.set_argument('--no-sandbox')  # 禁用沙盒模式
co.set_argument('--disable-dev-shm-usage')  # 禁用共享内存
co.set_argument('--disable-gpu')  # 禁用 GPU（可选，视情况而定）
co.set_argument('--window-size=1920,1080')  # 设置窗口大小，模拟真实用户
co.set_argument('--enable-webgl')  # 启用 webgl 指纹
co.set_argument('--ignore-gpu-blocklist')
# co.set_argument('--remote-debugging-port=9999')  # 设置远程调试端口（例如 9222）

dp = ChromiumPage(co)
dp.get('https://www.spiderdemo.cn/ob/ob_challenge1/?challenge_type=ob_challenge1')
time.sleep(2)

print(dp.run_js('return hex_md5("1234")'))

cookies = {
    'sessionid': config['Session']['value'],
}

headers = {
    'referer': 'https://www.spiderdemo.cn/ob/api/challenge/init/?challenge_type=ob_challenge1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}


def parse_page():
    resp = requests.get('https://www.spiderdemo.cn/ob/api/challenge/init/?challenge_type=ob_challenge1',
                        headers=headers, cookies=cookies).json()
    return sum(resp.get('page_data'))


def parse_page_data(page):
    t = str(int(time.time() * 1000))
    params = {
        'challenge_type': 'ob_challenge1',
        'sign': dp.run_js(f'return hex_md5("{t}{page}")'),
        'timestamp': t
    }

    response = requests.get('https://www.spiderdemo.cn/ob/api/ob_challenge1/page/%d/' % page, headers=headers,
                            cookies=cookies, params=params).json()
    return sum(response.get('page_data'))


try:
    count = parse_page()
    for page in range(2, 101):
        print('第 %d 页' % page)
        count += parse_page_data(page)

    print(count)
except:
    pass

dp.close()
dp.quit()
