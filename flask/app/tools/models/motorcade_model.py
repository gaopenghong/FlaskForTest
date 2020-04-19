#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2019 / 10 / 25

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


class MotorcadeTestData(db.Model):
    """
    创建车队测试数据
    """
    __tablename__ = 'motorcade_test_data'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    operator = db.Column(db.String(25), nullable=False, comment='操作人')
    environment = db.Column(db.String(25), nullable=False, comment='环境')
    mobile = db.Column(db.String(25), nullable=False, comment='手机号')
    customerMobile = db.Column(db.String(25), nullable=False, comment='货主账号')
    adminMobile = db.Column(db.String(25), nullable=False, comment='后台账号')
    motorcadeMobile = db.Column(db.String(25), nullable=False, comment='车队账号')
    driverMobile = db.Column(db.String(25), nullable=False, comment='司机账号')
    databaseName = db.Column(db.String(25), nullable=False, comment='数据库名称')
    code = db.Column(db.String(25), nullable=False, comment='验证码')
    transportType = db.Column(db.String(25), nullable=False, comment='运力类型')
    lineRouteId = db.Column(db.String(25), nullable=False, comment='项目线路id')
    startPlace = db.Column(db.String(255), nullable=False, comment='始发地')
    stopPlace = db.Column(db.String(255), nullable=False, comment='经停点')
    endPlace = db.Column(db.String(255), nullable=False, comment='目的地')
    orderSn = db.Column(db.String(25), nullable=False, comment='运单号')
    billNo = db.Column(db.String(25), nullable=False, comment='结算批次号')
    testData = db.Column(db.String(25), nullable=False, comment='数据类型')
    status = db.Column(db.String(25), nullable=False, comment='状态')
    lineId = db.Column(db.String(25), nullable=False, comment='福佑线路id')
    appType = db.Column(db.String(25), nullable=False, comment='推送终端')
    msgType = db.Column(db.String(25), nullable=False, comment='消息类型')
    showType = db.Column(db.String(25), nullable=False, comment='展示方式')
    imgType = db.Column(db.String(25), nullable=False, comment='图片类型')
    result = db.Column(db.String(255), nullable=False, comment='执行结果')
    functionName = db.Column(db.String(255), nullable=False, comment='工具名')
    operatorTime = db.Column(db.DateTime, nullable=False, default=datetime.now(), comment='操作时间')

    def __init__(self, operator, environment, customer_mobile, admin_mobile, motorcade_mobile, driver_mobile,
                 start_place,
                 stop_place, end_place, order_sn, bill_no, test_data, database_name, code, status, transport_type,
                 mobile, line_route_id, line_id, app_type, msg_type, show_type, img_type, result, operator_time,
                 function_name):
        self.operator = operator
        self.environment = environment
        self.customerMobile = customer_mobile
        self.adminMobile = admin_mobile
        self.motorcadeMobile = motorcade_mobile
        self.driverMobile = driver_mobile
        self.startPlace = start_place
        self.stopPlace = stop_place
        self.endPlace = end_place
        self.orderSn = order_sn
        self.billNo = bill_no
        self.testData = test_data
        self.status = status
        self.operatorTime = operator_time
        self.databaseName = database_name
        self.code = code
        self.transportType = transport_type
        self.mobile = mobile
        self.lineRouteId = line_route_id
        self.lineId = line_id
        self.customerMobile = customer_mobile
        self.result = result
        self.appType = app_type
        self.msgType = msg_type
        self.showType = show_type
        self.imgType = img_type
        self.functionName = function_name

    def to_json(self):
        return {
            "id": self.id,
            "operator": self.operator,
            "environment": self.environment,
            "customerMobile": self.customerMobile,
            "adminMobile": self.adminMobile,
            "motorcadeMobile": self.motorcadeMobile,
            "driverMobile": self.driverMobile,
            "startPlace": self.startPlace,
            "stopPlace": self.stopPlace,
            "endPlace": self.endPlace,
            "orderSn": self.orderSn,
            "billNo": self.billNo,
            "testData": self.testData,
            "status": self.status,
            "operatorTime": self.operatorTime,
            "mobile": self.mobile,
            "databaseName": self.databaseName,
            "code": self.code,
            "transportType": self.transportType,
            "lineRouteId": self.lineRouteId,
            "lineId": self.lineId,
            "result": self.result,
            "appType": self.appType,
            "msgType": self.msgType,
            "showType": self.showType,
            "imgType": self.imgType,
        }

    @staticmethod
    def create(operator='', environment='', customer_mobile='', admin_mobile='', motorcade_mobile='',
               driver_mobile='',
               start_place='',
               stop_place='', end_place='', order_sn='', bill_no='', test_data='', database_name='',
               code='', status='',
               transport_type='',
               mobile='', line_route_id='', line_id='', app_type='', msg_type='', show_type='',
               img_type='', result='',
               operator_time='', function_name=''):
        print(operator, environment, customer_mobile, admin_mobile, motorcade_mobile, driver_mobile,
              start_place,
              stop_place, end_place, order_sn, bill_no, test_data, database_name, code, status, transport_type,
              mobile, line_route_id, line_id, app_type, msg_type, show_type, img_type, result, operator_time,
              function_name)
        res = MotorcadeTestData(operator, environment, customer_mobile, admin_mobile, motorcade_mobile, driver_mobile,
                                start_place,
                                stop_place, end_place, order_sn, bill_no, test_data, database_name, code, status,
                                transport_type,
                                mobile, line_route_id, line_id, app_type, msg_type, show_type, img_type, result,
                                operator_time, function_name)

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
    def get_motorcade_data_list():
        """
        获取车队测试数据历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '车队主要测试数据').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def select_check_code_list():
        """
        获取查询验证码历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '查询验证码').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def select_create_fy_line_list():
        """
        获取创建福佑线路历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '创建福佑线路').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def get_fy_driver_data_list():
        """
        获取固定司机历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '固定司机成单流程').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def get_push_messages_list():
        """
        获取推送消息历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '消息推送').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"

    @staticmethod
    def get_motorcade_contract_list():
        """
        获取车队合同历史
        :return:
        """
        try:
            res_list = MotorcadeTestData.query.filter(MotorcadeTestData.functionName == '车队合同').order_by(
                desc(MotorcadeTestData.id)).all()
            db.session.close()
            res_json_list = []
            for res in res_list:
                # print(res.to_json())
                if res.operatorTime is not None and isinstance(res.operatorTime, str) is False:
                    res.operatorTime = res.operatorTime.strftime('%Y-%m-%d %H:%M:%S')
                res_json_list.append(res.to_json())
            print(res_json_list)
            return json.dumps(res_json_list)
        except Exception as e:
            current_app.logger.error(e)
            return "获取历史失败"


db.create_all()
# if __name__ == '__main__':
#     res = CreateAgentTestData()
#     r = res.get_agent_data_list()
#     print(r)
