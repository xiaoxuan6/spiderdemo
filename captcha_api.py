# -*- coding: utf-8 -*-
"""
 @Author: xiaoxuan6
 @Date: 2025/9/18 13:40
 @File: captcha_api.py
 @Description: 
"""
import base64
import pprint
import re
from urllib.parse import urlparse

import requests
from PIL import Image

from base import *


class captcha_identify(object):
    def __init__(self, is_show=False):
        self.token = config['Captcha']['token']
        self.url = config['Captcha']['url']
        self.is_show = is_show
        self.model = config['Captcha']['model']

    def identify(self, img):
        return captcha(self.url, self.model, self.token, self.is_show).identify_text(img)

    def operation(self, img):
        return captcha(self.url, self.model, self.token, self.is_show).identify_operation(img)


class captcha(object):
    def __init__(self, url, model, token, is_show=False):
        self.url = url
        self.token = token
        self.headers = {
            'Authorization': 'Bearer ' + token
        }
        self.is_show = is_show
        self.model = model

    def img2base64(self, img):
        if isinstance(img, bytes):
            image = self.str2base64(img)
        elif isinstance(img, Image.Image):
            image = img.copy()
            img_bytes = image.tobytes()
            image = self.str2base64(img_bytes)
        else:
            if self.is_valid_url(img):
                image = img
            else:
                image = self.str2base64(img)

        return image

    def str2base64(self, img):
        return 'data:image/png;base64,' + base64.b64encode(img).decode('utf-8')

    def is_valid_url(self, string):
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])  # 检查是否有 scheme 和 netloc
        except ValueError:
            return False

    def identify_text(self, img):
        try:
            resp = self.identify(img, '识别内容')
            return self.parse_identify_text_response(resp)
        except Exception as e:
            print('识别失败：', e)
            return ''

    def identify_operation(self, img):
        try:
            resp = self.identify(img, '识别内容并给出计算答案, 计算结果两侧使用#包围')
            return self.parse_identify_operation_response(resp)
        except Exception as e:
            print('识别失败：', e)
            return ''

    def identify(self, img, text):
        if not isinstance(img, (bytes, str, Image.Image)):
            raise TypeError("未知图片类型")

        json_data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": self.img2base64(img)
                            }
                        }
                    ]
                }
            ]
        }

        if self.is_show:
            pprint.pprint(json_data)

        resp = requests.post(self.url + '/v1/chat/completions', headers=self.headers, json=json_data).json()
        if self.is_show:
            pprint.pprint(resp)

        return resp

    def parse_response(self, response):
        if response.get('error', '') is None:
            print('识别失败：', response.get('error').get('message'))
            return ''

        return response.get('choices')[0]['message']['content']

    def parse_identify_text_response(self, response):
        content = self.parse_response(response)
        result = re.findall(r'[A-Za-z0-9]{4}', content)
        return result[0] if len(result) > 0 else ''

    def parse_identify_operation_response(self, response):
        content = self.parse_response(response).replace('\n', '')
        result = re.findall(r'#(\d+)#', content)
        return result[0] if len(result) > 0 else ''
