#!/usr/bin/env python
# -*- codingL utf-8 -*-

from app.tools.api.api_bms import *
from app.tools.api.api_crm import *
from app.tools.api.api_customer_pc import *
from app.tools.api.api_dispatch import *
from app.tools.api.api_service import *
from app.tools.api.api_turing import *
from app.tools.api.api_ua import *
from app.tools.api.api_driver import *
from app.tools.api.api_finance import *
from app.tools.api.api_agent import *

from app.tools.api.conf import *
from app.tools.feature.customer_order import customer_ai_confirm


class AppointOrder(ApiBms, ApiCrm, ApiCustomerPC, ApiDispatch, ApiService, ApiTuring, ApiFinance,
                   ApiAgent, ApiDriver):
    """
    【自定义状态】
    目标运单状态: 1待审核, 2待报价, 3待下单, 4待支付, 5转账审核中, 6待安排司机, 7已安排司机,
    目标运单状态: 8待发车, 9卸货完成, 10已签收, 11询价取消, 12成单取消, 13待抢单, 14待接单
    运力类型：0-一口价、1-调度自营、2-日包车、3-固定司机、4-智能调度、5-企业运力

    【开发枚举】
    sch_type 运单类型：0-默认, 1-统调, 2-一口价试点
    transportType 运力类型：0-其他，1-自营运力,2-企业运力，3-固定司机
    order_status 运单状态：1-运单已取消, 2-待审核, 3-审核通过, 4-待报价, 6-已报价, 7-待客户确认,
    order_status 运单状态：8-待货主付款, 9-货主已付款, 10-客户已下单, 11-待智能调度安排司机, 12-已推送,
    order_status 运单状态：13-经纪人报价收集中, 14-竞价结束,经纪人已经中标, 15-待安排司机, 16-已安排司机, 17-待发车,
    order_status 运单状态：18-确认发车, 19-卸货完成, 21-待签收, 22-已签收, 23-已完成, 24-付款审核中
    """

    def __init__(self, environment, appoint_status, appoint_transfer_type, appoint_offline_pay):
        super().__init__(environment, appoint_status)
        print('appoint_status', type(appoint_status))
        self.env = environment
        self.target_status = int(appoint_status)
        self.appoint_transfer_type = int(appoint_transfer_type)
        self.appoint_offline_pay = appoint_offline_pay
        self.admin_mobile = get_config("admin_account", "admin_mobile")
        self.admin_password = get_config("admin_account", "admin_password")
        if self.appoint_offline_pay == "on":
            self.customer_mobile = get_config("customer_account", "customer_mobile_offline_pay")
        else:
            self.customer_mobile = get_config("customer_account", "customer_mobile_1")
        if self.appoint_transfer_type == 0:  # 一口价，OK
            self.agent_mobile = get_config("one_price_account", "agent_mobile")
            self.driver_mobile = get_config("driver_account", "one_price_driver_mobile")
            self.admin_mobile = get_config("one_price_account", "admin_mobile")
        elif self.appoint_transfer_type == 1:  # 调度自营，OK
            self.agent_mobile = get_config("self_run_account", "agent_mobile")
            self.driver_mobile = get_config("driver_account", "self_run_driver_mobile")
        # elif self.appoint_transfer_type == 2:  # 日包车，OK
        #     pass
        elif self.appoint_transfer_type == 3:  # 固定司机
            self.agent_mobile = get_config("out_sourcing_account", "agent_mobile")
            self.driver_mobile = get_config("driver_account", "fix_driver_mobile")
        # elif self.appoint_transfer_type == 4:  # 智能调度
        #     pass
            # self.agent_mobile = get_config("out_sourcing_account", "agent_mobile")
            # self.driver_mobile = get_config("driver_account", "team_driver_mobile")
        elif self.appoint_transfer_type == 5:  # 企业运力，OK
            self.agent_mobile = get_config("out_sourcing_account", "agent_mobile")
            self.driver_mobile = get_config("driver_account", "team_driver_mobile")
        else:  # 默认一口价
            self.agent_mobile = get_config("one_price_account", "agent_mobile")
            # self.driver_mobile = get_config("driver_account", "special_driver_mobile")
            self.driver_mobile = get_config("driver_account", "one_price_driver_mobile")
            self.admin_mobile = get_config("one_price_account", "admin_mobile")

    def turing_order_appoint(self):
        order_sn = ''
        try:
            r_check = self.base_check()
            if r_check != 'All data is OK!':
                return r_check
            # 货主PC登录
            # self.customer_mobile = get_config("customer_account", "customer_mobile_1")
            cookies_customer_pc = self.customer_pc_login()
            # 司机登录
            driver_login = ApiDriver(self.env).driver_login(self.driver_mobile, check_code='1123')
            driver_token = driver_login['data'][0]['token']
            print('driver_token-----', driver_token)
            # 管理员登录
            r_ua_request_id = self.ua_generate_check_code()
            cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
            r_crm_admin_info = self.crm_admin_info(cookies_ua)
            admin_id = r_crm_admin_info['property']['user']['id']
            admin_name = r_crm_admin_info['property']['user']['name']
            # 新增询价
            if self.target_status >= 1:
                if self.appoint_transfer_type == 0:  # 一口价
                    r_customer_pc_order_create = self.customer_pc_turing_order_one_price_create(cookies_customer_pc)
                    print('货主PC新增询价11: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 1:  # 调度自营
                    r_customer_pc_order_create = self.customer_pc_turing_order_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 2:  # 日包车
                    self.target_status = 4  # 日包车只走到下单即可
                    r_customer_pc_order_create = self.customer_pc_turing_order_daily_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 3:  # 固定司机
                    pass
                elif self.appoint_transfer_type == 4:  # 智能调度
                    self.target_status = 4  # 智能调度只走到下单即可
                    r_customer_pc_order_create = self.customer_pc_turing_order_scheduler_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 5:  # 企业运力
                    pass
                else:  # 默认一口价
                    r_customer_pc_order_create = self.customer_pc_turing_order_one_price_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
            # 询价阶段取消运单
            if self.target_status == 11:
                return '运单%s已取消' % order_sn
            # 初审询价
            if self.target_status >= 2:
                time.sleep(1)
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                order_status = r_order_detail['data'][0]['quote']['status']
                if order_status == 2:
                    # 服务系统开启接单
                    r_service_open = self.service_sys_update_user_status(1, cookies_ua)
                    print('服务系统开启接单: %s' % r_service_open)
                    # 任务全部列表查询任务
                    r_service_task_search = self.service_task_search(cookies_ua, order_sn)
                    print('服务系统查询任务: %s' % r_service_task_search)
                    task_id = r_service_task_search['data'][0]['id']
                    task_sn = r_service_task_search['data'][0]['taskSn']
                    # 重新分配任务
                    r_service_task_dispatch = self.service_task_dispatch(cookies_ua, task_id, admin_name, admin_id)
                    print('服务系统重新分配任务: %s' % r_service_task_dispatch)
                    # 任务详情
                    r_service_task_detail = self.service_task_detail(task_sn, cookies_ua)
                    print('服务系统任务详情: %s' % r_service_task_detail)
                    task_detail = r_service_task_detail['data'][0]
                    # 初审询价
                    task_detail_1 = dict()
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
                    r_service_task_check_pass = self.service_task_check_pass(task_id, None, task_detail_1, cookies_ua)
                    print('服务系统初审任务: %s' % r_service_task_check_pass)
                    # 服务系统开启接单
                    r_service_close = self.service_sys_update_user_status(0, cookies_ua)
                    print('服务系统关闭接单: %s' % r_service_close)
            # 图灵报价
            if self.target_status >= 3:
                r_turing_price = self.turing_price_to_order_core_quickly(order_sn)
                print('r_turing_price--------', r_turing_price)
                if not r_turing_price["success"]:
                    return '运单号：%s，图灵系统报价异常: %s' % (order_sn, r_turing_price)

                # time.sleep(1)
                # r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                # order_status = r_order_detail['data'][0]['quote']['status']
                # if order_status == 4:       # 待报价
                #     time.sleep(40)
                #     r_turing_submit_price = self.turing_offer_price(order_sn, 4000, cookies_ua)
                #     print('图灵系统报价: %s' % r_turing_submit_price)
                #     if not r_turing_submit_price["success"]:
                #         return '运单号：%s，图灵系统报价异常: %s' % (order_sn, r_turing_submit_price)
                #     time.sleep(180)
            # 确定下单
            if self.target_status >= 4:
                r_customer_pc_order_detail = self.customer_pc_order_detail(order_sn, cookies_customer_pc)
                print('货主PC运单详情: %s' % r_customer_pc_order_detail)
                r_customer_pc_order_confirm = self.customer_pc_order_confirm(order_sn, cookies_customer_pc)
                print('货主PC确定下单: %s' % r_customer_pc_order_confirm)
                # 在线支付-线下转账
                if self.appoint_offline_pay == "on":  # 开启线下支付
                    # 货主线下付款
                    r_customer_pc_order_confirm_transfer = self.customer_pc_confirm_transfer_accounts(order_sn,
                                                                                                      cookies_customer_pc)
                    print("运单号：%s，货主线下付款异常：%s" % (order_sn, r_customer_pc_order_confirm_transfer))
                    if not r_customer_pc_order_confirm_transfer["success"]:
                        return "运单号：%s，货主线下付款异常：%s" % (order_sn, r_customer_pc_order_confirm_transfer)
                    # 获取线下支付待审核的列表
                    r_online_check_list = self.finance_fy_online_check_list({'orderPara': order_sn}, cookies_ua)
                    print("线下支付待审核列表：%s" % r_online_check_list)
                    request_id = r_online_check_list['data'][0]['payRequestId']
                    # 线下支付-审核通过/拒绝
                    r_online_check = self.finance_fy_online_check(request_id, 2, cookies_ua)  # 2-通过
                    print("线下支付审核通过：%s" % r_online_check)
                else:
                    print("未开启线下支付")
            if self.target_status >= 5:  # todo
                pass
            # 在线支付-线下转账-审核通过
            if self.target_status >= 6:  # todo
                pass
            # 安排司机
            if self.target_status >= 7:
                time.sleep(5)
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_status = r_order_detail['data'][0]['quote']['status']
                transport_type = r_order_detail['data'][0]['businessInfo']['transportType']
                sch_type = r_order_detail['data'][0]['businessInfo']['schType']  # 1.统调 2.一口价
                trans_fee = r_order_detail['data'][0]['quote']['cusBareTransAmount']
                if order_status == 11:  # 待智能调度安排司机
                    msg = "订单号{}，待智能调度安排司机！".format(order_sn)
                    return msg
                elif order_status == 16:  # 已安排司机
                    pass
                elif order_status == 15:  # 待安排司机
                    if transport_type == 1 and (sch_type == 1 or sch_type == 0):  # 调度自营
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号%s安排司机失败（%s），请手动处理！" % (order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 1 and sch_type == 2:  # 调度一口价
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号{}，安排司机失败：{}，请手动处理！".format(order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 0:  # 0-其他，匹配到外协调度运力
                        # 意向单--拦截运单，重新匹配调度运力
                        pass
                else:
                    pass
            # 成单后取消运单
            if self.target_status == 12:
                pass
            # 确定发车
            if self.target_status >= 8:
                # 司机到达发货地打点
                auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                print("订单号%s，司机到达发货地打点%s" % (order_sn, auto_make_point))
            # 卸货完成
            if self.target_status >= 9:
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_point_length = len(r_order_detail["data"][0]["stopPoints"])
                for i in range(order_point_length * 2 - 1):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                    print("订单号%s，司机发货地发车打点到离开卸货地打点%s" % (order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            # 运单签收
            if self.target_status >= 10:
                bms_order_sign = self.bms_order_exception(order_sn, 13, 'ftest运单签收',
                                                          cookies_bms=cookies_ua)  # 13-异常修改签收
                print("订单号%s，异常修改签收%s" % (order_sn, bms_order_sign))
            # 最后获取运单详情
            time.sleep(2)
            r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
            return "运单号：" + order_sn + "，运单状态：" + str(r_order_detail['data'][0]['quote']['statusName'])
        except Exception as e:
            print(e)

    # 项目货
    def project_order_appoint(self):
        global agent_token
        order_sn = ''
        # 固定司机福佑线路（基础数据确认后修改）
        fy_line_id = '3416'
        try:
            r_check = self.base_check()
            if r_check != 'All data is OK!':
                return r_check
            # 货主PC登录
            self.customer_mobile = get_config("customer_account", "customer_mobile_2")
            print(self.customer_mobile)
            cookies_customer_pc = self.customer_pc_login()
            print('cookies_customer_pc-----', cookies_customer_pc)
            # 司机登录
            print('司机登录司机登录')
            driver_login = ApiDriver(self.env).driver_login(self.driver_mobile, check_code='1123')
            print('self.driver_mobile', self.driver_mobile)
            print('司机登录', driver_login)
            driver_token = driver_login['data'][0]['token']
            print('driver_token-----', driver_token)
            if self.appoint_transfer_type == 5:  # 企业运力
                # 外协经纪人登录
                r_agent_login = self.agent_app_login()
                print('self.agent_mobile------', self.agent_mobile)
                print('r_agent_login------', r_agent_login)
                agent_token = r_agent_login['data'][0]['token']
                # agent_id = r_agent_login['data'][0]['id']
            # 管理员登录
            r_ua_request_id = self.ua_generate_check_code()
            print('self.admin_mobile', self.admin_mobile)

            cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
            print('cookies_ua-----', cookies_ua)
            r_crm_admin_info = self.crm_admin_info(cookies_ua)
            # admin_id = r_crm_admin_info['property']['user']['id']
            # admin_name = r_crm_admin_info['property']['user']['name']

            if self.appoint_transfer_type == 3:     # 固定司机
                # 给司机推送并签署合同
                self.agent_crm_driver_contract(self.driver_mobile, fy_line_id, cookies_ua)
                # 完成当前司机承运的运单
                r_json = self.bms_order_list(cookies_ua, {'orderStatus': '17', 'driverMobile': self.driver_mobile})
                print('r_json-----', r_json)
                if r_json['status']['desc'] != '结果为空':
                    except_order_sn = r_json['data'][0]['orderSn']
                    self.bms_order_exception(except_order_sn, 12, cookies_bms=cookies_ua)
                # 司机上报空车
                r = self.driver_app_line_rank_change(driver_token, 1, '40.035968967013886', '116.30738932291666', fy_line_id)
                print("司机上报结果：" + str(r))

            # 新增询价
            if self.target_status >= 1:
                if self.appoint_transfer_type == 0:  # 一口价
                    r_customer_pc_order_create = self.customer_pc_project_order_one_price_create(cookies_customer_pc)
                    print('货主PC新增询价11: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 1:  # 调度自营
                    r_customer_pc_order_create = self.customer_pc_project_order_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 2:  # 日包车
                    self.target_status = 4  # 日包车只走到下单即可
                    r_customer_pc_order_create = self.customer_pc_project_order_daily_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 3:  # 固定司机
                    r_customer_pc_order_create = self.customer_pc_project_order_driver_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 4:  # 智能调度
                    self.target_status = 4  # 智能调度只走到下单即可
                    r_customer_pc_order_create = self.customer_pc_project_order_scheduler_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                elif self.appoint_transfer_type == 5:  # 企业运力
                    r_customer_pc_order_create = self.customer_pc_project_order_agengt_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
                else:  # 默认一口价
                    r_customer_pc_order_create = self.customer_pc_project_order_one_price_create(cookies_customer_pc)
                    print('货主PC新增询价: %s' % r_customer_pc_order_create)
                    order_sn = r_customer_pc_order_create['data'][0]['orderSn']
            # 询价阶段取消运单
            if self.target_status == 11:
                return '运单%s已取消' % order_sn
            # 确定下单
            if self.target_status >= 4:
                r_customer_pc_order_detail = self.customer_pc_order_detail(order_sn, cookies_customer_pc)
                print('货主PC运单详情: %s' % r_customer_pc_order_detail)
                time.sleep(5)
                r_customer_pc_order_confirm = self.customer_pc_order_confirm(order_sn, cookies_customer_pc)
                print('货主PC确定下单: %s' % r_customer_pc_order_confirm)
            # 在线支付-线下转账
            if self.target_status >= 5:  # todo
                pass
            # 在线支付-线下转账-审核通过
            if self.target_status >= 6:  # todo
                pass
            # 安排司机
            if self.target_status >= 7:
                time.sleep(5)
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_status = r_order_detail['data'][0]['quote']['status']
                transport_type = r_order_detail['data'][0]['businessInfo']['transportType']
                sch_type = r_order_detail['data'][0]['businessInfo']['schType']  # 1.统调 2.一口价
                trans_fee = r_order_detail['data'][0]['quote']['cusBareTransAmount']
                if order_status == 11:  # 待智能调度安排司机
                    msg = "订单号{}，待智能调度安排司机！".format(order_sn)
                    return msg
                elif order_status == 16:  # 已安排司机
                    pass
                elif order_status == 15:  # 待安排司机
                    if transport_type == 1 and (sch_type == 1 or sch_type == 0):  # 调度自营
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号%s安排司机失败（%s），请手动处理！" % (order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 1 and sch_type == 2:  # 调度一口价
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号{}，安排司机失败：{}，请手动处理！".format(order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 0:  # 企业运力
                        driver_info = self.agent_driver_detail(agent_token, self.driver_mobile)['data'][0]
                        time.sleep(2)
                        r_agent_arrange_driver = self.agent_order_arrange_driver(agent_token, driver_info=driver_info,
                                                                                 order_sn=order_sn)
                        if r_agent_arrange_driver['status']['desc'] != '操作成功':
                            msg = "订单号{} 安排司机失败：{}，请手动处理！".format(order_sn, r_agent_arrange_driver['status']['desc'])
                            return msg
                    # elif transport_type == 0:  # 0-其他，匹配到外协调度运力
                    #     # 意向单--拦截运单，重新匹配调度运力
                    #     pass
                else:
                    pass
            # 成单后取消运单
            if self.target_status == 12:
                pass
            # 确定发车
            if self.target_status >= 8:
                # 司机到达发货地打点
                auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                print("订单号%s，司机到达发货地打点%s" % (order_sn, auto_make_point))
            # 卸货完成
            if self.target_status >= 9:
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_point_length = len(r_order_detail["data"][0]["stopPoints"])
                for i in range(order_point_length * 2 - 1):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                    print("订单号%s，司机发货地发车打点到离开卸货地打点%s" % (order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            # 运单签收
            if self.target_status >= 10:
                bms_order_sign = self.bms_order_exception(order_sn, 13, 'ftest运单签收',
                                                          cookies_bms=cookies_ua)  # 13-异常修改签收
                print("订单号%s，异常修改签收%s" % (order_sn, bms_order_sign))
            # 最后获取运单详情
            time.sleep(2)
            r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
            return "运单号：" + order_sn + "，运单状态：" + str(r_order_detail['data'][0]['quote']['statusName'])
        except Exception as e:
            print(e)

    # 专车
    def ai_order_appoint(self):
        order_sn = ''
        print(self.target_status)
        try:
            r_check = self.base_check()
            if r_check != 'All data is OK!':
                return r_check
            # 货主PC登录
            self.customer_mobile = get_config("customer_account", "customer_mobile_offline_pay")
            # 司机登录
            driver_login = ApiDriver(self.env).driver_login(self.driver_mobile, check_code='1123')
            driver_token = driver_login['data'][0]['token']
            print('driver_token-----', driver_token)
            # 管理员登录
            r_ua_request_id = self.ua_generate_check_code()
            cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
            r_crm_admin_info = self.crm_admin_info(cookies_ua)
            # 新增询价
            if self.target_status >= 1:
                if self.target_status == 1:
                    return '专车业务运单无此状态'
            # 询价阶段取消运单
            if self.target_status == 11:
                if self.target_status == 1:
                    return '专车业务运单无此状态'
            # 初审询价
            if self.target_status >= 2:
                if self.target_status == 2:
                    return '专车业务运单无此状态'
            # 图灵报价
            if self.target_status >= 3:
                if self.target_status == 3:
                    return '专车业务运单无此状态'
            # 确定下单
            if self.target_status >= 6:
                print(self.customer_mobile)
                if self.target_status == 4:
                    ai_status = 0
                elif self.target_status == 5:
                    return '专车业务运单无此状态'
                else:
                    ai_status = 2
                if self.appoint_transfer_type == 0:  # 一口价
                    stock_lines = [['山西', '太原', '吉林', '长春', 8, 1, '杏花岭区', '朝阳区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines)
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
                elif self.appoint_transfer_type == 1:  # 调度自营
                    stock_lines = [['山西', '太原', '辽宁', '沈阳', 8, 1, '杏花岭区', '沈河区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines)
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
                elif self.appoint_transfer_type == 2:  # 日包车
                    stock_lines = [['西藏', '拉萨', '北京', '北京', 8, 1, '城关区', '昌平区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines)
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
                elif self.appoint_transfer_type == 3:  # 固定司机
                    stock_lines = [['内蒙古', '呼和浩特', '安徽', '安庆', 8, 1, '回民区', '宜秀区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines)
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
                elif self.appoint_transfer_type == 4:  # 智能调度
                    stock_lines = [['上海', '上海', '江苏', '苏州', 8, 1, '虹口区', '姑苏区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines,
                                                      dispatch_ai='on')
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
                elif self.appoint_transfer_type == 5:  # 企业运力
                    stock_lines = [['北京', '北京', '安徽', '安庆', 8, 1, '昌平区', '宜秀区']]
                    orders_info = customer_ai_confirm(self.env, self.customer_mobile, start_address=None,
                                                      end_address=None, order_status=ai_status, stock_lines=stock_lines)
                    print('专车APP下单: %s' % orders_info)
                    if type(orders_info) == list and len(orders_info) > 0:
                        order_sn = orders_info[0]
                    else:
                        return orders_info
            # 安排司机
            if self.target_status >= 7:
                time.sleep(5)
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_status = r_order_detail['data'][0]['quote']['status']
                transport_type = r_order_detail['data'][0]['businessInfo']['transportType']
                sch_type = r_order_detail['data'][0]['businessInfo']['schType']  # 1.统调 2.一口价
                trans_fee = r_order_detail['data'][0]['quote']['cusBareTransAmount']
                if order_status == 11:  # 待智能调度安排司机
                    msg = "订单号{}，待智能调度安排司机！".format(order_sn)
                    return msg
                elif order_status == 16:  # 已安排司机
                    pass
                elif order_status == 15:  # 待安排司机
                    if transport_type == 1 and (sch_type == 1 or sch_type == 0):  # 调度自营
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号%s安排司机失败（%s），请手动处理！" % (order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 1 and sch_type == 2:  # 调度一口价
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号{}，安排司机失败：{}，请手动处理！".format(order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 0:  # 0-其他，匹配到外协调度运力
                        # 意向单--拦截运单，重新匹配调度运力
                        pass
                else:
                    pass
            # 成单后取消运单
            if self.target_status == 12:
                pass
            # 确定发车
            if self.target_status >= 8:
                # 司机到达发货地打点
                auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                print("订单号%s，司机到达发货地打点%s" % (order_sn, auto_make_point))
            # 卸货完成
            if self.target_status >= 9:
                # bms运单详情
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_point_length = len(r_order_detail["data"][0]["stopPoints"])
                for i in range(order_point_length * 2 - 1):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, order_sn)
                    print("订单号%s，司机发货地发车打点到离开卸货地打点%s" % (order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            # 运单签收
            if self.target_status >= 10:
                bms_order_sign = self.bms_order_exception(order_sn, 13, 'ftest运单签收',
                                                          cookies_bms=cookies_ua)  # 13-异常修改签收
                print("订单号%s，异常修改签收%s" % (order_sn, bms_order_sign))
            # 最后获取运单详情
            time.sleep(2)
            r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
            return "运单号：" + order_sn + "，运单状态：" + str(r_order_detail['data'][0]['quote']['statusName'])
        except Exception as e:
            print(e)

    # 生成意向单
    def create_auto_query_order(self, line_id, plan_date):
        order_id = ''
        # 管理员登录
        admin_mobile_yxd = get_config("admin_account", "admin_mobile_yxd")
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua_yxd = self.ua_login(admin_mobile_yxd, self.admin_password, r_ua_request_id)
        print('cookies_ua_yxd', cookies_ua_yxd)
        print('plan_date', plan_date)
        ApiAutoQuery(self.env).create_bylineid_auto_query(lineid=line_id, plandate=plan_date, cookies=cookies_ua_yxd)
        # 查看线路信息
        r = ApiAutoQuery(self.env).get_line_detail(cookies_ua_yxd, line_id)
        company_id = r['data'][0]['companyId']
        end_province_id = r['data'][0]['endProvinceId']
        end_district_id = r['data'][0]['endDistrictId']
        # 意向单待确认列表
        r = ApiAutoQuery(self.env).auto_query_list_wait(cookies_ua_yxd, line_id)

        # for i in range(len(r['data'])):
        #     if r['data'][i]['lineId'] == line_id:
        #         order_id = r['data'][i]['id']
        #         break

        if r['success']:
            if len(r['data']) >= 1:
                order_id = r['data'][-1]['id']
                print('意向单ID', order_id)
            else:
                return "意向单待确认列表为空，请联系相关人员处理！"
        else:
            return "查询意向单待确认列表：%s，请联系相关人员处理！" % r['status']['desc']
        # 意向单确认发单
        r = ApiAutoQuery(self.env).confirm_auto_query(cookies_ua_yxd, order_id)
        if not r['success']:
            return r['data']
        else:
            yxd_order_sn = r['property']['orderList'][0]['orderSn']
            print('意向单单号', yxd_order_sn)
            return yxd_order_sn

    # 意向单
    def auto_query_order_appoint(self, plan_date):
        global agent_token
        yxd_order_sn = ''

        # 确认基础线路数据
        # 一口价项目货id
        one_line_id = '39423'
        # 调度自营项目货id
        dis_line_id = '39386'
        # 日包车项目货id
        day_line_id = '39426'
        # 固定司机项目货id
        driver_line_id = '39429'
        # 智能调度项目货id
        auto_line_id = '39387'
        # 企业运力项目货id
        agent_line_id = '39430'
        # 固定司机福佑线路
        fy_line_id = '3416'
        try:
            r_check = self.base_check()
            if r_check != 'All data is OK!':
                return r_check
            # 货主PC登录
            self.customer_mobile = get_config("customer_account", "customer_mobile_2")
            print(self.customer_mobile)
            cookies_customer_pc = self.customer_pc_login()
            print('cookies_customer_pc-----', cookies_customer_pc)
            # 司机登录
            login_driver = ApiDriver(self.env).driver_login(self.driver_mobile, check_code='1123')
            print('self.driver_mobile', self.driver_mobile)
            print('司机登录', login_driver)
            driver_token = login_driver['data'][0]['token']
            print('driver_token-----', driver_token)
            if self.appoint_transfer_type == 5:  # 企业运力
                # 外协经纪人登录
                r_agent_login = self.agent_app_login()
                print('self.agent_mobile------', self.agent_mobile)
                print('r_agent_login------', r_agent_login)
                agent_token = r_agent_login['data'][0]['token']
                # agent_id = r_agent_login['data'][0]['id']
            # 管理员登录
            r_ua_request_id = self.ua_generate_check_code()
            cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
            print('cookies_ua-----', cookies_ua)

            if self.appoint_transfer_type == 3:
                # 给司机推送并签署合同
                self.agent_crm_driver_contract(self.driver_mobile, fy_line_id, cookies_ua)
                # 完成当前司机承运的运单
                r_json = self.bms_order_list(cookies_ua, {'orderStatus': '17', 'driverMobile': self.driver_mobile})
                print('r_json-----', r_json)
                if r_json['status']['desc'] != '结果为空':
                    except_order_sn = r_json['data'][0]['orderSn']
                    self.bms_order_exception(except_order_sn, 12, cookies_bms=cookies_ua)
                # 司机上报空车
                r = self.driver_app_line_rank_change(driver_token, 1, '40.035968967013886', '116.30738932291666',
                                                     fy_line_id)
                print("司机上报结果：" + str(r))

            # 下意向单（到确认下单状态）
            if self.target_status >= 6:
                if self.appoint_transfer_type == 0:  # 一口价
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", one_line_id)
                    yxd_order_sn = self.create_auto_query_order(one_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", one_line_id)
                elif self.appoint_transfer_type == 1:  # 调度自营
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", dis_line_id)
                    yxd_order_sn = self.create_auto_query_order(dis_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", dis_line_id)
                elif self.appoint_transfer_type == 2:  # 日包车
                    self.target_status = 4  # 日包车只走到下单即可
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", day_line_id)
                    yxd_order_sn = self.create_auto_query_order(day_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", day_line_id)
                elif self.appoint_transfer_type == 3:  # 固定司机
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", driver_line_id)
                    yxd_order_sn = self.create_auto_query_order(driver_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", driver_line_id)
                elif self.appoint_transfer_type == 4:  # 智能调度
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", auto_line_id)
                    self.target_status = 4  # 智能调度只走到下单即可
                    yxd_order_sn = self.create_auto_query_order(auto_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", auto_line_id)
                elif self.appoint_transfer_type == 5:  # 企业运力
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", agent_line_id)
                    yxd_order_sn = self.create_auto_query_order(agent_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", agent_line_id)
                else:  # 默认一口价
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("1", one_line_id)
                    yxd_order_sn = self.create_auto_query_order(one_line_id, plan_date)
                    print('意向单%s' % yxd_order_sn)
                    # 线路自动生成意向单，1-开启，2-关闭
                    self.switch_yxd_of_line("2", one_line_id)
            # 询价阶段取消运单
            if self.target_status == 11:
                return '运单%s已取消' % yxd_order_sn
            # 在线支付-线下转账
            if self.target_status >= 5:  # todo
                pass
            # 在线支付-线下转账-审核通过
            if self.target_status >= 6:  # todo
                pass
            # 安排司机
            if self.target_status >= 7:
                time.sleep(5)
                # bms运单详情
                r_order_detail = self.bms_order_detail(yxd_order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                if not r_order_detail['success']:
                    return r_order_detail['status']['desc']
                order_status = r_order_detail['data'][0]['quote']['status']
                transport_type = r_order_detail['data'][0]['businessInfo']['transportType']
                sch_type = r_order_detail['data'][0]['businessInfo']['schType']  # 1.统调 2.一口价
                trans_fee = r_order_detail['data'][0]['quote']['cusBareTransAmount']
                if order_status == 11:  # 待智能调度安排司机
                    msg = "订单号{}，待智能调度安排司机！".format(yxd_order_sn)
                    return msg
                elif order_status == 16:  # 已安排司机
                    pass
                elif order_status == 15:  # 待安排司机
                    if transport_type == 1 and (sch_type == 1 or sch_type == 0):  # 调度自营
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(yxd_order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号%s安排司机失败（%s），请手动处理！" % (yxd_order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 1 and sch_type == 2:  # 调度一口价
                        r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                        driver_info = r_dispatch_get_driver_info['data'][0]
                        r_dispatch_arrange_driver = self.dispatch_arrange_driver(yxd_order_sn, driver_info, cookies_ua,
                                                                                 trans_fee, 0)
                        print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                        # 判断是否成功安排司机
                        if not r_dispatch_arrange_driver['success']:
                            msg = "订单号{}，安排司机失败：{}，请手动处理！".format(yxd_order_sn, r_dispatch_arrange_driver['status']['desc'])
                            return msg
                    elif transport_type == 0:  # 企业运力
                        driver_info = self.agent_driver_detail(agent_token, self.driver_mobile)['data'][0]
                        time.sleep(2)
                        r_agent_arrange_driver = self.agent_order_arrange_driver(agent_token, driver_info=driver_info,
                                                                                 order_sn=yxd_order_sn)
                        if r_agent_arrange_driver['status']['desc'] != '操作成功':
                            msg = "订单号{}，安排司机失败：{}，请手动处理！".format(yxd_order_sn, r_agent_arrange_driver['status']['desc'])
                            return msg
                    # elif transport_type == 0:  # 0-其他，匹配到外协调度运力
                    #     # 意向单--拦截运单，重新匹配调度运力
                    #     pass
                else:
                    pass
            # 成单后取消运单
            if self.target_status == 12:
                pass
            # 确定发车
            if self.target_status >= 8:
                # 司机到达发货地打点
                auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, yxd_order_sn)
                print("订单号%s，司机到达发货地打点%s" % (yxd_order_sn, auto_make_point))
            # 卸货完成
            if self.target_status >= 9:
                # bms运单详情
                r_order_detail = self.bms_order_detail(yxd_order_sn, cookies_ua)
                print('r_order_detail-----', r_order_detail)
                order_point_length = len(r_order_detail["data"][0]["stopPoints"])
                for i in range(order_point_length * 2 - 1):
                    auto_make_point = ApiDriver(self.env).driver_order_auto_make_point(driver_token, yxd_order_sn)
                    print("订单号%s，司机发货地发车打点到离开卸货地打点%s" % (yxd_order_sn, auto_make_point))
                    i += 1
                    time.sleep(1)
            # 运单签收
            if self.target_status >= 10:
                bms_order_sign = self.bms_order_exception(yxd_order_sn, 13, 'ftest运单签收',
                                                          cookies_bms=cookies_ua)  # 13-异常修改签收
                print("订单号%s，异常修改签收%s" % (yxd_order_sn, bms_order_sign))
            # 最后获取运单详情
            time.sleep(2)
            r_order_detail = self.bms_order_detail(yxd_order_sn, cookies_ua)
            return "运单号：" + yxd_order_sn + "，运单状态：" + str(r_order_detail['data'][0]['quote']['statusName'])

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # appoint_order = AppointOrder('t5', '10', 'on')
    appoint_order = AppointOrder('t4', '9', '1', 'off')
    # r_order = appoint_order.turing_order_appoint()        # 图灵订单
    r_order = appoint_order.project_order_appoint()     # 项目货订单
    # current_time = int(time.time())
    # yxd_time = (current_time + 3600 * 3) * 1000
    # r_order = appoint_order.auto_query_order_appoint("1575475200000")      # 意向单
    print('=====>>>当前运单号: %s' % r_order)
