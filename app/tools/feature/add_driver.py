#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
新增司机
"""
__author__ = "郭冰洁"
__date__ = "2019.10.17"

import requests
import os
from app.util.ssh_conf import *
import yaml
# from app.tools.api.api_driver.ApiDriver import  driver_api_register
from app.tools.api.api_driver import ApiDriver
import random
import json


class AddDriver(ApiDriver):
    def __init__(self, env):
        self.env = env

    # 司机信息、车辆信息均通过
    def add_driver_1(self, number, start):
        driver_list = []
        for i in range(int(number)):
            end = random.randint(100, 1000)
            driver_mobile = str(start) + "00000" + str(end)
            insert_driver_sql = "INSERT INTO `driver_info`(`name`, `password`, `token`, `tokenExpire`, `mobile`, `sex`, `remark`, `brokerId`, `brokerMobile`, `brokerName`, `transportType`, `transportId`, `idCardNumber`, `idCardAddress`, `imgIdCardFront`, `frontStatus`, `imgIdCardBack`, `backStatus`, `imgDriveLicense`, `licenStatus`, `auditName`, `checkRemark`, `status`, `checkDate`, `imgPortrait`, `wx`, `regSrcType`, `regSrcId`, `conTransSta`, `conInvoiceSta`, `taxProxyRegSta`, `drivingSta`, `createTime`, `updateTime`, `adminId`, `adminName`, `adminType`, `isNew`) VALUES ('平彦文', NULL, '677bc6f0bb10670d318473f762e62f4e', '2019-06-05 17:52:11', '" + driver_mobile + "', 0, NULL, 34325, '18519263629', 'gph经纪人', 1, NULL, '131126198109120635', '河北省衡水市故城县建国镇建国村425号', 'http://public.fuyoukache.com/Fr-Kodi5PzmzvuqugBu3wJNfeVUz', 2, 'http://public.fuyoukache.com/FmV1nP_QX9BLgNtzKgYQbdCUVRdz', 2, 'http://public.fuyoukache.com/Fvv81ZDXM-LxgNUumrNwPGv3AbMd', 2, '郭冰洁', '', 2, NULL, NULL, NULL, 3, NULL, 0, 0, 1, 0, '2019-06-04 20:04:35', '2019-06-05 17:53:11', 1649, '郭冰洁', 3, 0);"
            remote_database(self.env, 'fykc_xdriver_service', insert_driver_sql)
            select_driver = "select id  from driver_info where mobile= " + driver_mobile
            driver_id = remote_database(self.env, 'fykc_xdriver_service', select_driver)
            driver_id1 = str(driver_id[0][0])
            truck_number = "晋B11" + str(end)
            insert_truck_sql = "INSERT INTO `truck_info`(`plateNumber`, `carLengthId`, `carLengthName`, `carModelId`, `carModelName`, `carHeigh`, `carWidth`, `carBrand`, `onroadTime`, `carFixedLoad`, `carWeight`, `carAxis`, `carType`, `imgCarLicense`, `carLicenStatus`, `imgLoadLicense`, `loadLicenStatus`, `imgInsurance`, `insurStatus`, `auditName`, `checkRemark`, `checkTime`, `status`, `fuelConsumption`, `adminId`, `adminName`, `adminType`, `version`, `createTime`, `updateTime`, `loadLicenStatusNumber`, `recordStatus`) VALUES ('" + truck_number + "', 8, '9.6', 1, '厢式车', 6.0, 1.0, NULL, NULL, 1000,11000, 2, 0, 'https://public.fuyoukache.com/eecb1690-7b20-4878-bb8e-3917b3b4da64---14.jpg', 2, 'https://public.fuyoukache.com/9320acd2-4fcc-4782-82d8-1001fc08df44---21.jpg', 2, 'https://public.fuyoukache.com/21456509-c731-4705-b29f-a91fbfcac707---22.jpg', 2, NULL, NULL, NULL, 2, NULL, 1649, '高鹏鸿', 3, 1, '2019-06-04 20:15:34', '2019-06-05 11:30:36', NULL, 0);"
            remote_database(self.env, 'fykc_xdriver_service', insert_truck_sql)
            select_truck = "select id  from  truck_info where plateNumber='" + truck_number + "'"
            print(select_truck)
            truck_id = remote_database(self.env, 'fykc_xdriver_service', select_truck)
            truck_id1 = str(truck_id[0][0])
            driver_band_truck_sql = "INSERT INTO `driver_truck_map`(`driverId`, `truckId`, `imgDriverTruckGroup`, `driverTruckStatus`, `auditName`, `checkRemark`, `status`, `isDefault`, `createTime`, `updateTime`)  VALUES  (" + driver_id1 + ", " + truck_id1 + ", 'https://public.fuyoukache.com/20987071-1ad9-460c-9e7b-53c3cd0138ff---身份证x.png', 2, NULL, NULL, 0, 1, '2019-06-03 15:21:48', '2019-06-04 14:35:01');"
            remote_database(self.env, 'fykc_xdriver_service', driver_band_truck_sql)
            driver_band_bank_sql = "INSERT INTO  `bank_card_info`(`driverId`, `accountType`, `bankName`, `bankCardNumber`, `bankAccount`, `bankProvince`, `bankProvinceName`, `bankCity`, `bankCityName`, `depositBankName`, `bankColor`, `bankShort`) VALUES (" + driver_id1 + ", 1, '招商银行', '6225880150027531', '李东东', NULL, NULL, NULL, NULL, '', '#C85656', 'CMB');"
            remote_database(self.env, 'fykc_xdriver_service', driver_band_bank_sql)
            driver_pay1_sql1 = "INSERT INTO `driver_deposit`(`driverId`, `isDeposit`, `deposit`, `updateTime`) VALUES (" + driver_id1 + ", 1, 200, NULL);"
            remote_database(self.env, 'fykc_wxtrucking_bidding', driver_pay1_sql1)
            driver_pay2_sql = "INSERT INTO `driver_deposit`(`amount`, `driverId`, `driverName`, `driverMobile`, `status`, `createTime`, `updateTime`) VALUES (200.00, " + driver_id1 + ", '文彦平', '16666666667', 1, '2019-06-13 14:41:36', '2019-06-13 14:41:36');"
            remote_database(self.env, 'fykc_truck_scheduler', driver_pay2_sql)
            # 添加定位
            driver_location = "INSERT INTO driver_location`(`driverId`, `latitude`, `longitude`, `provinceName`, `cityName`, `districtName`, `address`, `orderSn`, `createTime`, `updateTime`) VALUES (" + driver_id1 + ", 40.03623, 116.307452, '北京市', '北京市', '海淀区', '北京市海淀区上地街道润莘泽学校金隅嘉华大厦', NULL, '2019-11-02 12:22:31', '2019-11-02 10:42:13');"
            remote_database(self.env, 'fykc_wxtrucking_bidding', driver_location)
            # 交固定路线押金
            # driver_pay1_sql2 = "INSERT INTO   driver_deposit_info`(`id`, `driverId`, `type`, `hasPayMoney`, `deductMoney`, `status`, `createTime`, `updateTime`) VALUES (2, " + driver_id1 + ", 2, 0.01, 0.00, 0, '2019-10-29 13:50:06', '2019-11-02 16:30:23');"
            # remote_database(env, 'fykc_xdriver_service', driver_pay1_sql2)
            driver_list.append(driver_mobile)
        return ' '.join(driver_list)

    # 司机信息、车辆信息均在审核中
    def add_driver_2(self, number):
        curpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        print(curpath)
        f = open(curpath + "\\data\\driver\\driver1.yaml", "r", encoding="utf-8")
        # 货主下单并安排司机  1.新增询价, 2.初审询价, 3.报价, 4.确定下单(4.1.在线支付, 4.2.财务审核), 5.安排司机, 6.运单打点,7.运单签收
        a = f.read()
        f.close()
        d = yaml.load(a)
        driver_result_list = []
        for driver in d:
            if "司机" in driver['desc']:
                result = ApiDriver.driver_login(driver["mobile"], "1123")
                if result['status']['desc'] != "操作成功":
                    return result['status']['desc']
                driver_result_list.append(result)
                driver_token = result["data"][0]["token"]
                driver["data_driver"]["token"] = driver_token
                driver["data_truck"]["token"] = driver_token
                ApiDriver.driver_update_driver_info(self.env, driver["data_driver"])
                ApiDriver.driver_truck_check(self.env, driver["data_truck"])
                ApiDriver.driver_truck_check_legal(self.env, driver["data_truck"]["plateNumber"].encode())
                ApiDriver.driver_update_truck_info(self.env, driver_token, driver["data_truck"]['plateNumber'])
                # 获取管理员信息
                r_admin_login = ApiDriver.base_admin_info(self.env, administrator_mobile=18334704870,
                                                          administrator_password_ua='Ab@123456789', )
                # 给调度添加工单处理权限。
                ApiDriver.test_update_GroupUser(self.env, r_admin_login)
                # 服务系统重新分配初审任务
                ApiDriver.test_redispatch(self.env, r_admin_login, result)
                # 审核
                ApiDriver.test_driver_aptitude_check(self.env, r_admin_login, result)
                # 加入刷脸白名单
                ApiDriver.test_face_scan(result)
                # 将司机加入绑卡白名单
                ApiDriver.crm_driver_drawings(self.env, result, r_admin_login)
                # 绑定银行卡
                ApiDriver.driver_bank_bind_card(self.env, result)
                # 司机交押金
                ApiDriver.test_pay_Deposit(self.env, result)
                # # 司机订阅路线
                # r=test_createOrUpdateDriverLine(driver_token)
    #都在审核中；车辆信息审核通过，司机信息审核不通过
    def add_driver_3(self, number, start, driver_status,truck_status):
        driver_list = []
        for i in range(int(number)):
            end = random.randint(100, 1000)
            driver_mobile = str(start) + "00000" + str(end)
            if driver_status == 1:  # 审核中
                insert_driver_sql = "INSERT INTO `driver_info`(`name`, `password`, `token`, `tokenExpire`, `mobile`, `sex`, `remark`, `brokerId`, `brokerMobile`, `brokerName`, `transportType`, `transportId`, `idCardNumber`, `idCardAddress`, `imgIdCardFront`, `frontStatus`, `imgIdCardBack`, `backStatus`, `imgDriveLicense`, `licenStatus`, `auditName`, `checkRemark`, `status`, `checkDate`, `imgPortrait`, `wx`, `regSrcType`, `regSrcId`, `conTransSta`, `conInvoiceSta`, `taxProxyRegSta`, `drivingSta`, `createTime`, `updateTime`, `adminId`, `adminName`, `adminType`, `isNew`) VALUES ('平彦文', NULL, '677bc6f0bb10670d318473f762e62f4e', '2019-06-05 17:52:11', '" + driver_mobile + "', 0, NULL, 34325, '18519263629', 'gph经纪人', 1, NULL, '131126198109120635', '河北省衡水市故城县建国镇建国村425号', 'http://public.fuyoukache.com/Fr-Kodi5PzmzvuqugBu3wJNfeVUz', 1, 'http://public.fuyoukache.com/FmV1nP_QX9BLgNtzKgYQbdCUVRdz', 1, 'http://public.fuyoukache.com/Fvv81ZDXM-LxgNUumrNwPGv3AbMd', 1, '郭冰洁', '', 1, NULL, NULL, NULL, 3, NULL, 0, 0, 1, 0, '2019-06-04 20:04:35', '2019-06-05 17:53:11', 1649, '郭冰洁', 3, 0);"
            elif driver_status == 2  :  # 审核通过
                insert_driver_sql = "INSERT INTO `driver_info`(`name`, `password`, `token`, `tokenExpire`, `mobile`, `sex`, `remark`, `brokerId`, `brokerMobile`, `brokerName`, `transportType`, `transportId`, `idCardNumber`, `idCardAddress`, `imgIdCardFront`, `frontStatus`, `imgIdCardBack`, `backStatus`, `imgDriveLicense`, `licenStatus`, `auditName`, `checkRemark`, `status`, `checkDate`, `imgPortrait`, `wx`, `regSrcType`, `regSrcId`, `conTransSta`, `conInvoiceSta`, `taxProxyRegSta`, `drivingSta`, `createTime`, `updateTime`, `adminId`, `adminName`, `adminType`, `isNew`) VALUES ('平彦文', NULL, '677bc6f0bb10670d318473f762e62f4e', '2019-06-05 17:52:11', '" + driver_mobile + "', 0, NULL, 34325, '18519263629', 'gph经纪人', 1, NULL, '131126198109120635', '河北省衡水市故城县建国镇建国村425号', 'http://public.fuyoukache.com/Fr-Kodi5PzmzvuqugBu3wJNfeVUz', 2, 'http://public.fuyoukache.com/FmV1nP_QX9BLgNtzKgYQbdCUVRdz', 2, 'http://public.fuyoukache.com/Fvv81ZDXM-LxgNUumrNwPGv3AbMd', 2, '郭冰洁', '', 2, NULL, NULL, NULL, 3, NULL, 0, 0, 1, 0, '2019-06-04 20:04:35', '2019-06-05 17:53:11', 1649, '郭冰洁', 3, 0);"
            elif driver_status == 3 :  # 审核不通过
                insert_driver_sql = "INSERT INTO `driver_info`(`name`, `password`, `token`, `tokenExpire`, `mobile`, `sex`, `remark`, `brokerId`, `brokerMobile`, `brokerName`, `transportType`, `transportId`, `idCardNumber`, `idCardAddress`, `imgIdCardFront`, `frontStatus`, `imgIdCardBack`, `backStatus`, `imgDriveLicense`, `licenStatus`, `auditName`, `checkRemark`, `status`, `checkDate`, `imgPortrait`, `wx`, `regSrcType`, `regSrcId`, `conTransSta`, `conInvoiceSta`, `taxProxyRegSta`, `drivingSta`, `createTime`, `updateTime`, `adminId`, `adminName`, `adminType`, `isNew`) VALUES ('平彦文', NULL, '677bc6f0bb10670d318473f762e62f4e', '2019-06-05 17:52:11', '" + driver_mobile + "', 0, NULL, 34325, '18519263629', 'gph经纪人', 1, NULL, '131126198109120635', '河北省衡水市故城县建国镇建国村425号', 'http://public.fuyoukache.com/Fr-Kodi5PzmzvuqugBu3wJNfeVUz', 3, 'http://public.fuyoukache.com/FmV1nP_QX9BLgNtzKgYQbdCUVRdz', 3, 'http://public.fuyoukache.com/Fvv81ZDXM-LxgNUumrNwPGv3AbMd', 3, '郭冰洁', '', 3, NULL, NULL, NULL, 3, NULL, 0, 0, 1, 0, '2019-06-04 20:04:35', '2019-06-05 17:53:11', 1649, '郭冰洁', 3, 0);"
            remote_database(self.env, 'fykc_xdriver_service', insert_driver_sql)
            select_driver = "select id  from driver_info where mobile= " + driver_mobile
            driver_id = remote_database(self.env, 'fykc_xdriver_service', select_driver)
            driver_id1 = str(driver_id[0][0])
            truck_number = "晋B11" + str(end)
            if truck_status == 1:  # 审核中
                insert_truck_sql = "INSERT INTO `truck_info`(`plateNumber`, `carLengthId`, `carLengthName`, `carModelId`, `carModelName`, `carHeigh`, `carWidth`, `carBrand`, `onroadTime`, `carFixedLoad`, `carWeight`, `carAxis`, `carType`, `imgCarLicense`, `carLicenStatus`, `imgLoadLicense`, `loadLicenStatus`, `imgInsurance`, `insurStatus`, `auditName`, `checkRemark`, `checkTime`, `status`, `fuelConsumption`, `adminId`, `adminName`, `adminType`, `version`, `createTime`, `updateTime`, `loadLicenStatusNumber`, `recordStatus`) VALUES ('" + truck_number + "', 8, '9.6', 1, '厢式车', 6.0, 1.0, NULL, NULL, 1000,11000, 2, 0, 'https://public.fuyoukache.com/eecb1690-7b20-4878-bb8e-3917b3b4da64---14.jpg', 1, 'https://public.fuyoukache.com/9320acd2-4fcc-4782-82d8-1001fc08df44---21.jpg', 1, 'https://public.fuyoukache.com/21456509-c731-4705-b29f-a91fbfcac707---22.jpg', 1, NULL, NULL, NULL, 2, NULL, 1649, '高鹏鸿', 3, 1, '2019-06-04 20:15:34', '2019-06-05 11:30:36', NULL, 0);"
            elif truck_status == 2:  # 审核通过
                insert_truck_sql = "INSERT INTO `truck_info`(`plateNumber`, `carLengthId`, `carLengthName`, `carModelId`, `carModelName`, `carHeigh`, `carWidth`, `carBrand`, `onroadTime`, `carFixedLoad`, `carWeight`, `carAxis`, `carType`, `imgCarLicense`, `carLicenStatus`, `imgLoadLicense`, `loadLicenStatus`, `imgInsurance`, `insurStatus`, `auditName`, `checkRemark`, `checkTime`, `status`, `fuelConsumption`, `adminId`, `adminName`, `adminType`, `version`, `createTime`, `updateTime`, `loadLicenStatusNumber`, `recordStatus`) VALUES ('" + truck_number + "', 8, '9.6', 1, '厢式车', 6.0, 1.0, NULL, NULL, 1000,11000, 2, 0, 'https://public.fuyoukache.com/eecb1690-7b20-4878-bb8e-3917b3b4da64---14.jpg', 2, 'https://public.fuyoukache.com/9320acd2-4fcc-4782-82d8-1001fc08df44---21.jpg', 2, 'https://public.fuyoukache.com/21456509-c731-4705-b29f-a91fbfcac707---22.jpg', 2, NULL, NULL, NULL, 2, NULL, 1649, '高鹏鸿', 3, 1, '2019-06-04 20:15:34', '2019-06-05 11:30:36', NULL, 0);"
            elif truck_status == 3:  # 审核不通过
                insert_truck_sql = "INSERT INTO `truck_info`(`plateNumber`, `carLengthId`, `carLengthName`, `carModelId`, `carModelName`, `carHeigh`, `carWidth`, `carBrand`, `onroadTime`, `carFixedLoad`, `carWeight`, `carAxis`, `carType`, `imgCarLicense`, `carLicenStatus`, `imgLoadLicense`, `loadLicenStatus`, `imgInsurance`, `insurStatus`, `auditName`, `checkRemark`, `checkTime`, `status`, `fuelConsumption`, `adminId`, `adminName`, `adminType`, `version`, `createTime`, `updateTime`, `loadLicenStatusNumber`, `recordStatus`) VALUES ('" + truck_number + "', 8, '9.6', 1, '厢式车', 6.0, 1.0, NULL, NULL, 1000,11000, 2, 0, 'https://public.fuyoukache.com/eecb1690-7b20-4878-bb8e-3917b3b4da64---14.jpg', 3, 'https://public.fuyoukache.com/9320acd2-4fcc-4782-82d8-1001fc08df44---21.jpg', 3, 'https://public.fuyoukache.com/21456509-c731-4705-b29f-a91fbfcac707---22.jpg', 3, NULL, NULL, NULL, 2, NULL, 1649, '高鹏鸿', 3, 1, '2019-06-04 20:15:34', '2019-06-05 11:30:36', NULL, 0);"
            remote_database(self.env, 'fykc_xdriver_service', insert_truck_sql)
            select_truck = "select id  from  truck_info where plateNumber='" + truck_number + "'"
            print(select_truck)
            truck_id = remote_database(self.env, 'fykc_xdriver_service', select_truck)
            truck_id1 = str(truck_id[0][0])
            if truck_status ==1:
                driver_band_truck_sql = "INSERT INTO `driver_truck_map`(`driverId`, `truckId`, `imgDriverTruckGroup`, `driverTruckStatus`, `auditName`, `checkRemark`, `status`, `isDefault`, `createTime`, `updateTime`)  VALUES  (" + driver_id1 + ", " + truck_id1 + ", 'https://public.fuyoukache.com/20987071-1ad9-460c-9e7b-53c3cd0138ff---身份证x.png', 1, NULL, NULL, 0, 1, '2019-06-03 15:21:48', '2019-06-04 14:35:01');"
            elif truck_status==3 :
                driver_band_truck_sql = "INSERT INTO `driver_truck_map`(`driverId`, `truckId`, `imgDriverTruckGroup`, `driverTruckStatus`, `auditName`, `checkRemark`, `status`, `isDefault`, `createTime`, `updateTime`)  VALUES  (" + driver_id1 + ", " + truck_id1 + ", 'https://public.fuyoukache.com/20987071-1ad9-460c-9e7b-53c3cd0138ff---身份证x.png', 3, NULL, NULL, 0, 1, '2019-06-03 15:21:48', '2019-06-04 14:35:01');"
            elif truck_status == 2:
                driver_band_truck_sql = "INSERT INTO `driver_truck_map`(`driverId`, `truckId`, `imgDriverTruckGroup`, `driverTruckStatus`, `auditName`, `checkRemark`, `status`, `isDefault`, `createTime`, `updateTime`)  VALUES  (" + driver_id1 + ", " + truck_id1 + ", 'https://public.fuyoukache.com/20987071-1ad9-460c-9e7b-53c3cd0138ff---身份证x.png', 2, NULL, NULL, 0, 1, '2019-06-03 15:21:48', '2019-06-04 14:35:01');"
            print(driver_band_truck_sql)
            remote_database(self.env, 'fykc_xdriver_service', driver_band_truck_sql)
            driver_band_bank_sql = "INSERT INTO  `bank_card_info`(`driverId`, `accountType`, `bankName`, `bankCardNumber`, `bankAccount`, `bankProvince`, `bankProvinceName`, `bankCity`, `bankCityName`, `depositBankName`, `bankColor`, `bankShort`) VALUES (" + driver_id1 + ", 1, '招商银行', '6225880150027531', '李东东', NULL, NULL, NULL, NULL, '', '#C85656', 'CMB');"
            remote_database(self.env, 'fykc_xdriver_service', driver_band_bank_sql)
            driver_pay1_sql1 = "INSERT INTO `driver_deposit`(`driverId`, `isDeposit`, `deposit`, `updateTime`) VALUES (" + driver_id1 + ", 1, 200, NULL);"
            remote_database(self.env, 'fykc_wxtrucking_bidding', driver_pay1_sql1)
            driver_pay2_sql = "INSERT INTO `driver_deposit`(`amount`, `driverId`, `driverName`, `driverMobile`, `status`, `createTime`, `updateTime`) VALUES (200.00, " + driver_id1 + ", '文彦平', '16666666667', 1, '2019-06-13 14:41:36', '2019-06-13 14:41:36');"
            remote_database(self.env, 'fykc_truck_scheduler', driver_pay2_sql)
            # 添加定位
            driver_location = "INSERT INTO driver_location`(`driverId`, `latitude`, `longitude`, `provinceName`, `cityName`, `districtName`, `address`, `orderSn`, `createTime`, `updateTime`) VALUES (" + driver_id1 + ", 40.03623, 116.307452, '北京市', '北京市', '海淀区', '北京市海淀区上地街道润莘泽学校金隅嘉华大厦', NULL, '2019-11-02 12:22:31', '2019-11-02 10:42:13');"
            remote_database(self.env, 'fykc_wxtrucking_bidding', driver_location)
            # 交固定路线押金
            # driver_pay1_sql2 = "INSERT INTO   driver_deposit_info`(`id`, `driverId`, `type`, `hasPayMoney`, `deductMoney`, `status`, `createTime`, `updateTime`) VALUES (2, " + driver_id1 + ", 2, 0.01, 0.00, 0, '2019-10-29 13:50:06', '2019-11-02 16:30:23');"
            # remote_database(env, 'fykc_xdriver_service', driver_pay1_sql2)
            driver_list.append(driver_mobile)
        return ' '.join(driver_list)


if __name__ == "__main__":
    #审核通过 2   审核中1    不通过 3
    res = AddDriver("t9").add_driver_3(2,145,3,2)
    print(res)
