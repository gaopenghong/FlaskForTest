#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 9 / 2
import requests
import json


def send_message(url, msg):

    array = {
        "msgtype": "text",
        "text": {
             "content": msg
        }
    }
    res = requests.request(method='POST', url=url, data=json.dumps(array), headers={"Content-Type": "application/json; charset=UTF-8"})
    return res


if __name__ == '__main__':
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a110233a-29a1-472a-b5aa-3dad92df465d"
    send_message(webhook, '这次没有')
