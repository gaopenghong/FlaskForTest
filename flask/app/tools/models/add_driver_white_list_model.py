#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guobaohui'
__time__ = 2019 / 10 / 15

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
    def create(operator: object,  driver_phone: object, env: object, opt_type: object, result: object, opt_time: object) -> object:
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


if __name__ == '__main__':
    res = AddDriverWhiteList("test", "01234567890", "t5", "0", "test case", "2019-10-15 21:22:23")
    print(res)
    r = res.create("test", "01234567890", "t5", "0", "test case", "2019-10-15 21:22:23")
    print(r)
    r = res.get_driver_white_list()
    print(r)
