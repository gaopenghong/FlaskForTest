#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 9 / 2


import sys
import json
from app import create_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError
sys.path.append("/Users/liuchunfu/PycharmProjects/ftest/")

config_name = 'testing'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class Operate(db.Model):
    """

    """
    __tablename__ = 'operate_history'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    operate_type = db.Column(db.String(255), nullable=True)
    operate_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    commit = db.Column(db.String(255), nullable=True)

    def __init__(self, username, operate_type, operate_time, commit):
        self.username = username
        self.operate_type = operate_type
        self.operate_time = operate_time
        self.commit = commit

    # 自定义输出方式
    def __repr__(self):
        temp = '%s:%s:%s:%s:%s' % (self.id, self.username, self.operate_type, self.operate_time, self.commit)
        return temp

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "operate_type": self.operate_type,
            "operate_time": self.operate_time,
            "commit": self.commit
        }

    @staticmethod
    def get_operate_list():
        """
            获取列表
        :return:
        """
        try:
            res_list = Operate.query.order_by(desc(Operate.id)).limit(100)
            res_json_list = []
            for res in res_list:
                if isinstance(res.operate_time, str) is False:
                    res.operate_time = res.operate_time.strftime('%Y-%m-%d %H:%M:%S')
                print(res.to_json())
                res_json_list.append(res.to_json())
            return json.dumps(res_json_list)
        except InvalidRequestError:
            db.session.rollback()
        except Exception as e:
            # current_app.logger.error(e)
            print(e)
            db.session.rollback()
            return {"res:获取操作历史失败"}

    @staticmethod
    def create(username, operate_type, operate_time, commit):
        """
            新建
        :param username:
        :param operate_type:
        :param operate_time:
        :param commit:
        :return:
        """

        res = Operate(username, operate_type, operate_time, commit)
        db.session.add(res)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()


if __name__ == '__main__':
    s = Operate.get_operate_list()
    print(s)
