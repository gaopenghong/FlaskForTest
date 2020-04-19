# coding:utf-8
from .base import *


class ApiCustomerPC(Base):
    """货主PC接口"""

    # 货主PC-登录
    def customer_pc_login(self):
        url = self.mk_url('hz', 'api/pc/u/login')
        data = {
            'mobile': self.customer_mobile,
            'password': md5_encrypt(self.customer_password)
        }
        r = requests.post(url, data)
        return r.cookies.get_dict()

    # 货主PC-新增询价
    def customer_pc_order_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        data_stop_points = [
            {
                'address': '胜利街99号',
                'districtId': 2473,
                'districtName': '杏花岭区',
                'cityId': 300,
                'cityName': '太原',
                'provinceId': 23,
                'provinceName': '山西',
                'planInTime': (current_time + 3600 * 3) * 1000,
                'planOutTime': (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 112.570530,
                "latitude": 37.894030
            },
            {
                'address': '民悦广场',
                'districtId': 2060,
                'districtName': '沈河区',
                'cityId': 244,
                'cityName': '沈阳',
                'provinceId': 18,
                'provinceName': '辽宁',
                'planInTime': (current_time + 3600 * 12) * 1000,
                'planOutTime': '',
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 123.476390,
                "latitude": 41.771690
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'goodsCubage': 6,
            'goodsNum': 7,
            'needReceipt': 1,
            # 'planTransTime': 28800,
            'planTransTime': 71940,
            'goodsLoadDate': (current_time + 3600 * 12) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': '技术测试',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--调度自营
    def customer_pc_project_order_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        data_stop_points = [
            {
                'address': '胜利街99号',
                'districtId': 2473,
                'districtName': '杏花岭区',
                'cityId': 300,
                'cityName': '太原',
                'provinceId': 23,
                'provinceName': '山西',
                'planInTime': (current_time + 3600 * 3) * 1000,
                'planOutTime': (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 112.570530,
                "latitude": 37.894030
            },
            {
                'address': '民悦广场',
                'districtId': 2060,
                'districtName': '沈河区',
                'cityId': 244,
                'cityName': '沈阳',
                'provinceId': 18,
                'provinceName': '辽宁',
                'planInTime': (current_time + 3600 * 12) * 1000,
                'planOutTime': '',
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 123.476390,
                "latitude": 41.771690
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'goodsCubage': 6,
            'goodsNum': 7,
            'needReceipt': 1,
            # 'planTransTime': 28800,
            'planTransTime': 71940,
            'goodsLoadDate': (current_time + 3600 * 12) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货调度自营订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--一口价
    def customer_pc_project_order_one_price_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 项目货订单--一口价--路线信息
        data_stop_points = [
            {
                "address": "胜利街99号",
                "districtId": 2473,
                "districtName": "杏花岭区",
                "cityId": 300,
                "cityName": "太原",
                "provinceId": 23,
                "provinceName": "山西",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 112.570530,
                "latitude": 37.894030
            },
            {
                "address": "前进大街1855号",
                "districtId": 1770,
                "districtName": "朝阳区",
                "cityId": 211,
                "cityName": "长春",
                "provinceId": 15,
                "provinceName": "吉林",
                "planInTime": (current_time + 3600 * 40) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 125.288450,
                "latitude": 43.833270
            }
        ]
        print('data_stop_points-----------', data_stop_points)
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            # 'goodsCubage': 6,
            # 'goodsNum': 7,
            'needReceipt': 1,
            'planTransTime': 75600,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货一口价订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--企业运力
    def customer_pc_project_order_agengt_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        data_stop_points = [
            {
                'address': '政府街19号',
                'districtId': 512,
                'districtName': '昌平区',
                'cityId': 52,
                'cityName': '北京',
                'provinceId': 2,
                'provinceName': '北京',
                'planInTime': (current_time + 3600 * 3) * 1000,
                'planOutTime': (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 116.231280,
                "latitude": 40.220770
            },
            {
                'address': '邓石如路',
                'districtId': 400,
                'districtName': '宜秀区',
                'cityId': 36,
                'cityName': '安庆',
                'provinceId': 3,
                'provinceName': '安徽',
                'planInTime': (current_time + 3600 * 12) * 1000,
                'planOutTime': '',
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 116.989330,
                "latitude": 30.613580
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'goodsCubage': 6,
            'goodsNum': 7,
            'needReceipt': 1,
            # 'planTransTime': 28800,
            'planTransTime': 71940,
            'goodsLoadDate': (current_time + 3600 * 12) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货企业运力',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--固定司机
    def customer_pc_project_order_driver_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        data_stop_points = [
            {
                'address': '新华西街',
                'districtId': 2162,
                'districtName': '回民区',
                'cityId': 258,
                'cityName': '呼和浩特',
                'provinceId': 19,
                'provinceName': '内蒙古',
                'planInTime': (current_time + 3600 * 3) * 1000,
                'planOutTime': (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 111.622990,
                "latitude": 40.807720
            },
            {
                'address': '邓石如路',
                'districtId': 400,
                'districtName': '宜秀区',
                'cityId': 36,
                'cityName': '安庆',
                'provinceId': 3,
                'provinceName': '安徽',
                'planInTime': (current_time + 3600 * 42) * 1000,
                'planOutTime': '',
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 116.989330,
                "latitude": 30.613580
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'goodsCubage': 6,
            'goodsNum': 7,
            'needReceipt': 1,
            # 'planTransTime': 28800,
            'planTransTime': 100940,
            'goodsLoadDate': (current_time + 3600 * 12) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货固定司机',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--智能调度
    def customer_pc_project_order_scheduler_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 项目货订单--智能调度--路线信息
        data_stop_points = [
            {
                "address": "飞虹路518号",
                "districtId": 2712,
                "districtName": "虹口区",
                "cityId": 321,
                "cityName": "上海",
                "provinceId": 25,
                "provinceName": "上海",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 121.505150,
                "latitude": 31.264510
            },
            {
                "address": "十梓街338号",
                "districtId": 3494,
                "districtName": "姑苏区",
                "cityId": 221,
                "cityName": "苏州",
                "provinceId": 16,
                "provinceName": "江苏",
                "planInTime": (current_time + 3600 * 40) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 120.631320,
                "latitude": 31.302270
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'needReceipt': 1,
            'planTransTime': 75600,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货智能调度订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--项目货订单--日包车
    def customer_pc_project_order_daily_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 项目货订单--日包车--路线信息
        data_stop_points = [
            {
                "address": "北京东路9号",
                "districtId": 2931,
                "districtName": "城关区",
                "cityId": 344,
                "cityName": "拉萨",
                "provinceId": 28,
                "provinceName": "西藏",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 91.137750,
                "latitude": 29.652620
            },
            {
                "address": "政府街19号",
                "districtId": 512,
                "districtName": "昌平区",
                "cityId": 52,
                "cityName": "北京",
                "provinceId": 2,
                "provinceName": "北京",
                "planInTime": (current_time + 3600 * 72) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 116.231280,
                "latitude": 40.220770
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'needReceipt': 1,
            'planTransTime': 259200,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试项目货日包车订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--图灵订单--调度自营
    def customer_pc_turing_order_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 图灵订单--调度自营--路线信息
        data_stop_points = [
            {
                'address': '胜利街99号',
                'districtId': 2473,
                'districtName': '杏花岭区',
                'cityId': 300,
                'cityName': '太原',
                'provinceId': 23,
                'provinceName': '山西',
                'planInTime': (current_time + 3600 * 3) * 1000,
                'planOutTime': (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 112.570530,
                "latitude": 37.894030
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
                'planOutTime': '',
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 116.308170,
                "latitude": 40.036240
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'goodsCubage': 6,
            'goodsNum': 7,
            'needReceipt': 1,
            # 'planTransTime': 28800,
            'planTransTime': 71940,
            'goodsLoadDate': (current_time + 3600 * 12) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试图灵调度自营订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--图灵订单--一口价
    def customer_pc_turing_order_one_price_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 图灵订单--一口价--路线信息
        data_stop_points = [
            {
                "address": "胜利街99号",
                "districtId": 2473,
                "districtName": "杏花岭区",
                "cityId": 300,
                "cityName": "太原",
                "provinceId": 23,
                "provinceName": "山西",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 112.570530,
                "latitude": 37.894030
            },
            {
                "address": "前进大街1855号",
                "districtId": 1770,
                "districtName": "朝阳区",
                "cityId": 211,
                "cityName": "长春",
                "provinceId": 15,
                "provinceName": "吉林",
                "planInTime": (current_time + 3600 * 40) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 125.288450,
                "latitude": 43.833270
            }
        ]
        print('data_stop_points-----------', data_stop_points)
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            # 'goodsCubage': 6,
            # 'goodsNum': 7,
            'needReceipt': 1,
            'planTransTime': 75600,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试图灵一口价订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--图灵订单--智能调度
    def customer_pc_turing_order_scheduler_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 图灵订单--智能调度--路线信息
        data_stop_points = [
            {
                "address": "长宁路599号",
                "districtId": 2703,
                "districtName": "长宁区",
                "cityId": 321,
                "cityName": "上海",
                "provinceId": 25,
                "provinceName": "上海",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 121.423940,
                "latitude": 31.220240
            },
            {
                "address": "太湖东路",
                "districtId": 1851,
                "districtName": "吴中区",
                "cityId": 221,
                "cityName": "苏州",
                "provinceId": 16,
                "provinceName": "江苏",
                "planInTime": (current_time + 3600 * 40) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 120.632120,
                "latitude": 31.262490
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'needReceipt': 1,
            'planTransTime': 75600,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试图灵智能调度订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-新增询价--图灵订单--日包车
    def customer_pc_turing_order_daily_create(self, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        current_time = int(time.time()) - int(time.time()) % 3600
        # 图灵订单--日包车--路线信息
        data_stop_points = [
            {
                "address": "北京东路9号",
                "districtId": 2931,
                "districtName": "城关区",
                "cityId": 344,
                "cityName": "拉萨",
                "provinceId": 28,
                "provinceName": "西藏",
                "planInTime": (current_time + 3600 * 3) * 1000,
                "planOutTime": (current_time + 3600 * 4) * 1000,
                "contactMobile": "18000000001",
                "contactName": "测试一",
                "longitude": 91.137750,
                "latitude": 29.652620
            },
            {
                "address": "政府街19号",
                "districtId": 512,
                "districtName": "昌平区",
                "cityId": 52,
                "cityName": "北京",
                "provinceId": 2,
                "provinceName": "北京",
                "planInTime": (current_time + 3600 * 72) * 1000,
                # "planOutTime": None,
                "contactMobile": "18000000002",
                "contactName": "测试二",
                "longitude": 116.231280,
                "latitude": 40.220770
            }
        ]
        data = {
            'goodsName': '技术测试',
            'goodsWeight': 5,
            'needReceipt': 1,
            'planTransTime': 259200,
            'goodsLoadDate': (current_time + 3600 * 3) * 1000,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': '13,18',
            'comments': 'ftest技术测试图灵日包车订单',
            'stopPoints': json.dumps(data_stop_points)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-运单详情
    def customer_pc_order_detail(self, order_sn, cookies):
        url = self.mk_url('hz', 'api/pc/order/detail')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 货主PC-确定下单
    def customer_pc_order_confirm(self, order_sn, cookies):
        url = self.mk_url('hz', 'api/pc/quote/confirmOrder')
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

    # 货主PC-运单线下付款
    def customer_pc_confirm_transfer_accounts(self, order_sn, cookies):
        url = self.mk_url('hz', 'api/pc/pay/confirmTransferAccounts')
        data = {
            'orderSn': order_sn,
            'accountNum': '123454321'
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()


if __name__ == '__main__':
    pass
