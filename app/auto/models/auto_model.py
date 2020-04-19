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


class Auto(db.Model):
    """
    自动化
    """

    __tablename__ = 'autotest'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False)
    environment = db.Column(db.String(255), nullable=False)
    run_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    result = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    job_num = db.Column(db.String(255), nullable=False)
    report = db.Column(db.String(255), nullable=False)
    run_label = db.Column(db.String(255), nullable=False)
    uuid = db.Column(db.String(255), nullable=False)
    commit = db.Column(db.String(255), nullable=False)
    console = db.Column(db.String(255), nullable=False)

    def __init__(self, operator, environment, run_time, job_num, result, detail, report, run_label, uuid, commit,
                 console):
        self.operator = operator
        self.environment = environment
        self.run_time = run_time
        self.result = result
        self.detail = detail
        self.job_num = job_num
        self.report = report
        self.run_label = run_label
        self.uuid = uuid
        self.commit = commit
        self.console = console

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "environment": self.environment,
            "run_time": self.run_time,
            "result": self.result,
            "detail": self.detail,
            "job_num": self.job_num,
            "report": self.report,
            "run_label": self.run_label,
            "uuid": self.uuid,
            "commit": self.commit,
            "console": self.console,
        }

    @staticmethod
    def create(operator, environment, run_time, job_num, result, detail, report, run_label, uuid, commit, console):

        res = Auto(operator, environment, run_time, job_num, result, detail, report, run_label, uuid, commit, console)

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
    def get_auto_list():
        """
        获取历史
        :return:
        """
        try:
            # res_list = Auto.query.order_by(desc(Auto.id)).all()
            res_list = db.session.query(Auto).order_by(desc(Auto.id)).all()

            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.run_time is not None and isinstance(res.run_time, str) is False:
                    res.run_time = res.run_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def update_job_by_num(num, operator, run_time, result, report, run_label, uuid, console):
        res = Auto.query.filter_by(job_num=num).first()
        print("数据库数据为：%s" % res)
        if res:
            res.operator = operator
            res.run_time = run_time
            res.result = result
            res.report = report
            res.run_label = run_label
            res.uuid = uuid
            res.console = console
            db.session.add(res)
            db.session.commit()
            db.session.close()

    @staticmethod
    def get_info(num):
        res1 = Auto.query.filter_by(job_num=num).first()
        db.session.close()
        if isinstance(res1.run_time, str) is False:
            res1.run_time = res1.run_time.strftime('%Y-%m-%d %H:%M:%S')
        return res1.to_json()


class Label(db.Model):
    """
    自动化
    """

    __tablename__ = 'autotest_label'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    label_name = db.Column(db.String(25), nullable=False)
    label_commit = db.Column(db.String(255), nullable=False)
    label_owner = db.Column(db.String(255), nullable=False)

    def __init__(self, label_name, label_commit, label_owner):
        self.label_name = label_name
        self.label_commit = label_commit
        self.label_owner = label_owner

    def to_json(self):
        return {
            "id": self.id,
            "label_name": self.label_name,
            "label_commit": self.label_commit,
            "label_owner": self.label_owner,
        }

    @staticmethod
    def create(label_name, label_commit, label_owner):

        res = Label(label_name, label_commit, label_owner)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_label_list():
        """
        获取历史
        :return:
        """
        try:
            res_list = db.session.query(Label).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"


if __name__ == '__main__':
    operator = 'liuchunfu'
    run_env = 'r1'
    run_time = ''
    result = '1'
    # Auto.create(operator, run_env, run_time, result, 1, 1, 1, '12312', "")
    Auto.get_info(53)
