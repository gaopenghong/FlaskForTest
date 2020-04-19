from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_ua import ApiUa
from app.util.ssh_conf import *


class WihteDrawing(ApiCrm, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_Wihte_Drawing(self, driver_mobile):
        r_ua_request_id = self.ua_generate_check_code()
        sql1 = "select   id   from  driver_info  where  mobile=" + str(driver_mobile)
        print(sql1)
        driverId = remote_database(self.env, 'fykc_xdriver_service', sql1)
        if driverId == []:
            return "该司机不存在"
        cookies = self.ua_login("18334704870", "Ab@123456789", r_ua_request_id)
        res = self.crm_driver_drawings(driverId, cookies)
        print(res)
        return res["status"]["desc"]
        return res


if __name__ == "__main__":
    res = WihteDrawing("t4").driver_Wihte_Drawing(12033333333)
    print(res)
