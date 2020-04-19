#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2018 / 8 / 17

from flask import Blueprint
oauth_blue = Blueprint('oauth', __name__, static_folder='static', template_folder='templates')
# view 是itest环境登陆使用
from . import views
# views_test 是本地登陆使用
# from . import views_bak
# from . import views_test
