#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session

# models位置
from app.algorithm.models.fchat_model import *

# feature

from app.algorithm.feature.fchat_algorithm import *

# 导入蓝本 main
from app.algorithm import algorithm_blue
from app.stat.models import stat


# 算法相关
@algorithm_blue.route('/algorithm/fchatIndex')
def algorithm_index():
    return render_template('algorithm/fchat.html', name=session.get('username'))







