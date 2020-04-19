# coding:utf-8
from .base import *
from app.util.ssh_conf import *
import unittest


# 查询用户信息
class ApiDriver(Base):
    def driver_login(self, driver_mobile, check_code):
        url = self.mk_url("xdriver", "api/app/u/login")
        # url = "https://%sxdriver.fuyoukache.com/api/app/u/login" % env
        data = {
            'mobile': driver_mobile,
            'checkCode': check_code
        }
        r = requests.post(url, data)
        return r.json()

    def test_pay_Deposit(self, env, driver_mobile):
        sql_business_info = "select  name,id  from  driver_info where mobile=" + str(driver_mobile)
        result = remote_database(env, 'fykc_xdriver_service', sql_business_info)
        print(result)
        if result == []:
            print("该司机不存在")
            return "该司机不存在"
        elif result[0][0] == None:
            return "司机名字为空，请完善信息"
        else:
            driverName = result[0][0]
            driverId = result[0][1]
            print(driverId, driverName)
        # 调取小程序发起押金支付接口
        url = self.mk_url("proxy", "fykc-wxbidding-service/api/wxbidding/facade/toPayDeposit")
        data = {
            "source": 2,  # 平台来源1：小程序，2：app一般传2就行
            "payType": 23,  # 支付类型固定传23
            "driverId": driverId,  # 司机id
            "driverMobile": str(driver_mobile),  # 司机手机号
            "driverName": driverName  # 司机姓名
        }
        r = requests.post(url=url, data=data)
        print(r.json())
        re = r.json()
        if re["success"] == False:
            return re["status"]["desc"]
        print("发起押金支付接口")
        # 通过司机id 以及支付状态
        sql_business_info = "select payRequestId,payStatus from  deposit_pay where driverId='" + str(
            driverId) + "' and payStatus=0 order by id desc limit 1;"
        print(sql_business_info)
        result = remote_database(env, 'fykc_wxtrucking_bidding', sql_business_info)
        print(result)
        try:
            # 调用小程序支付成功回调接口
            url = self.mk_url("proxy", "fykc-wxbidding-service/api/wxbidding/facade/payCallBack")
            # url = "https://%sproxy.fuyoukache.com/fykc-wxbidding-service/api/wxbidding/facade/payCallBack" % env
            data = {
                "payRequestId": result[0][0],  # 支付请求编码
                "payStatus": 2,  # 支付状态2：成功 3：失败
                "payTime": 1570787211,  # 支付时间戳10位一般获取当前时间就行
            }
            r = requests.post(url=url, data=data)
            print(r)
            print("调用小程序支付成功回调")
            return r.json()
        except Exception as e:
            return "微信支付失败"

    def test_pay_lineDeposit(self, env, driver_mobile):
        driver_info = self.driver_login(driver_mobile, "1123")
        token = driver_info["data"][0]["token"]
        driverId = driver_info["data"][0]["id"]
        if "name" not in driver_info["data"][0]:
            return "司机名字为空，请完善信息"
        else:
            url = self.mk_url("xdriver", "api/app/deposit/pay")
            # url = "https://%sxdriver.fuyoukache.com/api/app/deposit/pay" % env
            data = {
                "money": 0.01,
                "token": token
            }
            r = requests.post(url=url, data=data)
            print(r.json())
            re = r.json()
            if re["status"]["code"] != 0:
                return re["status"]["desc"]
            print("发起押金支付接口")
            port = dbconfig[env]
            # 通过司机id 以及支付状态
            sql_business_info = "select payRequestId,payStatus from  driver_pay_log where driverId='" + str(
                driverId) + "' and payStatus=0 order by id desc limit 1;"
            print(sql_business_info)
            result = remote_database(env, 'fykc_xdriver_service', sql_business_info)
            print(result)
            try:
                # 调用小程序支付成功回调接口
                url = self.mk_url("xdriver", "api/internal/pay/payDepositBack")
                # url = "https://%sxdriver.fuyoukache.com/api/internal/pay/payDepositBack" % env
                data = {
                    "payRequestId": result[0][0],  # 支付请求编码
                    "payStatus": 2,  # 支付状态2：成功 3：失败
                    "payTime": 1570787211,  # 支付时间戳10位一般获取当前时间就行
                }
                r = requests.post(url=url, data=data)
                print(r)
                print("调用小程序支付成功回调")
                return r.json()
            except Exception as e:
                return "微信支付失败"

    # 更新心跳和上传定位
    def driver_pulse_location(self, driver_id, driver_mobile, action_type, order_sn='', location_info=[],
                              driver_token=None):
        url = self.mk_url('xdriver', 'api/app/log/appCalorie')
        if action_type == 1:
            data_temp = {
                'driverId': driver_id,
                'mobile': driver_mobile,
                'actionType': 1,
                'normalType': 1,
                'lat': location_info[0],
                'lng': location_info[1],
                'orderSn': order_sn,
                'provinceName': location_info[2],
                'cityName': location_info[3],
                'districtName': location_info[4],
                'address': location_info[5],
                'createTime': int(time.time()) * 1000
            }
        elif action_type == 2:
            data_temp = {
                'driverId': driver_id,
                'mobile': driver_mobile,
                'actionType': 2,
                'normalType': 1,
                'createTime': int(time.time()) * 1000
            }
        else:
            return False
        data_temp_1 = [data_temp]
        data = {
            'token': driver_token,
            'data': json.dumps(data_temp_1)
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-运单详情
    def driver_order_detail(self, driver_token, order_sn):
        url = self.mk_url("xdriver", "api/app/order/detail")
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/detail" % env
        data = {
            'token': driver_token,
            'orderSn': order_sn
        }

        r = requests.post(url, data)
        return r.json()

    def driver_bank_bind_card(self, driver_token, idCardNumber, bankAccount, bankCardNumber):
        url = self.mk_url("xdriver", "api/app/bank/bindCard")
        # url = "https://%sxdriver.fuyoukache.com/api/app/bank/bindCard" % env
        data = {
            'token': driver_token,
            'idCardNumber': idCardNumber,
            'bankAccount': bankAccount,
            'bankCardNumber': bankCardNumber
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-运单打点
    def driver_order_make_point(self, driver_token, order_sn, point_id, show_index, point_type, point_flag, longitude,
                                latitude):
        """
        :param driver_token:
        :param order_sn: 运单号
        :param point_id
        :param show_index
        :param point_type: 打点类型: 7到达装货地,8装货完成,9到达卸货地,10卸货完成
        :param point_flag: 1-到达 2-离开
        :param longitude:
        :param latitude:
        :return:
        """
        url = self.mk_url('xdriver', 'api/app/order/makePoint')
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/makePoint" % env
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'type': point_type,
            'latitude': latitude,
            'longitude': longitude,
            'image': '',
            'flag': point_flag,
            'code': '',
            'pointId': point_id,
            'showIndex': show_index
        }
        data = data
        # print(data_1)
        r = requests.post(url, data)
        return r.json()

    # 运单-运单打点信息
    def driver_order_make_point_info(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/getMakePointInfo')
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/getMakePointInfo" % env
        data = {

            'token': driver_token,
            'orderSn': order_sn
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-运单自动打点
    def driver_order_auto_make_point(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/foryou/autoMakePoint')
        # url = "https://%sxdriver.fuyoukache.com/api/app/foryou/autoMakePoint" % env
        data = {
            'customerType': 5,
            'token': driver_token,
            'orderSn': order_sn
        }
        r = requests.post(url, data)
        return r.json()

    # 司机详情
    def crm_driver_detail(self, driver_id, cookies):
        url = self.mk_url('xdriver', 'api/crm/driver/detail')
        # url = "https://%sxdriver.fuyoukache.com/api/crm/driver/detail" % env
        data = {
            'driverId': driver_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 运单-上传回单
    def driver_order_receipt_upload(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/uploadReceipt')
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/uploadReceipt" % env
        print(url)
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'imageUrl': 'http://public.fuyoukache.com/FlGtfm3dJLjQ5uujO5lbN-_mm43q'
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-上传回单快递信息
    def driver_order_receipt_mail(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/uploadReceiptMail')
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/uploadReceiptMail" % env
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'receiptCompanyName': '中通快递',
            'receiptPostNumber': 'ZT20190108115430'
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-异常上报
    def driver_order_exception_report(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/uploadException')
        # url = "https://%sxdriver.fuyoukache.com/api/app/order/uploadException" % env
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'type': 183,
            'content': '技术测试异常上报',
            'imageList': '',
            'tagJson': ''
        }
        r = requests.post(url, data)
        return r.json()

    def test_bank_driverWithDrawInitialize(self, driver_token):
        url = self.mk_url('xdriver', 'api/app/bank/driverWithDrawInitialize')
        # url = "https://%sxdriver.fuyoukache.com/api/app/bank/driverWithDrawInitialize" % env
        data = {
            "token": driver_token
        }
        r = requests.post(url=url, data=data)
        return r.json()

    def moneyPackage(self, token):
        url = self.mk_url('xdriver', 'api/app/bank/getDriverWallet')
        # url = "https://%sxdriver.fuyoukache.com/api/app/bank/getDriverWallet" % env
        data = {
            "token": token
        }
        r = requests.post(url, data=data)
        r = r.json()
        availableMoney = r["data"][0]["availableMoney"]
        return availableMoney

    def sendcode(self, token, mobile):
        url = self.mk_url('xdriver', 'api/app/u/sendCheckCode')
        # url = "https://%sxdriver.fuyoukache.com/api/app/u/sendCheckCode" % env
        data = {
            "token": token,
            "codeType": 0,
            "mobile": mobile
        }
        r = requests.post(url, data=data)
        return r.json()

    def test_draw_money(self, mobile, env):
        """申请提款"""
        sql_date = "SELECT code from check_code  where requestId = " + mobile
        draw_money_code = remote_database(env, 'fykc_xdriver_service', sql_date)
        return draw_money_code

    # 钱包-申请提款
    def driver_draw_money(self, driver_token, bank_card, mobile, draw_money_code, availableMoney):
        url = self.mk_url('xdriver', 'api/app/bank/driverWithDraw')
        # url = "https://%sxdriver.fuyoukache.com/api/app/bank/driverWithDraw" % env
        data = {
            'token': driver_token,
            'availableMoney': availableMoney,
            'bankCardNumber': bank_card,
            'mobile': mobile,
            'code': draw_money_code,
            'drawList': json.dumps({"yunxin": "", "pingan": ""})
        }
        r = requests.post(url, data)
        return r.json()

    # 活动提款
    def driver_activity_wallet(self, driver_token):
        url = self.mk_url('xdriver', 'api/app/activity/getDriverWallet')
        # url = "https://%sxdriver.fuyoukache.com/api/app/activity/getDriverWallet" % env
        data = {
            "token": driver_token
        }
        r = requests.post(url=url, data=data)
        return r.json()

    def driver_activity_driverdraw(self, driver_token, code, totalNoDrawMoney):
        url = self.mk_url('xdriver', 'api/app/activity/driverDraw')
        # url = "https://%sxdriver.fuyoukache.com/api/app/activity/driverDraw" % env
        data = {
            "token": driver_token,
            "code": code,
            "totalNoDrawMoney": totalNoDrawMoney
        }
        r = requests.post(url=url, data=data)
        return r.json()

    # 修改排队状态
    def driver_app_line_rank_change(self, token, car_status, longitude, latitude, line_id):
        url = self.mk_url('xdriver', 'api/app/rank/driverRank')
        data = {
            'token': token,
            'driverStatus': car_status,
            'latitude': latitude,
            'longitude': longitude,
            'lineId': line_id
        }
        r = requests.post(url, data)
        return r.json()

    # 三方打卡
    def driver_report_third_clock(self, token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/reportThirdClockIn')
        data = {
            'token': token,
            'orderSn': order_sn,
            'reportType': 1,
            'imgUrl': "http://1.png,http://2.png"
        }
        r = requests.post(url, data)
        return r.json()

    def driver_update_order_account(self, token, orderSn):
        url = self.mk_url('xdriver', 'api/app/orderMoney/updateOrderAccount')
        data = {
            'orderSn': orderSn,
            'token': token

        }
        res = requests.post(url, data)
        return res.json()
