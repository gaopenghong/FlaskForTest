#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'hancheng'
__time__ = 2019 / 11 / 12

from flask import render_template, request, session
# model
from app.tools.models.truck_trailer_model import Truck
from app.tools.models.fy_driver_model import FyDriver

# feature
from app.tools.feature.truck_add_trailer import *
from app.tools.feature.fy_driver_accept import *

# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from datetime import datetime


# 专车相关
@tools_blue.route('/tools/truckIndex')
def truck_index():
    return render_template('tools/truck.html', name=session.get('username'))


@tools_blue.route('/tools/getTrailerList', methods=['GET', 'POST'])
def get_trailer_list():
    return Truck.get_trailer_list()


@tools_blue.route('/tools/addTrailer', methods=['GET', 'POST'])
def truck_add_trailer():
    env = request.values.get('env')
    plate_number = request.values.get('plate_number')
    res = TruckAddTrailer(environment=env, admin_mobile='16888888888',
                          admin_password='Ab@123456789').add_truck_trailer(plate_number)
    print(res)
    Truck.create(session.get('username'), datetime.now(), plate_number, res, env)
    stat.Operate.create(session.get('username'), '/tools/addTrailer', datetime.now(),
                        '新增挂箱')

    return res


# 共建司机接单
@tools_blue.route('/tools/fyDriverAccept', methods=['GET', 'POST'])
def fy_driver_accept():
    env = request.values.get('env')
    order_sn = request.values.get('order_sn')
    driver_mobile = request.values.get('driver_mobile')
    order_status = request.values.get('order_status')
    ao = FyDriverAcceptOrder(env, admin_mobile='16888888888', admin_password='Ab@123456789')
    commit = ao.fy_driver_accept(order_sn, driver_mobile, order_status)
    print(commit)
    FyDriver.create(session.get('username'), env, order_sn, driver_mobile, order_status,
                    commit, datetime.now())
    stat.Operate.create(session.get('username'), '/tools/fyDriverAccept', datetime.now(), '共建司机接单')
    return commit


# 共建司机接单操作记录
@tools_blue.route('/tools/getFyDriverList', methods=['GET', 'POST'])
def get_fy_driver_list():
    return FyDriver.get_fy_driver_list()
