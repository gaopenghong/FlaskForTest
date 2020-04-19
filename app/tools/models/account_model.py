#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
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


class Accounts(db.Model):
    """
    账号
    """

    __tablename__ = 'accounts'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False)
    add_name = db.Column(db.String(25), nullable=False)
    add_phone = db.Column(db.String(25), nullable=False)
    commit = db.Column(db.String(255), nullable=False)
    environment = db.Column(db.String(255), nullable=False)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, operator, add_name, add_phone, add_time, type, commit, environment):
        self.operator = operator
        self.add_name = add_name
        self.add_phone = add_phone
        self.add_time = add_time
        self.type = type
        self.environment = environment
        self.commit = commit

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "add_name": self.add_name,
            "add_phone": self.add_phone,
            "commit": self.commit,
            "environment": self.environment,
            "add_time": self.add_time,
            "type": self.type,
        }

    @staticmethod
    def create(operator, add_phone, add_time, commit, type, environment, add_name=''):
        print(operator, add_phone, add_time, commit, type, environment)
        res = Accounts(operator, add_name, add_phone, add_time, type, commit, environment)

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
    def get_account_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = Accounts.query.order_by(desc(Accounts.id)).all()
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

    @staticmethod
    def get_account_by_type(type):
        """
        获取历史
        :return:
        """
        try:
            res_list = Accounts.query.filter_by(type=type).order_by(desc(Accounts.id)).all()
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


if __name__ == '__main__':
    res = Accounts()
    r = res.get_account_list()
    print(r)
