#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 11


import sys
import json
from app import create_app, check_host
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask import current_app

# config_name = 'testing'
config_name = check_host()
print(config_name)
app = create_app(config_name)
db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class Env(db.Model):
    """
    自动化
    """

    __tablename__ = 'environment'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    env = db.Column(db.String(255), nullable=False)
    port = db.Column(db.String(255), nullable=False)

    def __init__(self, env, port):
        self.env = env
        self.port = port

    def to_json(self):
        return {
            "id": self.id,
            "env": self.env,
            "port": self.port,
        }

    @staticmethod
    def get_env_list():
        """
        获取历史
        :return:
        """
        try:
            # res_list = Auto.query.order_by(desc(Auto.id)).all()
            res_list = db.session.query(Env).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取环境失败"
