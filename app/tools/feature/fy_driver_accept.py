from app.tools.api.api_self_driver_app import ApiFyDriverApp
from app.util.ssh_conf import remote_database
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_bms import ApiBms
import time


class FyDriverAcceptOrder(ApiUa, ApiBms, ApiFyDriverApp):
    def __init__(self, environment, admin_mobile, admin_password):
        self.env = environment
        request_id = self.ua_generate_check_code()
        self.cookies_ua = self.ua_login(admin_mobile, admin_password, request_id)

    # 共建司机接单
    def fy_driver_accept(self, order_sn, driver_mobile, order_status):
        # order_status = int(order_status)

        order_status_list = ['待接单', '已接单']
        driver_info = self.self_driver_login(driver_mobile)
        print(driver_info)
        if driver_info['data'][0]['isForYou'] == 0:
            return "该手机号未配置为共建车司机"
        else:
            driver_token = driver_info['data'][0]['token']
            r = self.self_driver_get_truck_detail(driver_token)
            plate_number1 = r['data'][0]['plateNumber']
            print('车牌号：', plate_number1)
            r3 = self.self_driver_order_list(driver_token)
            print(r3)
            if r3['status']['desc'] == '结果为空':
                pass
            else:
                # 已有运单时，异常修改完成

                r4 = self.bms_order_exception(r3['data'][0]['orderSn'], 12, cookies_bms=self.cookies_ua)
                print(r4)
                msg = r4

            try:
                # 待接单
                if order_status_list.index(order_status) >= 0:
                    sql = "update auto_dispatch_order set status = 2, plateNumber = \'{}\' where orderSn = {}".format(
                        plate_number1, order_sn)
                    remote_database(self.env, 'fykc_truckforyou_service', sql)
                    r1 = self.self_driver_wait_order_info(driver_token)
                    if r1['status']['desc'] == '操作成功':
                        time.sleep(1)
                        msg = '司机待接单状态'
                    else:
                        msg = "运单状态有问题"
                # 已接单
                if order_status_list.index(order_status) >= 1:
                    r2 = self.self_driver_accept(driver_token, order_sn)
                    if r2['status']['desc'] == '操作成功':
                        msg = '司机已接单状态'
                    elif r2['status']['desc'] == '获取运单信息失败':
                        msg = "运单号输入有误"
                    else:
                        msg = "司机运单有误"
    
                return msg
            except Exception as e:
                print(e)

