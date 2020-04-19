from app.tools.api.base import *
import datetime
import random
import time
import json
import requests
from app.tools.api.conf import *
from app.tools.api.config import *


class ApiDebang(Base):
    """德邦相关接口"""

    # 随机生成德邦整车单号
    def random_order_zc(self):
        r = random.randrange(1000, 9999)
        a = time.strftime('%Y%m%d%H', time.localtime())
        thirdSn = '%s%s%s' % ('ZC', a, r)
        # print(thirdSn)
        return thirdSn

    # 随机生成德邦整车单号
    def random_order_gx(self):
        r = random.randrange(1000, 9999)
        a = time.strftime('%Y%m%d%H', time.localtime())
        thirdSn = '%s%s%s' % ('GX', a, r)
        # print(thirdSn)
        return thirdSn

    # 德邦询价  productType 4是干线，5是整车(线上对账)
    def create_db_order(self, thirdSn, departureName, arrivalsName, models, boxType, productType, price=''):
        url = self.mk_url('nopen', 'debang/create')
        # print(url)
        requestEntity = {
            "orderCode": thirdSn,
            "goodsName": "货物名称",
            "dimensional": "8",
            "weight": "6",
            "departureName": departureName,
            "arrivalsName": arrivalsName,
            "useCarTime": (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "arrivalTime": (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "need_quantity": "3",
            "price": price,
            "cars": [
                {
                    "models": models,
                    "boxType": boxType
                },
            ],
            "productType": productType,
            "added_service": [1, 3],  # 传2是要传回单
            "failuretime": (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "contactsName": "张三",
            "contactsPhone": "13888888888",
            "createDeptName": "张健的营业部哈哈",
            "remarks": "备注"
        }
        data = {
            "type": "order",
            "requestEntity": requestEntity
        }
        data = json.dumps(data)
        #print(data)
        r = requests.post(url, data)
        #print(r.json())
        return r.json()

    # 确认下单
    '''orderStauts:订单状态 0：订单关闭 1：确认中标2:已打印运输合同3：确认发车：4确认到达
    5：已开单（传输货物价值、货物名称、数量、出发外场和包装、运单号）6：竞标失败7：已签收, 8(干线订单传车次号)'''

    def comfirm_db_order(self,  orderCode, orderStauts):
        url = self.mk_url('nopen', 'debang/order')
        requestEntity = {
            "allCost": None,
            "arrivalsDetaile": "沈阳北站",
            "bareCar": None,
            "billCode": None,
            "consigneeContactName": None,
            "consigneeMoblie": None,
            "courierDimensional": None,
            "courierWeight": None,
            "departureDetaile": "金隅嘉华大厦",
            "departureFieldNameCode": None,
            "dimensional": None,
            "goodsName": None,
            "goodsPrice": None,
            "lclDimensional": None,
            "lclWeight": None,
            "num": None,
            "operationTime": int(round(time.time() * 1000)),
            "orderCode": orderCode,
            "orderStauts": orderStauts,
            "packing": None,
            "paymentMethod": None,
            "price": None,
            "pushfoss": "0",
            "uniqueId": "119060326690",
            "vehicletips": "CC1234567890",
            "weight": None
        }
        data = {
            "requestEntity": requestEntity,
            "type": "ORDERSTAUTS"
        }

        data = json.dumps(data)
        r = requests.post(url, data)
        # print(r.json())
        return r.json()

    # 模拟德邦发起对账
    def push_fy_checking(self, thirdsn):
        url = self.mk_url('nopen', 'api/outer/deppon/depponCheckOrder')
        data = {
            "orderCode": thirdsn,
            "waybillNo": "1876543213",
            "interfaceCode": "PT20160510150444611",
            "signState": "1",
            "actualPayment": 5555,
            "quotationAmount": 5555,
            "adjustmentAmount": 0,
            "reason": "原因"
        }
        data = json.dumps(data)
        r = requests.post(url, data)
        # print(r.json())
        return r.json()


class ApiJd(Base):
    """京东相关接口"""

    # 获取京东sign
    def sign(self):
        a = '%s&%s&%s' % (get_config('open', 'app_key_jd'), int(time.time()), get_config('open', 'app_secret_jd'))
        sign = {
            "app_key": get_config('open', 'app_key_jd'),
            "time_stamp": int(time.time()),
            "sign_str": md5_encrypt(a)
        }
        return sign

    # 京东内部网点单号随机生成
    def random_in_numbers_jd(self):
        r = random.randrange(1000, 9999)
        a = time.strftime('%Y%m%d', time.localtime())
        thirdsn = '%s%s%s' % ('XJ', a, r)
        return thirdsn

    # 京东外部网点单号随机生成
    def random_out_numbers_jd(self):
        r = random.randrange(1000, 9999)
        a = time.strftime('%Y%m%d', time.localtime())
        thirdsn = '%s%s%s' % ('JD', a, r)
        return thirdsn

    # 京东调用福佑询价接口-外部网点
    def jd_xun_jia_out_point(self, carlengthtype, thirdsn, bengin_adress, end_adress):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/create', self.sign())
        data = {
            'thirdSn': thirdsn,
            'customerDept': 1,
            'customerName': '京东接口-发货员',
            'customerMobile': '12345678901',
            'goodsName': '小苹果',
            'goodsWeight': 234,
            'goodsCubage': 30,
            'addressType': 0,
            'startCityCode': bengin_adress['startCityCode'],
            'startCityName': bengin_adress['startCityName'],
            'startDistrictCode': bengin_adress['startDistrictCode'],
            'startDistrictName': bengin_adress['startDistrictName'],
            'startProvinceCode': bengin_adress['startProvinceCode'],
            'startProvinceName': bengin_adress['startProvinceName'],
            'startAddress': bengin_adress['startAddress'],
            'endProvinceName': end_adress['endProvinceName'],
            'endProvinceCode': end_adress['endProvinceCode'],
            'endCityName': end_adress['endCityName'],
            'endCityCode': end_adress['endCityCode'],
            'endDistrictName': end_adress['endDistrictName'],
            'endDistrictCode': end_adress['endDistrictCode'],
            'endAddress': end_adress['endAddress'],
            'loadTime': int(time.time() + 10000),
            'unloadTime': int(time.time() + 20000),
            'carModelCode': carlengthtype,
            'addedService': '',
            'needReceipt': 1,
            'needInsurance': '1',
            'goodsValue': 3000000,
            'goodsType': 'CB011',
            'packageType': '101',
            'comments': '',
            'businessDeptName': '',
            'sendTime': int(time.time() + 15000)
        }
        data2 = json.dumps(data, ensure_ascii=False)  # 去除汉字乱码
        data3 = data2.encode()  # 把body转换成utf-8
        r = requests.post(url, data3, headers=headers)  # 发送请求
        r_1 = r.json()
        return r_1

    # 京东调用福佑询价接口-内部网点
    def jd_xun_jia_in_point(self):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/create', self.sign())
        thirdsn = self.random_in_numbers_jd()
        data = {
            'thirdSn': thirdsn,
            'customerDept': 0,
            'customerName': '京东接口-发货员',
            'customerMobile': '12345678901',
            'goodsName': '苹果',
            'goodsWeight': 234.44,
            'goodsCubage': 30,
            'addressType': 0,
            'startCityCode': '1',
            'startCityName': '北京',
            'startDistrictCode': '72',
            'startDistrictName': '朝阳区',
            'startProvinceCode': '1',
            'startProvinceName': '北京',
            'startAddress': '技术测试始发地址',
            'endProvinceName': '河南',
            'endProvinceCode': '7',
            'endCityName': '郑州市',
            'endCityCode': '412',
            'endDistrictName': '新密市',
            'endDistrictCode': '415',
            'endAddress': '河南省郑州市新密市实验高中',
            'loadTime': int(time.time() + 5000),
            'unloadTime': int(time.time() + 20000),
            'carModelCode': 17,
            'addedService': '23,24,25',
            'needReceipt': 0,
            'needInsurance': '1',
            'goodsValue': 3000000,
            'goodsType': 'CB011',
            'packageType': '101',
            'comments': '',
            'businessDeptName': '',
            'sendTime': int(time.time() + 6000),
            'stopPoints': [
                {
                    'address': '上海市金山区调度公园',
                    'cityCode': '2',
                    'cityName': '上海',
                    'districtCode': '2835',
                    'districtName': '金山区',
                    'provinceCode': '2',
                    'provinceName': '上海',
                    'stopType': 0,
                    'planInTime': int(time.time() + 8000),
                    'planOutTime': int(time.time() + 10000)
                }
            ]
        }
        data2 = json.dumps(data, ensure_ascii=False)  # 去除汉字乱码
        data3 = data2.encode()  # 把body转换成utf-8
        r = requests.post(url, data3, headers=headers)  # 发送请求
        r_1 = r.json()
        return r_1

    # 京东外部网点确认下单接口
    def jd_out_xia_dan(self, thirdsn):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/confirm', self.sign())
        # print(url)
        data = {
            'loadAddress': '北京市通州区 123 号',
            'loaderMobile': '13512341234',
            'loaderName': '张三',
            'thirdSn': thirdsn,
            'unloadAddress': '上海市青浦区 234 号',
            'unloaderMobile': '13512341234',
            'unloaderName': '张三'
        }
        data2 = json.dumps(data, ensure_ascii=False)  # 去除汉字乱码
        data3 = data2.encode()  # 把body转换成utf-8
        r = requests.post(url, data3, headers=headers)  # 发送请求
        return r.json()

    # 京东内部网点确认下单接口
    def jd_in_xia_dan(self, thirdsn):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/confirm', self.sign())
        # print(url)
        stoplist = []
        # stoplist = [
        #     {
        #         'contactName': '张三',
        #         'contactMobile': '13812341234',
        #         'address': '北京市海淀区知春路113号'
        #     }
        # ]
        data = {
            'loadAddress': '北京市通州区 123 号',
            'loaderMobile': '13512341234',
            'loaderName': '张三',
            'stopPoints': stoplist,
            'thirdSn': thirdsn,
            'unloadAddress': '上海市青浦区 234 号',
            'unloaderMobile': '13512341234',
            'unloaderName': '张三'
        }
        data2 = json.dumps(data, ensure_ascii=False)  # 去除汉字乱码
        data3 = data2.encode()  # 把body转换成utf-8
        r = requests.post(url, data3, headers=headers)  # 发送请求
        return r.json()


class ApiKy(Base):
    """跨越相关接口"""

    # 获取跨越sign
    def ky_sign(self):
        a = '%s&%s&%s' % (get_config('open', 'app_key_ky'), int(time.time()), get_config('open', 'app_secret_ky'))
        sign = {
            "app_key": get_config('open', 'app_key_ky'),
            "time_stamp": int(time.time()),
            "sign_str": md5_encrypt(a)
        }
        return sign

    # 跨越三方单号随机生成
    def random_numbers_ky(self):
        r = random.randrange(1000, 9999)
        a = time.strftime('%Y%m%d', time.localtime())
        thirdsn = '%s%s-%s' % ('KY', r, a)
        # print(thirdSn)
        return thirdsn

    # 跨域询价接口
    def ky_create_order(self, carlengthtype, thirdsn, bengin_adress, end_adress):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/create', self.ky_sign())
        # print(url)
        data = {
            "addedService": "",
            "businessDeptName": "",
            "carModelCode": carlengthtype,
            "comments": "测试数据",
            "customerDept": 1,
            "customerMobile": "12345678901",
            "customerName": "跨越发货员",
            "endAddress": end_adress["endAddress"],
            "endCityCode": end_adress["endCityCode"],
            "endCityName": end_adress["endCityName"],
            "endDistrictCode": end_adress["endDistrictCode"],
            "endDistrictName": end_adress["endDistrictName"],
            "endProvinceCode": end_adress["endProvinceCode"],
            "endProvinceName": end_adress["endProvinceName"],
            "fykcAddedService": 0,
            "goodsCubage": 102.98,
            "goodsName": "歼20",
            "goodsType": "CB016",
            "goodsValue": 3000,
            "goodsWeight": 234,
            "loadTime": int(time.time() + 5000),
            "needInsurance": 1,
            "needReceipt": "0",
            "packageType": 701,
            "sendTime": int(time.time() + 6000),
            "startAddress": bengin_adress["startAddress"],
            "startCityCode": bengin_adress["startCityCode"],
            "startCityName": bengin_adress["startCityName"],
            "startDistrictCode": bengin_adress["startDistrictCode"],
            "startDistrictName": bengin_adress["startDistrictName"],
            "startProvinceCode": bengin_adress["startProvinceCode"],
            "startProvinceName": bengin_adress["startProvinceName"],
            "thirdSn": thirdsn,
            "unloadTime": int(time.time() + 20000)
        }

        data = json.dumps(data, ensure_ascii=False)
        data = data.encode()
        r = requests.post(url, data, headers=headers)
        return r.json()

    # 确认下单接口
    def ky_query_confirm(self, thirdsn):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/confirm', self.ky_sign())
        data = {
            'loadAddress': '北京市通州区 123 号',
            'loaderMobile': '13512341234',
            'loaderName': '张三',
            'thirdSn': thirdsn,
            'unloadAddress': '上海市青浦区 234 号',
            'unloaderMobile': '13512341234',
            'unloaderName': '张三'
        }
        data = json.dumps(data, ensure_ascii=False)
        data = data.encode()
        r = requests.post(url, data, headers=headers)
        return r.json()


class ApiSf(Base):
    """顺丰相关接口"""

    # 顺丰造询价数据，调用sfTestCreateQuery接口
    def make_sf_order_create(self,  vehicleton, vehicletypecode, bengin_adress, cross_adress, end_adress):
        url = self.mk_url('nopen', 'api/internal/sfTestCreateQuery')
        if cross_adress == 'null':
            data = {
                "exceptionReportPhoneMailbox": "",
                "contestDepteName": "山西区部",
                "reserveRoad": "",
                "modifyTm": time.strftime("%Y%m%d%H%M%S"),
                "accountName": "顺丰速运有限公司",
                "modifier": "StartRunTask",
                "transactionNo": "351Y-T-{0}{1}".format(time.strftime("%Y%m%d%H", time.localtime()), int(time.time())),
                "remark": "我来也",
                "contestNo": "351Y(竞)-201807-095",
                "appointPrice": 0,
                "isNeedLoadingserve": "1",
                "conclusion": "",
                "createTm": time.strftime("%Y%m%d%H%M%S"),
                "lineDetail": [
                    {"transportName": "大芬上步1107",
                     "modifyTm": "20190530145352",
                     "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S"),
                     "srcLongitude": bengin_adress['srcLongitude'],
                     "destinationDeptCode": "755AC",
                     "modifier": "000138",
                     "destLongitude": end_adress['destLongitude'],
                     "userPhone": "13480733650",
                     "lineCross": [
                         {"thruDeptCode": "755AB",
                          "crossPointLatitude": bengin_adress["crossPointLatitude"],
                          "planWaitTime": 35, "thruSeqCode": "1",
                          "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "sendBatchCode": "755AB02D",
                          "lineDistance": 33.926,
                          "thruPointsId": 66626781614,
                          "receiveTime": 20180726154510,
                          "lineManageId": 9114914,
                          "crossDays": "0",
                          "crossPointAddress": bengin_adress["crossPointAddress"],
                          "workType": "1",
                          "planSendTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "id": 19863296,
                          "crossPointLongitude": bengin_adress["crossPointLongitude"],
                          "transportLastArriveTime": (datetime.datetime.now() + datetime.timedelta(hours=5)).strftime(
                              "%Y%m%d%H%M%S")},
                         {"thruDeptCode": "755AC",
                          "crossPointLatitude": end_adress["crossPointLatitude"],
                          "arriveBatchCode": "755AC03D",
                          "thruSeqCode": "3",
                          "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "thruPointsId": 66626781616,
                          "receiveTime": 20180726154510,
                          "lineManageId": 9114914,
                          "crossDays": "0",
                          "crossPointAddress": end_adress["crossPointAddress"],
                          "workType": "2",
                          "id": 19863298,
                          "crossPointLongitude": end_adress["crossPointLongitude"]}],
                     "destLatitude": end_adress['destLatitude'],
                     "totalKm": 78.05,
                     "lineCode": "755AB755AC1107",
                     "expiryDate": (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y%m%d%H%M%S"),
                     "vehicleTon": vehicleton,  # 吨数判断车型
                     "createTm": time.strftime("%Y%m%d%H%M%S"),
                     "destAddress": end_adress['destAddress'],
                     "versionNo": 1532591108155,
                     "planSendTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S"),
                     "id": 9114914,
                     "mainRequireId": 666666623164,
                     "srcLatitude": bengin_adress['srcLatitude'],
                     "loadWeight": 1000,
                     "creator": "sys_tempRequireManage",
                     "srcZonePlanarriveTime": "20190531145352",
                     "acrossDayNum": 1,
                     "isStop": "2",
                     "lineId": 365166,
                     "originDeptCode": "755AB",
                     "srcAddress": bengin_adress['srcAddress'],
                     "requirePlanId": 11317147,
                     "workDay": "5",
                     "runMode": "3",
                     "lineLevel": "3",
                     "requireId": 1807277959875,
                     "vehicleTypeCode": vehicletypecode,
                     "loadCapacity": 7000,
                     "deptCode": "755Y",
                     "effectiveDate": (datetime.datetime.now() + datetime.timedelta(hours=10)).strftime(
                         "%Y%m%d%H%M%S")}],
                "id": "{0}{1}".format(random.randint(100, 999), time.strftime("%Y")),
                "creator": "000138",
                "accountCode": "C102",
                "businessContacts": "",
                "contestDeadline": (datetime.datetime.now() + datetime.timedelta(minutes=50)).strftime("%Y%m%d%H%M%S"),
                "contestStartTm": time.strftime("%Y%m%d%H%M%S"),
                "contestDepteCode": "351Y",
                "lineId": 365166,
                "stayContestLineId": 2359852,
                "requirePlanId": 11317147,
                "contestUnit": "2",  # 2为整车，按趟
                "runMode": "3",
                "lineManageId": 9114914,
                "mainDriveRoad": "",
                "isNeedImportedcar": "1",
                "status": "1"
            }

        else:
            data = {
                "exceptionReportPhoneMailbox": "",
                "contestDepteName": "山西区部",
                "reserveRoad": "",
                "modifyTm": time.strftime("%Y%m%d%H%M%S"),
                "accountName": "顺丰速运有限公司",
                "modifier": "StartRunTask",
                "transactionNo": "351Y-T-{0}{1}".format(time.strftime("%Y%m%d%H", time.localtime()), int(time.time())),
                "remark": "我来也",
                "contestNo": "351Y(竞)-201807-095",
                "appointPrice": 0,
                "isNeedLoadingserve": "1",
                "conclusion": "",
                "createTm": time.strftime("%Y%m%d%H%M%S"),
                "lineDetail": [
                    {"transportName": "大芬上步1107",
                     "modifyTm": "20190530145352",
                     "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S"),
                     "srcLongitude": bengin_adress['srcLongitude'],
                     "destinationDeptCode": "755AC",
                     "modifier": "000138",
                     "destLongitude": end_adress['destLongitude'],
                     "userPhone": "13480733650",
                     "lineCross": [
                         {"thruDeptCode": "755AB",
                          "crossPointLatitude": bengin_adress["crossPointLatitude"],
                          "planWaitTime": 35, "thruSeqCode": "1",
                          "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "sendBatchCode": "755AB02D",
                          "lineDistance": 33.926,
                          "thruPointsId": 66626781614,
                          "receiveTime": 20180726154510,
                          "lineManageId": 9114914,
                          "crossDays": "0",
                          "crossPointAddress": bengin_adress["crossPointAddress"],
                          "workType": "1",
                          "planSendTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "id": 19863296,
                          "crossPointLongitude": bengin_adress["crossPointLongitude"],
                          "transportLastArriveTime": (datetime.datetime.now() + datetime.timedelta(hours=5)).strftime(
                              "%Y%m%d%H%M%S")},
                         {"thruDeptCode": "755AE",
                          "crossPointLatitude": cross_adress["crossPointLatitude"],
                          "planWaitTime": 1408,
                          "arriveBatchCode": "755AE03D",
                          "thruSeqCode": "2",
                          "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "sendBatchCode": "755AE02D",
                          "lineDistance": 44.124,
                          "thruPointsId": 66626781615,
                          "receiveTime": 20180726154510,
                          "lineManageId": 9114914,
                          "crossDays": "1",
                          "crossPointAddress": cross_adress["crossPointAddress"],
                          "workType": "1",
                          "planSendTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "id": 19863297,
                          "crossPointLongitude": cross_adress["crossPointLongitude"],
                          "transportLastArriveTime": (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime(
                              "%Y%m%d%H%M%S")},
                         {"thruDeptCode": "755AC",
                          "crossPointLatitude": end_adress["crossPointLatitude"],
                          "arriveBatchCode": "755AC03D",
                          "thruSeqCode": "3",
                          "planArriveTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                              "%Y%m%d%H%M%S"),
                          "thruPointsId": 66626781616,
                          "receiveTime": 20180726154510,
                          "lineManageId": 9114914,
                          "crossDays": "0",
                          "crossPointAddress": end_adress["crossPointAddress"],
                          "workType": "2",
                          "id": 19863298,
                          "crossPointLongitude": end_adress["crossPointLongitude"]}],
                     "destLatitude": end_adress['destLatitude'],
                     "totalKm": 78.05,
                     "lineCode": "755AB755AC1107",
                     "expiryDate": (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y%m%d%H%M%S"),
                     "vehicleTon": vehicleton,  # 吨数判断车型
                     "createTm": time.strftime("%Y%m%d%H%M%S"),
                     "destAddress": end_adress['destAddress'],
                     "versionNo": 1532591108155,
                     "planSendTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y%m%d%H%M%S"),
                     "id": 9114914,
                     "mainRequireId": 666666623164,
                     "srcLatitude": bengin_adress['srcLatitude'],
                     "loadWeight": 1000,
                     "creator": "sys_tempRequireManage",
                     "srcZonePlanarriveTime": "20190531145352",
                     "acrossDayNum": 1,
                     "isStop": "2",
                     "lineId": 365166,
                     "originDeptCode": "755AB",
                     "srcAddress": bengin_adress['srcAddress'],
                     "requirePlanId": 11317147,
                     "workDay": "5",
                     "runMode": "3",
                     "lineLevel": "3",
                     "requireId": 1807277959875,
                     "vehicleTypeCode": vehicletypecode,
                     "loadCapacity": 7000,
                     "deptCode": "755Y",
                     "effectiveDate": (datetime.datetime.now() + datetime.timedelta(hours=10)).strftime(
                         "%Y%m%d%H%M%S")}],
                "id": "{0}{1}".format(random.randint(100, 999), time.strftime("%Y")),
                "creator": "000138",
                "accountCode": "C102",
                "businessContacts": "",
                "contestDeadline": (datetime.datetime.now() + datetime.timedelta(minutes=50)).strftime("%Y%m%d%H%M%S"),
                "contestStartTm": time.strftime("%Y%m%d%H%M%S"),
                "contestDepteCode": "351Y",
                "lineId": 365166,
                "stayContestLineId": 2359852,
                "requirePlanId": 11317147,
                "contestUnit": "2",  # 2为整车，按趟
                "runMode": "3",
                "lineManageId": 9114914,
                "mainDriveRoad": "",
                "isNeedImportedcar": "1",
                "status": "1"
            }

        datalist = []
        datalist.append(data)
        r = requests.post(url, json=datalist)
        r_1 = r.json()
        # print(r_1)
        return r_1

    # 模拟顺丰确认下单
    def get_sf_confirm_order(self, thirdsn):
        url = self.mk_url('nopen', 'api/internal/sfTestComfirmOrder')
        base_url = '{0}?thirdSn={1}'.format(url, thirdsn)
        r = requests.get(base_url)
        r_1 = r.json()
        # print(r_1)
        return r_1


class ApiYt(Base):
    """圆通相关接口"""

    # 获取圆通访问福佑sign
    def yt_sign(self):
        a = '%s&%s&%s' % (
            get_config('open', 'app_yttofy_appkey'), int(time.time()), get_config('open', 'app_yttofy_appsecret'))
        sign = {
            "app_key": get_config('open', 'app_yttofy_appkey'),
            "time_stamp": int(time.time()),
            "sign_str": md5_encrypt(a)
        }
        return sign

    # 随机生成圆通三方单号
    def random_order_yt(self):
        a = time.strftime('%Y%m%d%H%M%S', time.localtime())
        thirdsn = a[:-1]
        # print(thirdsn)
        return thirdsn

    # 圆通访问福佑询价接口
    def yt_create_order(self,  thirdsn, carlengthtype, bengin_adress, end_adress):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/create', self.yt_sign())
        # print(url)
        data = {
            "thirdSn": thirdsn,
            "customerName": "发货员",
            "customerMobile": "15944582222",
            "goodsName": "快递货",
            "goodsWeight": 10,
            "goodsCubage": 10,
            "carModelCode": carlengthtype,
            "startProvinceName": bengin_adress["startProvinceName"],
            "startProvinceCode": bengin_adress["startProvinceCode"],
            "startCityName": bengin_adress["startCityName"],
            "startCityCode": bengin_adress["startCityCode"],
            "startDistrictName": bengin_adress["startDistrictName"],
            "startDistrictCode": bengin_adress["startDistrictCode"],
            "startAddress": bengin_adress["startAddress"],
            "endProvinceName": end_adress["endProvinceName"],
            "endProvinceCode": end_adress["endProvinceCode"],
            "endCityName": end_adress["endCityName"],
            "endCityCode": end_adress["endCityCode"],
            "endDistrictName": end_adress["endDistrictName"],
            "endDistrictCode": end_adress["endDistrictCode"],
            "endAddress": end_adress["endAddress"],
            "loadTime": int(time.time() + 5000),
            "unloadTime": int(time.time() + 20000),
            "sendTime": int(time.time() + 6000),
            "tags": "20,21",
            "addedService": "",
            "needReceipt": "0",
            "needInsurance": "0",
            "goodsValue": "23456",
            "goodsType": "",
            "packageType": 701,
            "comments": "",
            "businessDeptName": ""
        }
        data = json.dumps(data)
        r = requests.post(url, data, headers=headers)
        # print(r.json())
        return r.json()

    # 确认下单接口
    def yt_confirm_order(self, thirdsn):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/confirm', self.yt_sign())
        data = {
            "thirdSn": thirdsn,
            "loaderName": "王一",
            "loaderMobile": "13112341234",
            "loadAddress": "北京市海淀区知春里112号号",
            "unloaderName": "李二三",
            "unloaderMobile": "13212341234",
            "unloadAddress": "上海市青浦区234号XX转运场",
            "stopPoints": [
                # {
                #     "contactName": "张三",
                #     "contactMobile": "13312341234",
                #     "address": "北京市石景山区调度公园"
                # }
            ]
        }
        data = json.dumps(data)
        r = requests.post(url, data, headers=headers)
        # print(r.json())
        return r.json()


class ApiHydd(Base):
    """华宇嘟嘟相关接口"""

    # 获取华宇嘟嘟访问福佑sign
    def hydd_sign(self):
        a = '%s&%s&%s' % (
            get_config('open', 'app_hytofy_appkey'), int(time.time()), get_config('open', 'app_hytofy_appsecret'))
        sign = {
            "app_key": get_config('open', 'app_hytofy_appkey'),
            "time_stamp": int(time.time()),
            "sign_str": md5_encrypt(a)
        }
        return sign

    # 随机生成华宇嘟嘟三方单号
    def random_order_hydd(self):
        r = random.randrange(1000, 9999)
        thirdsn = '%s%s' % ('117', r)
        # print(thirdsn)
        return thirdsn

    # 华宇嘟嘟访问福佑询价接口
    def hydd_create_order(self,  thirdsn, carlengthtype, bengin_adress, end_adress):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/create', self.hydd_sign())
        # print(url)
        data = {
            "thirdSn": thirdsn,
            "customerName": "发货员",
            "customerMobile": "15944582222",
            "goodsName": "快递货",
            "goodsWeight": 10,
            "goodsCubage": 10,
            "carModelCode": carlengthtype,
            "startProvinceName": bengin_adress["startProvinceName"],
            "startProvinceCode": bengin_adress["startProvinceCode"],
            "startCityName": bengin_adress["startCityName"],
            "startCityCode": bengin_adress["startCityCode"],
            "startDistrictName": bengin_adress["startDistrictName"],
            "startDistrictCode": bengin_adress["startDistrictCode"],
            "startAddress": bengin_adress["startAddress"],
            "endProvinceName": end_adress["endProvinceName"],
            "endProvinceCode": end_adress["endProvinceCode"],
            "endCityName": end_adress["endCityName"],
            "endCityCode": end_adress["endCityCode"],
            "endDistrictName": end_adress["endDistrictName"],
            "endDistrictCode": end_adress["endDistrictCode"],
            "endAddress": end_adress["endAddress"],
            "loadTime": int(time.time() + 5000),
            "unloadTime": int(time.time() + 20000),
            "sendTime": int(time.time() + 6000),
            "tags": "20,21",
            "addedService": "",
            "needReceipt": "0",
            "needInsurance": "0",
            "goodsValue": "23456",
            "goodsType": "",
            "packageType": 701,
            "comments": "",
            "businessDeptName": ""
        }
        data = json.dumps(data)
        r = requests.post(url, data, headers=headers)
        # print(r.json())
        return r.json()

    # 确认下单接口
    def hydd_confirm_order(self,  thirdsn):
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.mk_url('nopen', 'api/query/confirm', self.hydd_sign())
        data = {
            "thirdSn": thirdsn,
            "loaderName": "王一",
            "loaderMobile": "13112341234",
            "loadAddress": "北京市海淀区知春里112号号",
            "unloaderName": "李二三",
            "unloaderMobile": "13212341234",
            "unloadAddress": "上海市青浦区234号XX转运场",
            "stopPoints": [
                # {
                #     "contactName": "张三",
                #     "contactMobile": "13312341234",
                #     "address": "北京市石景山区调度公园"
                # }
            ]
        }
        data = json.dumps(data)
        r = requests.post(url, data, headers=headers)
        # print(r.json())
        return r.json()


if __name__ == '__main__':
    tt = ApiJd().random_out_numbers_jd()
    ApiJd().jd_xun_jia_out_point('t7', tt, get_config('adress', 'bengin1'), get_config('adress', 'end1'))
