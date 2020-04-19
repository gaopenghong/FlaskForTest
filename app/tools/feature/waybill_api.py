# -*- coding: utf-8 -*-
# __author__ = liuchunfu
# __time__   = 2019-09-02

# coding: utf-8
import json
import requests
import time

env = 'r1'
data_agent = {
    'appVersion': '2.7.0',
    'osVersion': '8.0.0',
    'osType': 1,
    'network': 4,
    'networkType': -1,
    'imei': '862258033319303',
    'model': 'MI 5',
    'devVersion': 50,
    'PhoneType': 'MEIZU'
}
data_driver = {
    'appVersion': '3.4.0',
    'osVersion': '8.0.0',
    'osType': 1,
    'network': 4,
    'networkType': -1,
    'imei': '862258033319303',
    'model': 'MI 5',
    'devVersion': '80',
}


# 货主PC-登录
def customer_login(mobile):
    url = 'https://%shz.fuyoukache.com/api/pc/u/login' % env
    data = {
        'mobile': mobile,
        'password': 'e10adc3949ba59abbe56e057f20f883e'
    }
    r = requests.post(url, data)
    return r.cookies.get_dict()


# 货主PC-新增询价
def customer_order_create(car_model=1, cookies=None):
    url = 'https://%shz.fuyoukache.com/api/pc/quote/confirm' % env
    current_time = int(time.time()) - int(time.time()) % 3600
    data_stop_points = [
        {
            'address': '杏花岭区',
            'districtId': 2473,
            'districtName': '杏花岭区',
            'cityId': 300,
            'cityName': '太原',
            'provinceId': 23,
            'provinceName': '山西',
            'planInTime': (current_time + 3600 * 3) * 1000,
            'planOutTime': (current_time + 3600 * 4) * 1000
        },
        {
            'address': '金隅嘉华大厦',
            'districtId': 502,
            'districtName': '海淀区',
            'cityId': 52,
            'cityName': '北京',
            'provinceId': 2,
            'provinceName': '北京',
            'planInTime': (current_time + 3600 * 12) * 1000,
            'planOutTime': ''
        }
    ]
    data = {
        'goodsName': '技术测试',
        'goodsWeight': 5,
        'goodsCubage': 6,
        'goodsNum': 7,
        'needReceipt': 1,
        'planTransTime': 28800,
        'goodsLoadDate': (current_time + 3600 * 3) * 1000,
        'carLengthId': 8,
        'carModelId': car_model,
        'tags': '13,18',
        'comments': '技术测试',
        'stopPoints': json.dumps(data_stop_points)
    }
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 货主PC-运单详情
def customer_order_detail(order_sn, cookies):
    url = 'https://%shz.fuyoukache.com/api/pc/order/detail' % env
    data = {
        'orderSn': order_sn
    }
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 货主PC-确定下单
def customer_order_confirm(order_sn, cookies):
    url = 'https://%shz.fuyoukache.com/api/pc/quote/confirmOrder' % env
    data_contacts = [
        {
            'id': 19771880,
            'contactMobile': '13011111111',
            'contactName': '测试一'
        },
        {
            'id': 19771881,
            'contactMobile': '13022222222',
            'contactName': '测试二'}
    ]
    data = {
        'orderSn': order_sn,
        'stopPoints': json.dumps(data_contacts)
    }
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 统一登录-生成登录验证码
def ua_generate_check_code():
    url = 'https://%sua.fuyoukache.com/api/uc/src/image/genCheckCodeRequest' % env
    r = requests.get(url)
    return r.text


# 经纪人登录
def agent_app_login(mobile, check_code='1123'):
    url = 'https://%sxbroker.fuyoukache.com/api/app/u/login' % env
    data_2 = {
        'mobile': mobile,
        'checkCode': check_code
    }
    data = {k: v for data in [data_agent, data_2] for k, v in data.items()}
    r = requests.post(url, data)
    return r.json()


# 经纪人安排司机
def agent_arrange_driver(order_sn, driver_info, token):
    url = 'https://%sxbroker.fuyoukache.com/api/app/orderinfo/arrangeDriver.do' % env
    data = {
        'token': token,
        'orderSn': order_sn,
        'driverId': driver_info['driverId'],
        'driverName': driver_info['driverName'],
        'driverMobile': driver_info['driverMobile'],
        'plateNumber': driver_info['truckInfoList'][0]['plateNumber'],
        'identificationNumber': driver_info['idCardNo'],
        'carLength': driver_info['truckInfoList'][0]['carLengthId'],
        'carModel': driver_info['truckInfoList'][0]['carModelId'],
        'loadTime': str(int(time.time()) * 1000 + 12000000),
        'unloadTime': str(int(time.time()) * 1000 + 48000000)
    }
    data.update(data_agent)
    r = requests.post(url, data)
    return r.json()


# 司机登录
def driver_login(mobile, check_code='1123'):
    url = 'https://%sxdriver.fuyoukache.com/api/app/u/login' % env
    data = {
        'mobile': mobile,
        'checkCode': check_code
    }
    data.update(data_driver)
    r = requests.post(url, data)
    return r.json()


# 统一登录-登录
def ua_login(mobile, password, request_id):
    url = 'https://%sua.fuyoukache.com/api/uc/auth/login' % env
    data = {
        'userName': mobile,
        'userPassword': password,
        'srcType': '',
        'redirectUrl': '',
        'checkCode': '1123',
        'requestId': request_id
    }
    r = requests.post(url, data)
    return r.cookies.get_dict()


# 运单系统-运单详情
def bms_order_detail(order_sn, cookies):
    url = 'https://%sbms.fuyoukache.com/service/fykc-bms-wrapper/api/order/detail.do' % env
    data = {
        'orderSn': order_sn
    }
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 调度系统-获取司机详情
def dispatch_get_driver_info(mobile, cookies):
    url = 'https://%sdd.fuyoukache.com/service/fykc-truck-scheduler/api/dispatch/getDriverInfo.do' % env
    data = {
        'driverMobile': mobile,
        'needHistoryOrder': 0,
        'needForYouInfo': 1
    }
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 调度系统-安排司机
def dispatch_arrange_driver(order_sn, driver_info, cookies):
    url = 'https://%sdd.fuyoukache.com/service/fykc-truck-scheduler/api/dispatch/arrangeDriver.do' % env
    data = {
        'orderSn': order_sn,
        'driverId': driver_info['driverId'],
        'driverName': driver_info['driverName'],
        'driverMobile': driver_info['driverMobile'],
        'plateNo': driver_info['truckInfoList'][0]['plateNumber'],
        'idCardNo': driver_info['idCardNo'],
        'carLengthId': driver_info['truckInfoList'][0]['carLengthId'],
        'carModelId': driver_info['truckInfoList'][0]['carModelId'],
        'idCardFrontPic': driver_info['idCardFrontPic'],  # 身份证人像面
        'idCardBackPic': driver_info['idCardBackPic'],  # 身份证国徽面
        'idCardAddress': driver_info['idCardAddress'],  # 身份证地址
        'licensePic': driver_info['licensePic'],  # 驾驶证
        'driverPic': driver_info['truckInfoList'][0]['imgCarLicense'],  # 行驶证
        'loadPic': driver_info['truckInfoList'][0]['imgLoadLicense'],  # 运输许可证
        'insurancePic': driver_info['truckInfoList'][0]['imgInsurance'],  # 保险卡
        'driverCarPic': driver_info['truckInfoList'][0]['imgDriverTruckGroup'],  # 人车合影
        'checkStatus': '3',  # 审核状态
        'transFee': '6000',  # 运费
        'tradeDeposit': '0',  # 回单押金
        'deposit': '2000',  # 押金
        'payDepositType': '0',  # 押金渠道: 0微信, 1运满满
        'tags': '',
        'remark': '',
        "driverTruckMapId": driver_info['truckInfoList'][0]['driverTruckMapId'],
        'truckInfoId': driver_info['truckInfoList'][0]['id'],
        'from': '',
        'deduct': '',
        'deductReason': '',
        'isDefault': driver_info['truckInfoList'][0]['isDefault']
    }
    print('调度系统安排司机: %s, %s' % (url, data))
    r = requests.post(url, data, cookies=cookies)
    return r.json()


# 运单流程
def flow(customer_mobile, agent_mobile, driver_mobile, admin_mobile='16888888888', car_model=1):
    print('env: %s' % env)
    # 货主登录
    cookies_customer = customer_login(customer_mobile)
    print('货主PC登录: %s' % cookies_customer)
    # 管理员登录
    check_code = ua_generate_check_code()
    cookies_ua = ua_login(admin_mobile, 'Fy@123456789', check_code)
    print('管理员登录: %s' % cookies_ua)
    # 货主新增询价
    r_order_create = customer_order_create(car_model, cookies_customer)
    print('货主PC新增询价: %s' % r_order_create)
    order_sn = r_order_create['data'][0]['orderSn']
    print('运单号: %s' % order_sn)
    # 货主运单详情
    time.sleep(1)
    r_order_detail = customer_order_detail(order_sn, cookies_customer)
    print('货主运单详情: %s' % r_order_detail)
    r_order_confrim = customer_order_confirm(order_sn, cookies_customer)
    print('货主确定下单: %s' % r_order_confrim)
    # 运单系统-运单详情
    time.sleep(1)
    r_bms_order_detail = bms_order_detail(order_sn, cookies_ua)
    print('运单系统运单详情: %s' % r_bms_order_detail)
    return order_sn


if __name__ == '__main__':
    order_1 = flow('12211111111', '18310179572', '16011111111', '16888888888', 1)  # 厢式车
    order_2 = flow('12211111111', '18310179572', '13121768752', '16888888888', 2)  # 平板车
    print('%s, %s' % (order_1, order_2))
