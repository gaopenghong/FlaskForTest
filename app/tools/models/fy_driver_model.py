#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuxiongjin'
__time__ = 2019 / 11 / 30

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

db = SQLAlchemy(app)  # 实例化


class FyDriver(db.Model):
    """
    共建司机接单
    """

    __tablename__ = 'self_driver'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    order_sn = db.Column(db.String(255), nullable=False, index=True)
    driver_mobile = db.Column(db.String(255), nullable=False, index=True)
    order_status = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, env, order_sn, driver_mobile, order_status, commit,
                 add_time):
        self.operator = operator
        self.env = env
        self.order_sn = order_sn
        self.driver_mobile = driver_mobile
        self.order_status = order_status
        self.commit = commit
        self.add_time = add_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "env": self.env,
            "order_sn": self.order_sn,
            "driver_mobile": self.driver_mobile,
            "order_status": self.order_status,
            "commit": self.commit,
            "add_time": self.add_time

        }

    @staticmethod
    def create(operator: object, env: object, order_sn: object, driver_mobile: object, order_status: object,
               commit: object, add_time: object) -> object:
        res = FyDriver(operator, env, order_sn, driver_mobile, order_status, commit, add_time)

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
    def get_fy_driver_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = FyDriver.query.order_by(desc(FyDriver.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.add_time is not None and isinstance(res.add_time, str) is False:
                    res.add_time = res.add_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    # if __name__ == '__main__':
    #     res = FyDriver()
    #     r = res.create()
    #     print(r)
