#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5


from flask import render_template, request, session
# model
from app.tools.models import server_model, server_im_model

# feature
from app.tools.feature import service_task_deal
from app.tools.feature.service_deal import *
from app.tools.feature.batch_add_configure_words import *
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from datetime import datetime


# 服务系统相关
@tools_blue.route('/tools/serverIndex')
def server_index():
    return render_template('tools/server.html', name=session.get('username'))


@tools_blue.route('/tools/getServiceTaskCheckist', methods=['GET', 'POST'])
def get_service_task_check_list():
    return server_model.ServiceDb.get_service_list()


# 任务无法被分配原因查询
@tools_blue.route('/tools/taskcheck', methods=['GET', 'POST'])
def task_check():
    user_mobile = request.values.get('user_mobile')
    task_id = request.values.get('task_id')
    env = request.values.get('env')
    res = ServiceDeal(env).task_not_to_allocate_check( user_mobile, task_id)
    server_model.ServiceDb.create(session.get('username'), user_mobile, datetime.now(), env, res, '任务无法被分配原因查询')
    stat.Operate.create(session.get('username'), '/tools/taskcheck', datetime.now(),
                        '任务无法被分配原因查询')
    return res


@tools_blue.route('/tools/getServiceTaskorWrkordDealList', methods=['GET', 'POST'])
def get_service_taskorwrkord_deal_list():
    return server_model.ServiceDb.get_service_list()


# 清空列表（工单/任务）
@tools_blue.route('/tools/taskOrWrkordAllDeal', methods=['GET', 'POST'])
def task_wrkord_all_deal():
    user_mobile = request.values.get('user_mobile2')
    deal_type = request.values.get('deal_type')
    method_type = request.values.get('method_type')
    env = request.values.get('env2')
    res = ServiceDeal(env).task_or_wrkord_all_deal(user_mobile, deal_type, method_type)
    server_model.ServiceDb.create(session.get('username'), user_mobile, datetime.now(), env, res, '清空列表（工单/任务）')
    stat.Operate.create(session.get('username'), '/tools/taskOrWrkordAllDeal', datetime.now(),
                        '清空列表（工单/任务）')
    return res


@tools_blue.route('/tools/getServiceTaskCreateDtaList', methods=['GET', 'POST'])
def get_service_task_create_data_list():
    return server_model.ServiceCreate.get_service_list()


# 生成任务
@tools_blue.route('/tools/taskCreateData', methods=['GET', 'POST'])
def task_create():
    order_sn = request.values.get('order_sn')
    task_type_id = request.values.get('task_type_id')
    env = request.values.get('env3')
    print(order_sn, task_type_id, env)
    res = ServiceDeal(env).task_create_data(order_sn, task_type_id)
    server_model.ServiceCreate.create(session.get('username'), order_sn, task_type_id, datetime.now(), env, res)
    stat.Operate.create(session.get('username'), '/tools/taskCreateData', datetime.now(), '生成任务')
    return res

# 批量创建(敏感词/违禁词)
@tools_blue.route('/tools/taskImCreateData', methods=['GET', 'POST'])
def task_im_create():
    print("获取页面数据.........")
    word_name = request.values.get('word_name')
    task_im_type_id = request.values.get('task_im_type_id')
    env = request.values.get('env4')
    num = request.values.get('num')
    user_mobile = request.values.get('user_mobile4')
    print(word_name, num, task_im_type_id, env, user_mobile)
    res = BatchOperationSensitiveWords(env).batch_add_words_1(word_name, num, task_im_type_id)
    print("res:", res)
    # 创建数据库表数据
    server_im_model.ServiceImCreate.create(session.get('username'), word_name, task_im_type_id, datetime.now(), env, res)
    stat.Operate.create(session.get('username'), '/tools/taskImCreateData', datetime.now(), '批量创建违禁词/敏感词')

# 不同角色批量创建(会话标签)
@tools_blue.route('/tools/taskImCreateTagData', methods=['GET', 'POST'])
def task_im_tag_create():
    print("获取页面数据.........")
    tag_name = request.values.get('tag_name')
    task_im_role = request.values.get('task_im_role')
    env = request.values.get('env5')
    num = request.values.get('num')
    user_mobile = request.values.get('user_mobile4')
    print(tag_name, num, task_im_role, env, user_mobile)
    res = BatchOperationSensitiveWords(env).batch_add_words_2(task_im_role, tag_name, num)
    print("res:", res)
    server_im_model.ServiceImTagCreate.create(session.get('username'), tag_name, task_im_role, datetime.now(), env, res)
    stat.Operate.create(session.get('username'), '/tools/taskImCreateTagData', datetime.now(), '不同角色批量创建标签')

# 不同角色批量创建(快捷回复)
@tools_blue.route('/tools/taskImCreateQrData', methods=['GET', 'POST'])
def task_im_qr_create():
    print("获取页面数据.........")
    tag_name = request.values.get('tag_name')
    task_im_role = request.values.get('task_im_role')
    env = request.values.get('env6')
    num = request.values.get('num')
    user_mobile = request.values.get('user_mobile4')
    print(tag_name, num, task_im_role, env, user_mobile)
    res = BatchOperationSensitiveWords(env).batch_add_words_3(task_im_role, tag_name, num)
    print("res:", res)
    server_im_model.ServiceImTagCreate.create(session.get('username'), tag_name, task_im_role, datetime.now(), env, res)
    stat.Operate.create(session.get('username'), '/tools/taskImCreateQrData', datetime.now(), '不同角色批量创建快捷回复')

# 获取创建快捷回复返回数据
@tools_blue.route('/tools/getImServiceCreateQrList', methods=['GET', 'POST'])
def get_im_service_create_qr():
    return server_im_model.ServiceImTagCreate.get_service_list()


# 获取创建标签返回数据
@tools_blue.route('/tools/getImServiceCreateTagList', methods=['GET', 'POST'])
def get_im_service_create_tag():
    return server_im_model.ServiceImTagCreate.get_service_list()

# 获取创建敏感词返回数据
@tools_blue.route('/tools/getImServiceCreateWordList', methods=['GET', 'POST'])
def get_im_service_create_word_list():
    return server_im_model.ServiceImCreate.get_service_list()


@tools_blue.route('/tools/task', methods=['GET', 'POST'])
def task():
    task_id = request.values.get('taskId')
    order_id = request.values.get('orderId')
    env = request.values.get('env')
    status = request.values.get('status')

    if task_id != "" or order_id != "":
        res = service_task_deal.task_deal(env, order_id, task_id, status)
        stat.Operate.create(session.get('username'), '/tools/task', datetime.now(),
                            '任务处理')
        # ServiceTask(operator, order_id, task_id, status, env, commit, create_time)
        server_model.ServiceTask.create(session.get('username'), order_id, task_id, status, env, res, datetime.now())
        return res
    else:
        return "处理fail"


# 任务处理列表
@tools_blue.route('/tools/getServiceTaskList')
def server_task():
    return server_model.ServiceTask.get_service_list()


