#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "guobaohui"
__date__ = "2019.11.04"

import requests
from app.util.ssh_conf import remote_database

dbconfig = {
    't1': 30110,
    't2': 30120,
    't3': 30130,
    't4': 30140,
    't5': 30150,
    't6': 30160,
    't7': 30170,
    't8': 30180,
    't9': 30190,
    't10': 30200,
    'r1': 30112,
    'r2': 30122
}


def schedule_switch(env, opt_type):
    try:
        url = "http://%sproxy.fuyoukache.com/fykc-order-core/internal/shortcut/internal/aiSchSwitch" % env
        data = {
            "userName": "root-internal",
            "password": "fyhowareyou1qa2ws3ed"
        }
        if opt_type == "on":
            data["switch"] = True
        elif opt_type == "off":
            data["switch"] = False
        else:
            return "操作类型非法！"
        res = requests.get(url, data).json()
        # {'status': {'desc': '操作失败', 'code': 1}, 'success': False}
        if res["status"]["desc"] == "操作成功":
            return "操作成功，智能调度：%s ！" % opt_type
        else:
            return "操作异常，请稍后重试！"
    except Exception as e:
        return str(e) + "\n" + "出现异常，请联系%s！" % __author__


if __name__ == '__main__':
    r = schedule_switch('t5', 'off')
    print(r)
