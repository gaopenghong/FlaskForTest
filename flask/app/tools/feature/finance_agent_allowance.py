# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.feature.flow_normal import *


class TestAgentAllowance(ApiFinance, ApiUa, ApiBms):
    """企业运力补贴"""
    def test_flow_allowance(self, order_sn):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = {}
        for password in ['Fy@123456789', 'Ab@123456789']:
            url = self.mk_url('ua', 'api/uc/auth/login')
            data = {
                'userName': '16888888888',
                'userPassword': password,
                'srcType': '',
                'redirectUrl': '',
                'checkCode': '1123',
                'requestId': r_ua_request_id
            }
            r = requests.post(url, data)
            # print(r.text)
            if r.json()['status']['code'] == 0:
                cookies_ua = r.cookies.get_dict()
                break
        print(cookies_ua)
        """异常修改-取消运单-补贴企业运力"""
        data_dict = {
            "cancelFirstReason": 1,
            "comment": "0",
            "customerReason": 1,
            "subsidizeTarget2": 2,
            "extraAmount": "200",
            "subsidizeAmount": "200",
            "cancelSecondReason": 1,
            "subsidizeTarget": 2,
            "extraAmountSysCalcd": "",
            "subsidizeAmountSysCalcd": ""
        }
        r = self.bms_order_exception(order_sn=order_sn, modify_function=11, modify_reason=101,
                                     modify_data=data_dict, cookies_bms=cookies_ua)
        print(r)
        return str(r)


if __name__ == '__main__':
    flow = TestAgentAllowance(environment='t2', role=1, target_status=4,
                              admin_mobile='16888888888', admin_password='Fy@123456789',
                              customer_mobile='12211111111', agent_mobile='16499999999', driver_mobile='16011111111')
    r_order = flow.test_flow_allowance(order_sn=429120961668)
    print('=====>>>当前运单号: %s' % r_order)


