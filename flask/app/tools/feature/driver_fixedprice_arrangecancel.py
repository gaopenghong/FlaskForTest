from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_dispatch import ApiDispatch
from app.tools.api.api_ua import ApiUa
from app.util.ssh_conf import *


class FixedpriceArrangecancel(ApiDispatch, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_Fixedprice_Arrangecancel(self, driver_mobile, dispatch_mobile):
        sql1 = "select   driverId,orderSn   from  order_driver_map  where  driverMobile=" + str(
            driver_mobile) + "  and status=2"
        result = remote_database(self.env, 'fykc_truck_scheduler', sql1)
        print(result)
        if result == []:
            print("该司机下没有待确认单子")
            return "该司机下没有待确认单子"
        driver_id = result[0][0]
        order_sn = result[0][1]
        print(order_sn, driver_id)
        r_ua_request_id = self.ua_generate_check_code()
        cookies = self.ua_login(16888888888, "Ab@123456789", r_ua_request_id)
        res = self.dispatch_bind_agent_list(cookies)
        if res["status"]["code"] == 0:
            for i in res["data"]:
                if i["ownBrokerMobile"] == dispatch_mobile:
                    adminMobile = i["adminMobile"]
        else:
            return res["status"]["desc"]
        # r_ua_request_id1 = self.ua_generate_check_code()
        cookies1 = self.ua_login(adminMobile, "Ab@123456789", r_ua_request_id)
        # 调度获取司机详情
        driver_info = self.dispatch_get_driver_info(driver_mobile, cookies1)
        # 调度确认司机不符合
        res1 = self.dispatch_fixedPrice_arrangeCancel(order_sn, driver_info['data'][0], cookies1)
        print(res1)
        return res1["status"]["desc"]


if __name__ == "__main__":
    res = FixedpriceArrangecancel("t4").driver_Fixedprice_Arrangecancel(19888888888, 18334704870)
    print(res)
