# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/20 10:10
 @File: base.py
 @Description: 
"""
import configparser
import threading
from concurrent.futures import ThreadPoolExecutor

config = configparser.ConfigParser()
config.read('./../config.ini', encoding='utf-8')


class base(object):
    def __init__(self):
        self.cookies = {
            "sessionId": config['Session']['value']
        }
        self.headers = None
        self.count = 0
        self.max_page = 101
        self.max_workers = int(config['Setting']['max_workers'])
        # 创建线程锁--线程锁
        self.lock = threading.Lock()

    def fetch_page(self, page):
        pass

    def update_result(self, page):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.fetch_page, range(1, page))
            with self.lock:
                for page_sum in results:
                    self.count += page_sum

    def run(self):
        # 在线程中运行
        thread = threading.Thread(target=self.update_result, args=(self.max_page,), daemon=True)
        thread.start()
        # 等待线程完成
        thread.join()

        print("计算总和：", self.count)
