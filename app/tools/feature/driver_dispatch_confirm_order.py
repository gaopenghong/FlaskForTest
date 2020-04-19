from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_dispatch import ApiDispatch
from app.tools.api.api_ua import ApiUa
from app.util.ssh_conf import *


class DispatchArrangeDriver(ApiDispatch, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_Dispatch_Arrange_Driver(self, driver_mobile, dispatch_mobile):
        sql1 = "select   driverId,orderSn   from  order_driver_map  where  driverMobile=" + str(
            driver_mobile) + "  and status=2"
        print(sql1)
        result = remote_database(self.env, 'fykc_truck_scheduler', sql1)
        print(result)
        if result == []:
            print("该司机下没有待确认单子")
            return "该司机下没有待确认单子"
        driver_id = result[0][0]
        order_sn = result[0][1]
        print(order_sn, driver_id)
        sql2 = "select   transFee   from  order_push  where  orderSn=" + str(order_sn)
        print(sql2)
        transFee = remote_database(self.env, 'fykc_truck_scheduler', sql2)
        transFee = transFee[0][0]
        r_ua_request_id = self.ua_generate_check_code()
        cookies = self.ua_login(dispatch_mobile, "Ab@123456789", r_ua_request_id)
        # 调度获取司机详情
        driver_info = self.dispatch_get_driver_info(driver_mobile, cookies)
        try:
            print(driver_info)
        except:
            return "服务器内部错误"
        # 调度确认运单
        res = self.dispatch_arrange_driver(order_sn, driver_info['data'][0], cookies, transFee, type=1)
        print(res)
        return res["status"]["desc"]


if __name__ == "__main__":
    res = DispatchArrangeDriver("t4").driver_Dispatch_Arrange_Driver(19333333333, 18636299591)
    print(res)
