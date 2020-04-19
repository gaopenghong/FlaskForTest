#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 10 / 25

import sys
import json
from app import create_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask import current_app


config_name = 'testing'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class CreateOmsTestData(db.Model):
    """
    创建运营测试数据
    """
    __tablename__ = 'oms_test_history'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, comment='操作人')
    environment = db.Column(db.String(25), nullable=False, comment='环境')
    app_type = db.Column(db.String(25), nullable=False, comment='app终端类型')
    type_id = db.Column(db.String(25), nullable=False, comment='广告类型')
    title = db.Column(db.String(25), nullable=False, comment='标题')
    link_url = db.Column(db.String(25), nullable=False, comment='活动图片')
    start_time = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='开始时间')
    end_time = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='结束时间')
    pic_url = db.Column(db.String(25), nullable=False, comment='活动图片url')
    rank = db.Column(db.String(25), nullable=False, comment='banner排名')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, environment, app_type, type_id, title, link_url,  pic_url, rank):
        self.operator = operator
        self.environment = environment
        self.app_type = app_type
        self.type_id = type_id
        self.title = title
        self.link_url = link_url
        self.pic_url = pic_url
        self.rank = rank

    def to_json(self):
        return {
            'id': self.id,
            'operator': self.operator,
            'environment': self.environment,
            'app_type': self.app_type,
            'type_id': self.type_id,
            'title': self.title,
            'link_url': self.link_url,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'pic_url': self.pic_url,
            'rank': self.rank,
            'create_time': self.create_time
        }

    @staticmethod
    def create(operator: object, environment: object, app_type: object, type_id: object, title: object, link_url: object,
               pic_url: object, rank: object):
        res = CreateOmsTestData(operator, environment, app_type, type_id, title, link_url, pic_url, rank)

        try:
            db.session.add(res)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def select_check_banner_list():
        """
        获取新增广告位历史
        :return:
        """
        try:
            res_list = CreateOmsTestData.query.order_by(desc(CreateOmsTestData.id)).all()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                if res.start_time is not None and isinstance(res.start_time, str) is False:
                    res.start_time = res.start_time.strftime('%Y-%m-%d %H:%M:%S')
                if res.end_time is not None and isinstance(res.end_time, str) is False:
                    res.end_time = res.end_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class CreateIosTestData(db.Model):
    """
    创建ios提审配置测试数据
    """
    __tablename__ = 'ios_config_history'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, comment='操作人')
    environment = db.Column(db.String(25), nullable=False, comment='环境')
    customer_type = db.Column(db.String(25), nullable=False, comment='客户端类型')
    dev_version = db.Column(db.String(25), nullable=False, comment='开发版本号')
    host = db.Column(db.String(25), nullable=False, comment='环境')
    remark = db.Column(db.String(25), nullable=False, comment='备注')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, environment, customer_type, dev_version, host, remark):
        self.operator = operator
        self.environment = environment
        self.customer_type = customer_type
        self.dev_version = dev_version
        self.host = host
        self.remark = remark

    def to_json(self):
        return {
            'id': self.id,
            'operator': self.operator,
            'environment': self.environment,
            'customer_type': self.customer_type,
            'dev_version': self.dev_version,
            'host': self.host,
            'remark': self.remark,
            'create_time': self.create_time
        }

    @staticmethod
    def create(operator: object, environment: object, customer_type: object, dev_version: object, host: object,
               remark: object):
        res = CreateIosTestData(operator, environment, customer_type, dev_version, host, remark)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def select_ios_config_list():
        """
        获取新增ios配置历史
        :return:
        """
        try:
            res_list = CreateIosTestData.query.order_by(desc(CreateIosTestData.id)).all()
            db.session.close()

            res_json_list = []
            for res in res_list:
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

# db.create_all()