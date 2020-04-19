# coding:utf-8
from .base import *
import os

import requests
import xlrd
import platform
from xlutils.copy import copy

from app.tools.api.base import Base

project_path = os.path.dirname(os.path.dirname(__file__))
# 导出、下载文件目录
export_path = project_path + '/data'


class ApiFinance(Base):
    """财务系统接口"""

    # 获取线下支付待审核的列表
    def finance_fy_online_check_list(self, data1, cookies):
        url = self.mk_url('caiwu', 'api/fy/offline/getOfflineRecords.do')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'checkStatus': 0
        }
        data.update(data1)
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 线下支付-审核通过/拒绝
    def finance_fy_online_check(self, request_id, check_status, cookies):
        url = self.mk_url('caiwu', 'api/fy/offline/checkOfflinePay.do')
        data = {
            'payRequestId': request_id,  # 付款请求号，可以从待审核列表获取
            'checkStatus': check_status,  # 2 成功；3 失败
            'checkComment': '审核'
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 客户对账管理-线下对账-列表
    def finance_customer_order_checking_under_line_list(self, data1, cookies):
        url = self.mk_url('caiwu', 'api/customer/statementmg/getCheckOrderListBySta.do')
        data = {
            'pageIndex': 1,
            'pageSize': 30
        }
        data.update(data1)
        print('线下对账参数data', data)
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()

    # 异常修改-客户原因产生经纪人补贴
    def finance_bms_allowance(self, order_sn, subsidize_amount, cookies):
        url = self.mk_url('bms', 'api/order/abnormal/modify')
        change_data = {
            'cancelFirstReason': 1,
            'comment': '222',
            'customerReason': 1,
            'subsidizeTarget2': 2,
            'extraAmount': 0,
            'subsidizeAmount': subsidize_amount,
            'cancelSecondReason': 1,
            'subsidizeTarget': 2,
            'extraAmountSysCalcd': '',
            'subsidizeAmountSysCalcd': ''
        }
        data = {
            'orderSn': order_sn,
            'secondLevel': 101,
            'comment': '111',
            'voucherImg': '',
            'type': 11,
            'changeData': json.dumps(change_data)
        }
        print(data)
        r = requests.post(url, data, cookies=cookies)
        print(r.text)
        return r.json()

    # 经纪人红包和补贴--列表(待付款)
    def finance_agent_wallet_list(self, order_sn, cookies_finance):
        url = self.mk_url('caiwu', 'api/agent/wallettmg/getWalletPaymentList.do')
        data = {
            'pageNo': 1,
            'pageSize': 30,
            'order_sn': order_sn,
            'brokerName': '',
            'mobile': '',
            'paymentType': '',
            'areaId': '',
            'provinceId': '',
            'payStatus': '',
            'invoiceCompany': ''
        }
        r = requests.post(url, data, cookies=cookies_finance)
        return r.json()

    # 客户对账管理-线下对账-导出对账单
    def finance_customer_order_checking_under_line_export(self, export_ids, cookies):

        url = self.mk_url('caiwu', 'api/customer/statementmg/exportCheckOrderList.do')
        data = {
            'exportids': json.dumps(export_ids)
        }
        r = requests.post(url, data, cookies=cookies)
        if platform.system().lower() == 'windows':
            print("windows")
            file_path = export_path + "\\customer_check_export1.xls"
        else:
            print("linux")
            file_path = export_path + "/customer_check_export1.xls"

        print('file_path', file_path)
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
        f.close()
        return file_path

    # 客户对账管理-导入对账单
    def finance_customer_order_checking_under_line_import(self, file, cookies):
        url = self.mk_url('caiwu', 'api/customer/statementmg/trick/importCheckOrderList.do')
        r = requests.post(url, files=file, cookies=cookies)
        return r.json()

    # 客户对账管理-提交对账结果
    def finance_customer_order_checking_under_line_limit(self, request_str, cookies):
        url = self.mk_url('caiwu', 'api/customer/statementmg/getImportTempResult.do')
        data = {
            'requestStr': request_str
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 客户对账管理-确认本次对账（标记对账成功）
    def finance_customer_order_checking_under_line_confirm(self, request_str, cookies):
        url = self.mk_url('caiwu', 'api/customer/statementmg/commitCheckResult.do')
        data = {
            'requestStr': request_str,
            'imgArr': "['https://public.fuyoukache.com/common/5bc1eb7dd5d63.png.do']",
            'checkImgArr': "['https://public.fuyoukache.com/common/5bc1eb7dd5d63.png.do']",
            'documentArr': "[{'path':'https://public.fuyoukache.com/40797d4a-5a72-40cb-b639-b59987b4fe5c---asdfghjkl.xls.do','name':'asdfghjkl.xls'}]"
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    def write_excel(self, path, row, col, write_value, sheet_index=0):
        """
        excel写入(只能写入xls文件,不能写入xlsx文件。)
        :param excel_path: excel路径
        :param sheet_index: sheet
        :param row: 行
        :param col: 列
        :param write_value: 写入的值
        :return:
        """
        rb = xlrd.open_workbook(path, formatting_info=True)
        # 复制
        new_excel = copy(rb)
        # 取sheet表
        excel_sheet = new_excel.get_sheet(sheet_index)
        excel_sheet.write(row, col, write_value)
        new_excel.save(path)

    # 获取所有的账单发票
    def finance_broker_list_all_broker_invoices(self, cookies_finance):
        url = self.mk_url('caiwu', 'api/broker/bill/getAllBrokerInvoices.do')
        data = {
            'type': '',
            'billNos': '',
            'brokerName': '',
            'brokerMobile': '',
            'brokerAreaId': '',
            'brokerProvinceId': '',
            'invoiceCompany': '',
            'providerHeader': '',
            'invoiceNo': '',
            'invoiceCode': '',
            'checkStatus': '',
            'pageNo': 1,
            'pageSize': 30,
            'pageIndex': 1
        }
        r = requests.post(url, data, cookies=cookies_finance)
        return r.json()

    # 审核发票
    def finance_broker_list_check_broker_bill_invoice(self, invoice_ids, cookies_finance, check_status=2):
        """
        :param invoice_ids:
        :param cookies_finance:
        :param check_status: 2:通过，3：不通过
        :return:
        """

        url = self.mk_url('caiwu', 'api/broker/bill/checkBrokerBillInvoice.do')
        data = {
            'invoiceIds': str([invoice_ids]),
            'comment': '123',
            'checkStatus': check_status,
        }
        print(data)
        r = requests.post(url, data, cookies=cookies_finance)
        return r.json()

    # 对外-账单提款
    def finance_broker_list_payment_broker_bill(self, broker_id, bill_no, cookies_finance):
        url = self.mk_url('caiwu', 'api/internal/broker/paymentBrokerBill.do')
        data = {
            'brokerId': broker_id,
            'billNo': bill_no
        }
        print(data)
        r = requests.post(url, data, cookies=cookies_finance)
        print(r.json())
        return r.json()

    # 财务数据修改-客户放空费修改-导入
    def finance_fy_modify_customer_punish_fee_import(self, file, cookies):
        url = self.mk_url('caiwu', 'api/customer/receiptmgr/imCusEmptyFeeModifyData.do')
        r = requests.post(url, files=file, cookies=cookies)
        return r.json()

    # 财务数据修改-客户放空费修改-申请/批量申请
    def finance_fy_modify_customer_punish_fee_apply(self, order_sn, order_money, cookies):
        url = self.mk_url('caiwu', 'api/fy/fundsmgr/bathOrderClaim.do')
        claim_details = []
        for index in range(len(order_sn)):
            claim_details.append({
                "orderSn": order_sn[index],
                "receiptId": "",
                "moneyDetails": [
                    {
                        "moneyType": 40,
                        "money": order_money[index]
                    }
                ]
            })
        msg_body = {
            "proof": [
            ],
            "proofName": [
                {
                    "name": "",
                    "url": ""
                }
            ],
            "claimType": 14,
            "claimComment": "77",
            "claimDetails": json.dumps(claim_details)
        }
        data = {
            "msgBody": json.dumps(msg_body)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 资金单管理--新建资金单--导出银行资金管理的表格
    def finance_fy_fund_manage_template_download(self, temple_type, cookies):
        url = self.mk_url('caiwu', 'api/download/export/exportTemplate.do')
        data = {
            'type': temple_type
        }
        r = requests.post(url, data, cookies=cookies)
        if platform.system().lower() == 'windows':
            print("windows")
            file_path = export_path + "\\import_finance_fund_manage_template.xls"
        else:
            print("linux")
            file_path = export_path + "/import_finance_fund_manage_template.xls"

        with open(file_path, 'wb+') as f:
            f.write(r.content)
        return file_path

    # 资金单管理--新建资金单--导入银行资金管理的表格
    def finance_fy_fund_manage_template_import(self, cookies, file):
        url = self.mk_url('caiwu', 'api/fy/fundsmgr/importBankFundDetail.do')
        data = {}
        r = requests.post(url, data, files=file, cookies=cookies)
        return r.json()

    # 财务数据修改-修改开票公司-获取开票公司
    def finance_fy_modify_get_invoice_company(self, cookies):
        url = self.mk_url('caiwu', 'api/fy/taxmgr/getInvCompany.do')
        r = requests.post(url, cookies=cookies)
        return r.json()

    # 修改开票公司-运单查询（新修）
    def finance_fy_modify_get_invoice_company_old(self, order_sn, cookies):
        url = self.mk_url('caiwu', 'api/fy/abnormalApply/checkModifyInvoiceCompany')
        data = {
            'orderSns': order_sn,
            'pageIndex': 1,
            'pageSize': 30
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 财务数据修改-修改开票公司-修改
    def finance_fy_modify_change_invoice_company(self, cookies, order_sn, invoice_company_new):
        url = self.mk_url('caiwu', 'api/fy/abnormalApply/changeOrdOriBroAreaInfo.do')
        data = {
            'newInvoiceCompany': invoice_company_new,
            'orderSns': order_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 测试支付通道
    def payment_channels(self, payDebug, cookies):
        url = self.mk_url('caiwu', 'api/sys/short/setPayDebug.do')
        data = {
            'payDebug': payDebug,  # true-开启；false-关闭
            'password': '11231qa2ws3ed'
        }
        r = requests.get(url, params=data, cookies=cookies)
        print(r.url, r.json())
        return r.json()

    # 添加日包车/长途包车/里程奖励到司机账户
    def add_driver_reward(self, driver_id, rewards_type, amount, cookies_ua):
        url = self.mk_url('xdriver', 'api/internal/activity/addDriverReward')
        print(url)
        para_data = {
            'id': 1123  # 日包车奖励标的id,司机系统仅校验非空
        }
        data = {
            'driverId': driver_id,  # 发放奖励到哪个司机的账户
            'type': rewards_type,  # type=2 for 日包车；type=3 for 长途包车；type=4 for 里程奖励
            'money': amount,  # 发放金额
            'params': para_data
        }
        r = requests.post(url, data, cookies=cookies_ua)
        print(r.json())
        return r.json()

    # 获取司机奖励钱包信息
    def get_driver_wallet_info(self, token):
        url = self.mk_url('xdriver', 'api/app/activity/getDriverWallet')
        data = {
            'token': token  # 司机token
        }
        r = requests.post(url, data)
        print(r.json())
        return r.json()

    # 司机奖励提现
    def driver_draw(self, total_no_draw_money, code, token, cookies_ua):
        url = self.mk_url('xdriver', 'api/app/activity/driverDraw')
        data = {
            'totalNoDrawMoney': total_no_draw_money,
            'code': code,
            'token': token

        }
        r = requests.post(url, data, cookies=cookies_ua)
        print(r.json())
        return r.json()

    # 财务系统奖励汇总
    def get_rewards_sums(self, reward_type, cookies_ua, driver_id=None, driver_name=None):
        url = self.mk_url('caiwu', 'api/driver/reward/getRewardSums')
        data = {
            'driverId': driver_id,
            'driverName': driver_name,
            'type': reward_type,
            'pageIndex': ' 1',
            'pageSize': ' 30',
            'endTime': ''
        }
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()

    # 财务系统奖励汇总详情界面
    def get_reward_detail(self, driver_id, reward_type, cookies_ua):
        url = self.mk_url('caiwu', 'api/driver/reward/getRewardDetail')
        data = {
            'driverId': driver_id,
            'type': reward_type,
            'endTime': ''
        }
        print(data)
        r = requests.post(url, data, cookies=cookies_ua)
        print(r.json())
        return r.json()

    # 财务奖励提现明细
    def get_driver_reward_payments(self, driver_id, cookies_ua):
        url = self.mk_url('caiwu', 'api/driver/reward/getDriverRewardPayments')
        data = {
            'driverId': driver_id,
            'payStatus': '',
            'pageIndex': ' 1',
            'pageSize': ' 30',
            'applyDrawTimeStart': '',
            'applyDrawTimeEnd': '',
            'payTimeStart': '',
            'payTimeEnd': ''
        }
        r = requests.post(url, data, cookies=cookies_ua)
        # print(r.json())
        return r.json()

    # 金融系统渠道配置
    def update_channel_info(self, value, cookies_ua):
        url = self.mk_url('jr', 'api/payChannelConf/upChannelInfo')
        data = {
            'value': value  # value=0 云信；value=1 平安
        }
        r = requests.post(url, data, cookies=cookies_ua)
        # print(r.url, r.json())
        return r.json()

    # 金融系统渠道配置信息
    def get_channel_info(self, cookies_ua):
        url = self.mk_url('jr', 'api/payChannelConf/getChannelInfo')
        r = requests.post(url, cookies=cookies_ua)
        value = r.json()['data'][0]['value']
        # print(r.url,r.json())
        return value

    # 获取所有可结算账单
    def finance_broker_list_settlement_bill(self, bill_no, order_sn, type_id, cookies_finance):
        url = self.mk_url('caiwu', 'api/broker/bill/getAllBrokerBill.do')
        data = {
            'billName': '',
            'billNos': bill_no,
            'orderSns': order_sn,
            'brokerName': '',
            'brokerMobile': '',
            'brokerAreaId': '',
            'brokerProvinceId': '',
            'invoiceCompany': '',
            'billStatus': '',
            'settStatus': '',
            'pageIndex': 1,
            'pageSize': 30,
            'type': type_id   # 0 月度账单  1 补贴月度账单
        }
        r = requests.post(url, data, cookies=cookies_finance)
        return r.json()
