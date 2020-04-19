from app.tools.api.api_bms import *
from app.tools.api.api_ua import *

admin_mobile = '17313157107'


# 司机所有运单(待发车、确认发车)卸货完成
def driver_orders_done(env, driver_mobile):
    print(driver_mobile)
    try:
        orders_result, cookies_admin = orders_query({'driverMobile': driver_mobile, 'orderStatus': '17,18'}, env=env)
        if len(orders_result) == 0:
            return '该司机无待发车、确认发车运单', 0
        else:
            for j in orders_result:
                result = ApiBms(env).bms_order_exception(j, 12, '', {}, cookies_admin)
                print(result)
    except Exception as e:
        print(e)
        return '发生异常，请联系相关人员处理', 0
    return result['status']['desc'], len(orders_result)


# 查询司机所有运单
def orders_query(condition=None, env=None):
    print(env)
    admin_info = ApiBms(env).admin_info_get(admin_mobile)
    print(33)
    cookies_admin = admin_info['cookies_ua']
    orders_result = []
    r = ApiBms(env).bms_order_list(admin_info['cookies_ua'], condition)
    print(222)
    if r['status']['code'] != 3:
        for i in r['data']:
            print(i['baseInfo']['orderSn'])
            orders_result.append(i['baseInfo']['orderSn'])
        pages = r['page']['totalPage']
        for j in range(2, pages + 1):
            condition.update({'pageIndex': j})
            r1 = ApiBms(env).bms_order_list(cookies_admin, condition)
            for k in r1['data']:
                print(k['baseInfo']['orderSn'])
                orders_result.append(k['baseInfo']['orderSn'])
    print('运单总数：%s' % (len(orders_result)))
    return orders_result, cookies_admin


if __name__ == '__main__':
    # orders_query({'driverMobile': '16011111111', 'orderStatus': '17,18'}, env='t4')
    l, k = driver_orders_done('r1', '13555767238')
    print(k)
