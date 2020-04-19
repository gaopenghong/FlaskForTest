#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib
import logging

logging.getLogger().setLevel(logging.DEBUG)
importlib.reload(sys)

basedir = os.path.abspath(os.path.dirname(__file__))  # 获得当前文件(比如配置文件)所在的路径


class Config:
    """
        author = liuchunfu
        date = 2017-9-6
        desc = 默认配置
        说明: 这里给出基本配置,额外配置可以在需要的时候自己加入。注释按照示例方式给出
        说明：后面有需要可以扩充从配置文件读取配置
    """
    # 通用配置
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # True, 每次请求结束后都会自动提交数据库中的变动,db.session.commit()
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # 密钥,session、cookie、第三方扩展中使用,是加密过程中作为算法的一个参数使用
    SQLALCHEMY_DATABASE_URI = "mysql://fykctest:fykctest_88@rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com/ftestcenter_new?charset=utf8"  # 用于连接的数据库 URI
    SQLALCHEMY_POOL_RECYCLE = 10
    SQLALCHEMY_POOL_SIZE = 200
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_MAX_OVERFLOW = 50
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 设置flask-mail的邮件主题
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # 发送邮件用到
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'  # 邮件用到
    SESSION_TYPE = "filesystem"  # 设计和维护Session,只有后端sess = Session()才需要设置
    SESSION_FILE_DIR = "/tmp/flask_session"  # 存储会话文件的目录。默认在当前工程下用flask_session安装目录

    def __init__(self):
        """
            desc = 创建对象默认调用
        """
        pass

    @staticmethod
    def init_app(app):
        """
            @author = liuchunfu
            @date   = 2017-9-6
            @desc   = Execute configuration initialization for the current environment
            :param app: [required] application instance
            配置类可以定义一个将应用程序实例作为参数的init_app()静态方法
            :return: None
        """
        pass


class TestingConfig(Config):
    """
    测试环境使用
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://fykctest:fykctest_88@rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com/ftest?charset=utf8"  # 用于连接的数据库 URI


class ProductionConfig(Config):
    """运行环境配置"""
    # SQLALCHEMY_DATABASE_URI = "mysql://fykctest:fykctest_88@rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com/ftestcenter_new?charset=utf8"  # 用于连接的数据库 URI
    SQLALCHEMY_DATABASE_URI = "mysql://root:fyadmin@192.168.2.68/ftest_online?charset=utf8"  # 用于连接的数据库 URI


# 不同的配置是注册在配置字典中,将其中一个配置(开发配置注册为默认配置)
config = {
    'testing': TestingConfig,
    'product': ProductionConfig,
    'default': ProductionConfig
}

if __name__ == 'main':
    print('over')
