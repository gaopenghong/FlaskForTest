# -*- coding: utf-8 -*-
#__author__ = 'liuchunfu'
#__time__   = '2018/4/3'
# __init__.py:导入包时即导入此文件,这样导入这个目录下的module
# 蓝图的作用:将应用程序组织成不同的组件,站点中每一个独立的区域(比如功能)也可以在代码上隔绝开来,最终将应用程序依据许多能完成单一任务的小应用组织起来
# main包下除__init__.py除外,auth.py、errors、view都是一个蓝图,在__init__.py文件中,加载这些蓝图并在flask()对象中注册
# 引入蓝图,所有url_for的用法要注意

from flask import Blueprint
stat_blue = Blueprint('stat', __name__, static_folder='static', template_folder='templates')
from . import views

if __name__ == '__main__':
    print(stat_blue.root_path)
