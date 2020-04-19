# -*- coding: utf-8 -*-
# __author__ = liuchunfu
# __time__   = 2019-09-02

from flask import Blueprint, Flask

tools_blue = Blueprint('tools', __name__, static_folder='static', template_folder='templates')
from . import views
from .view import driver_views
from .view import account_views
from .view import customer_views
from .view import finance_views
from .view import motorcade_views
from .view import order_views
from .view import server_views
from .view import crontab_views
from .view import oms_views
from .view import truck_views