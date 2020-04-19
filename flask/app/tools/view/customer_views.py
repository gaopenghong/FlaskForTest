#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5


from flask import render_template, request, session
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
# models导入
from app.tools.models.customer_model import *
# feature导入
from app.tools.feature.customer_order import *


# 客户相关
@tools_blue.route('/tools/customerIndex')
def customer_index():
    return render_template('tools/customer.html', name=session.get('username'))


# 吸货下单
@tools_blue.route('/tools/customerNewConfirm', methods=['GET', 'POST'])
def customer_new_confirm():
    env = request.values.get('env')
    customer_mobile = request.values.get('customer_mobile')
    load_time = request.values.get('load_time')
    order_num = request.values.get('order_num')
    start_address = request.values.get('start_address')
    end_address = request.values.get('end_address')
    receipt_need = request.values.get('receipt_need')
    stop_need = request.values.get('stop_need')
    dispatch_ai = request.values.get('dispatch_ai')
    comment = request.values.get('comment')
    order_status = request.values.get('order_status')
    modify_price = request.values.get('modify_price')
    print(customer_mobile, load_time, start_address, end_address, receipt_need, stop_need, dispatch_ai, comment)
    try:
        return '结果返回成功，请查看列表'
    finally:
        if load_time:
            load_time_stamp = int(time.mktime(time.strptime(load_time.replace('T', ' ') + ':00', "%Y-%m-%d %H:%M:%S"))*1000)
            print(load_time_stamp)
        else:
            load_time_stamp = None
        dic_bool = {
            '0': False,
            '1': True
        }
        res = customer_ai_confirm(env, customer_mobile, int(order_num), modify_price, load_time=load_time_stamp,
                                  end_address=end_address, receipt_need=dic_bool[receipt_need], start_address=start_address,
                                  dispatch_ai=dispatch_ai, stop_need=dic_bool[stop_need], comment=comment,
                                  order_status=int(order_status))
        print(res)
        order_info = {
            '运单状态': order_status,
            '车长车型': '9.6米厢式车',
            '装货时间': load_time,
            '装货地': start_address,
            '卸货地': end_address,
            '回单要求': receipt_need,
            '经停点要求': stop_need,
            '智能调度': dispatch_ai,
            '运单金额': modify_price,
            '备注信息': comment
        }
        commit = str(res)
        CustomerOrderConfirm.create(session.get('username'), str(customer_mobile), str(order_info), env, commit,
                                    datetime.now())
        stat.Operate.create(session.get('username'), '/tools/customerNewConfirm', datetime.now(), '吸货下单')
        return str(res)


# 吸货下单记录
@tools_blue.route('/tools/getCustomeNewConfirmList', methods=['GET', 'POST'])
def customer_new_confirm_list():
    res = CustomerOrderConfirm.get_customer_order_confirm_list()
    return res


# 项目货线路id下单
@tools_blue.route('/tools/customerConfirmByLineId', methods=['GET', 'POST'])
def customer_confirm_by_line_id():
    env = request.values.get('env')
    order_status = request.values.get('order_status')
    line_id = request.values.get('line_id')
    order_num = request.values.get('order_num')
    res = quote_by_line_id(env, line_id, int(order_status), int(order_num))
    commit = res
    CustomerConfirmByLineId.create(session.get('username'), line_id, order_num, env, commit, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/customerConfirmByLineId', datetime.now(), '项目货线路id下单')
    return res


# 项目货线路id下单记录
@tools_blue.route('/tools/customerConfirmByLineIdList', methods=['GET', 'POST'])
def customer_confirm_by_line_id_list():
    res = CustomerConfirmByLineId.get_confirm_line_id_list()
    return res


# 运单上传司机定位心跳
@tools_blue.route('/tools/orderDriverPositionHeartbeat', methods=['GET', 'POST'])
def order_driver_position_heartbeat():
    env = request.values.get('env')
    order_sn = request.values.get('order_sn')
    lng = request.values.get('lng')
    lat = request.values.get('lat')
    action_type = request.values.get('action_type')
    res = order_driver_position_now(env, order_sn, lng, lat, int(action_type))
    commit = res
    lng_lat = str(lng) + ',' + str(lat)
    type_dic = {
        '1': '上传定位',
        '2': '上传心跳'
    }
    OrderPositionHeartbeat.create(session.get('username'), order_sn, lng_lat, type_dic[action_type], env, commit,
                                  datetime.now())
    stat.Operate.create(session.get('username'), '/tools/orderDriverPositionHeartbeat', datetime.now(), '运单上传司机定位心跳')
    return res


# 运单上传司机定位心跳记录
@tools_blue.route('/tools/orderDriverPositionHeartbeatList', methods=['GET', 'POST'])
def order_driver_position_now_list():
    res = OrderPositionHeartbeat.get_order_position_heartbeat_list()
    return res


# 司机上传压车时长
@tools_blue.route('/tools/orderTimeOut', methods=['GET', 'POST'])
def order_time_out():
    env = request.values.get('env')
    order_sn = request.values.get('order_sn')
    time_out = request.values.get('time_out')
    customer_app = ApiCustomerApp(env)
    res = str(customer_app.time_out_money(env, order_sn, time_out))
    commit = res
    print(res)
    OrderTimeOut.create(session.get('username'), order_sn, time_out, env, commit, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/orderTimeOut', datetime.now(), '司机上传压车时长')
    return res


# 司机上传压车时长记录
@tools_blue.route('/tools/orderTimeOutList', methods=['GET', 'POST'])
def order_time_out_now_list():
    res = OrderTimeOut.get_order_time_out_list()
    return res


# 发放优惠卷
@tools_blue.route('/tools/GrantCoupon', methods=['GET', 'POST'])
def customer_grant_coupon():
    env = request.values.get('env')
    mobile = request.values.get('mobile')
    number = request.values.get('number')
    res = str(customer_grant_coupon_feature(env, mobile, number))
    commit = res
    CustomerGrantCoupon.create(session.get('username'), mobile, number, env, commit, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/GrantCoupon', datetime.now(), '发放优惠卷')
    return res


# 发放优惠卷记录
@tools_blue.route('/tools/GrantCouponList', methods=['GET', 'POST'])
def grant_coupon_now_list():
    res = CustomerGrantCoupon.get_grant_coupon_list()
    return res
