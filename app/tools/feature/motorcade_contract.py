import traceback

from app.tools.api.api_agent import ApiAgent
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_ua import ApiUa
from app.tools.api.common import get_strf_time
from app.util.ssh_conf import remote_database


class MotorcadeContract(ApiCrm, ApiUa, ApiAgent):
    def __init__(self, environment, admin_mobile='', admin_password='',
                 agent_mobile=''):
        self.env = environment
        self.admin_mobile = admin_mobile
        self.admin_password = admin_password
        self.agent_mobile = agent_mobile
        request_id = self.ua_generate_check_code()
        self.cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, request_id)
        r_agent_login = self.agent_app_login()
        self.agent_token = r_agent_login['data'][0]['token']
        self.agent_id = r_agent_login['data'][0]['id']

    def motorcade_contract_data(self, status):
        r_json = dict()
        contract_id = ''
        contract_code = ''
        try:
            if status >= '0':  # 创建合同
                r_json = self.agent_get_broker(self.agent_token)
                company_id = r_json['data'][0]['companyId']
                company_name = r_json['data'][0]['companyName']
                r_json = self.agent_crm_insert_or_update_contract(self.cookies_ua,
                                                                  get_strf_time(days=-10, strf='%Y-%m-%d'),
                                                                  get_strf_time(days=10, strf='%Y-%m-%d'), company_id,
                                                                  company_name)
            if status >= '1':  # 发起合同签署，合同状态：待签署
                r_json = self.agent_crm_select_contract_list(self.cookies_ua)
                contract_id = r_json['data'][0]['id']
                r_json = self.agent_crm_sign_contract(self.cookies_ua, contract_id, self.agent_id)
            if status == '2':  # 合同撤回，合同状态：已撤回
                r_json = self.test_update_contract_status(contract_id, 8, self.cookies_ua)
            if status >= '3':  # 合同签署，合同状态：已签署
                r_json = self.agent_commit_recharge(self.agent_token, amount=1000)
                print(r_json)
                if r_json['status']['desc'] == '线下转账失败,请稍后再试':
                    r_json = '请确认牛顿系统是否正常启动'
                    return r_json
                r_json = self.agent_get_offlines(self.cookies_ua)
                print(r_json)
                pay_request_id = r_json['data'][0]['payRequestId']
                r_json = self.agent_check_offline_pay(self.cookies_ua, pay_request_id)
                print(r_json)
                r_json = self.agent_sign_contract(contract_id, self.agent_token)
            if status == '4':  # 合同终止，合同状态：已终止
                r_json = self.test_update_contract_status(contract_id, 4, self.cookies_ua)
                sql = "UPDATE company_contract_info SET updateTime = '" + get_strf_time(
                    days=-92) + "' WHERE id = " + str(contract_id)
                remote_database(self.env, 'fykc_xbroker_service', sql)
                print(sql)
            if status == '5':  # 合同状态：已过期
                sql = "UPDATE company_contract_info SET startTime ='" + get_strf_time(
                    days=-2) + "', endTime = '" + get_strf_time(
                    days=-1) + "' WHERE id = " + str(contract_id)
                print(sql)
                remote_database(self.env, 'fykc_xbroker_service', sql)
            if 'status' in r_json:
                r_json = r_json['status']['desc']
            if contract_id != '':
                sql = "SELECT contractCode FROM company_contract_info WHERE id=" + str(contract_id)
                r = remote_database(self.env, 'fykc_xbroker_service', sql)
                contract_code = r[0][0]
                print(contract_code)
        except Exception as e:
            traceback.print_exc()
            print(e)
        finally:
            return '合同编码:' + str(contract_code) + '，结果:' + str(r_json)
