#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '郭冰洁'
__time__ = 2019 / 10 / 25

import sys
import json
from app import create_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask import current_app

# config_name = 'testing'
config_name = 'product'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class AddDriverTest(db.Model):
    """
    创建司机记录
    """

    __tablename__ = 'add_driver_test'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    num = db.Column(db.Integer, nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(25), nullable=False, index=True)
    opt_type = db.Column(db.String(255), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, num, env, commit, opt_type, add_time):
        self.operator = operator
        self.num = num
        self.env = env
        self.commit = commit
        self.opt_type = opt_type
        self.add_time = add_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "num": self.num,
            "env": self.env,
            "commit": self.commit,
            "opt_type": self.opt_type,
            "add_time": self.add_time,
        }

    @staticmethod
    def create(operator: object, num: object, env: object, commit: object, opt_type: object,
               add_time: object) -> object:
        res = AddDriverTest(operator, num, env, commit, opt_type, add_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "注册司机失败"
        # return db.session.commit()

    @staticmethod
    def get_driver_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AddDriverTest.query.order_by(desc(AddDriverTest.id)).all()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.add_time is not None and isinstance(res.add_time, str) is False:
                    res.add_time = res.add_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class AddDriverWhiteList(db.Model):
    """
    司机人脸识别白名单维护记录
    """

    __tablename__ = 'add_driver_white_list'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_phone = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(25), nullable=False, index=True)
    opt_type = db.Column(db.String(25), nullable=False, index=True)
    result = db.Column(db.String(200), nullable=False, index=True)
    opt_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_phone, env, opt_type, result, opt_time):
        self.operator = operator
        self.driver_phone = driver_phone
        self.env = env
        self.opt_type = opt_type
        self.result = result
        self.opt_time = opt_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_phone": self.driver_phone,
            "env": self.env,
            "opt_type": self.opt_type,
            "result": self.result,
            "opt_time": self.opt_time,
        }

    @staticmethod
    def create(operator: object, driver_phone: object, env: object, opt_type: object, result: object,
               opt_time: object) -> object:
        res = AddDriverWhiteList(operator, driver_phone, env, opt_type, result, opt_time)

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
    def get_driver_white_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AddDriverWhiteList.query.order_by(desc(AddDriverWhiteList.id)).all()
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


class DriverBankBindCard(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_bind_bank'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, create_time: object) -> object:
        res = DriverBankBindCard(operator, driver_mobile, env, commit, create_time)
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
    def get_driverbankbindcard_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverBankBindCard.query.order_by(desc(DriverBankBindCard.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverDispatchConfirmOrder(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_dispatch_confirm_order'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    opt_type = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, opt_type, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.opt_type = opt_type
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "opt_type": self.opt_type,
            "create_time": self.create_time
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, opt_type: object,
               create_time: object) -> object:
        res = DriverDispatchConfirmOrder(operator, driver_mobile, env, commit, opt_type, create_time)
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
    def get_dispatchconfirmorder_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverDispatchConfirmOrder.query.order_by(desc(DriverDispatchConfirmOrder.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverOrderMakePoint(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_order_make_point'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, create_time: object) -> object:
        res = DriverOrderMakePoint(operator, driver_mobile, env, commit, create_time)
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
    def get_driverordermakepoint_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverOrderMakePoint.query.order_by(desc(DriverOrderMakePoint.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverPayDeposit(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_paydeposit'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    opt_type = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, opt_type, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.opt_type = opt_type
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "opt_type": self.opt_type,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, opt_type: object,
               create_time: object) -> object:
        res = DriverPayDeposit(operator, driver_mobile, env, commit, opt_type, create_time)
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
    def get_driverpaydeposit_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverPayDeposit.query.order_by(desc(DriverPayDeposit.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverWhiteDrawing(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_whitedrawing'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, create_time: object) -> object:
        res = DriverWhiteDrawing(operator, driver_mobile, env, commit, create_time)
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
    def get_driverwhite_drawing_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverWhiteDrawing.query.order_by(desc(DriverWhiteDrawing.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverUploadReceipt(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_upload_receipt'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object,
               create_time: object) -> object:
        res = DriverUploadReceipt(operator, driver_mobile, env, commit, create_time)
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
    def get_uploadreceipt_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverUploadReceipt.query.order_by(desc(DriverUploadReceipt.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverUploadException(db.Model):
    """
    创建记录
    """
    __tablename__ = 'driver_upload_exception'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object,
               create_time: object) -> object:
        res = DriverUploadException(operator, driver_mobile, env, commit, create_time)
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
    def driver_uploadException_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverUploadException.query.order_by(desc(DriverUploadException.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverDispatchpreConfirm(db.Model):
    """
    创建记录
    """
    __tablename__ = 'driver_dispatch_preConfirm'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object,
               create_time: object) -> object:
        res = DriverDispatchpreConfirm(operator, driver_mobile, env, commit, create_time)
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
    def driver_dispatchpreConfirm_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverDispatchpreConfirm.query.order_by(desc(DriverDispatchpreConfirm.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverWithDraw(db.Model):
    """
    创建记录
    """
    __tablename__ = 'driver_withdraw'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    opt_type = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, opt_type, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.opt_type = opt_type
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "opt_type": self.opt_type,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, opt_type: object,
               create_time: object) -> object:
        res = DriverWithDraw(operator, driver_mobile, env, commit, opt_type, create_time)
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
    def driver_withdraw_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverWithDraw.query.order_by(desc(DriverWithDraw.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverDispatchArrange(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_dispatch_arrange'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    # session.get('username'), driver_mobile, env, res, order_sn, datetime.now())
    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, create_time: object) -> object:
        res = DriverDispatchArrange(operator, driver_mobile, env, commit, create_time)
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
    def get_driver_dispatcharrange_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverDispatchArrange.query.order_by(desc(DriverDispatchArrange.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverShortRent(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_shortrent'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    address = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, address, env, commit, create_time):
        self.operator = operator
        self.address = address
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "address": self.address,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    # session.get('username'), driver_mobile, env, res, order_sn, datetime.now())
    @staticmethod
    def create(operator: object, address: object, env: object, commit: object, create_time: object) -> object:
        res = DriverShortRent(operator, address, env, commit, create_time)
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
    def get_driver_shortrent_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = DriverShortRent.query.order_by(desc(DriverShortRent.id)).all()
            db.session.close()
            print(res_list)
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverAbout(db.Model):
    """
    创建记录
    """

    __tablename__ = 'driver_about'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operationtype = db.Column(db.String(200), nullable=False, index=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operationtype, operator, driver_mobile, env, commit, create_time):
        self.operator = operator
        self.operationtype = operationtype
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operationtype": self.operationtype,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "create_time": self.create_time,
        }

    @staticmethod
    def create(operationtype: object, operator: object, driver_mobile: object, env: object, commit: object,
               create_time: object) -> object:
        res = DriverAbout(operationtype, operator, driver_mobile, env, commit, create_time)
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
    def get_driverabout_list(type):
        """
        获取缴纳历史
        :return:
        """
        try:
            # res_list = DriverAbout.query.order_by(desc(DriverAbout.id)).all()
            # filter_by(name='alex')
            res_list = DriverAbout.query.order_by(desc(DriverAbout.id)).filter_by(operationtype=type).all()
            db.session.close()
            print("&&&&&&")
            print(res_list)
            print("&&&&&&")
            res_json_list = []
            for res in res_list:
                print("****")
                print(res.to_json())
                print("****")
                if res.create_time is not None and isinstance(res.create_time, str) is False:
                    res.create_time = res.create_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            print(e)
            return "获取历史失败"


class DriverCreateAndOrder(db.Model):
    """
    创建司机并安排单子
    """

    __tablename__ = 'driver_create_and_order'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    num = db.Column(db.Integer, nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    lineid = db.Column(db.String(255), nullable=False, index=True)
    status = db.Column(db.String(255), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, num, env, commit, lineid, status,add_time):
        self.operator = operator
        self.num = num
        self.env = env
        self.commit = commit
        self.lineid = lineid
        self.status=status
        self.add_time = add_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "num": self.num,
            "env": self.env,
            "commit": self.commit,
            "lineid": self.lineid,
            "status":self.status,
            "add_time": self.add_time,
        }

    @staticmethod
    def create(operator: object, num: object, env: object, commit: object, lineid: object,status:object,
               add_time: object) -> object:
        res = DriverCreateAndOrder(operator, num, env, commit, lineid,status, add_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "注册司机失败"
        # return db.session.commit()

    @staticmethod
    def get_driver_create_and_order_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = DriverCreateAndOrder.query.order_by(desc(DriverCreateAndOrder.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.add_time is not None and isinstance(res.add_time, str) is False:
                    res.add_time = res.add_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


class DriverHandleAllexception(db.Model):
    """
    一键处理所有异常
    """

    __tablename__ = 'driver_handle_all_exception'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    order_sn = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(25), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, order_sn, env, commit, add_time):
        self.operator = operator
        self.order_sn = order_sn
        self.env = env
        self.commit = commit
        self.add_time = add_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "order_sn": self.order_sn,
            "env": self.env,
            "commit": self.commit,
            "add_time": self.add_time,
        }

    @staticmethod
    def create(operator: object, order_sn: object, env: object, commit: object,
               add_time: object) -> object:
        res = DriverHandleAllexception(operator, order_sn ,env, commit, add_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "注册司机失败"
        # return db.session.commit()

    @staticmethod
    def get_driver_handle_all_exception_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = DriverHandleAllexception.query.order_by(desc(DriverHandleAllexception.id)).all()
            db.session.close()
            db.session.close()
            res_json_list = []
            for res in res_list:
                if res.add_time is not None and isinstance(res.add_time, str) is False:
                    res.add_time = res.add_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


# db.create_all()
