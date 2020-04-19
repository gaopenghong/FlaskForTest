#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from typing import Union

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session
# models位置
from app.tools.models.order_model import *
from app.tools.models.order_model import AppointOrderInfo
from app.tools.models.order_model import ScheduleSwitch
from app.tools.models.order_model import OperateOrder

# feature
from app.tools.feature.flow_third import *
from app.tools.feature.appoint_order import *
from app.tools.feature.driver_orders_done import *
from app.tools.feature.order_less_money import *
from app.tools.feature.flow_auto_query import *
from app.tools.feature.order_abnormal_modify import *
from app.tools.feature import schedule_switch
from app.tools.feature.operate_appoint_order import *

# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from datetime import datetime


# 运单首页
@tools_blue.route('/tools/orderIndex')
def order_index():
    return render_template('tools/order.html', name=session.get('username'))


# 德邦询价页面
@tools_blue.route('/tools/orderDebangIndex')
def order_debang_index():
    return render_template('tools/order.html', name=session.get('username'))


# 德邦询价连接后台方法
@tools_blue.route('/tools/orderDebang', methods=['GET', 'POST'])
def order_debang():
    env = request.values.get('env')
    orderCode = request.values.get('orderCode')
    orderStauts = request.values.get('orderStauts')
    dotype = request.values.get('dotype')
    departureName = request.values.get('departureName')
    arrivalsName = request.values.get('arrivalsName')
    models = request.values.get('models')
    boxType = request.values.get('boxType')
    productType = request.values.get('productType')
    price = request.values.get('price')
    global db_order
    try:
        if dotype == '1':
            res = DeBangFlow(environment=env).debangorder(departureName, arrivalsName, models, boxType, productType,
                                                          price)
            third_res = res[1]
            db_order = res[1]
            if res[0]['responseType'] == '1':
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), db_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderDebang', datetime.now(),
                                '德邦询价单')
            return third_res
        elif dotype == '2':
            res = DeBangFlow(environment=env).debangconfim(orderCode, orderStauts)
            if res['status']['code'] == 0:
                result = '德邦中标成功'
            else:
                result = '德邦中标失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), db_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderDebang', datetime.now(),
                                '德邦询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception as e:
        print(e)
        return "系统异常，请联系管理员"


# 德邦模拟对账
@tools_blue.route('/tools/orderDebangChecking', methods=['GET', 'POST'])
def order_debang_checking():
    env = request.values.get('env')
    orderCode = request.values.get('orderCode')
    res = DeBangFlow(environment=env).debang_checking(orderCode)
    try:
        if res['status']['code'] == 0:
            result = '德邦对账成功'
        else:
            result = '德邦对账失败'
        AddThirdOrder.create(session.get('username'), db_order, env, result, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/orderDebangChecking', datetime.now(),
                            '德邦询价单对账')
        return res['status']['desc']

    except Exception:
        return '运单号不能为空！'


# 德邦询价数据入库
@tools_blue.route('/tools/getOrderDebangList', methods=['GET', 'POST'])
def get_debang_list():
    res = AddThirdOrder.get_third_list()
    return res


# 京东询价页面
@tools_blue.route('/tools/orderJdIndex')
def order_jd_index():
    return render_template('tools/order.html', name=session.get('username'))


# 京东询价连接后台方法
@tools_blue.route('/tools/orderJd', methods=['GET', 'POST'])
def order_jd():
    env = request.values.get('env')
    order_code = request.values.get('order_code')
    dotype = request.values.get('dotype')
    bengin_adress = request.values.get('bengin_adress')
    end_adress = request.values.get('end_adress')
    carlengthtype = request.values.get('carlengthtype')
    global jd_order
    try:
        if dotype == '1':
            res = JDFlow(environment=env).jdorder(carlengthtype, bengin_adress, end_adress)
            third_res = res[1]
            jd_order = res[1]
            if res[0]['status']['code'] == 0:
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), jd_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderJd', datetime.now(),
                                '京东询价单')
            return third_res
        elif dotype == '2':
            res = JDFlow(environment=env).jdconfirm(order_code)
            if res['status']['code'] == 0:
                result = '京东中标成功'
            else:
                result = '京东中标失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), jd_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderJd', datetime.now(),
                                '京东询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception:
        return "系统异常，请联系管理员"


# 京东询价数据入库
@tools_blue.route('/tools/getOrderJdList', methods=['GET', 'POST'])
def get_jd_list():
    res = AddThirdOrder.get_third_list()
    return res


# 跨越询价页面
@tools_blue.route('/tools/orderKyIndex')
def order_ky_index():
    return render_template('tools/order.html', name=session.get('username'))


# 跨越询价连接后台方法
@tools_blue.route('/tools/orderKy', methods=['GET', 'POST'])
def order_ky():
    env = request.values.get('env')
    order_code = request.values.get('order_code')
    dotype = request.values.get('dotype')
    bengin_adress = request.values.get('bengin_adress')
    end_adress = request.values.get('end_adress')
    carlengthtype = request.values.get('carlengthtype')
    global ky_order
    try:
        if dotype == '1':
            res = KYFlow(environment=env).kyorder(carlengthtype, bengin_adress, end_adress)
            third_res = res[1]
            ky_order = res[1]
            if res[0]['status']['code'] == 0:
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), ky_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderKy', datetime.now(),
                                '跨越询价单')
            return third_res
        elif dotype == '2':
            res = KYFlow(environment=env).kyconfirm(order_code)
            if res['status']['code'] == 0:
                result = '跨越中标成功'
            else:
                result = '跨越中标失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), ky_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderKy', datetime.now(),
                                '跨越询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception:
        return "系统异常，请联系管理员"


# 跨越询价数据入库
@tools_blue.route('/tools/getOrderKyList', methods=['GET', 'POST'])
def get_ky_list():
    res = AddThirdOrder.get_third_list()
    return res


# 顺丰询价页面
@tools_blue.route('/tools/orderSfIndex')
def order_sf_index():
    return render_template('tools/order.html', name=session.get('username'))


# 顺丰询价连接后台方法
@tools_blue.route('/tools/orderSf', methods=['GET', 'POST'])
def order_sf():
    env = request.values.get('env')
    order_code = request.values.get('order_code')
    dotype = request.values.get('dotype')
    vehicleton = request.values.get('vehicleton')
    vehicletypecode = request.values.get('vehicletypecode')
    bengin_adress = request.values.get('bengin_adress')
    cross_adress = request.values.get('cross_adress')
    end_adress = request.values.get('end_adress')
    global sf_order
    try:
        if dotype == '1':
            res = SfFlow(environment=env).sforder(vehicleton, vehicletypecode, bengin_adress, cross_adress, end_adress)
            third_res = res['data'][0]
            sf_order = res['data'][0]
            if res['status']['code'] == 0:
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), sf_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderSf', datetime.now(),
                                '顺丰询价单')
            return third_res
        elif dotype == '2':
            res = SfFlow(environment=env).sfconfirm(order_code)
            if res['status']['code'] == 0:
                result = '顺丰中标成功'
            else:
                result = '顺丰中标失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), sf_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderSf', datetime.now(),
                                '顺丰询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception:
        return "系统异常，请联系管理员"


# 顺丰询价数据入库
@tools_blue.route('/tools/getOrderSfList', methods=['GET', 'POST'])
def get_sf_list():
    res = AddThirdOrder.get_third_list()
    return res


# 圆通询价页面
@tools_blue.route('/tools/orderYtIndex')
def order_yt_index():
    return render_template('tools/order.html', name=session.get('username'))


# 圆通询价连接后台方法
@tools_blue.route('/tools/orderYt', methods=['GET', 'POST'])
def order_yt():
    env = request.values.get('env')
    order_code = request.values.get('order_code')
    dotype = request.values.get('dotype')
    bengin_adress = request.values.get('bengin_adress')
    end_adress = request.values.get('end_adress')
    carlengthtype = request.values.get('carlengthtype')
    global yt_order
    try:
        if dotype == '1':
            res = YtFlow(environment=env).ytorder(carlengthtype, bengin_adress, end_adress)
            third_res = res[1]
            yt_order = res[1]
            if res[0]['status']['code'] == 0:
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), yt_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderYt', datetime.now(),
                                '圆通询价单')
            return third_res
        elif dotype == '2':
            res = YtFlow(environment=env).ytconfirm(order_code)
            if res['status']['code'] == 0:
                result = '圆通中标成功'
            else:
                result = '圆通中标失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), yt_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderYt', datetime.now(),
                                '圆通询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception:
        return "系统异常，请联系管理员"


# 圆通询价数据入库
@tools_blue.route('/tools/getOrderYtList', methods=['GET', 'POST'])
def get_yt_list():
    res = AddThirdOrder.get_third_list()
    return res


# 华宇嘟嘟询价页面
@tools_blue.route('/tools/orderHyddIndex')
def order_hydd_index():
    return render_template('tools/order.html', name=session.get('username'))


# 华宇嘟嘟询价连接后台方法
@tools_blue.route('/tools/orderHydd', methods=['GET', 'POST'])
def order_hydd():
    env = request.values.get('env')
    order_code = request.values.get('order_code')
    dotype = request.values.get('dotype')
    bengin_adress = request.values.get('bengin_adress')
    end_adress = request.values.get('end_adress')
    carlengthtype = request.values.get('carlengthtype')
    global hydd_order
    try:
        if dotype == '1':
            res = HyddFlow(environment=env).hyddorder(carlengthtype, bengin_adress, end_adress)
            third_res = res[1]
            hydd_order = res[1]
            if res[0]['status']['code'] == 0:
                result = '询价成功'
            else:
                result = '询价失败'
            AddThirdOrder.create(session.get('username'), hydd_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderHydd', datetime.now(),
                                '华宇嘟嘟询价单')
            return third_res
        elif dotype == '2':
            res = HyddFlow(environment=env).hyddconfirm(order_code)
            if res['status']['code'] == 0:
                result = '华宇嘟嘟中标成功'
            else:
                result = '华宇嘟嘟中标成功失败'
            third_res = result
            AddThirdOrder.create(session.get('username'), hydd_order, env, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/orderHydd', datetime.now(),
                                '华宇嘟嘟询价单中标')
            return third_res
        else:
            return '异常错误！'
    except Exception as e:
        print(e)
        return "系统异常，请联系管理员"


# 华宇嘟嘟询价数据入库
@tools_blue.route('/tools/getOrderHyddList', methods=['GET', 'POST'])
def get_hydd_list():
    res = AddThirdOrder.get_third_list()
    return res


# 孙竹叶-司机所有运单卸货完成
@tools_blue.route('/tools/driverOrdersDoneIndex')
def dirver_orders_done_index():
    return render_template('tools/order.html', name=session.get('username'))


# 孙竹叶-司机所有运单卸货完成
@tools_blue.route('/tools/driverOrdersDone', methods=['GET', 'POST'])
def dirver_orders_done():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    res, num = driver_orders_done(env=env, driver_mobile=driver_mobile)
    DriverOrdersDone.create(session.get('username'), driver_mobile, datetime.now(), env, res, num)
    stat.Operate.create(session.get('username'), '/tools/driverOrdersDone', datetime.now(),
                        '司机所有运单卸货完成')
    return res


# 孙竹叶-司机所有运单卸货完成
@tools_blue.route('/tools/getDriverOrdersDoneList', methods=['GET', 'POST'])
def driver_orders_list():
    res = DriverOrdersDone.get_driver_orders_list()
    return res


# 孙竹叶-运单产生时效轨迹扣款首页
@tools_blue.route('/tools/orderLessMoneyIndex')
def order_less_money_index():
    return render_template('tools/order.html', name=session.get('username'))


# 孙竹叶-运单产生时效轨迹扣款
@tools_blue.route('/tools/orderLessMoney', methods=['GET', 'POST'])
def order_less_money_do():
    order_sn = request.values.get('order_sn')
    env = request.values.get('env')
    pay_type = request.values.get('pay_type')
    operate_type = request.values.get('type')
    res = order_money_less(order_sn, env, pay_type)
    OrderLessMoney.create(session.get('username'), env, order_sn, res, datetime.now(), operate_type)
    stat.Operate.create(session.get('username'), '/tools/orderLessMoney', datetime.now(),
                        '运单产生时效轨迹扣款')
    return res


# 孙竹叶-运单产生时效轨迹扣款列表
@tools_blue.route('/tools/getOrderLessMoneyList', methods=['GET', 'POST'])
def order_less_moneylist():
    res = OrderLessMoney.get_order_less_money_list('时效轨迹扣款')
    return res


# 孙竹叶-运单修改装卸货地址首页
@tools_blue.route('/tools/orderUpdateAddressIndex')
def order_update_address_index():
    return render_template('tools/order.html', name=session.get('username'))


# 孙竹叶-运单修改装卸货地址
@tools_blue.route('/tools/orderUpdateAddress', methods=['GET', 'POST'])
def order_update_address_do():
    order_sn = request.values.get('order_sn')
    env = request.values.get('env')
    is_long = request.values.get('is_long')
    has_stop = request.values.get('has_stop')
    operate_type = request.values.get('type')
    res = order_update_address(order_sn, env, is_long, has_stop)
    OrderLessMoney.create(session.get('username'), env, order_sn, res, datetime.now(), operate_type)
    stat.Operate.create(session.get('username'), '/tools/orderUpdateAddress', datetime.now(),
                        '运单修改装卸货地址')
    return res


# 孙竹叶-运单修改装卸货地址列表
@tools_blue.route('/tools/getOrderUpdateAddress', methods=['GET', 'POST'])
def order_update_addresslist():
    res = OrderLessMoney.get_order_less_money_list('修改装卸货地址')
    return res


# 运单异常修改首页
@tools_blue.route('/tools/abnormalModifyIndex')
def abnormal_modify_index():
    return render_template('tools/abnormalModify.html', name=session.get('username'))


# 运单异常修改
@tools_blue.route('/tools/abnormalModify', methods=['GET', 'POST'])
def abnormal_modify():
    env = request.values.get('env')
    orderSn = request.values.get('orderSn')
    modify_reason = request.values.get('modifyReason')
    order_status = request.values.get('orderStatusModify')
    res = OrderAbnormalModifySet(env).order_abnormal_modify(orderSn, modify_reason, order_status)
    commit = res
    OrderAbnormalModify.create(session.get('username'), orderSn, env, order_status, modify_reason, commit,
                               create_time=datetime.now())
    stat.Operate.create(session.get('username'), '/tools/abnormalModify', datetime.now(), '运单异常修改')
    return res


# 运单异常修改操作记录
@tools_blue.route('/tools/getOrderAbnormalModifyList', methods=['GET', 'POST'])
def get_abnormal_modify_list():
    res = OrderAbnormalModify.abnormal_modify()
    return res


# 生成意向单页面
@tools_blue.route('/tools/createAllAutoQueryIndex')
def auto_query_index():
    return render_template('tools/order.html', name=session.get('username'))


# 操作意向单后台
@tools_blue.route('/tools/createAllAutoQuery', methods=['GET', 'POST'])
def all_auto_query():
    env = request.values.get('env')
    plandate = request.values.get('plandate')
    lineid = request.values.get('lineid')
    type = request.values.get('type')
    if lineid == '':
        lineid = '-'
    if plandate:
        plandate_stamp = int(time.mktime(time.strptime(plandate.replace('T', ' ') + ':00', "%Y-%m-%d %H:%M:%S")) * 1000)
    else:
        plandate_stamp = None
    try:
        if type == '1':
            res = AllAutoQuery(environment=env).all_auto_query(plandate=plandate_stamp)
            if '操作成功' in res:
                result = '意向单生成成功'
            elif 'TIMEOUT' in res:
                result = 'r1意向单生成成功'
            else:
                result = '意向单生成失败'
            res = result
            AddAutoQuery.create(session.get('username'), env, lineid, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/createAllAutoQuery', datetime.now(),
                                '批量生成意向单')
            return res
        else:
            res = AllAutoQuery(environment=env).lineid_auto_query(lineid, plandate=plandate_stamp)
            if '操作成功' in res:
                result = '意向单生成成功'
            else:
                result = '意向单生成失败'
            res = result
            AddAutoQuery.create(session.get('username'), env, lineid, result, datetime.now())
            stat.Operate.create(session.get('username'), '/tools/createIdAutoQuery', datetime.now(),
                                '按线路id生成意向单')
            return res
    except Exception:
        return "系统异常，请联系管理员"


# 生成意向单入库
@tools_blue.route('/tools/getAutoQueryList', methods=['GET', 'POST'])
def get_auto_query_list():
    res = AddAutoQuery.get_auto_query_list()
    return res


# 智能调度派车开关操作记录
@tools_blue.route('/tools/getScheduleSwitchList', methods=['GET', 'POST'])
def get_schedule_switch_list():
    return ScheduleSwitch.get_schedule_switch_list()


# 智能调度派车开关页面
@tools_blue.route('/tools/scheduleSwitchIndex')
def get_schedule_switch_index():
    return render_template('tools/order.html', name=session.get('username'))


# 智能调度派车开关
@tools_blue.route('/tools/scheduleSwitch', methods=['GET', 'POST'])
def schedule_switch_res():
    env = request.values.get('env')
    opt_type = request.values.get('opt_type')
    print('env', env)
    print('opt_type', opt_type)
    if env != "" and opt_type != "":
        res = schedule_switch.schedule_switch(env, opt_type)
        print('res', res)
        ScheduleSwitch.create(session.get('username'), env, opt_type, res, datetime.now())
        msg = '智能调度：%s' % opt_type
        stat.Operate.create(session.get('username'), '/tools/scheduleSwitch', datetime.now(), msg)
        return res
    else:
        return "环境或者操作类型为空！"


# 指定运单生成页面
@tools_blue.route('/tools/appointOrderIndex')
def appoint_order_index():
    return render_template('tools/order.html', name=session.get('username'))


# 指定运单生成操作记录
@tools_blue.route('/tools/getAppointOrderList', methods=['GET', 'POST'])
def get_appoint_order_list():
    res = AppointOrderInfo.get_appoint_order_list()
    return res


# 指定运单生成
@tools_blue.route('/tools/appointOrder', methods=['GET', 'POST'])
def appoint_order_res():
    global order_res
    env = request.values.get('env')
    appoint_order_type = request.values.get('appoint_order_type')
    appoint_order_status = request.values.get('appoint_order_status')
    appoint_transfer_type = request.values.get('appoint_transfer_type')
    appoint_order_offline_pay = request.values.get('appoint_order_offline_pay')
    auto_query_create_time = request.values.get('auto_query_create_time')
    if auto_query_create_time:
        auto_query_create_time = int(time.mktime(time.strptime(auto_query_create_time.replace('T', ' ') + ':00', "%Y-%m-%d %H:%M:%S")) * 1000)
    else:
        auto_query_create_time = None
    if env != "" and appoint_order_type != "" and appoint_order_status != "" and appoint_transfer_type != "":
        # order_appoint = AppointOrder(env, appoint_order_status, appoint_transfer_type, appoint_order_offline_pay)
        # 项目货订单
        if appoint_order_type == "22":
            appoint_order_offline_pay = "off"  # 项目货订单为合同结算，不走线下支付
            order_appoint = AppointOrder(env, appoint_order_status, appoint_transfer_type, appoint_order_offline_pay)
            if appoint_order_status == "1" or appoint_order_status == "2":
                order_res = "项目货订单自动审核和报价！"
            else:
                order_res = order_appoint.project_order_appoint()
        # 图灵订单
        elif appoint_order_type == "21":
            order_appoint = AppointOrder(env, appoint_order_status, appoint_transfer_type, appoint_order_offline_pay)
            order_res = order_appoint.turing_order_appoint()
        # 25-意向单
        elif appoint_order_type == "25":
            order_appoint = AppointOrder(env, appoint_order_status, appoint_transfer_type, appoint_order_offline_pay)
            order_res = order_appoint.auto_query_order_appoint(auto_query_create_time)
        # 26-计划项目货订单
        elif appoint_order_type == "26":
            order_res = "计划项目货订单暂不支持！"
        # 28-吸货订单
        elif appoint_order_type == "28":
            order_appoint = AppointOrder(env, appoint_order_status, appoint_transfer_type, appoint_order_offline_pay)
            order_res = order_appoint.ai_order_appoint()
        # 从配置文件获取运单类型
        appoint_order_type_str = get_config("appoint_order", "appoint_order_type")
        appoint_order_type_value = json.loads(appoint_order_type_str)[appoint_order_type]
        # 从配置文件获取运单状态
        appoint_order_status_str = get_config("appoint_order", "appoint_order_status")
        appoint_order_status_value = json.loads(appoint_order_status_str)[appoint_order_status]
        # 从配置文件获取运力类型
        appoint_transfer_type_str = get_config("appoint_order", "appoint_transfer_type")
        appoint_transfer_type_value = json.loads(appoint_transfer_type_str)[appoint_transfer_type]

        AppointOrderInfo.create(session.get('username'), env, appoint_order_type_value, appoint_transfer_type_value,
                                appoint_order_status_value, appoint_order_offline_pay, auto_query_create_time, order_res, datetime.now())
        msg = '指定运单生成，环境：%s，运单类型：%s，运单状态：%s，运力类型：%s' % (env, appoint_order_type_value, appoint_order_status_value, appoint_transfer_type_value)
        stat.Operate.create(session.get('username'), '/tools/appointOrder', datetime.now(), msg)
        return order_res
    else:
        return "环境或者运单类型或运力类型或运单状态为空！"


# 运单指定操作页面
@tools_blue.route('/tools/operateOrderIndex')
def operate_order_index():
    return render_template('tools/order.html', name=session.get('username'))


# 运单指定操作记录
@tools_blue.route('/tools/getOperateAppointOrderList', methods=['GET', 'POST'])
def get_operate_order_list():
    res = OperateOrder.get_operate_order_list()
    return res


# 运单指定操作
@tools_blue.route('/tools/operateAppointOrder', methods=['GET', 'POST'])
def operate_order_res():
    env = request.values.get('env')
    operate_appoint_order_sn = request.values.get('operate_appoint_order_sn')
    operate_appoint_order_status = request.values.get('operate_appoint_order_status')

    if env != "" and operate_appoint_order_sn != "" and operate_appoint_order_status != "":
        # 项目货订单
        appoint_order_offline_pay = "off"  # 项目货订单为合同结算，不走线下支付
        operate_appoint_order = OperateAppointOrder(env, operate_appoint_order_sn, int(operate_appoint_order_status))
        operate_order = operate_appoint_order.operate_order()
        if 'status' in operate_order:
            if 'desc' in operate_order['status']:
                operate_order = operate_order['status']['desc']

        # 从配置文件获取运单指定操作状态
        operate_appoint_order_status_str = get_config("appoint_order", "operate_appoint_order_status")
        operate_appoint_order_status_value = json.loads(operate_appoint_order_status_str)[operate_appoint_order_status]

        OperateOrder.create(session.get('username'), env, operate_appoint_order_sn, operate_appoint_order_status_value,
                            operate_order, datetime.now())
        msg = '指定运单生成，环境：%s，运单类型：%s，运单状态：%s' % (env, operate_appoint_order_sn, operate_appoint_order_status_value,)
        stat.Operate.create(session.get('username'), '/tools/operateAppointOrder', datetime.now(), msg)
        return operate_order
    else:
        return "环境或运单号或指定运单状态为空！"
