from app.tools.api.api_agent import ApiAgent
from app.tools.api.api_bms import get_port
from app.util.ssh_conf import remote_database


class MotorcadeRegister(ApiAgent):

    def __init__(self, environment):
        self.env = environment

    # 注册经纪人
    def register_agent(self, broker_mobile, is_change='flase'):
        broker_r, broker_info = self.agent_api_register(broker_mobile)
        try:
            broker_token = broker_r['data'][0]['token']
        except Exception as e:
            print(e)
            if broker_r['status']['desc'] == '身份证已存在，请更换后重新提交':
                sql = "select brokerMobile from broker_info where identity='" + broker_info['identity'] + "'"
                r = remote_database(self.env, 'fykc_xbroker_service', sql)
                old_broker_mobile = r[0][0]
                if is_change == "true":
                    sql = "update broker_info set brokerMobile='" + broker_mobile + "',companyId=766" + " where" \
                           " identity='" + broker_info['identity'] + "'"
                    remote_database(self.env, 'fykc_xbroker_service', sql)
                    msg = '更换企业运力手机号成功，原手机号:' + str(old_broker_mobile) + ',新手机号:' + str(broker_mobile)
                    return msg
                else:
                    msg = "身份证被" + old_broker_mobile + "使用"
                    return msg
            else:
                return broker_r['status']['desc']
        company_r = self.agent_bind_company(broker_token)
        return company_r['status']['desc']
