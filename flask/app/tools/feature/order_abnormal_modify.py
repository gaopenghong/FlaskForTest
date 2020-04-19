# coding:utf-8
from app.tools.api.api_bms import *
from app.tools.api.api_ua import *


class OrderAbnormalModifySet(ApiBms, ApiUa):
    def order_abnormal_modify(self, orderSn, modify_reason, order_status):
        request_id_r = self.ua_generate_check_code()
        login_r = self.ua_login('18911487112', 'Ab@123456789', request_id=request_id_r)
        modify_r = self.modify(orderSn, modify_reason, order_status, login_r)
        desc = modify_r['status']['desc']
        print(desc)
        return desc

