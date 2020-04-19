# -*- coding: utf-8 -*-
# __author__ = liuchunfu
# __time__   = 2019-09-02

from flask import Blueprint

algorithm_blue = Blueprint('algorithm', __name__, static_folder='static', template_folder='templates')
from . import views
# from .view import config_views
# # from .view import fchat_views