from app.tools.api.api_finance import *
from app.tools.api.api_ua import *
import os


class FinanceFlowUnderLineCheck(ApiFinance, ApiUa):

    def under_the_line_checking(self, order_sns):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        # 筛选下运单号，组装成list
        order_sn_list = order_sns.split()
        check_ids = []
        order_num = len(order_sn_list)
        # 获取线下待对账的列表
        data1 = {
            'orderSn': json.dumps(order_sn_list),
            'status': 1
        }
        r_list = self.finance_customer_order_checking_under_line_list(data1, cookies_ua)
        for i in range(order_num):
            check_ids.append(r_list['data'][i]['id'])

        # 导出对账单
        global file_name1
        file_name1 = self.finance_customer_order_checking_under_line_export(check_ids, cookies_ua)  # 导出对账单
        print(5)
        time.sleep(5)

        # 导入对账单
        for i in range(order_num):
            self.write_excel(file_name1, i+3, 35, 'T')
        f = open(file_name1, 'rb')
        file = {'file': f}
        r1 = self.finance_customer_order_checking_under_line_import(file, cookies_ua)
        global request_str
        request_str = str(r1['property']['requestId'])
        print('导入对账单的返回的self.requestStr', request_str)
        f.close()
        time.sleep(5)

        # 提交对账结果
        r2 = self.finance_customer_order_checking_under_line_limit(request_str, cookies_ua)
        print(r2)
        time.sleep(5)

        # 标记对账成功
        r3 = self.finance_customer_order_checking_under_line_confirm(request_str, cookies_ua)
        print(r3)
        return r3['status']['desc']




