# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.feature.flow_normal import *


class TestFyInvoiceInternal(ApiFinance, ApiUa):
    """内部关联运单"""

    def test_finance_invoice_internal(self, order_sn):
        """内部关联运单"""
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
            r0 = requests.post(url, data)
            if r0.json()['status']['code'] == 0:
                cookies_ua = r0.cookies.get_dict()
                break
        print(cookies_ua)
        company_r = self.finance_fy_modify_get_invoice_company(cookies_ua)  # 获取开票公司下拉列表
        print(company_r)
        r = self.finance_fy_modify_get_invoice_company_old(order_sn, cookies_ua)
        print(r)
        if type(r['status']) == int:
            return '运单开票信息列表接口错误：%s' %r
        elif r['status']['code'] != 0:
            return '运单开票信息列表结果：%s' % r
        else:
            for order_info in r['data']:
                invoice_company_list = [company_info['companyName'] for company_info in company_r['data']]
                order_sn = order_info['orderSn']
                invoice_company_old = order_info['invoiceCompany']
                print(invoice_company_old)
                if invoice_company_old in invoice_company_list:
                    invoice_company_list.remove(invoice_company_old)
                invoice_company_new = random.choice(invoice_company_list)
                print(invoice_company_list)
                print(invoice_company_new)
                r2 = self.finance_fy_modify_change_invoice_company(cookies_ua, order_sn, invoice_company_new)
                print(r2)
        return str(r2)




