#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.tools.models.server_model import ServiceDb

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


class ServiceImCreate(db.Model):
    """
    创建记录
    """
    __tablename__ = 'service_im_task_create'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    word_name = db.Column(db.String(25), nullable=False, index=True)
    task_im_type_id = db.Column(db.String(10), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)

    def __init__(self, operator, word_name, task_im_type_id, create_time, env, commit):
        self.operator = operator
        self.word_name = word_name
        self.task_im_type_id = task_im_type_id
        self.create_time = create_time
        self.env = env
        self.commit = commit

    def to_json(self):
        return {
            "id": self.id,
            "name": self.operator,
            "word_name": self.word_name,
            "task_im_type_id": self.task_im_type_id,
            "create_time": self.create_time,
            "env": self.env,
            "commit": self.commit
        }

    @staticmethod
    def create(operator: object, word_name: object, task_im_type_id: object, create_time: object, env: object,
               commit: object) -> object:
        res = ServiceImCreate(operator, word_name, task_im_type_id, create_time, env, commit)
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
            res_list = ServiceImCreate.query.order_by(desc(ServiceImCreate.id)).all()
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

class ServiceImTagCreate(db.Model):
    """
    创建记录
    """
    __tablename__ = 'service_im_tag_create'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    tag_name = db.Column(db.String(25), nullable=False, index=True)
    task_im_role = db.Column(db.String(10), nullable=False, index=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    env = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)

    def __init__(self, operator, tag_name, task_im_role, create_time, env, commit):
        self.operator = operator
        self.tag_name = tag_name
        self.task_im_role = task_im_role
        self.create_time = create_time
        self.env = env
        self.commit = commit

    def to_json(self):
        return {
            "id": self.id,
            "name": self.operator,
            "tag_name": self.tag_name,
            "task_im_role": self.task_im_role,
            "create_time": self.create_time,
            "env": self.env,
            "commit": self.commit
        }

    @staticmethod
    def create(operator: object, tag_name: object, task_im_role: object, create_time: object, env: object,
               commit: object) -> object:
        res = ServiceImTagCreate(operator, tag_name, task_im_role, create_time, env, commit)
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
            res_list = ServiceImTagCreate.query.order_by(desc(ServiceImTagCreate.id)).all()
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
    # sc = ServiceImCreate()
    # sc.create()
    pass

