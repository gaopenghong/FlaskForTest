from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_ua import ApiUa
from app.util.ssh_conf import *


class Withdraw(ApiDriver, ApiCrm, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_Withdraw(self, driver_mobile):
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] == 0:
            token = driver_info["data"][0]["token"]
            # 初始化
            r1 = self.test_bank_driverWithDrawInitialize(token)
            print(r1)
            if r1["status"]["code"] != 0:
                return r1["status"]["desc"]
            availableMoney = self.moneyPackage(token)
            r2 = self.sendcode(token, driver_info["data"][0]["mobile"])
            if r2["status"]["code"] != 0:
                return r2["status"]["desc"]
            draw_money_code = self.test_draw_money(driver_info["data"][0]["mobile"], self.env)
            print(draw_money_code)
            r3 = self.driver_draw_money(token, '6228481983226202212', driver_info["data"][0]["mobile"],
                                        draw_money_code[0][0], availableMoney)
            return r3["status"]["desc"]
        else:
            return driver_info

    def driver_activity_withdraw(self, driver_mobile):
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] == 0:
            token = driver_info["data"][0]["token"]
            r1 = self.driver_activity_wallet(token)
            if r1["status"]["code"] != 0:
                return r1["status"]["desc"]
            totalNoDrawMoney = r1["data"][0]["totalNoDrawMoney"]
            r2 = self.sendcode(token, driver_info["data"][0]["mobile"])
            if r2["status"]["code"] != 0:
                return r2["status"]["desc"]
            draw_money_code = self.test_draw_money(driver_info["data"][0]["mobile"], self.env)
            r3 = self.driver_activity_driverdraw(token, draw_money_code[0][0], totalNoDrawMoney)
            return r3["status"]["desc"]
        else:
            return driver_info


#
if __name__ == "__main__":
    res = Withdraw('t4').driver_activity_withdraw('12800000479')
    print(res)
