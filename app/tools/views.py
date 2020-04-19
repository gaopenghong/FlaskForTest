#!/usr/bin/env python
# coding=utf-8

from flask import render_template, request, session

# models位置
from app.tools.models.env_model import Env
from app.tools.models.account_model import Accounts

# 导入蓝本 main
from . import tools_blue
from ..stat.models import stat
from datetime import datetime


@tools_blue.route('/tools/getEnvList', methods=['GET', 'POST'])
def get_env_list():
    res = Env.get_env_list()
    return res


@tools_blue.route('/tools/getAccounttest', methods=['GET', 'POST'])
def get_account_test():
    type = request.values.get('type')
    return Accounts.get_account_by_type(type)



