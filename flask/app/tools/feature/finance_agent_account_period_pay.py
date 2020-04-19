# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.api.api_financial import *
from app.tools.feature.flow_normal import *


class TestAgentAccountPay(ApiFinance, ApiFinancial, ApiBms, ApiUa):
    """企业运力账期日（外）提款"""
    def __init__(self, environment, order_sn):
        # 获取cookie
        super().__init__(environment)
        self.env = environment
        self.order_sn = order_sn
        r_ua_request_id = self.ua_generate_check_code()
        global cookies_ua
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)

    def test_order_detail(self):
        """从运单详情查到经纪人id，从数据库查到运单对应的结算批号"""
        r1 = self.bms_order_detail(self.order_sn, cookies_ua)
        broker_id = r1['data'][0]['brokers'][0]['brokerId']
        print(broker_id)
        sql_bill_no = 'select * from  broker_bill_order_map  where orderSn = "%s"' % self.order_sn
        remote_database(self.env, 'caiwu', sql_bill_no)
        print(sql_bill_no)
        bill_bos = remote_database(self.env, 'caiwu', sql_bill_no)
        print(bill_bos)
        bill_no = bill_bos[0][1]
        # 执行付款接口
        r = self.finance_broker_list_payment_broker_bill(broker_id, bill_no, cookies_ua)
        return r['status']['desc']

    # def test_financial_reconciliation(self):
    #     """金融系统对账"""
    #     r2 = self.finance_contrast_bill(cookies_ua)
    #     print(r2)
    #
    # def test_financial_payback(self):
    #     """金融系统还款"""
    #     r3 = self.finance_pay_back(cookies_ua)
    #     print(r3)


if __name__ == '__main__':
    flow = TestAgentAccountPay(environment='t1', order_sn=429122471832)
    r_order = flow.test_order_detail()
    print('=====>>>当前运单号提款结果: %s' % r_order)
