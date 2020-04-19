#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guobaohui'
__time__ = 2019 / 10 / 12
import requests
import json


def send_message_wechat(url, msg, user_list=None, mobile_list=None):
    """
    :param url: 群机器人地址
    :param msg: 消息文本
    :param user_list: 企业微信的邮箱，提醒指定成员(@某个成员)，提醒所有人(@all)
    :param mobile_list: 手机号列表，提醒手机号对应的群成员
    :return:
    """
    if user_list is None:
        user_list = []
    if mobile_list is None:
        mobile_list = []
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    data = {
        "msgtype": "text",
        "text": {
             "content": msg,
             "mentioned_list": user_list,
             "mentioned_mobile_list": mobile_list
        }
    }
    res = requests.post(url, headers=headers, json=data)
    return res


if __name__ == '__main__':
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2d3bd0c7-2a10-4674-8a30-dd6055606d0e"
    send_message_wechat(webhook, "It's a test message", [], ["13366863847"])
    send_message_wechat(webhook, "It's a test message", [], ["13366863847"])
