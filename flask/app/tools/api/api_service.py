# coding:utf-8
from .base import *


class ApiService(Base):
    """服务系统接口"""
    # 开启/关闭接单
    def service_sys_update_user_status(self, new_status, cookies):
        url = self.mk_url('fuwu', 'api/u/com/updateUserStatus.do')
        data = {
            'newStatus': new_status  # 目标状态：0,关闭接单, 1 正常接单'
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 获取管理员信息
    def service_sys_admin_info(self, cookies):
        url = self.mk_url('fuwu', 'api/u/com/getUserInfo')
        r = requests.get(url, cookies=cookies)
        return r.json()

    # 查询任务组下所有管理员
    def service_sys_task_group_users(self, cookies, group_id):
        url = self.mk_url('fuwu', 'api/u/com/listGroupUser.do')
        data = {
            'groupId': group_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 更新任务组下管理员信息
    def service_sys_task_group_user_update(self, cookies, group_id, group_name, user_json):
        url = self.mk_url('fuwu', 'api/u/com/updateGroupUser.do')
        data = {
            'groupId': group_id,
            'groupName': group_name,
            'userJson': json.dumps(user_json)
        }
        print(data)
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 任务系统-全部任务列表
    def service_task_search(self, cookies, order_sn='', third_quote_sn='', task_sn=''):
        url = self.mk_url('fuwu', 'api/task/selectAllList.do')
        data = {
            'pageSize': 30,
            'pageIndex': 1,
            'orderSn': order_sn,
            'thirdQuoteSn': third_quote_sn,
            'taskSn': task_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 任务系统-任务重新分配
    def service_task_dispatch(self, cookies, task_id='', user_name='', user_id=''):
        url = self.mk_url('fuwu', 'api/task/dispatchProcessor.do')
        data = {
            'taskId': task_id,  # 任务Id
            'userId': user_id,
            'userName': user_name  # 分配人姓名
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 查看任务详情
    def service_task_detail(self, task_sn, cookies):
        url = self.mk_url('fuwu', 'api/task/selectTaskDetail')
        data = {
            'taskSn': task_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 任务系统-审核通过
    def service_task_check_pass(self, task_id, task_json=None, data_json=None, cookies=None):
        url = self.mk_url('fuwu', 'api/task/passTask')
        data = {
            'taskId': task_id,
            'taskJson': '',
            'dataJson': ''
        }
        if task_json is None:
            task_json = {
                'content': '技术测试',
                'imgJson': ["https://public.fuyoukache.com/3e62682b-d84d-4d7f-90b1-9ee5b5779d48---abc.jpg"]
            }
        data['taskJson'] = json.dumps(task_json)
        if data_json is not None:
            data['dataJson'] = json.dumps(data_json)
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 任务系统-审核不通过
    def service_task_check_reject(self, task_id, task_json=None, data_json=None, cookies=None):
        url = self.mk_url('fuwu', 'api/task/rejectTask')
        data = {
            'taskId': task_id,
            'taskJson': '',
            'dataJson': ''
        }
        if task_json is None:
            task_json = {
                'content': '技术测试',
                'imgJson': ["https://public.fuyoukache.com/3e62682b-d84d-4d7f-90b1-9ee5b5779d48---abc.jpg"]
            }
        data['taskJson'] = json.dumps(task_json)
        if data_json is not None:
            data['dataJson'] = json.dumps(data_json)
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 工单系统-全部工单列表
    def service_work_order_list(self, cookies, order_sn='', work_order_sn=''):
        url = self.mk_url('fuwu', 'api/workorder/getAllOrderList')
        data = {
            'pageSize': 30,
            'pageIndex': 1,
            'orderSn': order_sn,
            'wrkordSn': work_order_sn,
            'startDate': time.strftime('%Y-%m-%d', time.localtime())
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 工单系统-工单重新分配
    def service_work_order_dispatch(self, cookies, work_order_id='', user_name='', user_id=''):
        url = self.mk_url('fuwu', 'api/workorder/dispatchOrder')
        data = {
            'workOrderId': work_order_id,  # 工单Id
            'userId': user_id,
            'userName': user_name  # 分配人姓名
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 工单系统-工单处理
    def service_work_order_check(self, cookies, work_order_id):
        url = self.mk_url('fuwu', 'api/workorder/handleOrder')
        data = {
            'handleImgJson': ["https://public.fuyoukache.com/5bf69a74-5dbe-401b-b2bf-e0c89aba8a2a---find_element_by_xpath.png"],
            'department': '',
            'methodType': 1,
            'handleResult': '技术测试',
            'visibleRange': '',
            'id': work_order_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 获取用户接单状态
    def service_get_user_status(self, cookies):
        url = self.mk_url('fuwu', 'api/u/com/getUserStatus.do')
        r = requests.get(url, cookies=cookies)
        return r.json()

    # 获得分组用户列表
    def service_list_group_user(self, group_id, cookies, page_index=1, pagesize=100, id=None, name=None):
        url = self.mk_url('fuwu', 'api/u/com/listGroupUser')
        data = {
            'pageIndex': page_index,
            'pageSize': pagesize,
            'id': id,
            'name': name,  # 分组名称
            'groupId': group_id,
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 获取分组列表
    def service_list_groups(self, type, cookies_service):
        url = self.mk_url('fuwu', 'api/u/com/listGroups.do')
        data = {
            'type': type
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 查看待办任务列表
    def service_handling_task_list(self, cookies_service):
        url = self.mk_url('fuwu', 'api/task/selectHandlingList.do')
        data = {
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    #  任务审核通过接口
    def service_pass_task(self, task_id, task_json, data_json, cookies_service):
        url = self.mk_url('fuwu', 'api/task/passTask')
        data = {
            'taskId': task_id,
            'taskJson': json.dumps(task_json),
            'dataJson': json.dumps(data_json)
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    #  任务审核不通过接口
    def service_reject_task(self, task_id, task_json, data_json, cookies_service):
        url = self.mk_url('fuwu', 'api/task/rejectTask.do')
        data = {
            'taskId': task_id,
            'taskJson': json.dumps(task_json),
            'dataJson': json.dumps(data_json)
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 工单办理、暂缓或者流转
    def service_handle_order(self, wkord_id, method_type, cookies_service, handle_result='接口自动化处理', rule_id=None,
                             content=None, img_json=None, urgency_type_id=None, department=None, visible_range=None,
                             feedck_effect=None, flow_department=101, handle_img_json=None):
        url = self.mk_url('fuwu', 'api/workorder/handleOrder.do')
        data = {
            'id': wkord_id,  # 工单id
            'ruleId': rule_id,  # 业务场景id
            'content': content,  # 工单内容
            'imgJson': json.dumps(img_json),  # 工单上报时选择的照片。例如["123.png","456.png"]
            'urgencyTypeId': urgency_type_id,  # 紧急程度
            'department': department,  # 任务部门
            'visibleRange': visible_range,  # 可见角色。多个角色之间用逗号隔开
            'methodType': method_type,  #  处理类型（1 完结处理 2暂存处理 3 流转处理）
            'handleResult': handle_result,  # 处理结果
            'feedckEffect': feedck_effect,  # 反馈时效
            'flowDepartment': flow_department,  # 101总部职能
            'handleImgJson': json.dumps(handle_img_json)  # 处理工单时选择的照片。例如：["123.png","456.png"]
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 查询待处理、暂缓处理、二次流转、区域待处理工单列表接口
    def service_get_order_list(self, type, cookies_service, page_size=30, page_index=1):
        url = self.mk_url('fuwu', 'api/workorder/getOrderList.do')
        data = {
            'pageSize': page_size,
            'pageIndex': page_index,
            'type': type  # 页面类型：1 暂缓处理 2 待处理 3 二次流转, 4 区域待处理列表
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 监控公司任务完结接口
    def service_handle_monitor_company(self, task_id, cookies_service):
        url = self.mk_url('fuwu', 'api/task/handleMonitorCompany.do')
        data = {
            'taskId': task_id
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 暂存任务接口
    def service_suspend_task(self, task_id, task_json, cookies_service):
        url = self.mk_url('fuwu', 'api/task/suspendTask.do')
        data = {
            'taskId': task_id,  # 任务Id
            'taskJson': json.dumps(task_json)  # 意见
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 更新用户接单状态
    def service_update_user_status(self, new_status, cookies_service):
        url = self.mk_url('fuwu', 'api/u/com/updateUserStatus.do')
        data = {
            'newStatus': new_status  # 目标状态：0,关闭接单, 1 正常接单'
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # ***********待司机完善迁移************
    # 司机登录
    def driver_login(self, driver_mobile, check_code='1123'):
        url = self.mk_url('xdriver', 'api/app/u/login')
        data = {
            'mobile': driver_mobile,
            'checkCode': check_code
        }
        r = requests.post(url, data)
        return r.json()

    # 运单-上传回单
    def driver_order_receipt_upload(self, driver_token, order_sn):
        url = self.mk_url('xdriver', 'api/app/order/uploadReceipt')
        print(url)
        data = {
            'token': driver_token,
            'orderSn': order_sn,
            'imageUrl': 'http://public.fuyoukache.com/FlGtfm3dJLjQ5uujO5lbN-_mm43q'
        }
        r = requests.post(url, data)
        return r.json()

    # ***********待调度完善迁移************
    #   异常申请付款
    def dispatch_pay_apply(self, order_sn, driver_id, cookies):
        url = self.mk_url('dd', 'api/dispatch/paymentApply.do')
        data = {
            'orderSn': order_sn,
            'driverId': driver_id,
            'images': '',
            'reason': '技术测试',
            'type': 2,
            'fee': 1000
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()
