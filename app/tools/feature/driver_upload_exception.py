# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新增司机
"""
__author__ = "郭冰洁"
__date__ = "2019.10.17"

import requests
import os
from app.util.ssh_conf import remote_database
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_bms import ApiBms
from app.util.ssh_conf import *
import time


class uploadException(ApiUa, ApiDriver, ApiBms):
    def __init__(self, env):
        self.env = env

    def driver_upload_Exception(self, order_sn, driver_mobile):
        r_ua_request_id = self.ua_generate_check_code()
        cookies1 = self.ua_login(16866666666, "Ab@123456789", r_ua_request_id)
        admin_info = self.bms_admin_info(cookies1)
        if admin_info["status"]["code"] != 0:
            return admin_info
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] != 0:
            return driver_info
        else:
            token = driver_info["data"][0]["token"]
            # 司机上报
            r = self.driver_order_exception_report(token, order_sn)
            if r["status"]["code"] != 0:
                return r
            # 运单系统异常处理
            re = self.bms_order_exception(order_sn, 22, modify_reason='',
                                          modify_data={"hasLoadLocation": 1, "hasUnloadLocation": 1},
                                          cookies_bms=cookies1)
            # return re["status"]["desc"]
            return re

if __name__ == "__main__":
    res = uploadException("t4").driver_upload_Exception(429110691616, 19555555555)
    print(res)
