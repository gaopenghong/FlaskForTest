from app.tools.api.api_finance import *
from app.tools.api.api_ua import *
import os
import platform


class FinanceModifyPunishFee(ApiFinance, ApiUa):

    def modify_punish_fee(self, order_sns, money_list):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        # 筛选下运单号，组装成list
        order_sn_list = order_sns.split()
        money_list = money_list.split()
        order_num = len(order_sn_list)
        print('系统版本：%s' % platform.system().lower())
        if platform.system().lower() == 'windows':
            print("windows")
            file_path = export_path + "\\import_modify_punish_fee.xls"
        else:
            print("linux")
            file_path = export_path + "/import_modify_punish_fee.xls"
        for index in range(order_num):
            self.write_excel(file_path, 1, 0, order_sn_list[index])
            self.write_excel(file_path, 1, 1, money_list[index])
        f = open(file_path, 'rb')
        file = {'file': f}
        r = self.finance_fy_modify_customer_punish_fee_import(file, cookies_ua)
        print('上传结果： ', r)
        r1 = self.finance_fy_modify_customer_punish_fee_apply(order_sn_list, money_list, cookies_ua)
        print('提交结果', r1)
        return r1['status']['desc']





