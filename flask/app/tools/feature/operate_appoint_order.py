#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/30 10:43 AM 
# @Author : zhangjian
# @File : operate_appoint_order.py

from app.tools.api.api_xcusotmer_app import *
from app.tools.api.api_customer_app import ApiCustomerApp
from app.tools.api.api_bms import *
from app.tools.api.api_crm import *
from app.tools.api.api_customer_pc import *
from app.tools.api.api_dispatch import *
from app.tools.api.api_service import *
from app.tools.api.api_turing import *
from app.tools.api.api_driver import *
from app.tools.api.api_finance import *
from app.tools.api.api_agent import *
from app.tools.feature.driver_withdraw import *
from app.tools.feature.add_driver import *


# 运单指定操作
class OperateAppointOrder(ApiXcustomerAPP, ApiCustomerApp, ApiBms, ApiCrm, ApiCustomerPC, ApiDispatch, ApiService,
                          ApiTuring, ApiFinance,
                          ApiAgent, ApiDriver, ApiAutoQuery):
    """
        sch_type 运单类型：0-默认, 1-统调, 2-一口价试点
        transportType 运力类型：0-其他，1-自营运力,2-企业运力，3-固定司机
        order_status 运单状态：1-运单已取消, 2-待审核, 3-审核通过, 4-待报价, 6-已报价, 7-待客户确认,
        order_status 运单状态：8-待货主付款, 9-货主已付款, 10-客户已下单, 11-待智能调度安排司机, 12-已推送,
        order_status 运单状态：13-经纪人报价收集中, 14-竞价结束,经纪人已经中标, 15-待安排司机, 16-已安排司机, 17-待发车,
        order_status 运单状态：18-确认发车, 19-卸货完成, 21-待签收, 22-已签收, 23-已完成, 24-付款审核中
    """

    def __init__(self, environment, order_sn, status):
        super().__init__(environment)
        self.status = status
        self.order_sn = order_sn
        self.admin_mobile = '16888888888'
        self.admin_password = 'Ab@123456789'
        # 管理员登录
        r_ua_request_id = self.ua_generate_check_code()
        self.cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        print('cookies_ua-----', self.cookies_ua)
        # bms运单详情
        self.order_detail = self.bms_order_detail(order_sn, self.cookies_ua)
        print('r_order_detail-----', self.order_detail)
        self.order_status = self.order_detail['data'][0]['quote']['status']
        # 运力账号
        if 'orderBroker' in self.order_detail['data'][0]:
            self.agent_mobile = self.order_detail['data'][0]['orderBroker']['brokerMobile']
        else:
            self.agent_mobile = ''
            print('请确认运单状态')
        # if self.status == '0':
        #     self.operate_service_order_check()

    def operate_service_order_check(self):
        """初审"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['statusCus']
            if quote_status == 1:
                # 获取管理员信息
                r_service_admin_info = self.service_sys_admin_info(self.cookies_ua)
                if 'code' not in str(r_service_admin_info['status']):
                    return '获取管理员信息接口错误：%s' % r_service_admin_info
                elif r_service_admin_info['status']['code'] != 0:
                    return '获取管理员信息接口失败：%s' % r_service_admin_info
                print('管理员信息: %s' % r_service_admin_info)
                admin_id = r_service_admin_info['property']['user']['id']
                admin_name = r_service_admin_info['property']['user']['name']
                # 查询任务
                r_tasks = self.service_task_search(self.cookies_ua, order_sn=self.order_sn)
                if 'code' not in str(r_tasks['status']):
                    return '查询任务接口错误：%s' % r_tasks
                elif r_tasks['status']['code'] != 0:
                    return '查询任务接口失败：%s' % r_tasks
                print('查询所有任务: %s' % r_tasks)
                # 开启接单
                r_service_open = self.service_sys_update_user_status(1, self.cookies_ua)
                if 'code' not in str(r_service_open['status']):
                    return '开启接单接口错误：%s' % r_service_open
                elif r_service_open['status']['code'] != 0:
                    return '开启接单接口失败：%s' % r_service_open
                print('服务系统开启接单: %s' % r_service_open)

                task_id = r_tasks['data'][0]['id']
                task_sn = r_tasks['data'][0]['taskSn']
                task_type = r_tasks['data'][0]['taskTypeId']
                task_name = r_tasks['data'][0]['name']
                print('任务编号: %s, 任务类型: %s, 任务名称: %s' % (task_sn, task_type, task_name))

                # 重新分配任务
                r_service_task_dispatch = self.service_task_dispatch(self.cookies_ua, task_id, admin_name, admin_id)
                print('任务重新分配: %s' % r_service_task_dispatch)
                if 'code' not in str(r_service_task_dispatch['status']):
                    return '任务重新分配接口错误：%s' % r_service_task_dispatch
                elif r_service_task_dispatch['status']['code'] != 0:
                    if '不能是原分配人' not in r_service_task_dispatch['status']['desc']:
                        return '任务分配异常：%s' % r_service_task_dispatch['status']['desc']

                # 获取任务详情
                r_service_task_detail = self.service_task_detail(task_sn, self.cookies_ua)
                print('任务详情: %s' % r_service_task_detail)
                if 'code' not in str(r_service_task_detail['status']):
                    return '任务详情接口错误：%s' % r_service_task_detail
                elif r_service_task_detail['status']['code'] != 0:
                    return '任务详情接口异常：%s' % r_service_task_detail['status']['desc']

                task_detail = r_service_task_detail['data'][0]
                task_detail_1 = dict()
                if len(r_service_task_detail['data'][0]['stopPointsInfo']) == 0:
                    pass
                else:
                    plan_time = int(time.time()) * 1000
                    for point_info in r_service_task_detail['data'][0]['stopPointsInfo']:
                        point_info['id'] = point_info['stopPointId']
                        if 'planInTime' in point_info:
                            plan_time = point_info['planInTime'] + 3600000  # 发车时间增加1小时
                        else:
                            point_info['planInTime'] = plan_time
                            plan_time = point_info['planInTime'] + 3600000
                        if 'planOutTime' in point_info:
                            plan_time = point_info['planOutTime']
                        else:
                            point_info['planOutTime'] = plan_time
                            plan_time += 86400000  # 到达时间增加一天
                task_detail_1['quoteInfo'] = {
                    'goodsName': task_detail['baseInfo']['goodsName'],
                    'goodsWeight': task_detail['baseInfo']['goodsWeight'],
                    'goodsCubage': task_detail['baseInfo']['goodsCubage'],
                    'goodsNum': task_detail['baseInfo']['goodsNum'],
                    'carLengthId': task_detail['baseInfo']['carLengthId'],
                    'carModelId': task_detail['baseInfo']['carModelId'],
                    'quoteCreateTime': task_detail['queryBaseInfo']['createTime'],
                }
                task_detail_1['loadingInfo'] = task_detail['loadingInfo']
                task_detail_1['stopPointsInfo'] = task_detail['stopPointsInfo']
                task_detail_1['otherInfo'] = task_detail['otherInfo']
                task_detail_1['otherInfo']['checkComments'] = ''
                check_data = task_detail_1

                r_service_task_check = self.service_task_check_pass(task_id, data_json=check_data,
                                                                    cookies=self.cookies_ua)
                print('初审通过：%s' % r_service_task_check)
                if 'code' not in str(r_service_task_check['status']):
                    return '任务初审接口错误：%s' % r_service_task_detail
                elif r_service_task_check['status']['code'] != 0:
                    return '任务初审接口异常：%s' % r_service_task_check['status']['desc']

                r_service_close = self.service_sys_update_user_status(0, self.cookies_ua)
                print('服务系统关闭接单: %s' % r_service_close)
                return '操作成功'
            else:
                return "当前运单状态不支持初审"
        except Exception as e:
            return e

    def operate_turing_offer_price(self):
        """报价"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            if quote_status == 4:
                turing_price_result = self.turing_price_to_order_core_quickly(self.order_sn)
                if 'code' not in str(turing_price_result['status']):
                    return '图灵报价接口错误：%s' % turing_price_result
                elif turing_price_result['status']['code'] == 0:
                    return turing_price_result['status']['desc']
                else:
                    return '图灵报价接口异常：%s' % turing_price_result['status']['desc']
            else:
                return '当前运单状态不支持图灵报价'
        except Exception as e:
            return e

    def operate_base_order_confirm(self):
        """确认下单"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            mobile_customer = self.order_detail['data'][0]['businessInfo']['customerMobile']
            len_points = len(self.order_detail['data'][0]['stopPoints'])
            if quote_status == 7:
                login_result = self.customer_app_token(mobile_customer)
                if 'code' not in str(login_result['status']):
                    return '货主登录接口异常：%s' % login_result
                elif login_result['status']['code'] == 0:
                    customer_token = login_result['data'][0]['token']
                else:
                    return '货主登录异常：%s' % login_result['status']['desc']
                customer_confirm = self.customer_app_order_confirm(customer_token, self.order_sn, len_points)
                if 'code' not in str(customer_confirm['status']):
                    return '货主确认下单接口错误：%s' % login_result
                elif customer_confirm['status']['code'] == 0:
                    return customer_confirm['status']['desc']
                else:
                    return '货主确认下单异常：%s' % customer_confirm['status']['desc']
            else:
                return "当前运单状态不支持确认下单"
        except Exception as e:
            return e

    def operate_online_pay_check(self):
        """在线支付及审核"""
        try:
            order_status = self.order_detail['data'][0]['orderBase']['orderStatus']
            if order_status == 8:
                mobile_customer = self.order_detail['data'][0]['businessInfo']['customerMobile']
                # 货主登录
                login_result = self.customer_app_token(mobile_customer)
                if 'code' not in str(login_result['status']):
                    return '货主登录接口异常：%s' % login_result
                elif login_result['status']['code'] == 0:
                    token_customer = login_result['data'][0]['token']
                else:
                    return '货主登录异常：%s' % login_result['status']['desc']

                # 货主线下支付
                pay_result = self.customer_app_confirm_transferaccounts(self.order_sn, token=token_customer)
                if 'code' not in str(pay_result['status']):
                    return '线下转账接口错误：%s' % pay_result
                elif pay_result['status']['code'] != 0:
                    return '货主线下转账失败，%s' % pay_result['status']['desc']
                else:
                    # 财务线下支付审核
                    check_result = fiance_pay_online_check(self.env, self.order_sn, self.cookies_ua)
                    if 'code' not in str(check_result['status']):
                        return '财务审核接口错误：%s' % check_result
                    elif check_result['status']['code'] != 0:
                        return '财务线下转账审核失败: %s' % check_result['status']['desc']
                    else:
                        return '操作成功'
            else:
                return "当前运单状态不支持支付"
        except Exception as e:
            return e

    def operate_order_arrange_driver(self):
        """安排司机"""
        try:
            order_status = self.order_detail['data'][0]['quote']['status']
            if order_status == 15:
                transport_type = self.order_detail['data'][0]['businessInfo']['transportType']
                sch_type = self.order_detail['data'][0]['businessInfo']['schType']
                agent_mobile = self.order_detail['data'][0]['orderBroker']['brokerMobile']
                order_free = self.order_detail['data'][0]['finance']['cusTotalFee']
                driver_mobile = AddDriver(self.env).add_driver_1(1, '121')
                if transport_type == 1:
                    r_driver_info = self.dispatch_get_driver_info(driver_mobile, self.cookies_ua)
                    if 'code' not in str(r_driver_info['status']):
                        return '调度系统获取司机信息错误：%s' % r_driver_info
                    elif r_driver_info['status']['code'] != 0:
                        return '调度系统获取司机信息失败：%s' % r_driver_info
                    print('调度系统获取司机信息: %s' % r_driver_info)

                    r_dispatch_info = self.dispatch_get_all_scheduler_orders(self.cookies_ua,
                                                                             {'orderSns': self.order_sn})  # 获取调度列表
                    if 'code' not in str(r_dispatch_info['status']):
                        return '获取调度列表错误：%s' % r_dispatch_info
                    elif r_dispatch_info['status']['code'] != 0:
                        return '获取调度列表失败：%s' % r_dispatch_info
                    dispatch_bind_list = self.dispatch_bind_agent_list(self.cookies_ua)  # 获取调度绑定列表
                    if 'code' not in str(dispatch_bind_list['status']):
                        return '获取调度绑定列表错误：%s' % dispatch_bind_list
                    elif dispatch_bind_list['status']['code'] != 0:
                        return '获取调度绑定列表失败：%s' % dispatch_bind_list
                    dispatch_admin_list = []
                    for dispatch_bind_info in dispatch_bind_list['data']:
                        dispatch_admin_list.append(dispatch_bind_info['adminMobile'])
                    # 一口价运单或管理员未绑定经纪人
                    if sch_type == 2 or str(self.admin_mobile) not in dispatch_admin_list:
                        admin_dispatch_mobile = r_dispatch_info['data'][0]['brokerMap']['adminMobile']
                        print('调度管理员账号：%s' % admin_dispatch_mobile)
                        request_id = self.ua_generate_check_code()
                        for password in ['Ab@123456789', 'Fy@123456789']:
                            cookies_ua = self.ua_login(admin_dispatch_mobile, password, request_id)
                            if cookies_ua:
                                break
                        if not cookies_ua:
                            return '管理员账号%s获取cookies失败，请检查数据配置' % admin_dispatch_mobile
                    # 查询司机承运中的运单并异常修改卸货完成
                    order_unload_for_driver_free(self.env, self.cookies_ua,
                                                 driver_mobile=r_driver_info['data'][0]['driverMobile'])
                    r_arrange_driver = self.dispatch_arrange_driver(self.order_sn, r_driver_info['data'][0],
                                                                    self.cookies_ua, order_free * 0.8, 0)
                    print('调度系统安排司机: %s' % r_arrange_driver)
                    if 'code' not in str(r_arrange_driver['status']):
                        return '调度安排司机接口错误：%s' % r_arrange_driver
                    else:
                        return r_arrange_driver['status']['desc']

                elif transport_type == 0:
                    r_agent_login = self.agent_app_login(agent_mobile)
                    agent_token = r_agent_login['token']
                    r_driver_info = self.agent_driver_detail(agent_token, driver_mobile)
                    if 'code' not in str(r_driver_info['status']):
                        return '车队获取司机信息错误：%s' % r_driver_info
                    elif r_driver_info['status']['code'] != 0:
                        return '车队获取司机信息失败：%s' % r_driver_info
                    print('经纪人获取司机信息: %s' % r_driver_info)
                    # 查询司机承运中的运单并异常修改卸货完成
                    order_unload_for_driver_free(self.env, self.cookies_ua, r_driver_info['data'][0]['mobile'])
                    # 车队安排司机
                    r_arrange_driver = self.agent_order_arrange_driver(agent_token, self.order_sn,
                                                                       driver_info=r_driver_info['data'][0])
                    print('经纪人安排司机: %s' % r_arrange_driver)
                    if 'code' not in str(r_arrange_driver['status']):
                        return '车队安排司机接口错误：%s' % r_arrange_driver
                    else:
                        return r_arrange_driver['status']['desc']
            else:
                return "当前运单状态不支持安排司机"
        except Exception as e:
            return e

    def operate_dispatch_check_driver(self):
        """调度确认司机符合/不符合"""
        pass

    def operate_driver_order_make_point_one(self):
        """运单打点（单个）"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            order_point_length = len(self.order_detail["data"][0]["stopPoints"])
            if quote_status == 16 or quote_status == 17 or quote_status == 18:  # 已安排司机/待发车/确认发车
                driver_mobile = self.order_detail['data'][0]['orderDriver']['driverMobile']
                login_driver = ApiDriver(self.env).driver_login(driver_mobile, check_code='1123')
                driver_token = login_driver['data'][0]['token']
                for i in range(order_point_length * 2):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, self.order_sn)
                    print("订单号：%s，司机打点：%s" % (self.order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            else:
                return "当前运单状态无法打点！"
        except Exception as e:
            return e

    def operate_driver_order_make_point_all(self):
        """运单打点（全部）"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            order_point_length = len(self.order_detail["data"][0]["stopPoints"])
            if quote_status == 16 or quote_status == 17 or quote_status == 18:  # 已安排司机/待发车/确认发车
                driver_mobile = self.order_detail['data'][0]['orderDriver']['driverMobile']
                login_driver = ApiDriver(self.env).driver_login(driver_mobile, check_code='1123')
                driver_token = login_driver['data'][0]['token']
                for i in range(order_point_length * 2):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, self.order_sn)
                    print("订单号：%s，司机打点：%s" % (self.order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            else:
                return "当前运单状态无法打点"
        except Exception as e:
            return e

    def operate_unload_for_driver_free(self):
        """卸货完成"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            if quote_status == 18:  # 确认发车
                bms_order_sign = self.bms_order_exception(self.order_sn, 12, 'ftest运单卸货完成',
                                                          cookies_bms=self.cookies_ua)  # 12-异常修改司机卸货完成
                print("订单号：%s，异常修改司机卸货完成：%s" % (self.order_sn, bms_order_sign))
                return bms_order_sign
            else:
                return "当前运单状态无法操作卸货"
        except Exception as e:
            return e

    def operate_order_sign(self):
        """签收"""
        try:
            quote_status = self.order_detail['data'][0]['quote']['status']
            if quote_status == 21:  # 待签收
                bms_order_sign = self.bms_order_exception(self.order_sn, 13, 'ftest运单签收',
                                                          cookies_bms=self.cookies_ua)  # 13-异常修改签收
                print("订单号：%s，异常修改签收：%s" % (self.order_sn, bms_order_sign))
                return bms_order_sign
            else:
                return "当前运单状态无法签收"
        except Exception as e:
            return e

    def operate_dispatch_confirm_order(self):
        """调度确认运单"""
        try:
            order_detail = self.order_detail['data'][0]
            if self.agent_mobile == '':
                return "请确认运单" + str(self.order_sn) + "的状态"
            else:
                operate_r = self.dispatch_bind_agent_list(self.cookies_ua, mobile=self.agent_mobile)
            print(operate_r)
            if 'data' in operate_r:
                dd_admin_mobile = operate_r['data'][0]['adminMobile']
                r_ua_request_id = self.ua_generate_check_code()
                dd_cookies_ua = self.ua_login(dd_admin_mobile, self.admin_password, r_ua_request_id)
                print('cookies_ua-----', dd_cookies_ua)
            else:
                return "请确认运单" + str(self.order_sn) + "的状态"
            if 'orderDriver' in order_detail:
                driver_id = order_detail['orderDriver']['driverId']
            else:
                return "请确认运单" + str(self.order_sn) + "的状态"
            operate_r = self.dispatch_confirm_order(driver_id, self.order_sn, dd_cookies_ua)
            return operate_r
        except Exception as e:
            return e

    def operate_upload_receipt(self):
        """上传回单并审核中"""
        try:
            order_detail = self.order_detail['data'][0]
            if order_detail['orderBroker']['openInvoice'] == 1:
                r_agent_login = self.agent_app_login()
                agent_token = r_agent_login['data'][0]['token']
                operate_r = self.agent_upload_receipt(agent_token, self.order_sn)
                print("上传结果" + str(operate_r))
                return operate_r
            elif 'orderDriver' in order_detail:
                driver_mobile = order_detail['orderDriver']['driverMobile']
                login_driver = ApiDriver(self.env).driver_login(driver_mobile, check_code='1123')
                driver_token = login_driver['data'][0]['token']
                operate_r = self.driver_order_receipt_upload(driver_token, self.order_sn)
                print("上传结果" + str(operate_r))
                return operate_r
            else:
                msg = '请确认' + str(self.order_sn) + '是否是可上传回单状态'
                return msg
        except Exception as e:
            return e

    def operate_upload_reject_check(self):
        """上传回单并审核不通过"""
        try:
            self.operate_upload_receipt()
            operate_r = self.servive_select_task(self.cookies_ua, order_sn=self.order_sn)
            task_id = operate_r['data'][0]['id']
            admin_info = self.bms_admin_info(self.cookies_ua)
            admin_id = admin_info['property']['user']['id']
            self.service_task_dispatch(self.cookies_ua, task_id=task_id, user_name='自动化测试', user_id=admin_id)
            operate_r = self.service_task_check_reject(task_id, cookies=self.cookies_ua,
                                                       task_json={"content": "技术测试", "cancelCauseType": 5,
                                                                  "remark": "123"},
                                                       data_json="技术测试")
            print("审核不通过结果" + str(operate_r))
            return operate_r
        except Exception as e:
            return e

    def operate_upload_pass_check(self):
        """上传回单并审核通过"""
        try:
            self.operate_upload_receipt()
            operate_r = self.servive_select_task(self.cookies_ua, order_sn=self.order_sn)
            task_id = operate_r['data'][0]['id']
            print("回单审核任务id:" + str(task_id))
            admin_info = self.bms_admin_info(self.cookies_ua)
            admin_id = admin_info['property']['user']['id']
            self.service_task_dispatch(self.cookies_ua, task_id=task_id, user_name='自动化测试', user_id=admin_id)
            time.sleep(2)
            operate_r = self.service_task_check_pass(task_id, data_json="技术测试", cookies=self.cookies_ua)
            print("回单审核结果:" + str(operate_r))
            return operate_r
        except Exception as e:
            return e

    def operate_get_receipt(self):
        """收回单"""
        try:
            operate_r = self.bms_order_receipt_confirm(self.order_sn, self.cookies_ua)
            print(operate_r)
            return operate_r
        except Exception as e:
            return e

    def operate_proof_report(self):
        """举证上报"""
        try:
            order_detail = self.order_detail['data'][0]
            print(order_detail)
            if 'orderDriver' in order_detail:
                driver_mobile = order_detail['orderDriver']['driverMobile']
            else:
                return "请确认运单" + str(self.order_sn) + "的状态"
            login_driver = ApiDriver(self.env).driver_login(driver_mobile, check_code='1123')
            driver_token = login_driver['data'][0]['token']
            operate_r = self.driver_order_upload_proof(driver_token, self.order_sn)
            return operate_r
        except Exception as e:
            return e

    def operate_day_car_push_sign(self):
        """日包车推标"""
        pass

    def operate_driver_draw_money(self):
        """司机提款"""
        try:
            order_detail = self.order_detail['data'][0]
            if 'orderDriver' in order_detail:
                driver_mobile = order_detail['orderDriver']['driverMobile']
            else:
                return "请确认运单" + str(self.order_sn) + "的状态"
            operate_r = Withdraw(self.env).driver_Withdraw(driver_mobile)
            return operate_r
        except Exception as e:
            return e

    def operate_broker_draw_money(self):
        """经纪人提款"""
        try:
            r_agent_login = self.agent_app_login()
            agent_token = r_agent_login['data'][0]['token']
            operate_r = self.agent_get_order_money(self.order_sn, agent_token)
            print("运费详情" + str(operate_r))
            if 'commission' in operate_r['data'][0] and 'realAvailableMoney' in operate_r['data'][0]:
                operate_r = self.agent_wallet_drawing_batch(agent_token,
                                                            broker_invoice=operate_r['data'][0]['brokerInvoice'],
                                                            broker_period=operate_r['data'][0]['brokerPeriod'],
                                                            broker_period_days=operate_r['data'][0]['brokerPeriodDays'],
                                                            commission=operate_r['data'][0]['commission'], is_new=1,
                                                            order_sn=self.order_sn,
                                                            trans_fee=operate_r['data'][0]['transFee'],
                                                            real_available_money=operate_r['data'][0][
                                                                'realAvailableMoney'])
            else:
                return "请确认运单" + str(self.order_sn) + "的状态"
            print("申请提款结果" + str(operate_r))
            return operate_r
        except Exception as e:
            return e

    def operate_order(self):
        if self.status == 9:
            # 调度确认
            operate_r = self.operate_dispatch_confirm_order()
            return operate_r
        elif self.status == 10:
            # 回单上传
            operate_r = self.operate_upload_receipt()
            return operate_r
        elif self.status == 11:
            # 回单审核不通过
            operate_r = self.operate_upload_reject_check()
            return operate_r
        elif self.status == 12:
            # 回单审核通过
            operate_r = self.operate_upload_pass_check()
            return operate_r
        elif self.status == 13:
            # 收回单
            operate_r = self.operate_get_receipt()
            return operate_r
        elif self.status == 14:
            # 举证上报
            operate_r = self.operate_proof_report()
            return operate_r
        elif self.status == 15:
            # 日包车推标，已拒绝
            pass
        elif self.status == 16:
            # 司机提款
            operate_r = self.operate_driver_draw_money()
            return operate_r
        elif self.status == 17:
            # 企业运力提款
            operate_r = self.operate_broker_draw_money()
            return operate_r
        elif self.status == 0:
            # 初审
            operate_r = self.operate_service_order_check()
            return operate_r
        elif self.status == 1:
            # 报价
            operate_r = self.operate_turing_offer_price()
            return operate_r
        elif self.status == 2:
            # 确认下单
            operate_r = self.operate_base_order_confirm()
            return operate_r
        elif self.status == 3:
            # 在线支付及审核
            operate_r = self.operate_online_pay_check()
            return operate_r
        elif self.status == 4:
            # 安排司机
            operate_r = self.operate_order_arrange_driver()
            return operate_r
        elif self.status == 5:
            # 运单打点（单个）
            operate_r = self.operate_driver_order_make_point_one()
            return operate_r
        elif self.status == 6:
            # 运单打点（全部）
            operate_r = self.operate_driver_order_make_point_all()
            return operate_r
        elif self.status == 7:
            # 卸载完成
            operate_r = self.operate_unload_for_driver_free()
            return operate_r
        elif self.status == 8:
            # 签收
            operate_r = self.operate_order_sign()
            return operate_r


if __name__ == '__main__':
    r = OperateAppointOrder(order_sn='929120488221', status=8, environment='t4').operate_order()
    print(r)
