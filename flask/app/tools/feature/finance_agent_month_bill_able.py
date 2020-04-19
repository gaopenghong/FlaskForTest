# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.feature.flow_normal import *


class TestAgentMonthMoney(ApiFinance, ApiUa, ApiAgent, ApiBms):
    """企业运力账期内提款造数据工具"""
    def __init__(self, environment, order_sn):
        # bms运单详情
        super().__init__(environment)
        self.env = environment
        self.order_sn = order_sn
        r_ua_request_id = self.ua_generate_check_code()
        global cookies_ua
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        self.order_detail = self.bms_order_detail(order_sn, cookies_ua)
        print('r_order_detail-----', self.order_detail)
        self.order_status = self.order_detail['data'][0]['quote']['status']
        # 运力账号
        if 'orderBroker' in self.order_detail['data'][0]:
            self.agent_mobile = self.order_detail['data'][0]['orderBroker']['brokerMobile']
        else:
            self.agent_mobile = ''
            print('请确认运单状态')

    def test_agent_month_money(self):
        """企业运力登录"""
        r_agent_login = self.agent_app_login()
        print(self.agent_mobile)
        print(r_agent_login)
        agent_token = r_agent_login['data'][0]['token']
        print(agent_token)
        self.bms_order_receipt_upload(self.order_sn, cookies_ua)
        self.bms_order_receipt_confirm(self.order_sn, cookies_ua)
        self.bms_order_exception(self.order_sn, modify_function=22, modify_reason='',
                                 modify_data={'hasLoadLocation': 1, 'hasUnloadLocation': 1},
                                 cookies_bms=cookies_ua)
        self.bms_order_mark_exception(self.order_sn, operation_type=2, cookies_bms=cookies_ua)
        self.agent_update_order_account(self.order_sn, agent_token)
        print(self.order_sn)
        print(agent_token)
        r1 = self.agent_get_order_money(self.order_sn, agent_token)
        print(r1)
        r = self.agent_wallet_drawing_batch(agent_token, account_amount='', broker_invoice=r1['data'][0]['brokerInvoice'],
                                            broker_period=r1['data'][0]['brokerPeriod'],
                                            broker_period_days=r1['data'][0]['brokerPeriodDays'],
                                            commission="", is_new=1, order_sn=self.order_sn,
                                            trans_fee=r1['data'][0]['transFee'], real_available_money="")
        print(r)
        return str(r)


if __name__ == '__main__':
    flow = TestAgentMonthMoney(environment='t9', order_sn=429121607840)
    r_order = flow.test_agent_month_money()
    print('=====>>>当前运单号: %s' % r_order)



