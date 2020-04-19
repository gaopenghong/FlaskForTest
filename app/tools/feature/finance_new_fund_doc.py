from app.tools.api.api_finance import *
from app.tools.api.api_ua import *


class FinanceNewFundDoc(ApiFinance, ApiUa):

    def new_fund_list(self, fund_number):
        temple_type = 11
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', r_ua_request_id)
        file_path = self.finance_fy_fund_manage_template_download(temple_type, cookies_ua)

        number = int(fund_number)
        for index in range(number):
            self.write_excel(file_path, index+1, 0, '2019/11/21')   # 交易时间
            self.write_excel(file_path, index+1, 1, '1234.56')       # 收款金额
            self.write_excel(file_path, index+1, 2, '')  # 付款金额
            self.write_excel(file_path, index+1, 3, '6227000015750110380')  # 对方账号
            self.write_excel(file_path, index+1, 4, '技术测试sxx')  # 对方账户名称
            self.write_excel(file_path, index+1, 5, '')  # 付款工作流号
            self.write_excel(file_path, index+1, 6, '技术测试sxx的摘要')  # 摘要
            self.write_excel(file_path, index+1, 7, '江苏银行')  # 银行名称
            self.write_excel(file_path, index+1, 8, '南京福佑在线电子商务有限公司')  # 账户所属公司
            self.write_excel(file_path, index+1, 9, '31120188000137420')  # 银行账号
            self.write_excel(file_path, index+1, 10, time.time()*1000)  # 银行业务流水号

        f = open(file_path, 'rb')
        file = {'file': f}
        r1 = self.finance_fy_fund_manage_template_import(cookies_ua, file)
        return r1['status']['desc']
