# -*- coding: utf-8 -*-
# __author__ = 'liuchunfu'
# __time__   = '2018/4/3'

import socket
from datetime import timedelta
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


from config import config
import pymysql
pymysql.install_as_MySQLdb()

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
# app = Flask(__name__)
# app.config.from_object('config')
# db = SQLAlchemy(app)
db = SQLAlchemy(use_native_unicode="utf8")


def create_app(config_name):
    """
        desc = 将应用程序放入一个工厂函数延迟创建,使其动态地适应配置的更改,实现从脚本中显示调用
    :param config_name: [required] 传入用于应用程序的配置名称,配置被保存在config.py的一个类中,使用FLASK的app.config配置对象的
                from_object()方法来直接导入。配置对象可以从config字典中取出,一旦应用程序被创建并配置好,扩展就可以被初始化。调用扩展里的
                init_app之前
    :return:
    """
    # print(config_name)

    app = Flask('app', static_folder='static', template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    from .oauth import oauth_blue
    from .stat import stat_blue
    from .tools import tools_blue
    from .auto import auto_blue
    from .algorithm import algorithm_blue
    app.register_blueprint(main_blueprint)
    app.register_blueprint(oauth_blue)
    app.register_blueprint(stat_blue)
    app.register_blueprint(tools_blue)
    app.register_blueprint(auto_blue)
    app.register_blueprint(algorithm_blue)

    # 读入配置并启动开始,进入到app context,可以访问配置文件、资源文件、通过规则反向构造url
    with app.app_context():
        app.config.from_object(config[config_name])
        app.permanent_session_lifetime = timedelta(minutes=30)

        # from .model import db
        # db.init_app(app)  # 如果没有该语句就无法建立全局的db对象,导致无法容易的创建models,即使db = SQLAlchemy(app)也没用

    return app


def check_host():
    hostname = socket.getfqdn(socket.gethostname())
    print(hostname)
    try:
        my_host = socket.gethostbyname(hostname)
        print(my_host)
    except:
        my_host = socket.gethostbyname("")
        print(my_host)
    if my_host != "192.168.2.68":
        name = 'testing'
    else:
        name = 'product'
    return name
