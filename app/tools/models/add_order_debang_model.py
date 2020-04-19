#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhangjian'
__time__ = 2019 / 10 / 17

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


class AddDeBang(db.Model):
    """
    创建德邦询价单记录
    """

    __tablename__ = 'debang_order'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    thirdSn = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    result = db.Column(db.String(255), nullable=False, index=True)
    confirm_res = db.Column(db.String(255), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, thirdSn, env, result, confirm_res, add_time):
        self.operator = operator
        self.thirdSn = thirdSn
        self.env = env
        self.result = result
        self.confirm_res = confirm_res
        self.add_time = add_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "thirdSn": self.thirdSn,
            "env": self.env,
            "result": self.result,
            "confirm_res": self.confirm_res,
            "add_time": self.add_time

        }

    @staticmethod
    def create(operator: object, thirdSn: object, env: object, result: object, confirm_res: object,
               add_time: object) -> object:
        res = AddDeBang(operator, thirdSn, env, result, confirm_res, add_time)
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
    def get_debang_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = AddDeBang.query.order_by(desc(AddDeBang.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.add_time is not None and isinstance(res.add_time, str) is False:
                    res.add_time = res.add_time.strftime('%Y-%m-%d %H:%M:%S')
                    res.result = res.result
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def update_debang_list(order_code, confirm_res):
        res = AddDeBang.query.filter_by(thirdSn=order_code).first()
        res.thirdSn = order_code
        res.confirm_res = confirm_res
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
            return AddDeBang.query.filter_by(thirdSn=order_code).first()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "更新表失败"


if __name__ == '__main__':
    res = AddDeBang()
    r = res.get_debang_list()
    print(r)
