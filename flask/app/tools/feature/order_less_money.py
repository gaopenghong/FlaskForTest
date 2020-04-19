from app.tools.api.api_bms import *
from app.tools.api.api_xcusotmer_app import *
from app.tools.api.api_self_driver_app import *


def order_money_less(order_sn, env, pay_type):
    api_object = ApiBms(env)
    try:
        admin_mobile = api_object.bms_admin_mobile()
        admin_info = api_object.admin_info_get(admin_mobile)
        cookies_admin = admin_info['cookies_ua']
        # 检查运单号是否存在
        result_list = api_object.bms_order_list(cookies_admin, {'orderSn': order_sn})
        if result_list['status']['code'] == 3:
            return '该运单号不存在'
        # 检查运单状态
        order_detail = api_object.bms_order_detail(order_sn, cookies_admin)
        order_status = order_detail['data'][0]['quote']['status']
        if order_status not in [17, 18]:
            return '此运单未安排司机或者已经卸货完成'
        # 仅轨迹扣款处理
        if pay_type == 'path':
            result_done_path = api_object.bms_order_exception(order_sn, 12, '', {}, cookies_admin)
            print('仅轨迹扣款处理结果：%s' %result_done_path)
            if result_done_path['status']['code'] == 0:
                return '执行成功'
        else:
            # 检查是否专车
            driver_mobile = order_detail['data'][0]['orderDriver']['driverMobile']
            foryou_truck = order_detail['data'][0]['businessInfo']['productType']
            if foryou_truck == 4 or foryou_truck == 5:
                driver_foryou_login = ApiFyDriverApp(env).self_driver_login(driver_mobile)
                driver_id = driver_foryou_login['data'][0]['id']
                driver_token = driver_foryou_login['data'][0]['token']
            else:
                driver_info = api_object.driver_info_get(driver_mobile)
                driver_token = driver_info['token']
                driver_id = driver_info['id']
            order_stop_points = order_detail['data'][0]['stopPoints']
            update_start = '河北-石家庄-藁城区'
            update_end = '云南-昆明-官渡区'
            info_start = address_search(update_start)
            info_end = address_search(update_end)

            # 修改运单计划运输时效
            if pay_type != 'not':
                sql_update_time = 'update base_info set planTransTime=60 where orderSn="' + order_sn + '"'
                remote_database(env, 'fykc_order_center', sql_update_time)
            # 修改运单装卸货地址
            address_start = order_stop_points[0]
            address_end = order_stop_points[-1]
            final_start = {
                'address': '藁城区人民法院',
                'districtName': info_start['district_name'],
                'districtId': info_start['district_id'],
                'cityName': info_start['city_name'],
                'cityId': info_start['city_id'],
                'provinceName': info_start['province_name'],
                'provinceId': info_start['province_id']
            }
            final_end = {
                'address': '昆明第十六中学',
                'districtName': info_end['district_name'],
                'districtId': info_end['district_id'],
                'cityName': info_end['city_name'],
                'cityId': info_end['city_id'],
                'provinceName': info_end['province_name'],
                'provinceId': info_end['province_id']
            }
            address_start.update(final_start)
            address_end.update(final_end)
            for point_num in order_stop_points:
                if len(order_stop_points) > 2:
                    order_stop_points.remove(order_stop_points[-2])
                else:
                    break
            re_update_address = api_object.bms_order_exception(order_sn, 41, 122, order_stop_points, cookies_admin)
            print('修改装卸货地址结果：%s' % re_update_address['status']['desc'])
            # 上传定位
            locations = [['河北省', '石家庄市', '藁城区', '藁城区人民法院'], ['河北省', '石家庄市', '藁城区', '幸福小院'], \
                         ['河北省', '石家庄市', '藁城区', '藁城农业科技园区'], ['云南省', '昆明市', '官渡区', '昆明第十六中学']]
            for loc in locations:
                send_location(env, loc[0], loc[1], loc[2], loc[3], order_sn, driver_mobile, driver_token, driver_id)
                time.sleep(6)
            # 仅时效扣款、都不扣款处理
            if pay_type == 'time' or pay_type == 'not':
                change_data_time = {
                    "hasLoadLocation": 1,
                    "hasUnloadLocation": 1
                }
                api_object.bms_order_exception(order_sn, 22, modify_data=change_data_time,
                                               cookies_bms=cookies_admin)
            # 运单卸货完成
            result_done = api_object.bms_order_exception(order_sn, 12, '', {}, cookies_admin)
            print('卸货完成结果:%s' % result_done['status']['desc'])

            # 确认有四条定位数据
            # r_order_loc_tra = api_object.bms_order_location_trajectory(order_sn, cookies_admin)
            # print('获取轨迹定位点结果:%s' %r_order_loc_tra)
            # if 'trajectory' in r_order_loc_tra['data'][0].keys():
            #     len_loc = len(r_order_loc_tra['data'][0]['trajectory'])
            #     if len_loc != 4:
            #         return '上传定位点数量不够，请查看'
            # else:
            #     return '无上传定位点，请上传'
            # 时效轨迹扣款确认装卸货地是否打勾
            if pay_type == 'both':
                order_draw_filter = api_object.bms_order_draw_filter(order_sn, cookies_admin)
                if order_draw_filter['data'][0]['hasLoadLocation'] == 1 and order_draw_filter['data'][0][ \
                        'hasUnloadLocation'] == 1:
                    return '此单有时效扣款无轨迹扣款，请重试！'
            # 确认有围栏时间
            time.sleep(3)
            order_time_info = api_object.bms_order_time(order_sn, cookies_admin)
            if 'deductTransTime' in order_time_info['data'][0].keys():
                return '执行成功'
            else:
                return '福佑调整时效未获取到，请重试！'

    except Exception:
        return '请联系相关人员处理'


# 司机上传定位点
def send_location(env, province_name, city_name, district_name, address, order_sn, driver_mobile, driver_token,
                  driver_id):
    url = ApiBms(env).mk_url('xdriver', 'api/app/log/appCalorie')
    l = get_location_by_address(env, province_name, city_name, district_name, address)
    lng = l[0]
    lat = l[1]
    data_1 = {
        "driverId": driver_id,
        "mobile": driver_mobile,
        "actionType": 1,
        "normalType": 1,
        "lat": lat,
        "lng": lng,
        "orderSn": order_sn,
        "provinceName": province_name,
        "cityName": city_name,
        "districtName": district_name,
        "address": address,
        "createTime": int(round(time.time() * 1000))
    }
    data = []
    data.append(data_1)
    data = json.dumps(data, ensure_ascii=False)
    headers = {
        'devVersion': '54',
        'network': '4',
        'appVersion': '3.8.4',
        'osType': '1',
        'imei': '864106034908434',
        'osVersion': '6.0.1',
        'uid': '',
        'model': 'vivoY66',
        'actionTime': '3',
        'networkType': '23',
        'phoneType': 'vivo',
        'customerType': '3',
        'token': driver_token,
        'data': data
    }
    print('请求头:%s' % headers)
    r = requests.post(url, headers)
    r_1 = r.json()
    print('上传定位点结果:%s' % r_1)


# 通过地址获取经纬度
def get_location_by_address(env, province_name, city_name, district_name, address):
    add = province_name + city_name + district_name + address
    r = Amap(env).amap_input_tips(add)
    l = r['tips'][0]['location'].split(',')
    print('获取的经纬度结果:%s' % l)
    return l


if __name__ == '__main__':
    l = order_money_less('429121472817', 't4', 'not')
    print(l)

    # admin = ApiBms('t10').admin_info_get('17313157107')
    # change_data_1 = {
    #     "hasLoadLocation": 0,
    #     "hasUnloadLocation": 0
    # }
    # ApiBms('t10').bms_order_exception(429121049692, 22, modify_data=change_data_1, cookies_bms=admin['cookies_ua'])
