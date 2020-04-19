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
from app.util.ssh_conf import remote_database

config_name = 'testing'
app = create_app(config_name)

db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


class Fchatrecord(db.Model):
    """
    智能客服执行结果记录
    """

    __tablename__ = 'algorithm_test_records'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    run_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    run_result = db.Column(db.String(255), nullable=False)

    def __init__(self, operator, type, run_time, run_result):
        self.operator = operator
        self.type = type
        self.run_time = run_time
        self.run_result = run_result

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "type": self.type,
            "run_time": self.run_time,
            "run_result": self.run_result,
        }

    @staticmethod
    def create(operator, type, run_time, run_result):
        res = Fchatrecord(operator, type, run_time, run_result)

        try:
            db.session.add(res)
            db.session.flush()
            record_id = res.id
            db.session.commit()
            db.session.close()
            return record_id
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_fchatrecord_list():
        """
        获取历史记录
        :return:
        """
        try:
            res_list = db.session.query(Fchatrecord).order_by(desc(Fchatrecord.id)).all()

            res_json_list = []
            for res in res_list:
                if res.run_time is not None and isinstance(res.run_time, str) is False:
                    res.run_time = res.run_time.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

class Fchatstatic(db.Model):
    """
    指标详情
    """

    __tablename__ = 'algorithm_test_statistics'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    record_id = db.Column(db.String(25), nullable=False)
    coverage = db.Column(db.String(255), nullable=False)
    accuracy = db.Column(db.String(255), nullable=False)
    precision = db.Column(db.String(255), nullable=False)
    recall = db.Column(db.String(255), nullable=False)
    f_measure = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, coverage, accuracy, precision,recall,f_measure):
        self.record_id = record_id
        self.coverage = coverage
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f_measure = f_measure

    def to_json(self):
        return {
            "id": self.id,
            "record_id": self.record_id,
            "coverage": self.coverage,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f_measure": self.f_measure,
        }

    @staticmethod
    def create_static(record_id, coverage, accuracy, precision,recall,f_measure):
        res = Fchatstatic(record_id, coverage, accuracy, precision,recall,f_measure)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_fchatstatic_list(ida):
        """
        获取历史记录
        :return:
        """
        try:
            #res_list = db.session.query(Fchatstatic).order_by(desc(Fchatstatic.id)).all()
            res_list = db.session.query(Fchatstatic).filter_by(record_id=ida).order_by(desc(Fchatstatic.id)).all()

            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

class Fchatdetail(db.Model):
    """
    数据详情
    """

    __tablename__ = 'algorithm_test_case_im'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    test_corpus = db.Column(db.String(255), nullable=False)
    match_corpus = db.Column(db.String(255), nullable=False)
    exact_intention = db.Column(db.String(255), nullable=False)
    hit_intention = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)

    def __init__(self, test_corpus, match_corpus, exact_intention, hit_intention,result):
        self.test_corpus = test_corpus
        self.match_corpus = match_corpus
        self.exact_intention = exact_intention
        self.hit_intention = hit_intention
        self.result = result

    def to_json(self):
        return {
            "id": self.id,
            "test_corpus": self.test_corpus,
            "match_corpus": self.match_corpus,
            "exact_intention": self.exact_intention,
            "hit_intention": self.hit_intention,
            "result": self.result,
        }

    @staticmethod
    def create_detail(test_corpus, match_corpus, exact_intention, hit_intention,result):
        res = Fchatdetail(test_corpus, match_corpus, exact_intention, hit_intention,result)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_fchatdetail_list():
        """
        获取历史记录
        :return:
        """
        try:

            res_list = db.session.query(Fchatdetail).order_by(desc(Fchatdetail.id)).all()
            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

class Fchatexactstatic(db.Model):
    """
    指标详情
    """

    __tablename__ = 'algorithm_fchatexact_statistics'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    record_id = db.Column(db.String(25), nullable=False)
    intention_exact = db.Column(db.String(255), nullable=False)
    coverage_exact = db.Column(db.String(255), nullable=False)
    accuracy_exact = db.Column(db.String(255), nullable=False)
    precision_exact = db.Column(db.String(255), nullable=False)
    recall_exact = db.Column(db.String(255), nullable=False)
    f_measure_exact = db.Column(db.String(255), nullable=False)

    def __init__(self, record_id, intention_exact,coverage_exact, accuracy_exact, precision_exact,recall_exact,f_measure_exact):
        self.record_id = record_id
        self.intention_exact = intention_exact
        self.coverage_exact = coverage_exact
        self.accuracy_exact = accuracy_exact
        self.precision_exact = precision_exact
        self.recall_exact = recall_exact
        self.f_measure_exact = f_measure_exact

    def to_json(self):
        return {
            "id": self.id,
            "record_id": self.record_id,
            "intention_exact": self.intention_exact,
            "coverage_exact": self.coverage_exact,
            "accuracy_exact": self.accuracy_exact,
            "precision_exact": self.precision_exact,
            "recall_exact": self.recall_exact,
            "f_measure_exact": self.f_measure_exact,
        }

    @staticmethod
    def create_exactstatic(record_id,intention_exact, coverage_exact, accuracy_exact, precision_exact,recall_exact,f_measure_exact):
        res = Fchatexactstatic(record_id, intention_exact, coverage_exact, accuracy_exact, precision_exact,recall_exact,f_measure_exact)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_fchatexact_list(ida):
        """
        获取历史记录
        :return:
        """
        try:
            #res_list = db.session.query(Fchatexactstatic).order_by(desc(Fchatexactstatic.id)).all()
            res_list = db.session.query(Fchatexactstatic).filter_by(record_id=ida).order_by(desc(Fchatexactstatic.id)).all()

            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"

class Fchatintention(db.Model):
    """
    指标详情
    """

    __tablename__ = 'algorithm_fchat_intention'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    icId = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    remark = db.Column(db.String(255), nullable=False)
    userId = db.Column(db.String(255), nullable=False)
    userName = db.Column(db.String(255), nullable=False)
    createTime = db.Column(db.String(255), nullable=False)
    updateTime = db.Column(db.String(255), nullable=False)

    def __init__(self, icId, name,remark, userId, userName,createTime,updateTime):
        self.icId = icId
        self.name = name
        self.remark = remark
        self.userId = userId
        self.userName = userName
        self.createTime = createTime
        self.updateTime = updateTime

    def to_json(self):
        return {
            "id": self.id,
            "icId": self.icId,
            "name": self.name,
            "remark": self.remark,
            "userId": self.userId,
            "userName": self.userName,
            "createTime": self.createTime,
            "updateTime": self.updateTime,
        }

    @staticmethod
    def create_fchatintention(icId,name, remark, userId, userName,createTime,updateTime):
        res = Fchatintention(icId, name, remark, userId, userName,createTime,updateTime)

        try:
            db.session.add(res)
            db.session.commit()
            db.session.close()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return "入库失败"

    @staticmethod
    def get_fchatintention_list():
        """
        获取历史记录
        :return:
        """
        try:
            res_list = db.session.query(Fchatintention).order_by(desc(Fchatintention.id)).all()
            res_json_list = []
            for res in res_list:
                res_json_list.append(res.to_json())
            db.session.close()
            return json.dumps(res_json_list)
            print(res_json_list)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return "获取历史失败"




if __name__ == '__main__':
    Fchatdetail.get_fchatdetail_list()
