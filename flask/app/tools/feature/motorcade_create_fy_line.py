from app.tools.api.api_agent import ApiAgent
from app.tools.api.api_bms import ApiBms
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_customer_pc import ApiCustomerPC
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_finance import ApiFinance
from app.tools.api.api_service import ApiService
from app.tools.api.api_ua import ApiUa


class MotorcadeCreateFyLine(ApiAgent, ApiCustomerPC, ApiCrm, ApiDriver, ApiBms, ApiService, ApiUa, ApiFinance):
    def __init__(self, environment, admin_mobile, admin_password):
        self.env = environment
        self.admin_mobile = admin_mobile
        self.admin_password = admin_password
        # self.mobile = mobile

    # 根据项目线路id创建福佑线路
    def create_fy_line(self, line_route_id, transport_type, mobile):
        request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, request_id)

        if transport_type == '1':
            r = self.agent_crm_create_broker_line(line_route_id=line_route_id, own_broker_mobile_1=mobile,
                                                  transport_type=transport_type, cookies_service=cookies_ua)
        elif transport_type == '2':
            r = self.agent_crm_create_broker_line(line_route_id=line_route_id, broker_mobile_1=mobile,
                                                  transport_type=transport_type, cookies_service=cookies_ua)
        elif transport_type == '3':
            r = self.agent_crm_create_broker_line(line_route_id=line_route_id, transport_type=transport_type,
                                                  cookies_service=cookies_ua)

        return r
