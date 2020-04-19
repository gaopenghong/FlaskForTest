#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新增司机
"""
__author__ = "郭冰洁"
__date__ = "2019.10.17"

import requests
import os
from app.util.ssh_conf import remote_database
import yaml
# from app.tools.api.api_driver.ApiDriver import  driver_api_register
from app.tools.api.api_driver import ApiDriver


def register_driver(env, number):
    curpath = os.path.dirname(os.path.realpath(__file__))
    f = open(curpath + "..\\data\\driver\\driver1.yaml", "r", encoding="utf-8")
    # lineId = 34523
    # 货主下单并安排司机  1.新增询价, 2.初审询价, 3.报价, 4.确定下单(4.1.在线支付, 4.2.财务审核), 5.安排司机, 6.运单打点,7.运单签收
    # order_status = 5
    a = f.read()
    f.close()
    d = yaml.load(a)
    driver_result_list = []
    for driver in d:
        if "司机" in driver['desc']:
            result = ApiDriver.driver_login(driver["mobile"])
            driver_result_list.append(result)
            driver_token = result["data"][0]["token"]
            driver["data_driver"]["token"] = driver_token
            driver["data_truck"]["token"] = driver_token
            ApiDriver.test_update__driver_info(driver["data_driver"])
            ApiDriver.test_truck_check(driver["data_truck"])
            ApiDriver.test_truck_check_legal(driver["data_truck"]["plateNumber"].encode())
            ApiDriver.test_update_truck_info(driver_token, driver["data_truck"]['plateNumber'])
            # 获取管理员信息
            r_admin_login = ApiDriver.base_admin_info(administrator_mobile=18334704870,
                                                      administrator_password_ua='Fy@123456789', )
            # 给调度添加工单处理权限。
            ApiDriver.test_update_GroupUser(r_admin_login)
            # 服务系统重新分配初审任务
            ApiDriver.test_redispatch(r_admin_login, result)
            # 审核
            ApiDriver.test_driver_aptitude_check(r_admin_login, result)
            # 加入刷脸白名单
            ApiDriver.test_face_scan(result)
            # 将司机加入绑卡白名单
            ApiDriver.crm_driver_drawings(result, r_admin_login)
            # 绑定银行卡
            ApiDriver.test_bank_bind_card(result)
            # 司机交押金
            ApiDriver.test_pay_Deposit(result)
            # # 司机订阅路线
            # r=test_createOrUpdateDriverLine(driver_token)
