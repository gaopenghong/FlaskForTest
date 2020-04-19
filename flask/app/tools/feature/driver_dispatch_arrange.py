from app.tools.api.api_dispatch import ApiDispatch
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_bms import ApiBms
from app.util.ssh_conf import *


class DispatchArrangedirect(ApiDispatch, ApiUa, ApiBms):

    def __init__(self, env):
        self.env = env

    def driver_Dispatch_Arrange_direct(self, order_sn, driver_mobile):
        r_ua_request_id = self.ua_generate_check_code()
        cookies1 = self.ua_login(16866666666, "Ab@123456789", r_ua_request_id)
        try:
            bms_order_detail = self.bms_order_detail(order_sn, cookies1)
        except:
            return "运单服务可能未启动"
        if bms_order_detail["status"]["code"] != 0:
            return bms_order_detail["status"]["desc"]
        else:
            try:
                print(bms_order_detail)
                print(bms_order_detail["data"][0])
                print(bms_order_detail["data"][0]["orderBroker"])
                brokerMobile = bms_order_detail["data"][0]["orderBroker"]["brokerMobile"]
            except:
                print(bms_order_detail["data"][0])
                print(bms_order_detail["data"][0]["brokers"])
                brokerMobile = bms_order_detail["data"][0]["brokers"][0]["brokerMobile"]
        transFee = ""
        r_ua_request_id = self.ua_generate_check_code()
        res = self.dispatch_bind_agent_list(cookies1)
        print(res)
        if res["status"]["code"] == 0:
            for i in res["data"]:
                if i["ownBrokerMobile"] == brokerMobile:
                    adminMobile = i["adminMobile"]
        else:
            return res["status"]["desc"]
        for password in ['Ab@123456789', 'Fy@123456789']:
            cookies2 = self.ua_login(adminMobile, password, r_ua_request_id)
            if cookies2:
                break
        if cookies2 == {}:
            return "运力账号" + brokerMobile + "的密码不是'Ab@123456789'或者 'Fy@123456789"
        # 调度获取司机详情
        try:
            driver_info = self.dispatch_get_driver_info(driver_mobile, cookies2)
        except:
            return "服务器内部错误"
        # 调度确认司机
        res = self.dispatch_arrange_driver(order_sn, driver_info['data'][0], cookies2, transFee, type=2)
        print(res)
        return res["status"]["desc"]

# if __name__ == "__main__":
#     res = DispatchArrangedirect("t4").driver_Dispatch_Arrange_direct(429111929776, 19555555555)
#     print(res)
