#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '郭冰洁'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat

from app.tools.models.driver_model import *

from app.tools.feature import driver_white_list
from app.tools.feature.driver_bank_bind_card import *
from app.tools.feature.driver_dispatch_confirm_order import *
from app.tools.feature.driver_order_make_point import *
from app.tools.feature.driver_PayDeposit import *
from app.tools.feature.driver_white_drawing import *
from app.tools.feature.add_driver import *
from app.tools.feature.driver_fixedprice_arrangecancel import *
from app.tools.feature.driver_upload_receipt import *
from app.tools.feature.driver_upload_exception import *
from app.tools.feature.driver_dispatch_preconfirm import *
from app.tools.feature.driver_withdraw import *
from app.tools.feature.driver_dispatch_arrange import *
from app.tools.feature.driver_shortrent import *
from app.tools.feature.driver_create_and_order import *
from app.tools.feature.driver_handle_all_exception import *
from app.tools.feature.driver_status_order import *


# 司机首页
@tools_blue.route('/tools/driverIndex')
def driver_index():
    return render_template('tools/driver.html', name=session.get('username'))


@tools_blue.route('/tools/getDriverWhiteList', methods=['GET', 'POST'])
def get_driver_white_list():
    return AddDriverWhiteList.get_driver_white_list()


@tools_blue.route('/tools/driverWhiteListIndex')
def driver_white_list_index():
    return render_template('tools/driver.html', name=session.get('username'))


@tools_blue.route('/tools/driverWhiteList', methods=['GET', 'POST'])
def driver_white_list_opt():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    opt_type = request.values.get('opt_type')
    print('opt_type', opt_type)
    if env != "" and driver_mobile != "":
        if opt_type == "加入":
            res = driver_white_list.add_white_list(env, driver_mobile)
        elif opt_type == "移出":
            res = driver_white_list.del_white_list(env, driver_mobile)
        else:
            return "操作非法，类型%s不存在！" % opt_type
        AddDriverWhiteList.create(session.get('username'), driver_mobile, env, opt_type, res, datetime.now())
        msg = '司机%s人脸识别白名单' % opt_type
        stat.Operate.create(session.get('username'), '/tools/driverWhiteList', datetime.now(), msg)
        return res
    else:
        return "环境或者手机号为空！"


@tools_blue.route('/tools/driverPayDepositIndex')
def driver_PayDeposit_index():
    return render_template('tools/driverPayDeposit.html', name=session.get('username'))


@tools_blue.route('/tools/driverPayDeposit', methods=['GET', 'POST'])
def driver_paydeposit():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    opt_type = request.values.get('opt_type')
    if driver_mobile == "":
        print("手机号不能为空")
    elif opt_type == "抢单押金":
        res = PayDeposit(env).driver_PayDeposit(driver_mobile)
    else:
        res = PayDeposit(env).driver_linePayDeposit(driver_mobile, )
    DriverPayDeposit.create(session.get('username'), driver_mobile, env, res, opt_type, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driverPayDeposit', datetime.now(),
                        '交押金')
    return res


@tools_blue.route('/tools/getDriverPayDepositList', methods=['GET', 'POST'])
def driver_paydeposit_list():
    res = DriverPayDeposit.get_driverpaydeposit_list()
    return res


@tools_blue.route('/tools/DriverWhiteDrawingIndex', methods=['GET', 'POST'])
def driver_white_drawings_index():
    return render_template('tools/driverWhiteDrawing.html', name=session.get('username'))


@tools_blue.route('/tools/DriverWhiteDrawing', methods=['GET', 'POST'])
def driver_white_drawings():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    # opt_type = request.values.get('opt_type')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = WihteDrawing(env).driver_Wihte_Drawing(driver_mobile)
        DriverAbout.create("添加绑卡白名单", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/DriverWhiteDrawing', datetime.now(),
                            '添加绑卡白名单')
    return res


@tools_blue.route('/tools/getDriverWhiteDrawingList', methods=['GET', 'POST'])
def driver_white_drawings_list():
    res = DriverAbout.get_driverabout_list("添加绑卡白名单")
    return res


@tools_blue.route('/tools/driverBankBindCardIndex')
def driver_bankbindcard_index():
    return render_template('tools/driverBankBindCard.html', name=session.get('username'))


@tools_blue.route('/tools/driverBankBindCard', methods=['GET', 'POST'])
def driver_bankbindcard():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    # opt_type = request.values.get('opt_type')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = bankBindCard(env).driver_bankBindCard(driver_mobile)
        DriverAbout.create("司机绑卡", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/driverBankBindCard', datetime.now(),
                            '添加绑卡')
    return res


@tools_blue.route('/tools/driverBankBindCardList', methods=['GET', 'POST'])
def driver_bankbindcard_list():
    res = DriverAbout.get_driverabout_list("司机绑卡")
    return res


@tools_blue.route('/tools/driverDispatchConfirmOrderIndex')
def driver_dispatch_confirm_order_index():
    return render_template('tools/driverDispatchConfirmOrder.html', name=session.get('username'))


@tools_blue.route('/tools/driverDispatchConfirmOrder', methods=['GET', 'POST'])
def driver_dispatch_confirm_order():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    dispatch_mobile = request.values.get('dispatch_mobile')
    opt_type = request.values.get('opt_type')
    print(opt_type)
    if driver_mobile == "":
        print("手机号不能为空")
    elif opt_type == "符合":
        res = DispatchArrangeDriver(env).driver_Dispatch_Arrange_Driver(driver_mobile, dispatch_mobile)
    else:
        res = FixedpriceArrangecancel(env).driver_Fixedprice_Arrangecancel(driver_mobile, dispatch_mobile)
    DriverDispatchConfirmOrder.create(session.get('username'), driver_mobile, env, res, opt_type, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driverDispatchConfirmOrder', datetime.now(),
                        '调度确认司机')
    return res


@tools_blue.route('/tools/driverDispatchConfirmOrderList', methods=['GET', 'POST'])
def driver_dispatch_confirm_order_list():
    res = DriverDispatchConfirmOrder.get_dispatchconfirmorder_list()
    return res


@tools_blue.route('/tools/driverOrderMakePointIndex')
def driver_order_make_point_index():
    return render_template('tools/driverOrderMakepoint.html', name=session.get('username'))


@tools_blue.route('/tools/driverOrderMakePoint', methods=['GET', 'POST'])
def driver_order_make_point():
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = orderMakePointAll(env).driver_order_make_point_all(order_sn, driver_mobile)
        DriverAbout.create("运单打点", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/driverOrderMakePoint', datetime.now(),
                            '运单打点')
    return res


@tools_blue.route('/tools/driverOrderMakePointList', methods=['GET', 'POST'])
def driver_order_make_point_list():
    res = DriverAbout.get_driverabout_list("运单打点")
    return res


# 郭冰洁--好运测试数据
@tools_blue.route('/tools/addDriverIndex')
def add_driver_index_test():
    return render_template('tools/addDriver.html', name=session.get('username'))


@tools_blue.route('/tools/addDrivertest', methods=['GET', 'POST'])
def addDriver_test():
    number = request.values.get('number')
    print(number)
    env = request.values.get('env')
    start = request.values.get('start')
    opt_type = request.values.get('opt_type')
    driver_status = request.values.get('driver_status')
    truck_status = request.values.get('truck_status')
    print(opt_type)
    if opt_type == "相同":
        res = AddDriver(env).add_driver_3(number, start, int(driver_status), int(truck_status))
    elif opt_type == "不同":
        res = AddDriver(env).add_driver_2(number)
    AddDriverTest.create(session.get('username'), number, env, res, opt_type, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/addDrivertest', datetime.now(),
                        '注册司机')
    return res


@tools_blue.route('/tools/addDrivertestlist', methods=['GET', 'POST'])
def add_driver_list_test():
    print(123)
    res = AddDriverTest.get_driver_list()
    return res


@tools_blue.route('/tools/uploadReceiptIndex')
def driver_uploadReceipt_index():
    return render_template('tools/uploadReceipt.html', name=session.get('username'))


@tools_blue.route('/tools/uploadReceipt', methods=['GET', 'POST'])
def driver_uploadReceipt():
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = UploadReceipt(env).driver_upload_receipt(order_sn, driver_mobile)
        DriverAbout.create("司机回单上传", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/uploadReceipt', datetime.now(),
                            '司机回单上传')
    return res


@tools_blue.route('/tools/uploadReceiptlist', methods=['GET', 'POST'])
def driver_uploadReceipt_list():
    res = DriverAbout.get_driverabout_list("司机回单上传")
    return res


@tools_blue.route('/tools/uploadExceptionIndex')
def driver_uploadException_index():
    return render_template('tools/uploadException.html', name=session.get('username'))


@tools_blue.route('/tools/uploadException', methods=['GET', 'POST'])
def driver_uploadException():
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = uploadException(env).driver_upload_Exception(order_sn, driver_mobile)
        DriverAbout.create("司机举证上传", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/uploadException', datetime.now(),
                            '司机举证上传')
    return res


@tools_blue.route('/tools/uploadExceptionlist', methods=['GET', 'POST'])
def driver_uploadException_list():
    res = DriverAbout.get_driverabout_list("司机举证上传")
    return res


@tools_blue.route('/tools/driver_dispatchpreConfirmIndex')
def driver_dispatchpreConfirm_index():
    return render_template('tools/dispatchpreConfirm.html', name=session.get('username'))


@tools_blue.route('/tools/dispatchpreConfirm', methods=['GET', 'POST'])
def driver_dispatchpreConfirm():
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    dispatch_mobile = request.values.get('dispatch_mobile')
    env = request.values.get('env')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = DispatchPreconfirm(env).driver_dispatch_Preconfirm(order_sn, driver_mobile, dispatch_mobile)
        DriverAbout.create("调度确认运单", session.get('username'), driver_mobile, env, str(res), datetime.now())
    stat.Operate.create(session.get('username'), '/tools/dispatchpreConfirm', datetime.now(),
                        '调度确认运单')
    return res


@tools_blue.route('/tools/dispatchpreConfirmlist', methods=['GET', 'POST'])
def driver_dispatchpreConfirm_list():
    res = DriverAbout.get_driverabout_list("调度确认运单")
    return res


@tools_blue.route('/tools/driver_WithDrawIndex')
def driver_withdraw_index():
    return render_template('tools/WithDraw.html', name=session.get('username'))


@tools_blue.route('/tools/driver_WithDraw', methods=['GET', 'POST'])
def driver_withdraw():
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    opt_type = request.values.get('opt_type')
    if driver_mobile == "":
        print("手机号不能为空")
    elif opt_type == "运费":
        res = Withdraw(env).driver_Withdraw(driver_mobile)
        DriverWithDraw.create(session.get('username'), driver_mobile, env, res, opt_type, datetime.now())
    else:
        res = Withdraw(env).driver_activity_withdraw(driver_mobile)
        DriverWithDraw.create(session.get('username'), driver_mobile, env, res, opt_type, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driver_WithDraw', datetime.now(),
                        '司机提款')
    return res


@tools_blue.route('/tools/driver_WithDrawlist', methods=['GET', 'POST'])
def driver_withdraw_list():
    res = DriverWithDraw.driver_withdraw_list()
    return res


@tools_blue.route('/tools/driverDispatchArrangeIndex')
def driver_dispatch_arrange_index():
    return render_template('tools/driverDispatchArrange.html', name=session.get('username'))


@tools_blue.route('/tools/driverDispatchArrange', methods=['GET', 'POST'])
def driver_dispatch_arrange():
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    env = request.values.get('env')
    if driver_mobile == "":
        print("手机号不能为空")
    else:
        res = DispatchArrangedirect(env).driver_Dispatch_Arrange_direct(order_sn, driver_mobile)
        DriverAbout.create("直接安排司机", session.get('username'), driver_mobile, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/driverDispatchArrange', datetime.now(),
                            '直接安排司机')
    return res


@tools_blue.route('/tools/driverDispatchArrangeList', methods=['GET', 'POST'])
def driver_dispatch_arrange_list():
    res = DriverAbout.get_driverabout_list("直接安排司机")
    return res


@tools_blue.route('/tools/driverShortRentIndex')
def driver_shortrent_index():
    return render_template('tools/driverShortRent.html', name=session.get('username'))


@tools_blue.route('/tools/driverShortRent', methods=['GET', 'POST'])
def driver_shortrent():
    start_provincename = request.values.get('start_provincename')
    start_cityname = request.values.get('start_cityname')
    end_provincename = request.values.get('end_provincename')
    end_cityname = request.values.get('end_cityname')
    env = request.values.get('env')
    address = start_provincename + "-" + start_cityname + "-" + end_provincename + "-" + end_cityname
    if start_provincename == "" or start_cityname == "" or end_provincename == "" or end_cityname == "":
        print("始末省市均不能未空")
    else:
        res = ShortRent(env).driver_ShortRent(start_provincename, start_cityname, end_provincename, end_cityname)
        DriverShortRent.create(session.get('username'), address, env, res, datetime.now())
        stat.Operate.create(session.get('username'), '/tools/driverShortRent', datetime.now(),
                            '日包车')
    return res


@tools_blue.route('/tools/driverShortRentList', methods=['GET', 'POST'])
def driver_shortrent_list():
    res = DriverShortRent.get_driver_shortrent_list()
    return res


@tools_blue.route('/tools/driverCreateAndOrderIndex')
def driver_driver_create_and_order_index():
    return render_template('tools/driverCreateAndOrder.html', name=session.get('username'))


@tools_blue.route('/tools/driverCreateAndOrder', methods=['GET', 'POST'])
def driver_create_and_order():
    number = request.values.get('number')
    env = request.values.get('env')
    start = request.values.get('start')
    lineid = request.values.get('lineid')
    res = TestCreateAndOrder(env).quote_by_line_id(number, start, lineid)
    DriverCreateAndOrder.create(session.get('username'), number, env, res, lineid, "承运中",datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driverCreateAndOrder', datetime.now(),
                        '新建有承运中单子的司机')
    return res


@tools_blue.route('/tools/driverCreateAndOrderList', methods=['GET', 'POST'])
def driver_driver_create_and_order_list():
    res = DriverCreateAndOrder.get_driver_create_and_order_list()
    return res


@tools_blue.route('/tools/driver_handle_all_exception_index')
def driver_handle_all_exception_index():
    return render_template('tools/dispatchpreConfirm.html', name=session.get('username'))


@tools_blue.route('/tools/driver_handle_all_exception', methods=['GET', 'POST'])
def driver_handleallexception():
    order_sn = request.values.get('order_sn')
    env = request.values.get('env')
    if order_sn == "":
        print("单号不可为空")
    else:
        res = DriverAllException(env).driver_all_exception(order_sn)
        DriverHandleAllexception.create(session.get('username'), order_sn, env, res, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driver_handle_all_exception', datetime.now(),
                        '一键处理所有异常')
    return res


@tools_blue.route('/tools/driver_handle_all_exception_list', methods=['GET', 'POST'])
def driver_handleallexception_list():
    res = DriverHandleAllexception.get_driver_handle_all_exception_list()
    return res


@tools_blue.route('/tools/driverStatusOrderIndex')
def driver_status_order_index():
    return render_template('tools/driverStatusOrder.html', name=session.get('username'))


@tools_blue.route('/tools/driverStatusOrder', methods=['GET', 'POST'])
def driver_status_order():
    mobile = request.values.get('mobile')
    env = request.values.get('env')
    start = request.values.get('start')
    lineid = request.values.get('lineid')
    status=request.values.get('status')
    type_exits = request.values.get('type')
    print(type_exits,type(type_exits))
    if type_exits == "1":
        res = TestDriverStatusOrder(env,type_exits,start,lineid).driver_status_order(status)
    elif type_exits == "2":
        res = TestDriverStatusOrder(env,type_exits,mobile,lineid).driver_status_order(status)
    DriverCreateAndOrder.create(session.get('username'), 1,env, res, lineid, status,datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driverCreateAndOrder', datetime.now(),
                        '运单状态')
    print(res)
    return res


@tools_blue.route('/tools/driverStatusOrderList', methods=['GET', 'POST'])
def driver_status_order_list():
    res = DriverCreateAndOrder.get_driver_create_and_order_list()
    return res
