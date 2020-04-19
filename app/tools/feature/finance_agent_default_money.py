# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.feature.flow_normal import *


class TestAgentDefaultMoney(ApiFinance, ApiUa, ApiBms):
    """企业运力违约金数据来源"""
    def test_agent_default_money(self, order_sn):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        data_dict = {
                "cancelFirstReason": 2,
                "comment": "取消经纪人原因",
                "companyReason": 0,
                "punishTarget": 1,
                "cancelSecondReason": 5,
                "punishAmount": 200,
                "subsidizeTarget": 2,
                "extraAmountSysCalcd": "",
                "subsidizeAmountSysCalcd": ""
        }
        r = self.bms_order_exception(order_sn, modify_function=11, modify_reason=102,
                                     modify_data=data_dict, cookies_bms=cookies_ua)
        return str(r)
