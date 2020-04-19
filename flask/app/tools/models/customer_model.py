#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liqi'
__time__ = 2019 / 10 / 27

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


class CustomerConfirmByLineId(db.Model):

    """
    创建项目货线路ID下单记录
    """

    __tablename__ = 'customer_confirm_line_id'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    line_id = db.Column(db.String(255), nullable=False, index=True)
    order_num = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, line_id, order_num, env, commit, create_time):
        self.operator = operator
        self.line_id = line_id
        self.order_num = order_num
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "line_id": self.line_id,
            "order_num": self.order_num,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, line_id: object, order_num: object, env: object, commit: object,
               create_time: object) -> object:
        res = CustomerConfirmByLineId(operator, line_id, order_num, env, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "项目货线路ID下单入库失败"
        # return db.session.commit()

    @staticmethod
    def get_confirm_line_id_list():
        """
        获取项目货线路ID下单历史
        :return:
        """
        try:
            res_list = CustomerConfirmByLineId.query.order_by(desc(CustomerConfirmByLineId.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class CustomerOrderConfirm(db.Model):

    """
    吸货下单记录
    """
    __tablename__ = 'customer_order_confirm'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    customer_mobile = db.Column(db.String(255), nullable=False, index=True)
    order_info = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, customer_mobile, order_info, env, commit, create_time):
        self.operator = operator
        self.customer_mobile = customer_mobile
        self.order_info = order_info
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "customer_mobile": self.customer_mobile,
            "order_info": self.order_info,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, customer_mobile: object, order_info: object, env: object, commit: object,
               create_time: object) -> object:
        res = CustomerOrderConfirm(operator, customer_mobile, order_info, env, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "吸货下单入库失败"
        # return db.session.commit()

    @staticmethod
    def get_customer_order_confirm_list():
        """
        获取吸货下单历史
        :return:
        """
        try:
            res_list = CustomerOrderConfirm.query.order_by(desc(CustomerOrderConfirm.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class OrderPositionHeartbeat(db.Model):

    """
    运单上传司机定位记录
    """
    __tablename__ = 'order_position_heartbeat'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    order_sn = db.Column(db.String(255), nullable=False, index=True)
    lng_lat = db.Column(db.String(255), nullable=False, index=True)
    action_type = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, order_sn, lng_lat, action_type, env, commit, create_time):
        self.operator = operator
        self.order_sn = order_sn
        self.lng_lat = lng_lat
        self.action_type = action_type
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "order_sn": self.order_sn,
            "lng_lat": self.lng_lat,
            "action_type": self.action_type,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }


    @staticmethod
    def create(operator: object, order_sn: object, lng_lat: object, action_type: object, env: object, commit: object,
               create_time: object) -> object:
        res = OrderPositionHeartbeat(operator, order_sn, lng_lat, action_type, env, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "吸货下单入库失败"
        # return db.session.commit()

    @staticmethod
    def get_order_position_heartbeat_list():
        """
        获取运单上传司机定位历史
        :return:
        """
        try:
            res_list = OrderPositionHeartbeat.query.order_by(desc(OrderPositionHeartbeat.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')

                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class OrderTimeOut(db.Model):

    """
    压车费上传记录
    """
    tablename__ = 'order_time_out'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    order_sn = db.Column(db.String(255), nullable=False, index=True)
    time_out = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, order_sn, time_out, env, commit, create_time):
        self.operator = operator
        self.order_sn = order_sn
        self.time_out = time_out
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "order_sn": self.order_sn,
            "time_out": self.time_out,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }


    @staticmethod
    def create(operator: object, order_sn: object, time_out: object, env: object, commit: object,
               create_time: object) -> object:
        res = OrderTimeOut(operator, order_sn, time_out, env, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "司机上传压车时长入库失败"
        # return db.session.commit()

    @staticmethod
    def get_order_time_out_list():
        """
        获取司机上传压车时长历史
        :return:
        """
        try:
            res_list = OrderTimeOut.query.order_by(desc(OrderTimeOut.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')

                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class CustomerGrantCoupon(db.Model):

    """
    发放优惠卷记录
    """
    tablename__ = 'customer_grant_coupon'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    mobile = db.Column(db.String(255), nullable=False, index=True)
    number = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, mobile, number, env, commit, create_time):
        self.operator = operator
        self.mobile = mobile
        self.number = number
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            'operator': self.operator,
            "mobile": self.mobile,
            "number": self.number,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }


    @staticmethod
    def create(operator: object, mobile: object, number: object, env: object, commit: object,
               create_time: object) -> object:
        res = CustomerGrantCoupon(operator, mobile, number, env, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "发放优惠卷入库失败"
        # return db.session.commit()

    @staticmethod
    def get_grant_coupon_list():
        """
        获取发放优惠卷历史
        :return:
        """
        try:
            res_list = CustomerGrantCoupon.query.order_by(desc(CustomerGrantCoupon.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')

                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


# db.create_all()