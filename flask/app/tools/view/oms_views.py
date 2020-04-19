#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5


from flask import render_template, request, session
# 导入蓝本 main
from .. import tools_blue
from app.tools.models.oms_models import *
from app.tools.feature.oms_advertisin_position import *


# 运营首页
@tools_blue.route('/tools/omsIndex')
def oms_index():
    return render_template('tools/oms.html', name=session.get('username'))


# 运营广告页
@tools_blue.route('/tools/omsAdsIndex')
def oms_ads_index():
    return render_template('tools/oms.html', name=session.get('username'))


# 创建好运广告位
@tools_blue.route('/tools/createOmsPosition', methods=['GET', 'POST'])
def create_driver_home_page_shuffling_figure():
    env = request.values.get('env')
    app_type = request.values.get('app_type')
    type_id = request.values.get('type_id')
    title = request.values.get('title')
    link_url = request.values.get('link_url')
    pic_url = request.values.get('pic_url')
    rank = request.values.get('rank')
    print(env, app_type, type_id, title, link_url, pic_url, rank)
    res = teds(env, int(app_type), int(type_id), title, link_url, pic_url, int(rank))
    CreateOmsTestData.create(session.get('username'), env, app_type, type_id, title, link_url,  pic_url, rank)
    return res


@tools_blue.route('/tools/selectOmsPositionTable', methods=['GET', 'POST'])
def get_select_check_banner_list():
    return CreateOmsTestData.select_check_banner_list()


# 运营ios提审配置
@tools_blue.route('/tools/omsIosIndex')
def oms_ios_index():
    return render_template('tools/oms.html', name=session.get('username'))


# 新增ios提审配置
@tools_blue.route('/tools/createIosConfig22', methods=['GET', 'POST'])
def create_ios_config():
    env = request.values.get('env')
    print(request.values)
    print(env)
    # return '123'
    customer_type = request.values.get('customer_type')
    dev_version = request.values.get('dev_version')
    host = request.values.get('host')
    remark = request.values.get('remark')
    # admin_name = request.values.get('adminName')
    print(env, customer_type, dev_version, host, remark)
    res = ios_config(env, customer_type, dev_version, host, remark)
    CreateIosTestData.create(session.get('username'), env, customer_type, dev_version, host, remark)
    return res


@tools_blue.route('/tools/selectIosConfigTable', methods=['GET', 'POST'])
def get_select_ios_config_list():
    return CreateIosTestData.select_ios_config_list()
