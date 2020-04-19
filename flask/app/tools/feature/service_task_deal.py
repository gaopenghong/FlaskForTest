# coding:utf-8
from app.tools.api.api_service import *
from app.tools.api.api_ua import *


class ServiceTaskDeal(ApiService, ApiUa):
    """任务处理"""
    def service_task_deal(self, order_sn='', task_sn='', check_result='pass'):
        # 管理员登录
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        print('管理员登录结果: %s' % cookies_ua)
        # 获取管理员信息
        r_service_admin_info = self.service_sys_admin_info(cookies_ua)
        print('管理员信息: %s' % r_service_admin_info)
        admin_id = r_service_admin_info['property']['user']['id']
        admin_name = r_service_admin_info['property']['user']['name']
        # 查询任务
        r_tasks = self.service_task_search(cookies_ua, order_sn=order_sn, task_sn=task_sn)
        print('查询所有任务: %s' % r_tasks)
        # 开启接单
        r_service_open = self.service_sys_update_user_status(1, cookies_ua)
        print('服务系统开启接单: %s' % r_service_open)
        for task in r_tasks['data']:
            # print(task)
            if task['status'] == 6:
                continue
            task_id = task['id']
            task_sn = task['taskSn']
            task_type = task['taskTypeId']
            task_name = task['name']
            print('=====>任务编号: %s, 任务类型: %s, 任务名称: %s' % (task_sn, task_type, task_name))
            # 查询任务组下所有管理员
            r_group_related_users = self.service_sys_task_group_users(cookies_ua, task_type)
            if self.admin_mobile not in str(r_group_related_users):
                print('%s任务组下管理员: %s' % (task_type, r_group_related_users))
                # task_name = r_group_related_users['data'][0]['name']
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
                # 更新任务组下管理员
                r_service_sys_group_user_update = self.service_sys_task_group_user_update(cookies_ua, task_type, task_name, origin_users)
                print('管理员更新: %s' % r_service_sys_group_user_update)
            # 重新分配任务
            r_service_task_dispatch = self.service_task_dispatch(cookies_ua, task_id, admin_name, admin_id)
            print('任务重新分配: %s' % r_service_task_dispatch)
            r_service_task_detail = self.service_task_detail(task_sn, cookies_ua)
            print('任务详情: %s' % r_service_task_detail)
            task_detail = r_service_task_detail['data'][0]
            # 处理任务
            if task_type == 2300:             # 2300初审
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
                check_data = task_detail_1
            elif task_type == 4400:             # 4400司机资质审核
                if check_result == 'pass':
                    check_status = 2
                else:
                    check_status = 3
                truck_info_list = list()
                for truck in task_detail['driverTruckMapList']:
                    truck_info = {
                        'id': truck['truckId'],
                        'plateNumber': truck['plateNumber'],
                        'carModelId': truck['carModelId'],
                        'carModelName': truck['carModelName'],
                        'carLengthName': truck['carLengthName'],
                        'carLengthId': truck['carLengthId'],
                        'status': check_status,
                        'carLicenStatus': check_status,
                        'loadLicenStatus': check_status,
                        'insurStatus': check_status,
                        'driverTruckStatus': check_status,
                    }
                    truck_info_list.append(truck_info)
                check_data = {
                    'oldCreateTime': task_detail['shDriverInfo']['createTime'],
                    'jsonStr': [
                        {
                            'id': task_detail['shDriverInfo']['id'],
                            'status': 2,
                            'idCardNumber': task_detail['shDriverInfo']['idCardNumber'],
                            'name': task_detail['shDriverInfo']['name'],
                            'mobile': task_detail['shDriverInfo']['mobile'],
                            'idCardAddress': task_detail['shDriverInfo']['idCardAddress'],
                            'frontStatus': check_status,
                            'backStatus': check_status,
                            'licenStatus': check_status,
                            'truckInfoList': truck_info_list
                        }
                    ]
                }
            elif task_type == 4800:             # 4800企业资质审核
                if check_result == 'pass':      # 2审核通过, 3审核不通过
                    check_status = 2
                else:
                    check_status = 3
                check_data = {
                    'id': task_detail['companyInfo']['id'],
                    'creditCode': task_detail['companyInfo']['creditCode'],
                    'companyName': task_detail['companyInfo']['companyName'],
                    'address': task_detail['companyInfo']['address'],
                    'legalPerson': task_detail['companyInfo']['legalPerson'],
                    'identity': task_detail['companyInfo']['identity'],
                    'foundingTime': task_detail['companyInfo']['foundingTime'],
                    'businessTermEndTime': task_detail['companyInfo']['businessTermEndTime'],
                    'bankDeposit': task_detail['companyInfo']['bankDeposit'],
                    'bankNumber': task_detail['companyInfo']['bankNumber'],
                    'licenceImageStatus': check_status,
                    'identityImageStatus': check_status,
                    'roadTransportStatus': check_status,
                    'bankInfoStatus': check_status,
                    'rejectType': random.choice([1, 2, 4]),
                    'remark': '技术测试',
                }
            elif task_type in [5000, 5500]:     # 5000扣款申诉(经纪人), 5500扣款申诉(司机)
                if check_result == 'pass':
                    check_status = 2
                else:
                    check_status = 3
                check_data = {
                    'detail': [
                        {
                            'newMoney': 200,
                            'status': check_status,                # 审核状态: 2通过, 3驳回
                            'oldMoney': task_detail['appealTaskInfo'][0]['deductMoney'],
                            'type': task_detail['appealTaskInfo'][0]['type'],            # 扣款类型: 1时效扣款, 2轨迹扣款
                            'handleContent': '技术测试'
                        }
                    ]
                }
            elif task_type == 5100:             # 5100运单取消审核
                if check_result == 'pass':
                    check_status = 1
                else:
                    check_status = 2
                check_data = {
                    'methodType': check_status,            # 1通过, 2驳回
                    'jsonParam': {
                        'cancelFirstReason': task_detail['orderCancelInfo']['cancelFirstReason'],
                        'cancelFirstReasonName': task_detail['orderCancelInfo']['cancelFirstReasonName'],
                        'cancelSecondReason': task_detail['orderCancelInfo']['cancelSecondReason'],
                        'cancelSecondReasonName': task_detail['orderCancelInfo']['cancelSecondReasonName'],
                        'orderSn': order_sn,
                        'comment': task_detail['orderCancelInfo']['comment'],
                        'voucherImg': task_detail['orderCancelInfo']['voucherImg'],
                        'customerReason': '',       # 客户对福佑放空: 1是, 0否
                        'companyReason': '',        # 福佑对客户放空: 1是, 0否
                        'extraAmount': '',          # 放空费用: 包括福佑补贴客户和客户对福佑防空补贴
                        'subsidizeTarget': '',      # 福佑补贴: 1司机, 2车队
                        'subsidizeTargetName': '',
                        'subsidizeAmount': '',      # 补贴费用
                        'punishTarget': '',         # 下游放空费: 1车队, 2司机
                        'punishTargetName': '',
                        'punishAmount': ''          # 下游放空费
                    }
                }
                fields = ['customerReason', 'companyReason', 'extraAmount', 'subsidizeTarget', 'subsidizeTargetName',
                       'subsidizeAmount', 'punishTarget', 'punishTargetName', 'punishAmount']
                for field in fields:
                    if field in task_detail['orderCancelInfo'].keys():
                        check_data['jsonParam'][field] = task_detail['orderCancelInfo'][field]
            elif task_type == 5200:             # 5200直采司机付款
                check_data = {
                    'isFirst': 'true'
                }
            elif task_type == 5300:             # 5300延迟发车预警
                json_data = list()
                for point in task_detail['stopPointsInfo']:
                    point_info = {
                        'id': point['id'],
                        'provinceId': point['provinceId'],
                        'provinceName': point['provinceName'],
                        'cityId': point['cityId'],
                        'cityName': point['cityName'],
                        'districtId': point['districtId'],
                        'districtName': point['districtName'],
                        'address': point['address'],
                        'stopType': point['stopType'],
                        'planInTime': point['planInTime'],
                        'planOutTime': point['planOutTime']
                    }
                    json_data.append(point_info)
                check_data = {
                    'json': json_data
                }
            elif task_type == 5700:             # 5700专车晚点扣款判定
                check_data = {
                    'amount': 111,
                    'lateTime': 1561
                }
            elif task_type == 6000:             # 6000货主申诉
                check_data = {
                    'appealId': task_detail['appealCustomerJson']['id'],
                    'amount': 100
                }
            else:                               # 3400回单审核, 4000司机付款申请, 4200运单跟踪CC, 4210运单跟踪区域, 5800吸货付款确认, 5900车速异常
                check_data = None
            if task_type in [4000, 4200, 4210, 5000, 5300, 5500, 5700, 5800, 6000] or check_result == 'pass':
                r_service_task_check = self.service_task_check_pass(task_id, data_json=check_data, cookies=cookies_ua)
            else:               # 驳回
                r_service_task_check = self.service_task_check_reject(task_id, data_json=check_data, cookies=cookies_ua)
            print('任务处理: %s, %s' % (task_sn, r_service_task_check))
        # 关闭接单
        r_service_close = self.service_sys_update_user_status(0, cookies_ua)
        print('服务系统关闭接单: %s' % r_service_close)
        return "处理success"


def task_deal(env, order_id, task_id, status):
    result = ServiceTaskDeal(environment=env, admin_mobile='16888888888', admin_password='Fy@123456789')
    return result.service_task_deal(order_id, task_id, status)


if __name__ == '__main__':
    result = ServiceTaskDeal(environment='r1', admin_mobile='16888888888', admin_password='Fy@123456789')
    result.service_task_deal(order_sn='123', task_sn='456', check_result='pass/reject')
