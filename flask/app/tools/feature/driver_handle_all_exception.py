__author__ = "郭冰洁"
__date__ = "2019.10.17"

from app.tools.api.api_ua import ApiUa
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_dispatch import ApiDispatch
from app.tools.feature.driver_upload_receipt import UploadReceipt
from app.tools.feature.driver_upload_exception import uploadException
from app.tools.feature.driver_dispatch_preconfirm import DispatchPreconfirm
from app.util.ssh_conf import *
from app.tools.api.api_bms import ApiBms
from _datetime import datetime, timedelta


class DriverAllException(ApiDispatch, ApiDriver, ApiUa, ApiBms):
    def __init__(self, env):
        self.env = env

    def driver_all_exception(self,order_sn):
        r_ua_request_id = self.ua_generate_check_code()
        cookies = self.ua_login(16866666666, "Ab@123456789", r_ua_request_id)
        order_detail = self.bms_order_detail(order_sn, cookies)
        if order_detail["status"]["code"] == 0:
            driver_mobile = order_detail["data"][0]["orderDriver"]["driverMobile"]
            dispatch_mobile = order_detail["data"][0]["brokers"][0]["brokerMobile"]
            res1 = uploadException(self.env).driver_upload_Exception(order_sn, driver_mobile)
            try:
                res11 = res1["status"]["desc"]
            except:
                res11 = res1
            res2 = UploadReceipt(self.env).driver_upload_receipt(order_sn, driver_mobile)
            try:
                res22 = res2["status"]["desc"]
            except:
                res22 = res2
            res3 = DispatchPreconfirm(self.env).driver_dispatch_Preconfirm(order_sn, driver_mobile, dispatch_mobile)
            print(res3)
            try:
                res33 = res3["status"]["desc"]
            except:
                res33 = res3
            try:
                # 修改时间
                t = datetime.now() - timedelta(hours=24)
                unloadTime = t.strftime("%Y-%m-%d %H:%M:%S")
                sql1 = "update order_transport_info set unloadTime='" + str(
                    unloadTime) + "'  where orderSn =" + order_sn
                print(sql1)
                remote_database(self.env, "fykc_order_center", sql1)
            except:
                pass
            return "回单上传结果：" + str(res22) + ";\n举证上传结果：" + str(res11) + ";\n调度处理结果：" + str(res33)
        else:
            return order_detail["status"]["desc"]

#
# if __name__ == "__main__":
#     qw = DriverAllException()
#     qw.driver_all_exception(429122411956, 13000000601, 15944584448)
