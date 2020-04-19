#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session
from app.tools.models.account_model import Accounts
from app.tools.feature.motorcade_register import MotorcadeRegister
from app.tools.feature import add_administrator, add_truck_driver
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from datetime import datetime


# 账号相关
@tools_blue.route('/tools/accountIndex')
def account_index():
    return render_template('tools/account.html', name=session.get('username'))


@tools_blue.route('/tools/getAccountList', methods=['GET', 'POST'])
def get_account_list():
    print(123)
    return Accounts.get_account_list()


@tools_blue.route('/tools/createAccount', methods=['GET', 'POST'])
def create_account():
    name = request.values.get('name')
    mobile = request.values.get('mobile')
    type = request.values.get('type')
    environment = request.values.get('environment')
    is_change = request.values.get('is_change')
    if mobile != "":
        if type == '1':
            # res = add_administrator.add_all_admin(name, mobile)
            res = add_administrator.add_admin(environment, name, mobile)
            # operator, add_phone, add_time, commit, type, add_name=''
            # operator, add_phone, add_time, commit, type, environment
            user_id = add_administrator.ConfClass(environment=environment).get_conf_user_id(mobile)
            add_administrator.ConfClass(environment=environment).add_new_user_conf(user_id)
            Accounts.create(session.get('username'), mobile, datetime.now(), res, type, environment)
            stat.Operate.create(session.get('username'), '/tools/createAccount', datetime.now(),
                                '添加后台账号')
            return res
        elif type == '2':
            res = add_truck_driver.AddTruckDr(environment=environment, admin_mobile='16888888888',
                                              admin_password='Ab@123456789').add_truck_driver(mobile)
            print(res)
            Accounts.create(session.get('username'), mobile, datetime.now(), res, type, environment)
            stat.Operate.create(session.get('username'), '/tools/createAccount', datetime.now(),
                                '新建司机')
            return res
        elif type == '3':
            res = MotorcadeRegister(environment).register_agent(mobile, is_change)
            Accounts.create(session.get('username'), mobile, datetime.now(), res, type, environment)
            stat.Operate.create(session.get('username'), '/tools/agentRegister', datetime.now(),
                                '注册车队')
            return res
        elif type == '4':
            res = add_truck_driver.AddTruckDr(environment=environment, admin_mobile='16888888888',
                                              admin_password='Ab@123456789').drivers_truck_add(mobile)
            Accounts.create(session.get('username'), mobile, datetime.now(), res, type, environment)
            stat.Operate.create(session.get('username'), '/tools/agentRegister', datetime.now(),
                                '新建共建车司机')
            return res
    else:
        return "手机号不能为空"
