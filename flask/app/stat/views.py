#!/usr/bin/env python
# coding=utf-8

from flask import render_template
from flask import session
# 导入蓝本 main
from . import stat_blue
from .models import stat


@stat_blue.route('/stat/index')
def index():
    return render_template('stat/stat.html', name=session.get('username'))


@stat_blue.route('/stat/getOperateList')
def get_operate_list():
    return stat.Operate.get_operate_list()
    # return render_template('stat/index.html', name=session.get('username'))
#
# @main.route('/test')
# def test():
#
#     return render_template('test.html', name=session.get('username'))

