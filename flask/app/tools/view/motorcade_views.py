#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.tools.feature.motorcade_contract import MotorcadeContract
from app.tools.feature.motorcade_create_fy_line import MotorcadeCreateFyLine
from app.tools.feature.motorcade_fy_driver_line import MotorcadeFyDriverLine
from app.tools.feature.motorcade_oms_push import MotorcadeOmsPush

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from datetime import datetime
from app.tools.feature.select_check_code import SelectCheckCode
from app.tools.models.motorcade_model import MotorcadeTestData
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from flask import request, render_template, session
from app.tools.feature.motorcade_create_test_data import MotorcadeCreateTestData


# 车队相关
@tools_blue.route('/tools/motorcadeIndex')
def motorcade_index():
    return render_template('tools/motorcade.html', name=session.get('username'))


# 造经纪人测试数据
@tools_blue.route('/tools/createMotorcadeTestData', methods=['GET', 'POST'])
def create_agent_test_data():
    env = request.values.get('env')
    admin_mobile = request.values.get('adminMobile')
    admin_password = request.values.get('adminPassword')
    customer_mobile = request.values.get('customerMobile')
    motorcade_mobile = request.values.get('motorcadeMobile')
    driver_mobile = request.values.get('driverMobile')
    start_place = request.values.get('startPlace')
    stop_place = request.values.get('stopPlace')
    end_place = request.values.get('endPlace')
    test_data = request.values.get('testData')
    receipt_check = request.values.get('receiptCheck')
    order_status = request.values.get('orderStatus')
    bill_status = request.values.get('billStatus')

    line_info_list = list()
    line_info_list.append(start_place)
    print(str(stop_place.split(',')))
    for place in stop_place.split(','):
        line_info_list.append(place)
    line_info_list.append(end_place)
    print(line_info_list)
    r = ''
    status = ''
    order_sn, bill_no = MotorcadeCreateTestData(env, admin_mobile, admin_password, motorcade_mobile, customer_mobile,
                                                driver_mobile).motorcade_create_test_data(line_info_list, test_data,
                                                                                          receipt_check, order_status,
                                                                                          bill_status)
    if test_data == '运单':
        r = "运单号:" + str(order_sn)
        status = order_status
    elif test_data == '月账单':
        status = bill_status
        r = "运单号:" + str(order_sn) + ",账号结算批次号:" + str(bill_no)

    MotorcadeTestData.create(session.get('username'), environment=env, customer_mobile=customer_mobile,
                             admin_mobile=admin_mobile, motorcade_mobile=motorcade_mobile,
                             driver_mobile=driver_mobile, start_place=start_place,
                             stop_place=stop_place, end_place=end_place, order_sn=order_sn, bill_no=bill_no,
                             test_data=test_data, status=status, operator_time=datetime.now(), function_name='车队主要测试数据')
    stat.Operate.create(session.get('username'), '/tools/createMotorcadeTestData', datetime.now(),
                        '创建车队测试数据')
    return r


@tools_blue.route('/tools/getMotorcadeTestDataList', methods=['GET', 'POST'])
def get_motorcade_test_data_list():
    return MotorcadeTestData.get_motorcade_data_list()


@tools_blue.route('/tools/selectCheckCode', methods=['GET', 'POST'])
def select_check_code():
    env = request.values.get('env')
    mobile = request.values.get('mobile')
    database_name = request.values.get('databaseName')
    code = SelectCheckCode(env).select_check_code(database_name, mobile)
    MotorcadeTestData.create(session.get('username'), environment=env, mobile=mobile, database_name=database_name,
                             code=code, operator_time=datetime.now(), function_name='查询验证码')
    stat.Operate.create(session.get('username'), '/tools/selectCheckCode', datetime.now(),
                        '查询验证码')
    return code


@tools_blue.route('/tools/selectCheckCodeList', methods=['GET', 'POST'])
def get_select_check_code_list():
    return MotorcadeTestData.select_check_code_list()


@tools_blue.route('/tools/createFyLine', methods=['GET', 'POST'])
def create_fy_line_view():
    env = request.values.get('env')
    admin_mobile = request.values.get('admin_mobile')
    admin_password = request.values.get('admin_password')
    line_route_id = request.values.get('line_route_id')
    transport_type = request.values.get('transport_type')
    mobile = request.values.get('mobile')
    line_id = MotorcadeCreateFyLine(env, admin_mobile=admin_mobile, admin_password=admin_password).create_fy_line(
        line_route_id, transport_type, mobile)
    MotorcadeTestData.create(session.get('username'), environment=env, admin_mobile=admin_mobile,
                             transport_type=transport_type, mobile=mobile, line_route_id=line_route_id,
                             line_id=line_id, operator_time=datetime.now(), function_name='创建福佑线路')
    stat.Operate.create(session.get('username'), '/tools/createFyLine', datetime.now(),
                        '创建福佑线路')
    return str(line_id)


@tools_blue.route('/tools/createFyLineList', methods=['GET', 'POST'])
def get_create_fy_line_list():
    return MotorcadeTestData.select_create_fy_line_list()


@tools_blue.route('/tools/createFyDriverTestData', methods=['GET', 'POST'])
def create_fy_driver_test_data():
    env = request.values.get('env')
    admin_mobile = request.values.get('adminMobile')
    admin_password = request.values.get('adminPassword')
    customer_mobile = request.values.get('customerMobile')
    start_place = request.values.get('startPlace')
    stop_place = request.values.get('stopPlace')
    end_place = request.values.get('endPlace')
    line_driver_status = request.values.get('lineDriverStatus')
    driver_mobiles = request.values.get('driverMobiles')
    line_info_list = list()
    line_info_list.append(start_place)
    print(str(stop_place.split(',')))
    for place in stop_place.split(','):
        line_info_list.append(place)
    line_info_list.append(end_place)
    print(line_info_list)
    r_json = ''
    try:
        motorcade_fy_driver_line = MotorcadeFyDriverLine(env, admin_mobile, admin_password, customer_mobile,
                                                         line_info_list)
    except Exception as e:
        print(e)
        r_json = "请确认账号/密码是否正确"
    else:
        driver_mobiles = driver_mobiles.split(',')
        print(driver_mobiles)
        r_json = motorcade_fy_driver_line.fy_driver_line(driver_mobiles, int(line_driver_status))
        line_driver_status_dict = {'1': '线路下添加司机', '2': '推送合同', '3': '签署合同', '4': '上报空车', '5': '承单', '6': '运单卸货完成',
                                   '7': '运单签收'}
        MotorcadeTestData.create(session.get('username'), environment=env, customer_mobile=customer_mobile,
                                 admin_mobile=admin_mobile, driver_mobile=str(driver_mobiles),
                                 start_place=start_place, stop_place=stop_place, end_place=end_place,
                                 status=line_driver_status_dict[line_driver_status],
                                 result=r_json, operator_time=datetime.now(), function_name='固定司机成单流程')
        stat.Operate.create(session.get('username'), '/tools/createFyDriverTestData', datetime.now(), '固定司机成单流程')
    finally:
        return str(r_json)


@tools_blue.route('/tools/fyDriverTestDataList', methods=['GET', 'POST'])
def get_fy_driver_data_list():
    return MotorcadeTestData.get_fy_driver_data_list()


@tools_blue.route('/tools/pushMessages', methods=['GET', 'POST'])
def push_messages():
    env = request.values.get('env')
    admin_mobile = request.values.get('adminMobile')
    admin_password = request.values.get('adminPassword')
    app_type = request.values.get('appType')
    msg_type = request.values.get('msgType')
    show_type = request.values.get('showType')
    img_type = request.values.get('imgType')
    motorcade_oms_push = MotorcadeOmsPush(env, admin_mobile, admin_password)
    if not motorcade_oms_push.cookies_ua:
        return "请确认账号/密码是否正确"
    r_json = ''
    try:
        r_json = motorcade_oms_push.push_messages(int(app_type), int(msg_type), int(show_type), int(img_type))
        print(r_json)
    except Exception as e:
        print(e)
    app_type_dict = {'1132': '好运APP', '3211': '车队APP', '2311': '专车APP', '3232': '共建车APP'}
    msg_type_dict = {'1': '系统消息', '2': '活动消息'}
    show_type_dict = {'3': '跳app首页', '1': '跳转指定链接'}
    img_type_dict = {'1': '有图片', '2': '无图片'}
    MotorcadeTestData.create(session.get('username'), environment=env, admin_mobile=admin_mobile,
                             app_type=app_type_dict[app_type],
                             msg_type=msg_type_dict[msg_type], show_type=show_type_dict[show_type],
                             img_type=img_type_dict[img_type], result=str(r_json),
                             operator_time=datetime.now(), function_name='消息推送')
    stat.Operate.create(session.get('username'), '/tools/pushMessages', datetime.now(), '消息推送')
    return str(r_json)


@tools_blue.route('/tools/pushMessagesList', methods=['GET', 'POST'])
def get_push_messages_list():
    return MotorcadeTestData.get_push_messages_list()


@tools_blue.route('/tools/motorcadeContract', methods=['GET', 'POST'])
def motorcade_contract():
    env = request.values.get('env')
    admin_mobile = request.values.get('adminMobile')
    admin_password = request.values.get('adminPassword')
    motorcade_mobile = request.values.get('motorcadeMobile')
    contract_status = request.values.get('contractStatus')
    r_json = ''
    contract = MotorcadeContract(env, admin_mobile, admin_password, motorcade_mobile)
    if not contract.cookies_ua:
        return "请确认账号/密码是否正确"
    try:
        r_json = contract.motorcade_contract_data(contract_status)
        contract_status_dict = {'1': '待签署', '2': '已撤回', '3': '已签署', '4': '已终止', '5': '已过期'}
        MotorcadeTestData.create(session.get('username'), environment=env, admin_mobile=admin_mobile,
                                 motorcade_mobile=motorcade_mobile, status=contract_status_dict[contract_status],
                                 result=str(r_json), operator_time=datetime.now(), function_name='车队合同')
        stat.Operate.create(session.get('username'), '/tools/motorcadeContract', datetime.now(), '车队合同')
    except Exception as e:
        print(e)
        r_json = e
    finally:
        return str(r_json)


@tools_blue.route('/tools/motorcadeContractList', methods=['GET', 'POST'])
def get_motorcade_contract_list():
    return MotorcadeTestData.get_motorcade_contract_list()
