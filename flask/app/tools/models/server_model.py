#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 10 / 25

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


class ServiceDb(db.Model):
    """
    创建记录
    """

    __tablename__ = 'service'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    user_mobile = db.Column(db.String(255), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    operate_name = db.Column(db.String(25), nullable=False, index=True)

    def __init__(self, operator, user_mobile, env, commit, create_time, operate_name):
        self.operator = operator
        self.user_mobile = user_mobile
        self.create_time = create_time
        self.env = env
        self.commit = commit
        self.operate_name = operate_name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.operator,
            "user_mobile": self.user_mobile,
            "create_time": self.create_time,
            "env": self.env,
            "commit": self.commit,
            "operate_name": self.operate_name
        }

    @staticmethod
    def create(operator: object, user_mobile: object, create_time: object, env: object, commit: object,
               operate_name: object) -> object:
        res = ServiceDb(operator, user_mobile, env, commit, create_time, operate_name)
        try:
            db.session.add(res)
            db.session.commit()
            db.create_all()

        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "操作失败"
        # return db.session.commit()

    @staticmethod
    def get_service_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = ServiceDb.query.order_by(desc(ServiceDb.id)).all()
            db.create_all()

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


class ServiceCreate(db.Model):
    """
    创建记录
    """

    __tablename__ = 'service_task_create'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    order_sn = db.Column(db.String(25), nullable=False, index=True)
    task_type_id = db.Column(db.String(10), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)

    def __init__(self, operator, order_sn, task_type_id, create_time, env, commit):
        self.operator = operator
        self.order_sn = order_sn
        self.task_type_id = task_type_id
        self.create_time = create_time
        self.env = env
        self.commit = commit

    def to_json(self):
        return {
            "id": self.id,
            "name": self.operator,
            "order_sn": self.order_sn,
            "task_type_id": self.task_type_id,
            "create_time": self.create_time,
            "env": self.env,
            "commit": self.commit
        }

    @staticmethod
    def create(operator: object, order_sn: object, task_type_id: object, create_time: object, env: object,
               commit: object) -> object:
        res = ServiceCreate(operator, order_sn, task_type_id, create_time, env, commit)
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
    def get_service_list():
        """
        获取缴纳历史
        :return:
        """
        try:
            res_list = ServiceCreate.query.order_by(desc(ServiceCreate.id)).all()
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


db.create_all()


if __name__ == '__main__':
    sc=ServiceCreate()
    sc.create()

