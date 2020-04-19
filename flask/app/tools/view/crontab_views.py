#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from typing import Union

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

import time
from flask import render_template, request, session, Flask
# models位置
from app.tools.models.crontab_model import CrontabInfo

# feature
from app.tools.feature.crontab_info import TaskInfo

# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat
from datetime import datetime


# app = Flask('__name__')
# ctx = app_context()
# ctx.push()

# 定时任务列表
@tools_blue.route('/tools/getCrontabList', methods=['GET', 'POST'])
def get_crontab_list():
    return CrontabInfo.get_crontab_list()


# 删除定时任务
@tools_blue.route('/tools/delCrontab', methods=['GET', 'POST'])
def del_crontab():
    task_id = request.values.get('task_id')
    # msg = '创建任务，名称：%s，类型：%s' % (run_name, run_type)
    # stat.Operate.create(session.get('use/rname'), '/tools/crontab', datetime.now(), msg)
    return CrontabInfo.del_crontab(task_id)

# 执行定时任务
@tools_blue.route('/tools/runCrontab', methods=['GET', 'POST'])
def run_crontab():
    task_id = request.values.get('task_id')
    run_date = request.values.get('run_date')
    run_time = request.values.get('run_time')
    start_week = request.values.get('start_week')
    end_week = request.values.get('end_week')
    robot_key = request.values.get('robot_key')
    run_name = request.values.get('run_name')
    job_content = request.values.get('job_content')
    run_type = request.values.get('run_type')

    a = TaskInfo(run_date, run_time, start_week, end_week, robot_key, run_name, job_content, run_type)
    CrontabInfo.run_crontab(task_id)
    return a.run_job()

# 定时任务页面
@tools_blue.route('/tools/crontabIndex')
def get_crontab_index():
    return render_template('tools/crontab.html', name=session.get('username'))


# 定时任务
@tools_blue.route('/tools/crontab', methods=['GET', 'POST'])
def crontab_res():
    run_name = request.values.get('run_name')
    run_type = request.values.get('run_type')

    run_date_year = request.values.get('run_date_year')
    run_date_month = request.values.get('run_date_month')
    run_date_day = request.values.get('run_date_day')
    run_date = None
    if run_date_year != "" and run_date_month != "" and run_date_day != "":
        run_date = run_date_year + "-" + run_date_month + "-" + run_date_day
        run_date = datetime.strptime(run_date, '%Y-%m-%d')
    else:
        run_date = run_date

    run_time_hour = request.values.get('run_time_hour')
    run_time_mint = request.values.get('run_time_mint')
    run_time_senc = request.values.get('run_time_senc')
    run_time = run_time_hour + ":" + run_time_mint + ":" + run_time_senc
    run_time = datetime.strptime(run_time, '%H:%M:%S')

    start_week = request.values.get('start_week')
    end_week = request.values.get('end_week')
    if start_week == "" or end_week == "":
        start_week = None
        end_week = None
    job_content = request.values.get('job_content')
    robot_key = request.values.get('robot_key')

    CrontabInfo.create(session.get('username'), run_name, run_type, run_date, run_time, start_week,
                       end_week, job_content, robot_key, datetime.now(), "close", datetime.now())
    msg = '创建任务，名称：%s，类型：%s' % (run_name, run_type)
    stat.Operate.create(session.get('use/rname'), '/tools/crontab', datetime.now(), msg)
    return "success"


if __name__ == "__main__":
    del_crontab()
