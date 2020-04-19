from app.tools.api.api_bms import *


def order_address_update(order_sn, env, is_long, has_stop):
    try:
        api_object = ApiBms(env)
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
        if order_status in [7,1,2,4,8,11,24]:
            return '此运单未成单或已取消，无法修改'
        # 获取地址信息
        order_stop_points = order_detail['data'][0]['stopPoints']
        len_stop = len(order_stop_points)

        if is_long == 1:
            final_start = '河北-石家庄-藁城区'
            specific_address_start = '藁城区人民法院'
        if is_long == 0:
            final_start = '云南-玉溪-红塔区'
            specific_address_start = '玉溪市财政局'
        final_end = '云南-昆明-官渡区'
        info_start = address_search(final_start)
        info_end = address_search(final_end)
        update_start = {
            'address': specific_address_start,
            'districtName': info_start['district_name'],
            'districtId': info_start['district_id'],
            'cityName': info_start['city_name'],
            'cityId': info_start['city_id'],
            'provinceName': info_start['province_name'],
            'provinceId': info_start['province_id']
        }
        update_end = {
            'address': '昆明第十六中学',
            'districtName': info_end['district_name'],
            'districtId': info_end['district_id'],
            'cityName': info_end['city_name'],
            'cityId': info_end['city_id'],
            'provinceName': info_end['province_name'],
            'provinceId': info_end['province_id']
        }
        address_start = order_stop_points[0]
        address_end = order_stop_points[-1]
        address_start.update(update_start)
        address_end.update(update_end)

        # 不需要经停点
        if has_stop == 0:
            for point_num in order_stop_points:
                if len(order_stop_points) > 2:
                    order_stop_points.remove(order_stop_points[-2])
                else:
                    break
        # 需要经停点
        if has_stop == 1:
            if is_long == 1:
                final_stop = '陕西-西安-莲湖区'
                specific_address_stop = '西安鼓楼'
            if is_long == 0:
                final_stop = '云南-昆明-晋宁区'
                specific_address_stop = '昆阳第一小学'
            info_stop = address_search(final_stop)
            update_stop = {
                'address': specific_address_stop,
                'districtName': info_stop['district_name'],
                'districtId': info_stop['district_id'],
                'cityName': info_stop['city_name'],
                'cityId': info_stop['city_id'],
                'provinceName': info_stop['province_name'],
                'provinceId': info_stop['province_id']
            }
            if len_stop == 2:
                # 添加经停点
                order_stop_points.insert(1, update_stop)
            if len_stop >= 3:
                if len_stop >3:
                    for j in order_stop_points:
                        if len(order_stop_points) > 3:
                            order_stop_points.remove(order_stop_points[-2])
                        else:
                            break
                order_stop_points[1].update(update_stop)
        re_update_address = api_object.bms_order_exception(order_sn, 41, 122, order_stop_points, cookies_admin)
        return re_update_address['status']['desc']
    except Exception:
        return '请联系相关人员处理'

if __name__ == '__main__':
    r = order_address_update(210010277695, 't4', 1, 0)
    print(r)