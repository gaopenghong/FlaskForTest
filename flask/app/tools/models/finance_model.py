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

# config_name = 'product'
config_name = 'testing'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class PaymentChannels(db.Model):
    """创建测试支付通道开启记录&司机奖励发放记录"""

    __tablename__ = 'payment_channels'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False, index=True)
    operate_id = db.Column(db.String(255), nullable=False, index=True)
    id_or_mobile = db.Column(db.String(255), nullable=False, index=True)
    reward_type = db.Column(db.String(255), nullable=False, index=True)
    reward_amount = db.Column(db.String(255), nullable=False, index=True)
    tool_id = db.Column(db.String(255), nullable=False, index=True)  # 1 for 支付通道；2 for 司机奖励
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, env, value, operate_id, id_or_mobile, reward_type, reward_amount, tool_id, commit,
                 create_time):
        self.name = name
        self.env = env
        self.value = value
        self.operate_id = operate_id
        self.id_or_mobile = id_or_mobile
        self.reward_type = reward_type
        self.reward_amount = reward_amount
        self.tool_id = tool_id
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "env": self.env,
            "value": self.value,
            "operate_id": self.operate_id,
            "id_or_mobile": self.id_or_mobile,
            "reward_type": self.reward_type,
            "reward_amount": self.reward_amount,
            "tool_id": self.tool_id,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(name: object, env: object, value: object, operate_id: object, id_or_mobile: object, reward_type: object,
               reward_amount: object, tool_id: object, commit: object,
               create_time: object) -> object:
        res = PaymentChannels(name, env, value, operate_id, id_or_mobile, reward_type, reward_amount, tool_id, commit,
                              create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "测试支付通道开启记录&司机奖励发放记录操作入库失败"

    @staticmethod
    def payment_channels(tool_id):
        """
        获取测试支付通道开启记录&司机奖励发放记录操作历史
        :return:
        """
        try:
            res_list = PaymentChannels.query.filter_by(tool_id=tool_id).order_by(desc(PaymentChannels.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)

        except Exception as e:
            current_app.logger.error(e)
            return "获取测试支付通道开启记录&司机奖励发放记录失败"


class FyInvoiceInternal(db.Model):

    """
    syh数据库
    """

    __tablename__ = 'finance_fy_internal_table'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(255), nullable=False, index=True)
    order_sn = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    check_result = db.Column(db.String(255), nullable=False, index=True)
    check_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    feature_type = db.Column(db.Integer, nullable=False)

    def __init__(self, operator, order_sn, env, check_result, check_time, feature_type):
        self.operator = operator
        self.order_sn = order_sn
        self.env = env
        self.check_result = check_result
        self.check_time = check_time
        self.feature_type = feature_type

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "order_sn": self.order_sn,
            "env": self.env,
            "check_result": self.check_result,
            "check_time": self.check_time,
            "type": self.feature_type
        }

    @staticmethod
    def create(operator: object, order_sn: object, env: object, check_result: object,
               check_time: object, feature_type: object) -> object:
        res = FyInvoiceInternal(operator, order_sn, env, check_result, check_time, feature_type)
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "操作失败"
        # return db.session.commit()

    @staticmethod
    def get_finance_fy_inter_by_type(feature_type):
        """
        获取历史
        :return:
        """
        try:
            res_list = FyInvoiceInternal.query.filter_by(feature_type=feature_type).order_by(desc(FyInvoiceInternal.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.check_time is not None and isinstance(res.check_time, str) is False:
                    res.check_time = res.check_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


db.create_all()






