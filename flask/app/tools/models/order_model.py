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


class DriverOrdersDone(db.Model):
    """
    孙竹叶-创建司机所有运单卸货完成单记录
    """
    __tablename__ = 'driver_orders_done'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    driver_phone = db.Column(db.String(255), nullable=False, index=True)
    order_num = db.Column(db.Integer, nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, driver_phone, create_time, env, commit, order_num):
        self.name = name
        self.driver_phone = driver_phone
        self.create_time = create_time
        self.env = env
        self.commit = commit
        self.order_num = order_num

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "driver_phone": self.driver_phone,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
            'order_num': self.order_num
        }

    @staticmethod
    def create(name: object, driver_phone: object, create_time: object, env: object, commit: object, order_num: object) -> object:
        res = DriverOrdersDone(name, driver_phone, create_time, env, commit, order_num)

        try:
            db.session.add(res)
            db.session.commit()
            db.create_all()

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "司机卸货完成入库失败"

    @staticmethod
    def get_driver_orders_list():
        """
        获取注册历史
        :return:
        """
        try:
            res_list = DriverOrdersDone.query.order_by(desc(DriverOrdersDone.id)).all()
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
            return "获取注册历史失败"


class OrderLessMoney(db.Model):
    """
    孙竹叶-运单产生时效轨迹扣款记录
    """
    __tablename__ = 'order_less_money'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    order_sn = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    type = db.Column(db.String(255), nullable=True, index=True)

    def __init__(self, name, env, order_sn, commit, create_time, type):
        self.name = name
        self.env = env
        self.order_sn = order_sn
        self.commit = commit
        self.create_time = create_time
        self.type = type

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "env": self.env,
            "order_sn": self.order_sn,
            "commit": self.commit,
            "create_time": self.create_time,
            "type": self.type
        }

    @staticmethod
    def create(name: object, env: object, order_sn: object, commit: object, create_time: object, type:object) -> object:
        res = OrderLessMoney(name, env, order_sn, commit, create_time, type)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "运单产生时效轨迹扣款入库失败"

    @staticmethod
    def get_order_less_money_list(type):
        """
        获取注册历史
        :return:
        """
        try:
            res_list = OrderLessMoney.query.filter_by(type=type).order_by(desc(OrderLessMoney.id)).all()
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
            return "获取注册历史失败"


class ScheduleSwitch(db.Model):
    """智能调度派车开关"""
    __tablename__ = 'schedule_switch_info'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(25), nullable=False, index=True)
    opt_type = db.Column(db.String(25), nullable=False, index=True)
    result = db.Column(db.String(200), nullable=False, index=True)
    opt_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, env, opt_type, result, opt_time):
        self.operator = operator
        self.env = env
        self.opt_type = opt_type
        self.result = result
        self.opt_time = opt_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "env": self.env,
            "opt_type": self.opt_type,
            "result": self.result,
            "opt_time": self.opt_time,
        }

    @staticmethod
    def create(operator: object, env: object, opt_type: object, result: object, opt_time: object) -> object:
        res = ScheduleSwitch(operator, env, opt_type, result, opt_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"
        # return db.session.commit()

    @staticmethod
    def get_schedule_switch_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = ScheduleSwitch.query.order_by(desc(ScheduleSwitch.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.opt_time is not None and isinstance(res.opt_time, str) is False:
                    res.opt_time = res.opt_time.strftime('%Y-%m-%d %H:%M:%S')
                # res.result = res.result[1:-1]
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class OrderAbnormalModify(db.Model):
    """创建运单异常修改记录"""

    __tablename__ = 'order_abnormal_modify'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    orderSn = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    order_status = db.Column(db.String(255), nullable=False, index=True)
    modify_reason = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, orderSn, env, order_status, modify_reason, commit, create_time):
        self.name = name
        self.orderSn = orderSn
        self.env = env
        self.order_status = order_status
        self.modify_reason = modify_reason
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "orderSn": self.orderSn,
            "env": self.env,
            "order_status": self.order_status,
            "modify_reason": self.modify_reason,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(name: object, orderSn: object, env: object, order_status: object, modify_reason: object,
               commit: object, create_time: object) -> object:
        res = OrderAbnormalModify(name, orderSn, env, order_status, modify_reason, commit, create_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "运单异常修改操作入库失败"

    @staticmethod
    def abnormal_modify():
        """
        获取运单异常修改操作历史
        :return:
        """
        try:
            res_list = OrderAbnormalModify.query.order_by(desc(OrderAbnormalModify.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取运单异常修改操作历史失败"


class AddAutoQuery(db.Model):
    """
    创建意向单记录
    """
    __tablename__ = 'auto_query'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    lineid = db.Column(db.String(255), nullable=False, index=True)
    result = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, env, lineid, result, create_time):
        self.operator = operator
        self.env = env
        self.lineid = lineid
        self.result = result
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "env": self.env,
            "lineid":self.lineid,
            "result": self.result,
            "create_time": self.create_time

        }

    @staticmethod
    def create(operator: object, env: object, lineid: object, result: object,
               create_time: object) -> object:
        res = AddAutoQuery(operator, env, lineid, result, create_time)
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"
        # return db.session.commit()

    @staticmethod
    def get_auto_query_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AddAutoQuery.query.order_by(desc(AddAutoQuery.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                    res.result = res.result
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class AppointOrderInfo(db.Model):
    """指定运单生成"""
    __tablename__ = 'appoint_order_create'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False)
    env = db.Column(db.String(25), nullable=False)
    appoint_order_type = db.Column(db.String(25), nullable=False)
    appoint_transfer_type = db.Column(db.String(25), nullable=False)
    appoint_order_status = db.Column(db.String(25), nullable=False)
    appoint_order_offline_pay = db.Column(db.String(25), nullable=True)
    auto_query_create_time = db.Column(db.DateTime, nullable=False)
    result = db.Column(db.String(200), nullable=False)
    opt_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, env, appoint_order_type, appoint_transfer_type, appoint_order_status, appoint_order_offline_pay, auto_query_create_time, result, opt_time):
        self.operator = operator
        self.env = env
        self.appoint_order_type = appoint_order_type
        self.appoint_transfer_type = appoint_transfer_type
        self.appoint_order_status = appoint_order_status
        self.appoint_order_offline_pay = appoint_order_offline_pay
        self.auto_query_create_time = auto_query_create_time
        self.result = result
        self.opt_time = opt_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "env": self.env,
            "appoint_order_type": self.appoint_order_type,
            "appoint_transfer_type": self.appoint_transfer_type,
            "appoint_order_status": self.appoint_order_status,
            "appoint_order_offline_pay": self.appoint_order_offline_pay,
            "auto_query_create_time": self.auto_query_create_time,
            "result": self.result,
            "opt_time": self.opt_time,
        }

    @staticmethod
    def create(operator: object, env: object, appoint_order_type: object, appoint_transfer_type: object,
               appoint_order_status: object, appoint_order_offline_pay: object, auto_query_create_time: object, result: object, opt_time: object) -> object:
        res = AppointOrderInfo(operator, env, appoint_order_type, appoint_transfer_type, appoint_order_status,
                               appoint_order_offline_pay, auto_query_create_time, result, opt_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"
        # return db.session.commit()

    @staticmethod
    def get_appoint_order_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AppointOrderInfo.query.order_by(desc(AppointOrderInfo.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.opt_time is not None and isinstance(res.opt_time, str) is False:
                    res.opt_time = res.opt_time.strftime('%Y-%m-%d %H:%M:%S')
                if res.auto_query_create_time is not None and isinstance(res.auto_query_create_time, str) is False:
                # if res.auto_query_create_time is not None:
                    auto_query_create_time_str = res.auto_query_create_time.strftime('%Y-%m-%d %H:%M:%S')
                    if auto_query_create_time_str == "0000-00-00 00:00:00":
                        res.auto_query_create_time = None
                    else:
                        res.auto_query_create_time = auto_query_create_time_str
                # res.result = res.result[1:-1]
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class OperateOrder(db.Model):
    """运单指定操作"""
    __tablename__ = 'appoint_order_operate'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False)
    env = db.Column(db.String(25), nullable=False)
    order_sn = db.Column(db.String(25), nullable=False)
    operate_appoint_order_status = db.Column(db.String(25), nullable=False)
    result = db.Column(db.String(200), nullable=False)
    opt_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, env, order_sn, operate_appoint_order_status, result, opt_time):
        self.operator = operator
        self.env = env
        self.order_sn = order_sn
        self.operate_appoint_order_status = operate_appoint_order_status
        self.result = result
        self.opt_time = opt_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "env": self.env,
            "order_sn": self.order_sn,
            "operate_appoint_order_status": self.operate_appoint_order_status,
            "result": self.result,
            "opt_time": self.opt_time,
        }

    @staticmethod
    def create(operator: object, env: object, order_sn: object, operate_appoint_order_status: object,
               result: object, opt_time: object) -> object:
        res = OperateOrder(operator, env, order_sn, operate_appoint_order_status, result, opt_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"
        # return db.session.commit()

    @staticmethod
    def get_operate_order_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = OperateOrder.query.order_by(desc(OperateOrder.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.opt_time is not None and isinstance(res.opt_time, str) is False:
                    res.opt_time = res.opt_time.strftime('%Y-%m-%d %H:%M:%S')
                # res.result = res.result[1:-1]
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class AddThirdOrder(db.Model):
    """
    创建三方询价单记录
    """

    __tablename__ = 'third_order'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    thirdsn = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    result = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, thirdsn, env, result, create_time):
        self.operator = operator
        self.thirdsn = thirdsn
        self.env = env
        self.result = result
        self.add_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "thirdsn": self.thirdsn,
            "env": self.env,
            "result": self.result,
            "create_time": self.create_time

        }

    @staticmethod
    def create(operator: object, thirdsn: object, env: object, result: object,
               create_time: object) -> object:
        res = AddThirdOrder(operator, thirdsn, env, result, create_time)
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"
        # return db.session.commit()

    @staticmethod
    def get_third_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AddThirdOrder.query.order_by(desc(AddThirdOrder.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                    res.result = res.result
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def update_third_list(order_code, result):
        res = AddThirdOrder.query.filter_by(thirdSn=order_code).first()
        res.thirdsn = order_code
        res.result = result
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
            return AddThirdOrder.query.filter_by(thirdSn=order_code).first()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "更新表失败"


if __name__ == '__main__':
    OrderLessMoney().create()

