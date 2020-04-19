import os
from app.tools.api.api_truck import *
from app.tools.api.api_ua import *


class AddTruckDr(AddDrivers, ApiUa):
    # 添加司机
    def add_truck_driver(self, mobile):
        # 管理员登录
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        # return cookies_ua
        print('管理员登录结果: %s' % cookies_ua)
        r_add_driver = self.add_driver(driver_mobile=mobile, cookies=cookies_ua)
        # return r_add_driver
        if r_add_driver['status']['desc'] == '此身份证已被他人使用':
            return '身份证已使用,请重新输入手机号'
        elif '手机号格式不正确' in r_add_driver['status']['desc']:
            return '手机号格式不正确,请重新输入手机号'
        elif '手机号已被占用' in r_add_driver['status']['desc']:
            return '手机号已被占用，请更换手机号'
        else:
            return r_add_driver['status']['desc']


#   添加专车司机
    def drivers_truck_add(self, mobile):
        # 管理员登录
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        # return cookies_ua
        print('管理员登录结果: %s' % cookies_ua)
        driver_info_list = self.driver_info_search()
        i = random.randint(0, 676)
        driver_info = driver_info_list[i]
        # url = self.mk_url('user', 'api/crm/driver/create')
        driver_plate = driver_info['plateNumber']
        driver_name = driver_info['name']
        driver_id_card_number = driver_info['idCardNumber']
        driver_id_card_address = driver_info['idCardAddress']
        r_add_drivers = self.add_drivers(driver_mobile=mobile, driver_plate=driver_plate, cookies=cookies_ua,
                                         driver_name=driver_name, driver_id_card_number=driver_id_card_number,
                                         driver_id_card_address=driver_id_card_address)
        if r_add_drivers['status']['desc'] == '此身份证已被他人使用':
            return '身份证已使用,请重新输入手机号'
        elif '手机号格式不正确' in r_add_drivers['status']['desc']:
            return '手机号格式不正确,请重新输入手机号'
        elif '手机号已被占用' in r_add_drivers['status']['desc']:
            return '手机号已被占用，请更换手机号'
        # else:
        #     return r_add_drivers['status']['desc']
        get_plate = self.get_driver_by_plate(driver_plate=driver_plate, cookies_ua=cookies_ua)
        print(get_plate)
        driver_id = get_plate['data'][0]['driverList'][0]['id']
        driver = self.driver_truck_add(driver_id=driver_id, name=driver_name, plate_number=driver_plate, mobile=mobile,
                                       cookies_ua=cookies_ua)
        if '合作时间在系统中已存在，不能添加' in driver['status']['desc']:
            return '该车辆已存在，请重新输入手机号'
        else:
            return driver['status']['desc']


if __name__ == '__main__':
    r = AddTruckDr(environment='t2', admin_mobile='16888888888', admin_password='Ab@123456789')
    print(r.drivers_truck_add(mobile='11211111111'))

















