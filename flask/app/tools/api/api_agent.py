# coding:utf-8
import os

from app.tools.api.base import *


class ApiAgent(Base):
    # 经纪人登录
    def agent_app_login(self, check_code='1123'):
        url = self.mk_url('xbroker', 'api/app/u/login')
        data = {
            'mobile': self.agent_mobile,
            'checkCode': check_code
        }
        r = requests.post(url, data)
        return r.json()

    # 获取司机详情
    def agent_driver_detail(self, agent_token, mobile, type_type=1, load_time='1551177000000',
                            unload_time='11551349800000'):
        url = self.mk_url('xbroker', 'api/app/driver/getDriverDetail')
        data = {
            'token': agent_token,
            'mobile': mobile,
            'type': type_type,
            'loadTime': load_time,
            'unloadTime': unload_time
        }
        r = requests.post(url, data)
        return r.json()

    # ocr识别身份证反面照
    def agent_id_card_back(self, image_url=' '):
        url = self.mk_url('xbroker', 'api/app/common/ocrIdcardBack')
        data = {
            'imageUrl': image_url
        }
        r = requests.post(url, data)
        return r.json()

    # ocr识别身份证正面照
    def agent_id_card_front(self, image_url=' '):
        url = self.mk_url('xbroker', 'api/app/common/ocrIdcardFront')
        data = {
            'imageUrl': image_url
        }
        r = requests.post(url, data)
        return r.json()

    # 查询经纪人信息
    def broker_info_search(self):
        file_name = os.path.join(os.path.dirname(__file__), '../data/broker_info.txt')
        fp = open(file_name, 'r+', encoding='utf-8')
        lines = fp.readlines()
        broker_info_list = []
        for line in lines:
            broker_info = line.replace('\n', '')
            broker_info_split = broker_info.split('|')
            broker_info_split.pop(-1)
            broker_info_key_list = ['brokerName', 'identity', 'identityFrontUrl', 'identityInverseUrl',
                                    'validDateStartFmt',
                                    'validDateEndFmt', 'workProvinceId', 'workProvinceName', 'workDistrictId',
                                    'workDistrictName',
                                    'workCityId', 'workCityName']
            broker_info_dict = dict(zip(broker_info_key_list, broker_info_split))
            broker_info_list.append(broker_info_dict)
        fp.close()
        return broker_info_list

    # 经纪人注册
    def agent_api_register(self, broker_mobile):
        broker_info_list = self.broker_info_search()
        i = random.randint(0, 494)
        print(i)
        broker_info = broker_info_list[i]
        url = self.mk_url('xbroker', 'api/app/u/register')
        print(url)
        broker_info['validDateStart'] = broker_info['validDateStartFmt']
        del broker_info['validDateStartFmt']
        broker_info['validDateEnd'] = broker_info['validDateEndFmt']
        del broker_info['validDateEndFmt']
        address = self.agent_id_card_front(image_url=broker_info['identityFrontUrl'])['data'][0]['address']
        issued_by = self.agent_id_card_back(image_url=broker_info['identityInverseUrl'])['data'][0][
            'issuedBy']
        data = {
            'brokerMobile': broker_mobile,
            'address': address,
            'issuedBy': issued_by,
        }
        data.update(broker_info)
        r = requests.post(url, data)
        print(r.json())
        return r.json(), broker_info

    # 根据企业信用代码\注册号和法人身份证号完成企业认证
    def agent_bind_company(self, agent_token, credit_code='91430000325714159U', identity='230231198801160632'):
        url = self.mk_url('xbroker', 'api/app/broker/bindCompanyInfo')
        data = {
            'token': agent_token,
            'creditCode': credit_code,
            'identity': identity
        }
        r = requests.post(url, data)
        return r.json()

        # 查询经纪人信息

    # 确认下单页面信息
    def customer_pc_confirmorder_info(self, ordersn=None, cookie=None):
        url = self.mk_url('hz', 'api/pc/quote/confirmOrderInfo')
        if ordersn is None:
            data_dic = {}
        else:
            data_dic = {
                'orderSn': ordersn
            }
        if cookie is None:
            r = requests.post(url, data=data_dic)
        else:
            r = requests.post(url, data=data_dic, cookies=cookie)
        print(r.json())
        return r.json()

    # 确认下单
    def customer_pc_order_confirm(self, order_sn=None, goodsworth=10000, stoppoints=True, cookies=None):
        url = self.mk_url('hz', 'api/pc/quote/confirmOrder')
        data_dic = {}
        if order_sn is not None:
            data_dic['orderSn'] = order_sn
        if goodsworth is not None:
            data_dic['goodsWorth'] = goodsworth
        if stoppoints is not None:
            d = self.customer_pc_confirmorder_info(ordersn=order_sn, cookie=cookies)
            print(d)
            stoppointlist = d['data'][0]['stopPointList']
            keys = ['id', 'contactName', 'contactMobile']
            contact = {
                'contactName': '测试',
                'contactMobile': '18000000001'
            }
            stoppoints = list(
                {key: value for key, value in stoppoint.items() if key in keys} for stoppoint in stoppointlist)
            stoppoints2 = []
            for stoppoint in stoppoints:
                stoppoint.update(contact)
                stoppoints2.append(stoppoint)
            data_dic['stopPoints'] = json.dumps(stoppoints2, ensure_ascii=False)

        if cookies:
            r = requests.post(url, data=data_dic, cookies=cookies)
        else:
            r = requests.post(url, data=data_dic)

        return r.json()

    # 保存司机
    def agent_bind_driver_broker(self, agent_token, driverid):
        url = self.mk_url('xbroker', 'api/app/driver/bindDriverAndBroker')
        data = {
            'token': agent_token,
            'driverId': driverid,
        }
        r = requests.post(url, data)
        return r.json()

    # 安排司机
    def agent_order_arrange_driver(self, agent_token, order_sn='229032134147', driverid='537365', driver_name='李飞',
                                   driver_mobile='15212340023', plate_number='新R26478',
                                   identification_number='142202199410201911',
                                   car_length_id=1, car_model_id=1, load_time=str(int(time.time()) * 1000 + 12000000),
                                   unload_time=str(int(time.time()) * 1000 + 48000000), driver_info={}):
        url = self.mk_url('xbroker', 'api/app/orderinfo/arrangeDriver.do')
        if driver_info != {}:
            data = {
                'token': agent_token,
                'orderSn': order_sn,
                'driverId': driver_info['id'],
                'driverName': driver_info['name'],
                'driverMobile': driver_info['mobile'],
                'plateNumber': driver_info['truckInfoList'][0]['plateNumber'],
                'identificationNumber': driver_info['idCardNumber'],
                'carLength': driver_info['truckInfoList'][0]['carLengthId'],
                'carModel': driver_info['truckInfoList'][0]['carModelId'],
                'loadTime': load_time,
                'unloadTime': unload_time
            }
        else:
            data = {
                'token': agent_token,
                'orderSn': order_sn,
                'driverId': driverid,
                'driverName': driver_name,
                'driverMobile': driver_mobile,
                'plateNumber': plate_number,
                'identificationNumber': identification_number,
                'carLength': car_length_id,
                'carModel': car_model_id,
                'loadTime': load_time,
                'unloadTime': unload_time
            }
        r = requests.post(url, data)
        return r.json()

    # 运单详情
    def agent_order_detail(self, agent_token, order_sn, search_type=''):
        """
        :param agent_token:
        :param order_sn:
        :param search_type: 运单状态: 1待派车, 2运输中, 3未结款, 4已结款, 5已取消
        :return:
        """
        url = self.mk_url('xbroker', 'api/app/orderinfo/getOrderDetail')
        data = {
            'token': agent_token,
            'orderSn': order_sn,
            'searchType': search_type
        }
        r = requests.post(url, data)
        return r.json()

    # 上传回单
    def agent_upload_receipt(self, agent_token, order_sn='429031124023',
                             imageurl='https://public.fuyoukache.com/common/5b6fa445d4892.png', back_status=1):
        url = self.mk_url('xbroker', 'api/app/orderinfo/uploadReceipt.do')
        json_data = {
            'backStatus': back_status,
            'imageUrl': imageurl,
            'orderSn': order_sn
        }
        data = {
            'token': agent_token,
            'jsonData': json.dumps(json_data)
        }
        r = requests.post(url, data)
        return r.json()

    # 按条件搜索任务
    def servive_select_task(self, cookies_service, task_type_ids='', status='', dispatch_person='', order_sn='',
                            task_sn='', third_quote_sn='',
                            customer_name='', com_name='', create_time_start='', create_time_end='',
                            dispatch_time_start='', dispatch_time_end='',
                            handle_time_start='', handle_time_end='', pagesize=10, pageindex=1):

        url = self.mk_url('fuwu', 'api/task/selectAllList.do')
        data = {
            'pageSize': pagesize,
            'pageIndex': pageindex,
            'taskTypeIds': task_type_ids,
            'status': status,
            'dispatchPerson': dispatch_person,
            'orderSn': order_sn,
            'taskSn': task_sn,
            'thirdQuoteSn': third_quote_sn,
            'customerName': customer_name,
            'comName': com_name,
            'createTimeStart': create_time_start,
            'createTimeEnd': create_time_end,
            'dispatchTimeStart': dispatch_time_start,
            'dispatchTimeEnd': dispatch_time_end,
            'handleTimeStart': handle_time_start,
            'handleTimeEnd': handle_time_end
        }
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()

    # 确认运单
    def agent_update_order_account(self, order_sn, token):
        url = self.mk_url('xbroker', 'api/app/orderinfo/updateOrderAccount.do')
        data = {
            'orderSn': order_sn,
            'token': token
        }
        r = requests.post(url, data=data)
        return r.json()

    # 申请提款
    def agent_get_order_money(self, order_sn, agent_token):
        url = self.mk_url('xbroker', 'api/app/orderinfo/getOrderMoneyDetail')
        data = {'orderSn': order_sn,
                'token': agent_token}
        r = requests.post(url, data)
        return r.json()

    # 提款
    def agent_wallet_drawing_batch(self, agent_token, account_amount='', broker_invoice='', broker_period='',
                                   broker_period_days='',
                                   commission='', is_new='', order_sn='', trans_fee='', real_available_money='', ):
        url = self.mk_url('xbroker', 'api/app/wallet/drawingBatch')
        data = {
            'orderList': str(
                [{"accountAmount": account_amount, "brokerInvoice": broker_invoice, "brokerPeriod": broker_period,
                  "brokerPeriodDays": broker_period_days, "commission": commission, "isNew": is_new,
                  "orderSn": order_sn, "realAvailableMoney": real_available_money, "transFee": trans_fee}]),
            'token': agent_token
        }
        r = requests.post(url, data=data)
        return r.json()

    # 查看账单列表
    def agent_account_list(self, agent_token, search_type=1, page_index=10):
        url = self.mk_url('xbroker', 'api/app/wallet/selectAccountSettleList')
        data = {
            'token': agent_token,
            'searchType': search_type,
            'pageIndex': page_index,
            'pageSize': 100

        }
        r = requests.post(url, data)
        return r.json()

    # 确认账单
    def agent_confirm_account(self, agent_token, bill_no):
        url = self.mk_url('xbroker', 'api/app/wallet/confirmAccount')
        data = {
            'billNo': bill_no,
            'token': agent_token
        }
        r = requests.post(url, data)
        return r.json()

    # 获取公司可用发票
    def agent_get_able_invoice_list(self, agent_token, company_name):
        url = self.mk_url('xbroker', 'api/app/wallet/getSubmitableInvoiceList')
        data = {
            'companyName': company_name,
            'token': agent_token
        }
        r = requests.post(url, data=data)
        return r.json()

    # 上传发票
    def agent_add_invoice(self, bill_no, total_money, invoice_date, agent_token, invoice_no='测试发票标号',
                          invoice_code="123456789",
                          invoice_company="江苏鼎福隆现代物流有限公司", provider_header='长安电力华中发电有限公司', tax_no="91430000325714159U"):
        url = self.mk_url('xbroker', 'api/app/wallet/addInvoice')
        data = {
            'billNo': bill_no,
            'data': str([{"checkStatus": 0, "expressCom": "申通快递", "expressNo": "123456",
                          "invoiceCode": invoice_code, "invoiceCompany": invoice_company, "invoiceDate": invoice_date,
                          "invoiceFee": "0", "invoiceNo": invoice_no, "isChecked": "true", "netPrice": total_money,
                          "position": 0,
                          "providerHeader": provider_header, "taxNo": tax_no, "totalInvoiceFee": total_money}]),
            "totalMoney": total_money,
            'invoiceCompany': invoice_company,
            'token': agent_token
        }
        print(data)
        r = requests.post(url, data)
        return r.json()

    # 修改排队状态
    def driver_app_line_rank_change(self, token, car_status, longitude, latitude, line_id):
        url = self.mk_url("xdriver", "api/app/rank/driverRank")
        data = {
            'token': token,
            'driverStatus': car_status,
            'latitude': latitude,
            'longitude': longitude,
            'lineId': line_id
        }
        r = requests.post(url, data)
        return r.json()

    # 顺丰运单司机上传举证信息
    def driver_order_upload_proof(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/uploadProof')
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'sealLogo': "586941019311",
            'gpsIsValid': 0,
            'sealLogoIsValid': 0,
            'sealLogoIsEcho': 1
        }
        r = requests.post(url, data)
        return r.json()

    # 用户信息 -- 查询用户信息
    def agent_get_broker(self, agent_token):
        url = self.mk_url('xbroker', 'api/app/broker/getBrokerInfo')
        data = {
            'token': agent_token
        }
        r = requests.post(url, data)
        return r.json()

    # 合同签署
    def agent_sign_contract(self, company_contract_id, agent_token):
        data = {
            'companyContractId': company_contract_id,
            'token': agent_token
        }
        url = self.mk_url('xbroker', 'api/app/company/contract/signContract')
        r_json = requests.post(url, data=data)
        return r_json.json()

    # 保证金-线下汇款
    def agent_commit_recharge(self, agent_token, pay_img='http://public.fuyoukache.com/FoanjMDw2dzYolLPFtx3NQV3zZE4',
                              pay_account_no='1234567890', pay_account_name='测试账户',
                              amount=0.01):
        data = {
            'token': agent_token,
            'payAccountNo': pay_account_no,
            'payAccountName': pay_account_name,
            'payImg': pay_img,
            'amount': amount
        }
        print(data)
        url = self.mk_url('xbroker', 'api/app/deposit/commitRecharge.do')
        r = requests.post(url, data=data)
        return r.json()

    # 获取充值审核列表
    def agent_get_offlines(self, cookies, page_no=1, page_size=30, start_time='', end_time='',
                           customer_name='',
                           customer_mobile='', company_name='', account_no='', account_name='', status=0):
        data = {
            'pageNo': page_no,
            'pageSize': page_size,
            'startTime': start_time,
            'endTime': end_time,
            'customerName': customer_name,
            'customerMobile': customer_mobile,
            'companyName': company_name,
            'accountNo': account_no,
            'accountName': account_name,
            'status': status
        }

        url = self.mk_url('caiwu', 'api/margin/getBrokerOfflines.do')
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()

    # 充值审核
    def agent_check_offline_pay(self, cookies, pay_request_id, check_status=2, check_comment='测试'):
        data = {
            'payRequestId': pay_request_id,
            'checkStatus': check_status,
            'checkComment': check_comment,
            'bankFlowNo': str(random.randint(100000, 900000))
        }
        url = self.mk_url('caiwu', 'api/margin/checkOfflinePay.do')
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()
