#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guobingjie'
__time__ = 2019 / 10 / 11

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
    opt_type=db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, driver_mobile,  env, commit,opt_type,create_time):
        self.operator = operator
        self.driver_mobile = driver_mobile
        self.env = env
        self.commit = commit
        self.opt_type= opt_type
        self.create_time = create_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "driver_mobile": self.driver_mobile,
            "env": self.env,
            "commit": self.commit,
            "opt_type":self.opt_type,
            "create_time": self.create_time
        }

    @staticmethod
    def create(operator: object, driver_mobile: object, env: object, commit: object, opt_type: object, create_time: object) -> object:
        res = DriverDispatchConfirmOrder(operator, driver_mobile, env, commit,opt_type,create_time)
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


if __name__ == '__main__':
    res = DriverDispatchConfirmOrder()
    r = res.get_dispatchconfirmorder_list()
    print(r)
