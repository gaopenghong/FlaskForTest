from app.tools.api.api_self_driver_app import ApiFyDriverApp
from app.util.ssh_conf import remote_database
from app.tools.feature.order_abnormal_modify import OrderAbnormalModifySet


class FyDriverReportRoad(ApiFyDriverApp):
    def __init__(self, environment):
        self.env = environment

    # 共建司机上报过路费
    def fy_driver_report_road(self, driver_mobile, report_status):
        order_sn = ApiFyDriverApp.self_driver_make_order()
        driver_info = self.self_driver_login(driver_mobile)
        print(driver_info)
        driver_token = driver_info['data'][0]['token']
        r = self.self_driver_get_truck_detail(driver_token)
        plate_number1 = r['data'][0]['plateNumber']
        sql = "update auto_dispatch_order set status = 2, plateNumber = \'{}\' where orderSn = {}".format(
            plate_number1, order_sn)
        remote_database(self.env, 'fykc_truckforyou_service', sql)
        r2 = self.self_driver_accept(driver_token, order_sn)
        print(r2)
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        print('管理员登录结果: %s' % cookies_ua)
        if report_status >= 0:
            # 司机可以上报过路费
            r3 = OrderAbnormalModifySet.order_abnormal_modify(order_sn, modify_reason='104', order_status='12')
            print(r3)

        if report_status >= 1:
            # 司机已上报过路费
            r4 = self.self_driver_parkfee_report(driver_token, order_sn)
            print(r4)
            r5 = self.truck_report_cashroad_fee_list(cookies_ua, order_sn)
            report_id1 = r5['data'][0]['id']
            print(report_id1)

        if report_status == 2:
            # 司机过路费审核通过
            r6 = self.truck_report_cashroad_fee_update(cookies_ua, report_id1, 2)
            print(r6)

        if report_status == 3:
            # 司机过路费审核未通过
            r7 = self.truck_report_cashroad_fee_update(cookies_ua, report_id1, 3)
            print(r7)
