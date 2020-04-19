#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'shanxinxin'
__time__ = 2019 / 11 / 2

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


class FinanceUnderLineCheckModel02(db.Model):

    """
    批量线下对账
    """

    __tablename__ = 'finance_under_line_check'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    order_num = db.Column(db.String(255), nullable=False, index=True)
    operator = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    check_result = db.Column(db.String(255), nullable=False, index=True)
    check_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, order_num, env, check_result,  check_time):
        self.operator = operator
        self.order_num = order_num
        self.env = env
        self.check_result = check_result
        self.check_time = check_time

    def to_json(self):
        return {
            "id": self.id,
            'order_num':self.order_num,
            'operator': self.operator,
            "env": self.env,
            "check_result": self.check_result,
            "check_time": self.check_time,
        }

    @staticmethod
    def create(operator: object, order_num: object, env: object, check_result: object, check_time: object) -> object:
        res = FinanceUnderLineCheckModel02(operator, order_num, env, check_result, check_time)
        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "审核失败"
        # return db.session.commit()

    @staticmethod
    def get_under_the_line_check_list03():
        """
        获取注册历史
        :return:
        """
        try:
            res_list = FinanceUnderLineCheckModel02.query.order_by(desc(FinanceUnderLineCheckModel02.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.check_time is not None and isinstance(res.check_time, str) is False:
                    res.check_time = res.check_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())

            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


if __name__ == '__main__':
    res = FinanceUnderLineCheckModel02()
    r = res.get_under_the_line_check_list03()
    print(r)

