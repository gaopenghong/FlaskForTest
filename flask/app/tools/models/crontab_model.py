#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator

__author__ = 'guobaohui'
__time__ = 2019 / 11 / 11

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


class CrontabInfo(db.Model):
    """定时任务"""
    __tablename__ = 'crontab_info'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, index=True)
    run_name = db.Column(db.String(25), nullable=False, index=True)
    run_type = db.Column(db.String(25), nullable=False, index=True)
    run_date = db.Column(db.Date, nullable=True, index=True)
    run_time = db.Column(db.Time, nullable=False, index=True)
    start_week = db.Column(db.String(25), nullable=True, index=True)
    end_week = db.Column(db.String(25), nullable=True, index=True)
    job_content = db.Column(db.String(250), nullable=False, index=True)
    robot_key = db.Column(db.String(50), nullable=False, index=True)
    opt_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    job_status = db.Column(db.String(25), nullable=False, index=True)
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, operator, run_name, run_type, run_date, run_time, start_week,
                 end_week, job_content, robot_key, opt_time, job_status, update_time):
        self.operator = operator
        self.run_name = run_name
        self.run_type = run_type
        self.run_date = run_date
        self.run_time = run_time
        self.start_week = start_week
        self.end_week = end_week
        self.job_content = job_content
        self.robot_key = robot_key
        self.opt_time = opt_time
        self.job_status = job_status
        self.update_time = update_time

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "run_name": self.run_name,
            "run_type": self.run_type,
            "run_date": self.run_date,
            "run_time": self.run_time,
            "start_week": self.start_week,
            "end_week": self.end_week,
            "job_content": self.job_content,
            "robot_key": self.robot_key,
            "opt_time": self.opt_time,
            "job_status": self.job_status,
            "update_time": self.update_time,
        }

    @staticmethod
    def create(operator: object, run_name: object, run_type: object, run_date: object,
               run_time: object, start_week: object, end_week: object, job_content: object,
               robot_key: object, opt_time: object, job_status: object, update_time: object) -> object:
        res = CrontabInfo(operator, run_name, run_type, run_date, run_time, start_week, end_week,
                          job_content, robot_key, opt_time, job_status, update_time)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def del_crontab(task_id):
        """
        逻辑删除指定定时任务
        """
        res = CrontabInfo.query.filter(CrontabInfo.id == task_id).first()
        res.job_status = "deleted"
        try:
            # db.session.delete(res)
            db.session.commit()
            db.session.close()
            return "删除成功"
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "删除失败"

    @staticmethod
    def run_crontab(task_id):
        """
        运行指定定时任务
        """
        res = CrontabInfo.query.filter(CrontabInfo.id == task_id).first()
        # res.job_status = "open"
        try:
            db.session.commit()
            db.session.close()
            return "操作成功"
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "操作失败"

    @staticmethod
    def get_crontab_list():
        """
        获取定时任务列表
        :return:
        """
        try:
            res_list = CrontabInfo.query.order_by(desc(CrontabInfo.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                if res.opt_time is not None and isinstance(res.opt_time, str) is False:
                    res.opt_time = res.opt_time.strftime('%Y-%m-%d %H:%M:%S')
                    res.update_time = res.update_time.strftime('%Y-%m-%d %H:%M:%S')
                    res.run_time = res.run_time.strftime('%H:%M:%S')
                elif str(res.run_date) != "None" and isinstance(res.run_date, str) is False:
                    res.run_date = res.run_date.strftime('%Y-%m-%d')
                res_json_list.append(res.to_json())
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败", str(e)


# if __name__ == '__main__':
#     d = CrontabInfo.del_crontab("1")
#     print(d)
