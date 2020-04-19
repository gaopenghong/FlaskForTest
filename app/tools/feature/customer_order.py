# coding:utf-8
from app.tools.api.api_xcusotmer_app import *
from app.tools.api.api_customer_app import *
from app.tools.api.api_turing import *
from app.tools.api.api_lbs_amap import *
from app.tools.api.api_driver import *
from app.tools.api.api_crm import *
from app.tools.api.api_ua import *
from app.tools.api.api_bms import *


# 吸货询价-下单-支付
def customer_ai_confirm(env, mobile_customer, order_num=1, price_modify=None, stop_need=False, receipt_need=False,
                        start_address=None, end_address=None, dispatch_ai='off', load_time=None, comment=None,
                        order_status=None, stock_lines=[]):
    ua = ApiUa(environment=env)
    request_id = ua.ua_generate_check_code()
    for password in ['Ab@123456789', 'Fy@123456789']:
        cookies_ua = ua.ua_login('16888888888', password, request_id)
        if cookies_ua:
            break
    if not cookies_ua:
        return '管理员账号16888888888获取cookies失败，请检查数据配置'

    if stock_lines:
        pass
    else:
        data_select = {}
        if start_address or end_address:
            data_select = province_city_district_to_search_dic(start_address, end_address)
        result_test = ApiTuring(environment=env).turing_customer_price_list(data_select, cookies_ua)
        if 'code' not in str(result_test['status']):
            return '吸货基础价格列表接口错误：%s' % result_test
        elif result_test['status']['code'] != 0:
            return '吸货基础价格列表查询异常：%s' % result_test
        else:
            stock_lines = []
            for base_price in result_test['data']:
                stock_line = []
                stock_line.append(base_price['startProvinceName'])
                stock_line.append(base_price['startCityName'])
                stock_line.append(base_price['endProvinceName'])
                stock_line.append(base_price['endCityName'])
                stock_line.append(base_price['carLengthId'])
                stock_line.append(base_price['carModelId'])
                stock_line.append(base_price['startDistrictName'])
                stock_line.append(base_price['endDistrictName'])
                stock_lines.append(stock_line)
            print('库存线路：', stock_lines)

    xcustomer_app = ApiXcustomerAPP(environment=env)
    login_result = xcustomer_app.customer_app_token(mobile_customer)
    if 'code' not in str(login_result['status']):
        return '货主登录接口异常：%s' % login_result
    elif login_result['status']['code'] == 0:
        token_customer = login_result['data'][0]['token']
    else:
        return '货主登录异常：%s' % login_result

    orders_info = []
    for stock_line in stock_lines:
        stop_ponits_info = []
        address_start = stock_line[0] + '-' + stock_line[1] + '-' + stock_line[6]
        address_info_start = address_search(address_start)
        point_info_start = {
            'provinceName': address_info_start['province_name'],
            'cityName': address_info_start['city_name'],
            'districtName': address_info_start['district_name'],
            'latitude': address_info_start['latitude'],
            'longitude': address_info_start['longitude']
        }
        print('装货地：', point_info_start)
        stop_ponits_info.append(point_info_start)

        if stop_need:
            point_info_middle = {
                'provinceName': '浙江',
                'cityName': '杭州',
                'districtName': '江干区',
                'latitude': '30.290953',
                'longitude': '120.213057',
            }
            stop_ponits_info.append(point_info_middle)

        address_stop = stock_line[2] + '-' + stock_line[3] + '-' + stock_line[7]
        address_info_stop = address_search(address_stop)
        point_info_stop = {
            'provinceName': address_info_stop['province_name'],
            'cityName': address_info_stop['city_name'],
            'districtName': address_info_stop['district_name'],
            'latitude': address_info_stop['latitude'],
            'longitude': address_info_stop['longitude']
        }
        print('卸货地：', point_info_stop)
        stop_ponits_info.append(point_info_stop)
        carlength_id = stock_line[4]
        carmodel_id = stock_line[5]

        data_test = {
            'carLengthId': carlength_id,
            'carModelId': carmodel_id,
            'highSpeed': 1
        }

        if load_time:
            data_test['goodsLoadDate'] = load_time
        else:
            data_test['goodsLoadDate'] = time_stamp_create()

        ai_price_result = xcustomer_app.customer_app_quote_ai_price(token_customer, data_test, stop_ponits_info)
        print('预估价结果：', ai_price_result)
        if 'code' not in str(ai_price_result['status']):
            return '报价接口错误：%s' % ai_price_result
        elif ai_price_result['status']['code'] == 0:
            if ai_price_result['property']['status'] == 1:
                break

    if ai_price_result['status']['code'] != 0 or 'priceId'not in ai_price_result['property']:
        return '未能报出价格：%s' % ai_price_result
    elif ai_price_result['property']['priceId'] is None:
        return '未能报出价格：%s' % ai_price_result
    else:
        price_id = ai_price_result['property']['priceId']
        if price_modify:
            xcustomer_app.customer_app_modify_price(price_id, price_modify)

        if ai_price_result['property']['status'] == 1:
            if receipt_need:
                data_test['needReceipt'] = 1                     # 需要回单，填写回单信息
                receipt_json = {
                    'cusName': '技术测试',
                    'cusMobile': '1810000000112',
                    'regionName': '北京北京海淀区',
                    'cusAddress': '金隅嘉华大厦A座1001室',
                    'cusCompany': '北京福佑多多信息技术有限公司'
                }
                data_test['receiptJson'] = json.dumps(receipt_json)
            else:
                data_test['needReceipt'] = 0

            data_test['planTransTime'] = ai_price_result['property']['duration']
            data_test['priceId'] = ai_price_result['property']['priceId']

            if comment:
                data_test['comments'] = comment

            point_info_new = {
                'address': '测试地址',
                'contactMobile': '18100000001',
                'contactName': '测试'
            }
            stop_ponits_info[0].update(point_info_new)
            stop_ponits_info[1].update(point_info_new)
            if stop_need:                            # 经停点联系人信息
                stop_ponits_info[2].update(point_info_new)

            if order_status > 1:
                switch_result = dispatch_ai_switch(env, dispatch_ai)
                if 'code' in switch_result['status']:
                    print('智能调度开关操作成功：%s' % switch_result)
                else:
                    return '智能调度开关操作失败：%s' % switch_result

            for index in range(order_num):
                time.sleep(1)
                confirm_result = xcustomer_app.customer_app_quote_confirm2pay(token_customer, data_test, stop_ponits_info)
                print('确认下单结果：', confirm_result)
                if 'code' not in str(confirm_result['status']):
                    return '确认下单接口错误：%s' % confirm_result
                elif confirm_result['status']['code'] != 0:
                    return '确认下单异常：%s' % confirm_result
                elif 'nonPaymentOrder' in confirm_result['property']:
                    return '货主有二次支付运单未支付，请取消或支付后再下单，运单号：%s' % confirm_result['property']['nonPaymentOrder']
                order_sn = confirm_result['property']['orderSn']
                orders_info.append(order_sn)

                if order_status > 1:
                    pay_result = xcustomer_app.customer_app_confirm_transferaccounts(order_sn, token=token_customer)
                    if 'code' not in str(pay_result['status']):
                        return '线下转账接口错误：%s' % pay_result
                    elif pay_result['status']['code'] != 0:
                        return '货主线下转账失败，%s' % pay_result
                    else:
                        check_result = fiance_pay_online_check(env, order_sn, cookies_ua)
                        if 'code' not in str(check_result['status']):
                            return '财务审核接口错误：%s' % check_result
                        elif check_result['status']['code'] != 0:
                            return '财务线下转账审核失败'

    return orders_info


# 吸货基本价格线路查询条件拼接
def province_city_district_to_search_dic(start_address, end_address):
    search_dic = {}
    if start_address:
        start_list = start_address.split('-')
        match_result = address_match(start_address)
        print(match_result)
        if len(start_list) == 1 and match_result:
            search_dic['startProvinceId'] = int(match_result['province_id'])
        elif len(start_list) == 2 and match_result:
            search_dic['startProvinceId'] = int(match_result['province_id'])
            search_dic['startCityId'] = int(match_result['city_id'])
        elif len(start_list) == 3 and match_result:
            search_dic['startProvinceId'] = int(match_result['province_id'])
            search_dic['startCityId'] = int(match_result['city_id'])
            search_dic['startDistrictId'] = int(match_result['district_id'])
    if end_address:
        start_list = end_address.split('-')
        match_result = address_match(end_address)
        print(match_result)
        if len(start_list) == 1 and match_result:
            search_dic['endProvinceId'] = int(match_result['province_id'])
        elif len(start_list) == 2 and match_result:
            search_dic['endProvinceId'] = int(match_result['city_id'])
            search_dic['endCityId'] = int(match_result['province_id'])
        elif len(start_list) == 3 and match_result:
            search_dic['endProvinceId'] = int(match_result['province_id'])
            search_dic['endCityId'] = int(match_result['city_id'])
            search_dic['endDistrictId'] = int(match_result['district_id'])
    print(search_dic)
    return search_dic


# 线路id获取线路信息及发货员信息
def get_line_info_by_lineid(env, line_id, cookies_ua):

    line_info = {}
    # 线路详情获取线路信息（经停点、车型、车长、子公司信息、合同信息，校验运力是否匹配）
    line_select_test = {
        'id': line_id
    }
    crm = ApiCrm(env)
    respones_lineroute = crm.crm_customer_lineroute_selectlist(line_select_test, cookies_ua)
    print('获取线路信息：%s' % respones_lineroute)
    if 'code' not in str(respones_lineroute['status']):
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

    response_customer_list = crm.crm_customer_customermanagerlist(companyname=subcompany_name, cookie=cookies_ua)
    print('发货员列表：%s' % response_customer_list)
    customer_mobile = None
    if response_customer_list['status']['code'] == 3:
        return '该合同所在子公司下尚未添加发货员'
    else:
        for customer_info in response_customer_list['data']:
            if customer_info['relation']['status'] == 1 and customer_info['relation']['inquiryFlag'] == 1:
                customer_id = customer_info['id']
                relation_id = customer_info['relation']['id']
                customer_detail = crm.crm_customer_customerdetail(customer_id, relation_id, cookies_ua)
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
            address_stop = respones_lineroute['data'][0]['stopPointList'][index-1]['provinceName'] + '-' + \
                           respones_lineroute['data'][0]['stopPointList'][index-1]['cityName'] + '-' + \
                           respones_lineroute['data'][0]['stopPointList'][index-1]['districtName']
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
def quote_by_line_id(env, line_id, order_status, order_num=1):
    ua = ApiUa(env)
    request_id = ua.ua_generate_check_code()
    cookies_ua = ua.ua_login('16888888888', 'Ab@123456789', request_id)
    # 获取线路信息
    line_info = get_line_info_by_lineid(env, line_id, cookies_ua)
    if 'region_list' not in line_info:
        return line_info
    else:
        carmodelid = line_info['car_model_id']
        carlengthid = line_info['car_length_id']
        region_list = line_info['region_list']
        customer_mobile = line_info['customer_mobile']

    customer_app = ApiCustomerApp(env)
    # 生成询价信息
    data_quote = customer_app.make_quote_info(carmodelid=carmodelid, carlengthid=carlengthid, region_list=region_list,
                                              comments='备注-技术测试', tags='33')

    # 登录线路发货员
    xcustomer_app = ApiXcustomerAPP(environment=env)
    login_result = xcustomer_app.customer_app_token(customer_mobile)
    if 'code' not in str(login_result['status']):
        return '货主登录接口异常：%s' % login_result
    elif login_result['status']['code'] == 0:
        token_customer = login_result['data'][0]['token']
    else:
        return '货主登录异常：%s' % login_result

    # 批量询价
    order_sns = []
    for number in range(0, order_num):
        print("新增询价第%d单" % (number + 1))
        for i in range(2):
            r_order_create = customer_app.customer_app_quote_confirm(data_dic=data_quote, token=token_customer)
            print('新增询价: %s' % r_order_create)
            if r_order_create['status']['code'] == 0:
                break
        if 'code' not in str(r_order_create['status']):
            return '新增询价接口错误：%s' % r_order_create
        elif r_order_create['status']['code'] != 0:
            return '新增询价接口异常：%s' % r_order_create
        else:
            order_sn = r_order_create['data'][0]['orderSn']
            print('运单号: %s' % order_sn)
            order_sns.append(order_sn)

        if order_status > 1:
            # bms = ApiBms(env)
            # r_order_info = bms.bms_order_list(cookies_ua, {'orderSn': order_sn})
            # pay_type = r_order_info['data'][0]['businessInfo']['payType']  # 获取支付类型（5.线上支付 3.合同结算）
            # model_id = r_order_info['data'][0]['modelEntry']['id']
            # quote_status = r_order_info['data'][0]['quote']['status']

            # # 初审
            # if model_id == 844 and order_status == 7:
            #     pass
            # else:
            #     base_order_check(order_sn, admin_id, admin_name, cookies_ua)

            # 确认下单
            # r_customer_app_order_detail = customer_app.customer_app_order_detail(customer_token, order_sn)
            # len_points = len(r_customer_app_order_detail['data'][0]['stopPoints'])
            len_points = len(region_list)
            r_customer_app_order_confirm = customer_app.customer_app_order_confirm(token_customer, order_sn, len_points)
            print('确定下单: %s' % r_customer_app_order_confirm)
            if 'code' not in str(r_customer_app_order_confirm['status']):
                return '确认下单接口错误：%s' % r_customer_app_order_confirm
            elif r_customer_app_order_confirm['status']['code'] != 0:
                return '确认下单异常：%s' % r_customer_app_order_confirm

    return str(order_sns)


# 上传司机当前位置
def order_driver_position_now(env, order_sn, lng, lat, action_type=1):
    # 管理系统登录
    ua = ApiUa(env)
    request_id = ua.ua_generate_check_code()
    cookies_ua = ua.ua_login('16888888888', 'Ab@123456789', request_id)
    print(cookies_ua)

    # 运单详情
    bms = ApiBms(env)
    order_info = bms.bms_order_detail(order_sn, cookies_ua)
    print(order_info)
    if 'code' not in str(order_info['status']):
        return '运单详情接口错误：%s' % order_info
    elif order_info['status']['code'] != 0:
        return '运单详情接口异常：%s' % order_info
    elif 'orderDriver' not in order_info['data'][0]:
        return '该运单缺少司机信息，请查看运单状态或详情'
    else:
        driver_id = order_info['data'][0]['orderDriver']['driverId']
        driver_mobile = order_info['data'][0]['orderDriver']['driverMobile']

    # 司机登录
    driver = ApiDriver(env)
    r_driver_login = driver.driver_login(env, driver_mobile)
    print(r_driver_login)
    if 'code' not in str(r_driver_login['status']):
        return '司机登录接口错误：%s' % r_driver_login
    elif r_driver_login['status']['code'] != 0:
        return '司机登录接口异常：%s' % r_driver_login
    else:
        driver_token = r_driver_login['data'][0]['token']

    # 高德地图逆解析
    amp = Amap(env)
    regeo_result = amp.amap_input_regeo(lng, lat)
    print(regeo_result)
    province_name = regeo_result['regeocode']['addressComponent']['province']
    if len(regeo_result['regeocode']['addressComponent']['city']) == 0:
        city_name = province_name
    else:
        city_name = regeo_result['regeocode']['addressComponent']['city']
    if len(regeo_result['regeocode']['addressComponent']['district']) == 0:
        disctrict_name = regeo_result['regeocode']['addressComponent']['township']
    else:
        disctrict_name = regeo_result['regeocode']['addressComponent']['district']
    address = regeo_result['regeocode']['formatted_address'].replace(province_name + city_name + disctrict_name, '')

    location_info = [lat, lng, province_name, city_name, disctrict_name, address]

    # 司机上传定位心跳
    point_result = driver.driver_pulse_location(driver_id, driver_mobile, action_type, order_sn, location_info, driver_token)
    print(point_result)
    if 'code' not in str(r_driver_login['status']):
        return '司机登录接口错误：%s' % r_driver_login
    elif r_driver_login['status']['code'] != 0:
        return '司机登录接口异常：%s' % r_driver_login
    else:
        return str(point_result)


# 发放优惠卷
def customer_grant_coupon_feature(env, mobile, number):
    ua = ApiUa(env)
    request_id = ua.ua_generate_check_code()
    cookies_bms = ua.ua_login('16888888888', 'Ab@123456789', request_id)
    print(cookies_bms)
    customer_app = ApiCustomerApp(env)
    result = customer_app.customer_grant_coupon(env, mobile, cookies_bms, number)
    print(result)
    return result


if __name__ == '__main__':
    # test_result = customer_ai_confirm('t5', '18366697487', pay=True)
    # print(test_result)
    # print(province_city_district_to_search_dic('江苏-淮安', '浙江-宁波'))
    # print(quote_by_line_id('t5', 34521, order_status=2, order_num=2))
    order_driver_position_now('t5', 289110658044, 23.018696, 113.743314)

