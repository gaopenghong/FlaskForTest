# __author__ = '沈玉会'
from app.tools.api.api_finance import *
from app.tools.feature.flow_normal import *
from app.util.ssh_conf import *
import time


class TestAgentTaxBill(ApiFinance, ApiUa, ApiAgent, ApiCrm, ApiBms):
    """企业运力账期内提款造数据工具"""
    def __init__(self, environment, agent_mobile):
        # bms运单详情
        super().__init__(environment, agent_mobile)
        self.env = environment
        self.agent_mobile = agent_mobile
        global cookies_ua, agent_token
        r_ua_request_id = self.ua_generate_check_code()
        r_agent_login = self.agent_app_login()
        print(r_agent_login)
        agent_token = r_agent_login['data'][0]['token']
        print(agent_token)
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)

    def test_tax_bill(self, order_sn):
        """企业运力月账单造发票工具"""
        sql_bill_no = 'select * from  broker_bill_order_map  where orderSn = "%s"' % order_sn
        remote_database(self.env, 'caiwu', sql_bill_no)
        print(sql_bill_no)
        bill_bos = remote_database(self.env, 'caiwu', sql_bill_no)
        print(bill_bos)
        global bill_no
        bill_no = bill_bos[0][1]
        r2 = self.finance_broker_list_settlement_bill(bill_no, order_sn, 0, cookies_ua)
        print(r2)
        global invoice_money, invoice_company
        # invoice_money = r2['data'][0]['undrawMoney']
        invoice_money = r2['data'][0]['transFee'] - r2['data'][0]['deductFee']
        print(invoice_money)
        invoice_company = r2['data'][0]['invoiceCompany']
        """修改进项税发票"""
        sql_1 = 'select * from input_tax_info where invoiceType = 4 and invoiceStatus = 0 ' \
                'and salesName != "长安电力华中发电有限公司" order by id limit 10'
        r_1 = remote_database(self.env, 'fykc_taxsys_service', sql_1)
        print(r_1)
        bill_bos_invoice = remote_database(self.env, 'fykc_taxsys_service', sql_1)
        print(bill_bos_invoice)
        global purchase_name, sales_name, invoice_code, invoice_no
        sales_name = bill_bos_invoice[0][3]
        invoice_code = bill_bos_invoice[0][4]
        invoice_no = bill_bos_invoice[0][5]
        # 财务前端校验不含税金额，税额，税率
        global net_price, invoice_fee, invoice_percent
        net_price = bill_bos_invoice[0][8]
        invoice_fee = bill_bos_invoice[0][9]
        invoice_percent = bill_bos_invoice[0][10]
        print(net_price, invoice_fee, invoice_percent)
        global company_name, tax_no
        purchase_name = bill_bos_invoice[0][2]
        company_name = '长安电力华中发电有限公司'
        tax_no = '91430000325714159U'
        sql_count_0 = 'update input_tax_info set purchaseName="%s", salesName="%s", ' \
                      'totalInvoiceFee=%s,salesTaxNo ="%s" where invoiceNo="%s" and invoiceCode="%s"' \
                      % (invoice_company, company_name, invoice_money, tax_no, invoice_no, invoice_code)
        remote_database(self.env, 'fykc_taxsys_service', sql_count_0)
        print(sql_count_0)
        sql_bill_time = 'select * from input_tax_info where invoiceNo="%s" and invoiceCode="%s" ' \
                        % (invoice_no, invoice_code)
        remote_database(self.env, 'fykc_taxsys_service', sql_bill_time)
        bill_time = remote_database(self.env, 'fykc_taxsys_service', sql_bill_time)
        invoice_date_1 = bill_time[0][13]
        time_array = time.strptime(str(invoice_date_1), "%Y-%m-%d %H:%M:%S")
        global invoice_date
        invoice_date = int(time.mktime(time_array)) * 1000
        time.sleep(2)
        r_list = self.agent_add_invoice(bill_no, invoice_money, invoice_date, agent_token, invoice_no,
                                        invoice_code, invoice_company, company_name, tax_no)
        # 将财务系统结算批发票列表里的对应发票不含税金额，税额，税率添上
        sql_count_1 = 'update broker_bill_invoice_info set netPrice="%s", invoicePercent="%s"/100, invoiceFee="%s" ' \
                      'where invoiceNo=%s and invoiceCode=%s' \
                      % (net_price, invoice_percent, invoice_fee, invoice_no, invoice_code)
        remote_database(self.env, 'caiwu', sql_count_1)
        print(sql_count_1)
        return str(r_list)


if __name__ == '__main__':
    flow = TestAgentTaxBill(environment='t1', agent_mobile='16499999999')
    r_order = flow.test_tax_bill(order_sn=429122400917)
