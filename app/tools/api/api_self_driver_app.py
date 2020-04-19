# coding:utf-8
from .base import *

data_mobile = {
    'appVersion': '1.0.0',
    'osVersion': '8',
    'osType': 1,
    'network': 3,
    'networkType': 23,
    'imei': '23232323232323',
    'model': 'IM8',
    'devVersion': 1,
    'phoneType': "IPHONE",
    'isForyou': 1,
    'customerType': 5
}


class ApiFyDriverApp(Base):
    """共建车APP接口"""

    # 司机登录
    def self_driver_login(self, driver_mobile, check_code=1123):
        url = self.mk_url('xdriver', 'api/app/u/login')
        data = {
            'mobile': driver_mobile,
            'checkCode': check_code
        }
        data.update(data_mobile)
        r = requests.post(url, data)
        return r.json()

    # 待接单信息
    def self_driver_wait_order_info(self, token):
        url = self.mk_url('xdriver', 'api/app/foryou/waitOrderInfo')
        data = {
            'token': token
        }
        r = requests.post(url, data)
        return r.json()

    # 司机接单
    def self_driver_accept(self, token, order):
        url = self.mk_url('xdriver', 'api/app/foryou/accept')
        data = {
            'token': token,
            'orderSn': order
        }
        r = requests.post(url, data)
        return r.json()

    # 专车车辆信息
    def self_driver_get_truck_detail(self, token):
        url = self.mk_url('xdriver', 'api/app/foryou/getTruckDetail')
        data = {
            'token': token
        }
        r = requests.post(url, data)
        return r.json()

    # 公里数申诉_34
    def self_driver_insert_apply(self, token, order_sn, free_distance=50, trans_distance=200):
        url = self.mk_url('xdriver', 'api/app/foryou/appeal/insertAppeal')
        data1 = [
            'https://public.fuyoukache.com/common/5bfbb39bb3565.jpg'
        ]
        data = {
            'token': token,
            'orderSn': order_sn,
            'freeDistance': free_distance,
            'transDistance': trans_distance,
            'reason': "测试申诉原因",
            'imgUrl': json.dumps(data1)

        }
        data.update(data_mobile)
        r = requests.post(url, data)
        return r.json()

    # 上报停车费_45
    def self_driver_parkfee_report(self, token, order, fee=20.5, note='测试数据'):
        url = self.mk_url('xdriver', 'api/app/foryou/parkingFee/report')
        data1 = [{
            'fee': fee,
            'note': note,
            'imgUrl': ['https://public.fuyoukache.com/common/5bfbb39bb3565.jpg'],
            'point': 1,
            "inTime": 1559028607000,
            "outTime": 1559029607000
        }]
        data = {
            'token': token,
            'orderSn': order,
            'detail': json.dumps(data1)
        }

        r = requests.post(url, data)
        return r.json()

    # 违章上报_48
    def self_driver_violation_report(self, token, order, bill_type, violate_type, penalty, deduct, violate_time, note):
        url = self.mk_url('xdriver', 'api/app/foryou/violation/report')
        data1 = ['https://public.fuyoukache.com/common/5bfbb39bb3565.jpg']
        data = {
            'token': token,
            'orderSn': order,
            'billType': bill_type,
            'violateType': violate_type,
            'penalty': penalty,
            'scoreDeduct': deduct,
            'violateTime': violate_time,
            'imgUrl': json.dumps(data1),
            'note': note
        }

        r = requests.post(url, data)
        return r.json()

    # 过路费上报_51
    def self_driver_road_report(self, token, order, fee, note):
        url = self.mk_url('xdriver', 'api/app/foryou/roadToll/report')
        data1 = ['https://public.fuyoukache.com/common/5bfbb39bb3565.jpg']
        data = {
            'token': token,
            'orderSn': order,
            'fee': fee,
            'imgUrl': json.dumps(data1),
            'note': note
        }

        r = requests.post(url, data)
        return r.json()

    # 运单生成
    def self_driver_make_order(self):
        url_login = self.mk_url('hz', 'api/pc/u/login')
        data_login = {
            'mobile': '12211111111',
            'password': 'e10adc3949ba59abbe56e057f20f883e'
        }
        r = requests.post(url_login, data_login, verify=False)
        cookies1 = r.cookies

        trans_point_list = [
            {"address": "上海市虹口区人民政府",
             "districtId": 2712,
             "districtName": "虹口区",
             "cityId": 321, "cityName": "上海", "provinceId": 25, "provinceName": "上海", "planInTime": '',
             "planOutTime": '',
             "contactMobile": "131", "contactName": "陆亿"},
            {"address": "苏州市姑苏区人民政府", "districtId": 3494, "districtName": "姑苏区", "cityId": 221,
             "cityName": "苏州", "provinceId": 16,
             "provinceName": "江苏", "planInTime": '', "planOutTime": '', "contactMobile": "132", "contactName": "柳二"}
        ]

        goods_load_time = (int(time.time()) + 3600 * random.randint(3, 5)) * 1000
        url_quote_create = self.mk_url('hz', 'api/pc/quote/confirm')
        data_quote_create = {
            'goodsName': '技术测试',
            'goodsWeight': 12,
            'needReceipt': 1,  # 回单
            'planTransTime': '108000',
            'goodsLoadDate': goods_load_time,
            'carLengthId': 8,
            'carModelId': 1,
            'comments': '',
            'stopPoints': json.dumps(trans_point_list)
        }

        r_create = requests.post(url_quote_create, data_quote_create, verify=False, cookies=cookies1)
        r_create_1 = r_create.json()
        print(r_create_1)

        quote_sn = r_create.json()['data'][0]['orderSn']
        print("运单号：" + quote_sn)

        time.sleep(2)

        data = [
            {"id": 285, "contactMobile": "131", "contactName": "陆亿"},
            {"id": 286, "contactMobile": "132", "contactName": "柳二"}
        ]

        url_quote_confirm = self.mk_url('hz', 'api/pc/quote/confirmOrder')
        data_quote_cofirm = {
            'orderSn': quote_sn,
            'stopPoints': json.dumps(data)
        }

        r = requests.post(url_quote_confirm, data_quote_cofirm, cookies=cookies1)
        r1 = r.json()
        print(r1)
        return quote_sn

    # 过路费上报记录列表
    def truck_report_cashroad_fee_list(self, cookies_bg, order_sn):
        url = self.mk_url('truckfy', '/api/reportFee/cashroadFeeList')
        data = {
            'pageSize': 1,
            'pageIndex': 10,
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()

    # 过路费审核
    def truck_report_cashroad_fee_update(self, cookies_bg, report_id, status):
        url = self.mk_url('truckfy', '/api/reportFee/cashroadFeeUpdate')
        data = {
            'id': report_id,  # 当前要申诉的Id
            'status': status,
            'operRemark': '哈哈哈哈'

        }
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()

    # 首页运单列表_10
    def self_driver_order_list(self, token, index=1, size=5):
        url = self.mk_url('xdriver', 'api/app/foryou/orderList')
        data = {
            'token': token,
            'pageIndex': index,
            'pageSize': size
        }

        r = requests.post(url, data)
        return r.json()
