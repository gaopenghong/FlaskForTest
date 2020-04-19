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

db = SQLAlchemy(app)  # 实例化


class Truck(db.Model):
    """
    创建闪送员记录
    """

    __tablename__ = 'trailer_list'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    plate_number = db.Column(db.String(255), nullable=False, index=True)
    commit = db.Column(db.String(255), nullable=False, index=True)
    env = db.Column(db.String(255), nullable=False, index=True)
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, add_time, plate_number, commit, env):
        self.operator = operator
        self.add_time = add_time
        self.env = env
        self.plate_number = plate_number
        self.commit = commit

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "commit": self.commit,
            "plate_number": self.plate_number,
            "env": self.env,
            "add_time": self.add_time,
        }

    @staticmethod
    def create(operator: object, add_time: object, plate_number: object,
               commit: object, env: object) -> object:
        res = Truck(operator, add_time, plate_number, commit, env)

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
    def get_trailer_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = Truck.query.order_by(desc(Truck.id)).all()
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
    res = Truck()
    r = res.get_trailer_list()
    print(r)
