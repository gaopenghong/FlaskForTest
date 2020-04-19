# coding:utf-8
from app.tools.api.api_service import *
from app.tools.api.api_ua import *


class ApiDispatch(ApiService,ApiUa):
    """调度系统接口"""
    # 获取司机详情
    def dispatch_get_driver_info(self, driver_mobile, cookies):
        url = self.mk_url('dd', 'api/dispatch/getDriverInfo.do')
        data = {
            'driverMobile': driver_mobile,
            'needHistoryOrder': 0,
            'needForYouInfo': 1
        }
        # print(url, data)
        r = requests.post(url, data, cookies=cookies)
        return r.json()


    #   确认运单
    def dispatch_confirm_order(self,driver_id=None,order_sn=None,cookie=None):
        url = self.mk_url('dd', 'api/dispatch/confirm.do')
        data = {
            'orderSn': order_sn,
            'driverId': driver_id,
            'operateType': 1
        }
        r = requests.post(url,data,cookies=cookie)
        print(r.content.decode('utf-8'))
        return r.json()

    #调度确认司机符合
    def dispatch_arrange_driver(self,order_sn, driver_info, cookies_dispatch,transFee,type):
        url = self.mk_url('dd', 'api/dispatch/arrangeDriver.do')
        if type==1: #调度确认
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
            'checkStatus': '2',  # 审核状态
            'transFee': transFee,  # 运费
            'tradeDeposit': '0',  # 回单押金
            'deposit': '2000',  # 押金
            'payDepositType': '0',  # 押金渠道: 0微信, 1运满满
            'tags': '',
            'tagId':'',
            'remark': '',
            'driverTruckMapId': driver_info['truckInfoList'][0]['driverTruckMapId'],
            'truckInfoId': driver_info['truckInfoList'][0]['id'],
            'deduct': '',
            'isDefault': driver_info['truckInfoList'][0]['isDefault'],
            'from':1   #1表示从调度一口价页面调用的这个接口，不传该参数表示直接安排司机

        }
        else:
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
                'checkStatus': '2',  # 审核状态
                'transFee': 4000,  # 运费
                'tradeDeposit': '0',  # 回单押金
                'deposit': '2000',  # 押金
                'payDepositType': '0',  # 押金渠道: 0微信, 1运满满
                'tags': '',
                'tagId': '',
                'remark': '',
                'driverTruckMapId': driver_info['truckInfoList'][0]['driverTruckMapId'],
                'truckInfoId': driver_info['truckInfoList'][0]['id'],
                'deduct': '',
                'isDefault': driver_info['truckInfoList'][0]['isDefault'],
                # 'from': 1  # 1表示从调度一口价页面调用的这个接口，不传该参数表示直接安排司机

            }
        print('调度系统安排司机: %s, %s' % (url, data))
        r = requests.post(url, data, cookies=cookies_dispatch)
        return r.json()

    def  dispatch_fixedPrice_arrangeCancel(self,order_sn, driver_info,cookies):
        url = self.mk_url('dd', 'api/fixedPrice/arrangeCancel')
        data = {
            'orderSn': order_sn,
            'driverMobile': driver_info["driverMobile"],
            'deduct': 0,
            'tagId': 31,
            'driverId': driver_info["driverId"],
            'type': 1,
            'detailReason': '公司倒闭，司机跑路',
            'typeReason': '公司破产（不扣押金'
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()
    def   dispatch_preConfirm(self,order_sn, driverId,cookies):
        url = self.mk_url('dd', 'api/dispatch/preConfirm')
        data = {
            'orderSn': order_sn,
            'driverId': driverId,
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()
    def   dispatch_Confirm(self,order_sn, driverId,cookies):
        url = self.mk_url('dd', 'api/dispatch/confirm')
        data = {
            'orderSn': order_sn,
            'driverId': driverId,
            'operateType':1
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    #   获取调度分配页运单列表
    def dispatch_get_all_scheduler_orders(self, cookies_bg, data_new):
        url = self.mk_url('dd', 'api/dispatch/getAllSchedulerOrders.do')
        data = {
            'pageIndex': 1,
            'pageSize': 30
        }
        data.update(data_new)
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()

    #   获取已绑定经纪人列表
    def dispatch_bind_agent_list(self, cookies_bg, name='', mobile=''):
        url = self.mk_url('dd', 'api/scheduler/ownBroker/getBindBrokerList')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'name': name,
            'mobile': mobile
        }
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()
