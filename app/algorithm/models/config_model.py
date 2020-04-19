#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 10 / 11

import json
from app import create_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask import current_app

config_name = 'testing'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class Indexconf(db.Model):
    """
    指标配置
    """

    __tablename__ = 'algorithm_conf_indicator'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, type, key, value):
        self.type = type
        self.key = key
        self.value = value

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "key": self.key,
            "value": self.value,
        }

    @staticmethod
    def create_conf(type, key, value):
        res = Indexconf(type, key, value)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_conf_list():
        """
        获取历史记录
        :return:
        """
        try:
            res_list = db.session.query(Indexconf).order_by(desc(Indexconf.type)).all()

            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def update_conf_list(ids,values):
        """
        更新记录
        :return:
        """
        db.session.query(Indexconf).filter(Indexconf.id == ids).update({"value": values})
        res_json = db.session.query(Indexconf).filter(Indexconf.id == ids).all()
        res_json_list = []
        for res in res_json:
            res_json_list.append(res.to_json())
        db.session.commit()
        db.session.close()
        return json.dumps(res_json_list)


if __name__ == '__main__':
    Indexconf.get_conf_list()
