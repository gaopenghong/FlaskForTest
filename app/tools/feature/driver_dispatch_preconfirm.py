__author__ = "郭冰洁"
__date__ = "2019.10.17"

import requests
import os
from app.util.ssh_conf import remote_database
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_dispatch import ApiDispatch
from app.util.ssh_conf import *


class DispatchPreconfirm(ApiDispatch, ApiDriver, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_dispatch_Preconfirm(self, order_sn, driver_mobile, dispatch_mobile):
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] == 0:
            driverid = driver_info["data"][0]["id"]
            r_ua_request_id = self.ua_generate_check_code()
            cookies = self.ua_login(dispatch_mobile, "Ab@123456789", r_ua_request_id)
            # 调度确认前校验
            r1 = self.dispatch_preConfirm(order_sn, driverid, cookies)
            if r1["status"]["code"] != 0:
                return r1
            # 调度确认
            r2 = self.dispatch_Confirm(order_sn, driverid, cookies)
            print(r2)
            return r2["status"]["desc"]
        else:
            return driver_info


if __name__ == "__main__":
    env = DispatchPreconfirm("t4").driver_dispatch_Preconfirm(429102824677, 16011111111, 18334704870)
    print(env)
