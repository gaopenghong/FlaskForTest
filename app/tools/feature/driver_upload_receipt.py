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
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_service import ApiService
from app.tools.api.api_bms import ApiBms
from app.util.ssh_conf import *

import time


class UploadReceipt(ApiUa, ApiDriver, ApiService,ApiBms):
    def __init__(self, env):
        self.env = env

    def driver_upload_receipt(self, order_sn, driver_mobile):
        r_ua_request_id = self.ua_generate_check_code()
        cookies1 = self.ua_login(16866666666, "Ab@123456789", r_ua_request_id)
        admin_info=self.bms_admin_info(cookies1)
        if admin_info["status"]["code"]!=0:
            return admin_info
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] != 0:
            return driver_info
        else:
            token = driver_info["data"][0]["token"]
            # 获取运单详情
            r_driver_order_detail = self.driver_order_detail(token, order_sn)
            if r_driver_order_detail["status"]["code"] != 0:
                return r_driver_order_detail
            else:
                res1 = self.driver_order_receipt_upload(token, order_sn)
                if res1["status"]["code"] == 1:
                    return res1
                res2 = self.driver_order_receipt_mail(token, order_sn)
                if res2["status"]["code"] == 1:
                    return res2
                print(r_driver_order_detail)
                if  "thirdClockIn" in r_driver_order_detail["data"][0]:
                    res3=self.driver_report_third_clock(token,order_sn)
                    if res3["status"]["code"] == 1:
                        return res3
                else:
                    pass
                # 用户分组
                r_group_related_users = self.service_sys_task_group_users(cookies1, 3400)
                if admin_info["property"]["user"]["mobile"] not in str(r_group_related_users):
                    print('工单组下管理员: %s' % r_group_related_users)
                    temp_admin_info = {
                        'userId': admin_info["property"]["user"]["id"],
                        'userName':admin_info["property"]["user"]["name"],
                        'mobile': admin_info["property"]["user"]["mobile"]
                    }
                    origin_users = r_group_related_users['data'][0]['groupMaps']
                    for temp_user in origin_users:
                        del temp_user['id']
                        del temp_user['groupId']
                    origin_users.append(temp_admin_info)
                    # 更新工单组下管理员
                    r_service_sys_group_user_update = self.service_sys_task_group_user_update(cookies1, 3400,
                                                                                              '回单审核',
                                                                                              origin_users)
                    print('管理员更新: %s' % r_service_sys_group_user_update)
                # 任务重新分配
                res3 = self.test_huidanspatch(admin_info,cookies1, order_sn)
                print(res3)
                if res3["status"]["code"] != 0:
                        return res3
                # 回单审核
                # res4 = self.test_driver_huidan_check(cookies1, order_sn)
                sql4="update task_order set handleTime='2020-01-07 13:53:19' and status=6  and handleResult='审核通过' where orderSn="+order_sn+" and  name='回单审核';"
                remote_database(self.env, "house_keeper", sql4)
                sql5="update order_receipt_info set comment='12311' and backStatus=2   where orderSn="+order_sn+";"
                remote_database(self.env, "fykc_order_center", sql5)
                sql6="update checkorderlist set tradecircular=3 where orderSn="+order_sn+";"
                remote_database(self.env, "caiwu", sql6)
                return "操作成功"

    def test_huidanspatch(self, admin_info, cookies1,order_sn):
        admin_name = admin_info["property"]["user"]["name"],
        cookies_ua = cookies1
        id = admin_info["property"]["user"]["id"]
        # 服务系统开启接单
        r = self.service_update_user_status(4, cookies_ua)
        print("服务系统已开启")
        sql1 = 'select id from task_order where  name = "回单审核" and orderSn = ' + str(order_sn)
        try:
            handle_list_orderSn_id1 = remote_database(self.env, 'house_keeper', sql1)[0][0]
            print("获取此运单初审任务id为：%s" % handle_list_orderSn_id1)
            # 服务系统重新分配初审任务
            r = self.service_task_dispatch(cookies_ua, task_id=handle_list_orderSn_id1, user_name=admin_name,
                                           user_id=id)
            print(r)
            return r
        except:
            print("未找到回单任务")

    def test_driver_huidan_check(self, cookies1, orderSn):
        sql1 = 'select id from task_order where `name` = "回单审核" and orderSn = ' + str(orderSn)
        task_id = remote_database(self.env, 'house_keeper', sql1)[0][0]
        print(task_id)
        time.sleep(3)
        task_json = {"content": "测试"}
        r = self.service_pass_task(task_id=task_id, task_json=task_json, data_json=None,
                                   cookies_service=cookies1)
        # 当有三方打开报备时
        try:
            sql2 = 'update order_third_backup  set   backupStatus=2   where orderSn = ' + str(orderSn)
            remote_database(self.env, 'fykc_order_center', sql2)
        except:
            pass
        return r



if __name__ == "__main__":
    res = UploadReceipt("t4").driver_upload_receipt(929120467714, 16011111111)
    print(res)
