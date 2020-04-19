from app.tools.api.api_finance import *
from app.tools.api.api_ua import *


class FinanceFlow(ApiFinance, ApiUa):
    def test_online_check(self, order_para, check_status):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        data = {
            'orderPara': order_para
        }
        r_list = self.finance_fy_online_check_list(data, cookies_ua)  # 获取列表
        pay_request_id = r_list['data'][0]['payRequestId']
        r2_check = self.finance_fy_online_check(pay_request_id, check_status, cookies_ua)  # 审核通过
        return r2_check['status']['desc']
