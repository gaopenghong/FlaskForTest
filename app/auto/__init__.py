#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 11


from flask import Blueprint
auto_blue = Blueprint('auto_blue', __name__, static_folder='static', template_folder='templates')
from . import views

