import time
import traceback

from app.tools.api.api_bms import ApiBms, ApiDriver, ApiUa, address_search
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_customer_pc import ApiCustomerPC
from app.tools.feature.driver_register_api import register_driver
from app.util.ssh_conf import remote_database


class MotorcadeFyDriverLine(ApiCrm, ApiBms, ApiDriver, ApiUa, ApiCustomerPC):
    """固定司机成单流程"""

    def __init__(self, environment, admin_mobile, admin_password, customer_mobile, line_info_list):
        super().__init__(environment, admin_mobile=admin_mobile, admin_password=admin_password,
                         customer_mobile=customer_mobile)
        self.line_info_list = line_info_list
        request_id = self.ua_generate_check_code()
        self.cookies_ua = self.ua_login(admin_mobile, admin_password, request_id)
        admin_info = self.bms_admin_info(self.cookies_ua)
        self.admin_id = admin_info['property']['user']['id']
        self.admin_name = admin_info['property']['user']['name']
        self.customer_cookie = self.customer_pc_login()
        for line_index in range(len(self.line_info_list)):
            self.line_info_list[line_index] = address_search(self.line_info_list[line_index])

    # # 新增司机
    # def add_driver(self, driver_mobiles):
    #     try:
    #         register_driver(driver_mobiles[0], driver_mobiles[-1])
    #         return "新增司机成功"
    #     except Exception as e:
    #         print(e)
    #         return "请确认手机号是否正确"

    # 创建项目路线
    def create_project_line(self):
        line_route_id = self.crm_create_project_line(self.line_info_list, self.customer_mobile, self.admin_id,
                                                     self.admin_name, self.cookies_ua)
        return line_route_id

    # 创建福佑线路
    def create_line(self, line_route_id):
        r_json = self.agent_crm_create_broker_line(self.cookies_ua, line_route_id=line_route_id, transport_type='3')
        # if 'data' not in r_json:
        #     return r_json
        # else:
        #     line_id = r_json['data'][0]['id']
        #     return line_id
        return r_json

    # 线路中添加司机
    def line_add_driver(self, driver_mobiles, line_id):
        r_json = ''
        try:
            for driver_mobile in driver_mobiles:
                driver_info = self.agent_crm_get_driver_info(driver_mobile, cookies=self.cookies_ua)
                r_json = driver_info
                driver_id = driver_info['data'][0]['id']
                plate_number = driver_info['data'][0]['truckInfoList'][0]['plateNumber']
                r_json = self.agent_crm_line_add_driver(line_id, driver_id, driver_mobile, plate_number,
                                                        cookies=self.cookies_ua)
        except Exception as e:
            print(e)
        finally:
            return r_json

    # 给司机推送合同
    def create_driver_contract(self, line_id):
        r_json = ''
        try:
            current_line_driver_ids = []
            r_json = self.agent_crm_select_contract_driver(line_id=line_id, cookies=self.cookies_ua)
            for driver_index in range(len(r_json['data'])):
                print(r_json['data'][driver_index]['id'])
                if 'current' not in r_json['data'][driver_index].keys():
                    current_line_driver_ids.append(r_json['data'][driver_index]['id'])
            if current_line_driver_ids:
                r_json = self.agent_crm_create_driver_contract(line_id, current_line_driver_ids,
                                                               cookies=self.cookies_ua)
        except Exception as e:
            print(e)
        finally:
            return r_json

    # 签署合同（通过数据库操作）
    def sign_contract(self, line_id):
        time.sleep(3)
        sql = 'UPDATE line_driver_contract SET status = 3 where lineId=%s' % (line_id)
        print(sql)
        remote_database(self.env, 'fykc_bms', sql)

    # 完成当前司机承运的运单
    def except_unloading(self, driver_mobiles):
        r_json = '请确认是否可以完成当前司机承运的运单'
        try:
            for driver_mobile in driver_mobiles:
                r_json = self.bms_order_list(self.cookies_ua, {'orderStatus': '17', 'driverMobile': driver_mobile})
                if r_json['status']['desc'] != '结果为空':
                    except_order_sn = r_json['data'][0]['orderSn']
                    r_json = self.bms_order_exception(except_order_sn, 12, cookies_bms=self.cookies_ua)
        except Exception as e:
            print(e)
        finally:
            return r_json

    def rank_driver(self, line_id, driver_mobiles):
        """司机上报空车"""
        r_json = '请确认司机是否可以上报空车'
        try:
            for driver_mobile in driver_mobiles:
                r_json = self.driver_login(driver_mobile, check_code='1123')
                driver_token = r_json['data'][0]['token']
                r_json = self.driver_app_line_rank_change(driver_token, 1, '40.035968967013886', '116.30738932291666',
                                                          line_id)
        except Exception as e:
            print(e)
        finally:
            return r_json

    # 发货
    def delivery(self):
        order_sn = ''
        try:
            order_sn = self.crm_agent_delivery(self.line_info_list, self.customer_cookie)
        except Exception as e:
            print(e)
            order_sn = "下单失败"
        finally:
            return order_sn

    # 运单系统异常标记司机卸货完成
    def bms_order_exception_unload(self, order_sn):
        time.sleep(5)
        r_json = self.bms_order_exception(order_sn, 12, cookies_bms=self.cookies_ua)
        return r_json

    # 运单系统异常标记签收完成
    def bms_order_exception_sign(self, order_sn):
        time.sleep(2)
        r_json = self.bms_order_exception(order_sn, 13, cookies_bms=self.cookies_ua)
        return r_json

    #  固定司机流程
    def fy_driver_line(self, driver_mobiles, status):
        r_json = '结果为空'
        order_sn = '运单未生成'
        try:
            # r_json = self.add_driver(driver_mobiles)
            r_json = self.create_project_line()
            line_route_id = r_json
            if 'status' in str(line_route_id):
                return line_route_id
            r_json = self.create_line(line_route_id)
            line_id = r_json
            if 'status' in str(line_id):
                return line_id
            # 添加司机
            if status >= 1:
                print('----福佑线路上添加司机----')
                r_json = self.line_add_driver(driver_mobiles, line_id)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = '福佑线路上添加司机:' + str(r_json)
            # 推送司机合同
            if status >= 2:
                print('----推送司机合同----')
                r_json = self.create_driver_contract(line_id)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = '推送司机合同:' + str(r_json)
            # 签署合同
            if status >= 3:
                print('----签署合同----')
                self.sign_contract(line_id)
                r_json = '签署合同成功'
            # 上报空车
            if status >= 4:
                print('----上报空车----')
                r_json = self.except_unloading(driver_mobiles)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = '上报空车:' + str(r_json)
                r_json = self.rank_driver(line_id, driver_mobiles)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = '上报空车:' + str(r_json)
            # 承单
            if status >= 5:
                print('----承单----')
                r_json = self.delivery()
                order_sn = r_json
                r_json = '承单:' + str(r_json)
                order_json = r_json
            # 运单卸货完成
            if status >= 6:
                print('----运单卸货完成----')
                r_json = self.bms_order_exception_unload(order_sn)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = order_json + ',' + '运单卸货完成:' + str(r_json)
            # 运单签收
            if status >= 7:
                print('----运单签收----')
                r_json = self.bms_order_exception_sign(order_sn)
                if 'status' in r_json:
                    r_json = r_json['status']['desc']
                r_json = order_json + ',' + '运单签收:' + str(r_json)
        except Exception as e:
            print(e)
            print(traceback.print_exc())
        finally:
            return r_json
