# coding:utf-8

from app.tools.api.api_crm import *
from app.tools.api.api_bms import *
from app.tools.feature.driver_dispatch_arrange import *
from app.tools.feature.add_driver import *
from app.tools.feature.driver_order_make_point import *
from app.tools.feature.driver_handle_all_exception import *
from app.tools.feature.driver_withdraw import *


# 目标运单状态: 1.新增询价, 2.初审询价, 3.报价, 4.确定下单(4.1.在线支付, 4.2.财务审核), 5.安排司机, 6.运单打点,7.运单签收
class TestDriverStatusOrder(DispatchArrangedirect, orderMakePointAll, DriverAllException, AddDriver, Withdraw,
                            ApiDriver, ApiCrm, ApiUa, ApiCustomerApp, ApiXcustomerAPP):

    def __init__(self, env, type, mob, line_id):
        self.env = env
        self.type = type
        self.mob = mob
        self.sns = self.quote_by_line_id(1, self.type, self.mob, line_id)
        print(self.sns, list(self.sns))
        print(self.sns[0])
        print(self.sns[0][0])
        print(self.sns[0][1])
        self.order_sn = self.sns[0][0]
        self.mobile = self.sns[0][1]

    def get_line_info_by_lineid(self, line_id, cookies_ua):

        line_info = {}
        # 线路详情获取线路信息（经停点、车型、车长、子公司信息、合同信息，校验运力是否匹配）
        line_select_test = {
            'id': line_id
        }
        respones_lineroute = self.crm_customer_lineroute_selectlist(line_select_test, cookies_ua)
        print('获取线路信息：%s' % respones_lineroute)
        if 'code' not in respones_lineroute['status']:
            return '项目线路列表接口错误：%s' % respones_lineroute
        elif respones_lineroute['status']['code'] != 0:
            return '线路id查询异常：%s' % respones_lineroute
        else:
            business_valid = respones_lineroute['data'][0]['businessValid']
            subcompany_name = respones_lineroute['data'][0]['companyName']
            line_info['car_model_id'] = respones_lineroute['data'][0]['carModelId']
            line_info['car_length_id'] = respones_lineroute['data'][0]['carLengthId']
            points = int(respones_lineroute['data'][0]['stopPointCount']) + 2

            # 校验合同是否可用
            if business_valid != 1:
                return '合同状态不可用，请手动修改'

        response_customer_list = self.crm_customer_customermanagerlist(companyname=subcompany_name, cookie=cookies_ua)
        print('发货员列表：%s' % response_customer_list)
        customer_mobile = None
        if response_customer_list['status']['code'] == 3:
            return '该合同所在子公司下尚未添加发货员'
        else:
            for customer_info in response_customer_list['data']:
                if customer_info['relation']['status'] == 1 and customer_info['relation']['inquiryFlag'] == 1:
                    customer_id = customer_info['id']
                    relation_id = customer_info['relation']['id']
                    customer_detail = self.crm_customer_customerdetail(customer_id, relation_id, cookies_ua)
                    customer_mobile = customer_detail['data'][0]['mobile']
                    break
            if customer_mobile is None:
                print("无可用发货员，请查看该公司下发货员信息")
        line_info['customer_mobile'] = customer_mobile
        print('发货员手机号：', customer_mobile)

        # 线路信息拼接
        addresses_list = []
        for index in range(points):
            if index == 0:
                address_start = respones_lineroute['data'][0]['startProvinceName'] + '-' + \
                                respones_lineroute['data'][0]['startCityName'] + '-' + \
                                respones_lineroute['data'][0]['startDistrictName']
                addresses_list.append(address_start)
            elif index == points - 1:
                address_end = respones_lineroute['data'][0]['endProvinceName'] + '-' + \
                              respones_lineroute['data'][0]['endCityName'] + '-' + \
                              respones_lineroute['data'][0]['endDistrictName']
                addresses_list.append(address_end)
            else:
                address_stop = respones_lineroute['data'][0]['stopPointList'][index - 1]['provinceName'] + '-' + \
                               respones_lineroute['data'][0]['stopPointList'][index - 1]['cityName'] + '-' + \
                               respones_lineroute['data'][0]['stopPointList'][index - 1]['districtName']
                addresses_list.append(address_stop)

        region_list = []
        for j in range(points):
            address_info = address_search(addresses_list[j])
            temp_region = {
                'address': '技术测试%s' % j,
                'provinceId': address_info['province_id'],
                'provinceName': address_info['province_name'],
                'cityId': address_info['city_id'],
                'cityName': address_info['city_name'],
                'districtId': address_info['district_id'],
                'districtName': address_info['district_name'],
                'latitude': address_info['latitude'],
                'longitude': address_info['longitude'],
                'planInTime': '',
                'planOutTime': '',
                'sort': j,
                'contactId': '',
                'contactName': '',
                'contactMobile': '',
            }
            region_list.append(temp_region)
        line_info['region_list'] = region_list
        print(line_info)
        return line_info

    # 线路id询价-下单
    def quote_by_line_id(self, order_num, type, mob, line_id):
        order_status = 5
        request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login('16888888888', 'Ab@123456789', request_id)
        # 获取线路信息
        line_info = self.get_line_info_by_lineid(line_id, cookies_ua)
        if 'region_list' not in line_info:
            return line_info
        else:
            carmodelid = line_info['car_model_id']
            carlengthid = line_info['car_length_id']
            region_list = line_info['region_list']
            customer_mobile = line_info['customer_mobile']

        # 生成询价信息
        data_quote = self.make_quote_info(carmodelid=carmodelid, carlengthid=carlengthid, region_list=region_list,
                                          comments='备注-技术测试', tags='33')

        # 登录线路发货员
        login_result = self.customer_app_token(customer_mobile)
        if 'code' not in login_result['status']:
            return '货主登录接口异常：%s' % login_result
        elif login_result['status']['code'] == 0:
            token_customer = login_result['data'][0]['token']
        else:
            return '货主登录异常：%s' % login_result

        # 批量询价
        order_sns = []
        for number in range(0, int(order_num)):
            print("新增询价第%d单" % (number + 1))
            if type == "1":
                driver_mobile = self.add_driver_1(1, mob)
            elif type == "2":
                driver_mobile = mob
            for i in range(2):
                r_order_create = self.customer_app_quote_confirm(data_dic=data_quote, token=token_customer)
                print('新增询价: %s' % r_order_create)
                if r_order_create['status']['code'] == 0:
                    break
            if 'code' not in r_order_create['status']:
                return '新增询价接口错误：%s' % r_order_create
            elif r_order_create['status']['code'] != 0:
                return '新增询价接口异常：%s' % r_order_create
            else:
                order_sn = r_order_create['data'][0]['orderSn']
                print('运单号: %s' % order_sn)
                order_sns.append([order_sn, driver_mobile])
            if order_status > 1:
                len_points = len(region_list)
                r_customer_app_order_confirm = self.customer_app_order_confirm(token_customer, order_sn, len_points)
                time.sleep(5)
                print('确定下单: %s' % r_customer_app_order_confirm)
                if 'code' not in r_customer_app_order_confirm['status']:
                    return '确认下单接口错误：%s' % r_customer_app_order_confirm
                elif r_customer_app_order_confirm['status']['code'] != 0:
                    return '确认下单异常：%s' % r_customer_app_order_confirm
            res = self.driver_Dispatch_Arrange_direct(order_sn, driver_mobile)
            if "运力账号" in res:
                return res
        return order_sns

    def driver_status_order(self, status_name):
        status_code = {"承运中": 5, "打点完成": 6, "异常处理完成": 7, "有可提款": 8, "提款完成": 9}
        for key in status_code:
            if key == status_name:
                status = status_code[status_name]
        print(status)
        # 运单打点（即创建待确认运单）
        if status >= 6:
            self.driver_order_make_point_all(self.order_sn, self.mobile)
        # 处理完所有异常
        if status >= 7:
            self.driver_all_exception(self.order_sn)
        # 有提金额
        if status >= 8:
            result = self.driver_login(self.mobile, "1123")
            if result['status']['desc'] != "操作成功":
                return result['status']['desc']
            driver_token = result["data"][0]["token"]
            res = self.driver_update_order_account(driver_token, self.order_sn)
            print("司机确认运单" + str(res))
        # 提款完成
        if status >= 9:
            self.driver_Withdraw(self.mobile)
        return str(["司机手机号："+self.mobile,"运单号："+self.order_sn])


if __name__ == "__main__":
    res = TestDriverStatusOrder("t4", 180, 39431).driver_status_order(9)
    print(res)
