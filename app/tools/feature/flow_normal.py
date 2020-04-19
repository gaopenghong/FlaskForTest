# coding:utf-8
# 普通运单数据生成
from app.tools.api.api_bms import *
from app.tools.api.api_crm import *
from app.tools.api.api_customer_pc import *
from app.tools.api.api_dispatch import *
from app.tools.api.api_service import *
from app.tools.api.api_turing import *
from app.tools.api.api_ua import *


class OrderFlow(ApiBms, ApiCrm, ApiCustomerPC, ApiDispatch, ApiService, ApiTuring, ApiUa):
    """
    运单数据生成脚本
    """
    # 初审询价
    def order_check(self):
        return

    # 图灵报价
    def order_offer_price(self):
        return

    # 安排司机
    def order_arrange_driver(self):
        return

    # 运单打点
    def order_make_point(self):
        return

    # 运单签收
    def order_sign(self):
        return

    # 运单流程
    def flow_normal(self):
        order_sn = ''
        try:
            r_check = self.base_check()
            if r_check != 'All data is OK!':
                return r_check
            # 货主PC登录
            cookies_customer_pc = self.customer_pc_login()
            # 管理员登录
            r_ua_request_id = self.ua_generate_check_code()
            cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
            r_crm_admin_info = self.crm_admin_info(cookies_ua)
            admin_id = r_crm_admin_info['property']['user']['id']
            admin_name = r_crm_admin_info['property']['user']['name']
            # 新增询价
            if self.target_status >= 1:
                r_customer_pc_order_create = self.customer_pc_order_create(cookies_customer_pc)
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
                time.sleep(1)
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                order_status = r_order_detail['data'][0]['quote']['status']
                if order_status == 4:
                    time.sleep(40)
                    r_turing_submit_price = self.turing_offer_price(order_sn, 4000, cookies_ua)
                    print('图灵系统报价: %s' % r_turing_submit_price)
                    time.sleep(180)
            # 确定下单
            if self.target_status >= 4:
                r_customer_pc_order_detail = self.customer_pc_order_detail(order_sn, cookies_customer_pc)
                print('货主PC运单详情: %s' % r_customer_pc_order_detail)
                r_customer_pc_order_confirm = self.customer_pc_order_confirm(order_sn, cookies_customer_pc)
                print('货主PC确定下单: %s' % r_customer_pc_order_confirm)
            # 在线支付-线下转账
            if self.target_status >= 5:
                pass
            # 在线支付-线下转账-审核通过
            if self.target_status >= 6:
                pass
            # 安排司机
            if self.target_status >= 7:
                time.sleep(1)
                r_order_detail = self.bms_order_detail(order_sn, cookies_ua)
                order_status = r_order_detail['data'][0]['quote']['status']
                transport_type = r_order_detail['data'][0]['businessInfo']['transportType']
                sch_type = r_order_detail['data'][0]['businessInfo']['schType']  # 1.统调 2.一口价
                if order_status == 11:              # 待智能调度安排司机
                    pass
                elif order_status > 17:             # 已安排司机
                    pass
                elif transport_type == 1 and sch_type == 1:         # 调度自营
                    r_dispatch_get_driver_info = self.dispatch_get_driver_info(self.driver_mobile, cookies_ua)
                    driver_info = r_dispatch_get_driver_info['data'][0]
                    r_dispatch_arrange_driver = self.dispatch_arrange_driver(order_sn, driver_info, cookies_ua)
                    print('调度系统安排司机: %s' % r_dispatch_arrange_driver)
                elif transport_type == 1 and sch_type == 2:         # 调度一口价
                    pass
                elif transport_type == 0:
                    pass
                else:
                    pass
            # 成单后取消运单
            if self.target_status == 12:
                pass
            # 确定发车
            if self.target_status >= 8:
                pass
            # 卸货完成
            if self.target_status >= 9:
                pass
            # 运单签收
            if self.target_status >= 10:
                pass
            return order_sn
        except Exception as e:
            print(e)

    # 三方运单
    def flow_third(self):
        return

    # 吸货
    def flow_customer(self):
        return 


if __name__ == '__main__':
    flow = OrderFlow(environment='t8', role=1, target_status=4,
                     admin_mobile='16888888888', admin_password='Fy@123456789',
                     customer_mobile='12211111111', agent_mobile='18310179572', driver_mobile='16011111111')
    r_order = flow.flow_normal()
    print('=====>>>当前运单号: %s' % r_order)
