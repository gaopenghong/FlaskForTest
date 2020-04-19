#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
白名单表：fykc_xdriver_service.face_verify_white_list
加入：直接调用接口
删除：删除表记录即可
"""
__author__ = "guobaohui"
__date__ = "2019.10.13"

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


def add_white_list(env, driver_mobile):
    try:
        # driverId 返回为嵌套列表，形如：[[11], [22], [33]]
        driverId = remote_database(env, "fykc_xdriver_service",
                                   "select id from fykc_xdriver_service.driver_info where mobile='%s';" % driver_mobile)
        url = "http://%sxdriver.fuyoukache.com/api/internal/driver/faceVerifyWhiteList/add" % env
        print('driverId', driverId)
        if len(driverId) == 1:
            driverId = driverId[0][0]
        elif len(driverId) == 0:
            return "该手机号不存在，请注册！"
        data = {
            'driverId': driverId
        }
        # print('data', data)
        res = requests.get(url, data).json()
        # {'status': {'desc': '操作失败', 'code': 1}, 'success': False}
        if res["status"]["desc"] == "操作失败":
            return "该手机号已加入白名单，请勿重复操作！"
        elif res["status"]["desc"] == "操作成功":
            return "加入白名单成功！"
    except IndexError as e:
        return str(e), "该手机号存在重复数据，请处理！"


def del_white_list(env, driver_mobile):
    "delete from fykc_xdriver_service.face_verify_white_list where driverId='558566';"

    try:
        # 根据手机号查询driverId，判断手机号是否存在
        # driverId 返回为嵌套列表，形如：[[11], [22], [33]]
        driverId = remote_database(env, "fykc_xdriver_service",
                                   "select id from fykc_xdriver_service.driver_info where mobile='%s';" % driver_mobile)
        print('driverId', driverId)
        if len(driverId) == 1:
            driverId = driverId[0][0]
        elif len(driverId) == 0:
            return "该手机号不存在，请注册！"

        # 根据driverId查询人脸识别白名单表，判断是否已经加入过
        select_driver = remote_database(env, "fykc_xdriver_service",
                                   "select * from fykc_xdriver_service.face_verify_white_list where driverId='%s';" % driverId)
        if len(select_driver) == 0:
            return "该手机号未加入人脸识别白名单！"
        else:
            # 移出人脸识别白名单
            del_driver = remote_database(env, "fykc_xdriver_service",
                                   "delete from fykc_xdriver_service.face_verify_white_list where driverId='%s';" % driverId)
            return "移出白名单成功！"
    except IndexError as e:
        return str(e), "该手机号存在重复数据，请处理！"


if __name__ == '__main__':
    r = add_white_list('t5', '12066666666')
    print(r)
    r = del_white_list('t5', '12066666666')
    print(r)
