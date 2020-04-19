# coding:utf-8
from app.tools.api.api_service import *
from app.tools.api.api_ua import *


class ServiceWorkOrderDeal(ApiService, ApiUa):
    """工单处理"""
    def service_work_order_deal(self, order_sn='', work_order_sn=''):
        # 管理员登录
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        print('管理员登录结果: %s' % cookies_ua)
        # 获取管理员信息
        r_service_admin_info = self.service_sys_admin_info(cookies_ua)
        print('管理员信息: %s' % r_service_admin_info)
        admin_id = r_service_admin_info['property']['user']['id']
        admin_name = r_service_admin_info['property']['user']['name']
        # 查询工单组下所有管理员
        r_group_related_users = self.service_sys_task_group_users(cookies_ua, 1123)
        if self.admin_mobile not in str(r_group_related_users):
            print('工单组下管理员: %s' % r_group_related_users)
            temp_admin_info = {
                'userId': admin_id,
                'userName': admin_name,
                'mobile': self.admin_mobile
            }
            origin_users = r_group_related_users['data'][0]['groupMaps']
            for temp_user in origin_users:
                del temp_user['id']
                del temp_user['groupId']
            origin_users.append(temp_admin_info)
            # 更新工单组下管理员
            r_service_sys_group_user_update = self.service_sys_task_group_user_update(cookies_ua, 1123, '工单处理专员', origin_users)
            print('管理员更新: %s' % r_service_sys_group_user_update)
        # 查询任务
        r_work_orders = self.service_work_order_list(cookies_ua, order_sn=order_sn, work_order_sn=work_order_sn)
        print('查询所有工单: %s' % r_work_orders)
        # 开启接单
        r_service_open = self.service_sys_update_user_status(1, cookies_ua)
        print('服务系统开启接单: %s' % r_service_open)
        work_order_list = []
        for work_order in r_work_orders['data']:
            # print(work_order)
            if work_order['status'] == 6:
                continue
            work_order_id = work_order['id']
            work_order_sn = work_order['sn']
            work_order_list.append(work_order_sn)
            print('=====>工单id: %s, 工单编号: %s' % (work_order_id, work_order_sn))
            # 工单重新分配
            r_service_work_order_dispatch = self.service_work_order_dispatch(cookies_ua, work_order_id, admin_name, admin_id)
            print('工单重新分配: %s' % r_service_work_order_dispatch)
            # 工单处理
            r_service_work_order_deal = self.service_work_order_check(cookies_ua, work_order_id)
            print('工单处理: %s' % r_service_work_order_deal)
        # 关闭接单
        r_service_close = self.service_sys_update_user_status(0, cookies_ua)
        print('服务系统关闭接单: %s' % r_service_close)
        return '以下工单处理完成: %s' % work_order_list


def service_work_order_deal(environment, order_sn='', work_order_sn=''):
    if order_sn == '' and work_order_sn == '':
        return '请填写运单号或工单编号'
    result = ServiceWorkOrderDeal(environment, admin_mobile='16888888888', admin_password='Fy@123456789')
    result.service_work_order_deal(order_sn, work_order_sn)


if __name__ == '__main__':
    service_work_order_deal('r1', work_order_sn='GD1910110141KNZQ')
