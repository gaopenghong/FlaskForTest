#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
__author__ = "yinqiang"
__date__ = "2019.10.16"

from app.tools.api.api_service import *
from app.tools.api.api_ua import *
from app.tools.api.api_driver import *
from app.tools.api.api_bms import *
from app.tools.api.api_customer_app import *
# from app.tools.api.api_system_config import *


class ServiceDeal(ApiService, ApiDriver, ApiUa, ApiBms, ApiCustomerApp):

    def task_not_to_allocate_check(self, user_mobile, task_id):
        try:
            r_ua_request_id = self.ua_generate_check_code()
            user_password = "Ab@123456789"
            login_info_r = self.ua_login_r(user_mobile, user_password, r_ua_request_id)
            # print(login_info_r.json())
            if login_info_r.json()['status']['desc'] == '用户名或密码错误':
                return '用户名或密码错误,请您检查后再次输入！'
            elif login_info_r.json()['status']['desc'] == '用户已被冻结':
                return '用户已被冻结误,请您检查后再次输入！'
            else:
                user_id = login_info_r.json()['data'][0]['id']
                # print(user_id)
                cookies_ua = login_info_r.cookies.get_dict()
                user_status_r = self.service_get_user_status(cookies_ua)
                # print(user_status_r)
                if user_status_r['data'][0] == 0:
                    return '【服务系统】未开启接单，请您前往【服务系统】开启接单！！！'
                else:
                    task_detail_r = self.service_task_detail(task_id, cookies_ua)
                    # print(task_detail_r)
                    if task_detail_r['status']['desc'] == '任务不存在':
                        return '查询的任务在【服务系统】中不存在，请检查后重新输入“任务编号”！！！'
                    else:
                        groups_list_r = self.service_list_groups(24, cookies_ua)
                        # print(groups_list_r)
                        task_user_list = []
                        for task_info in groups_list_r['data']:
                            # print(task_info)
                            if task_info['name'] == task_detail_r['data'][0]['taskOrder']['name']:
                                for user_info in task_info['groupMaps']:
                                    # print(user_info)
                                    task_user_list.append(user_info['userId'])
                                break
                            else:
                                continue
                        if (user_id in task_user_list) is False:
                            return "此用户未在【服务系统】-【系统配置】-【用户分组】-【%s】中的任务分组，请您移至服务系统进行配置！！！" % \
                                   task_detail_r['data'][0]['taskOrder']['name']
                        else:
                            handling_task_list_r = self.service_handling_task_list(cookies_ua)
                            # print(handling_task_list_r)
                            if handling_task_list_r['page']['totalCou'] == 30:
                                return "此用户【服务系统】-【任务系统】-【代办任列表】中待处理任务数量已达到最大值30，请您处理N条任务后重试！！！"
                            else:
                                return "亲爱的同志，你在搞事情哦^_^，此任务可以被分配给您的呢！！！"
        except Exception as e:
            return e

    def task_or_wrkord_all_deal(self, user_mobile, deal_type, method_type):
        try:
            r_ua_request_id = self.ua_generate_check_code()
            user_password = "Ab@123456789"
            login_info_r = self.ua_login_r(user_mobile, user_password, r_ua_request_id)
            # print(login_info_r.json())
            if login_info_r.json()['status']['desc'] == '用户名或密码错误':
                return '用户名或密码错误,请您检查后再次输入！'
            elif login_info_r.json()['status']['desc'] == '用户已被冻结':
                return '用户已被冻结误,请您检查后再次输入！'
            else:
                user_id = login_info_r.json()['data'][0]['id']
                # print(user_id)
                cookies_ua = login_info_r.cookies.get_dict()
                if int(deal_type) == 0:
                    order_list = self.service_get_order_list(2, cookies_ua)
                    # print(order_list)
                    if order_list['page']['totalCou'] != 0:
                        error_wrkord_id = None
                        error_desc = None
                        for wrkord_deatil in order_list['data']:
                            # print(wrkord_deatil['id'])
                            r = self.service_handle_order(wrkord_deatil['id'], method_type, cookies_ua, handle_result='自动化工具处理')
                            # print(r)
                            if r['status']['desc'] == '操作成功':
                                continue
                            else:
                                error_wrkord_id = wrkord_deatil['sn']
                                error_desc = r['status']['desc']
                                break
                        if self.service_get_order_list(2, cookies_ua)['page']['totalCou'] == 0:
                            return '操作成功，处理数量为%s' % order_list['page']['totalCou']
                        else:
                            return '工单（%s）处理出现出现问题，问题描述：%s' % (error_wrkord_id, error_desc)
                    else:
                        return '待处理工单数已为0'
                elif int(deal_type) == 1:
                    task_list = self.service_handling_task_list(cookies_ua)
                    # print(task_list)
                    if task_list['page']['totalCou'] != 0:
                        error = []
                        if int(method_type) == 1:
                            for task_deatil in task_list['data']:
                                # print(task_deatil)
                                if task_deatil['taskTypeId'] == 2300:  # 初审
                                    task_json = {"content": "自动化工具处理：取消运单", "cancelCauseType": 3, "remark": "自动化工具处理"}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                # elif task_deatil['taskTypeId'] == 3400:  # 回单审核
                                #     task_json = {"content": "自动化工具处理：驳回", "cancelCauseType": 1, "remark": "清空列表处理"}
                                #     deal_result = self.service_reject_task(task_deatil['id'], task_json, {}, cookies_ua)
                                #     if deal_result['status']['desc'] == "操作成功":
                                #         pass
                                #     else:
                                #         error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 4000:  # 司机付款申请
                                    task_json = {"content": "自动化工具处理：驳回", "cancelCauseType": 4, "remark": "清空列表处理"}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 4200 or task_deatil['taskTypeId'] == 4210:  # 运单跟踪(CC)
                                    task_json = {"content": "自动化工具处理：确认处理"}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 4400:  # 司机资质审核
                                    detail = self.service_task_detail(task_deatil['taskSn'], cookies_ua)
                                    driver_info = self.crm_driver_detail(task_deatil['customerId'], cookies_ua)
                                    # print(driver_info)
                                    task_json = {"content": "自动化工具处理：驳回"}
                                    data_json = {"oldCreateTime": detail['data'][0]['taskOrder']['createTime'],
                                                 "jsonStr": {
                                                     "id": driver_info['data'][0]['id'], "status": 3,
                                                     "idCardNumber": driver_info['data'][0]['idCardNumber'],
                                                     "name": driver_info['data'][0]['name'],
                                                     "mobile": driver_info['data'][0]['mobile'],
                                                     "idCardAddress": driver_info['data'][0]['idCardAddress'],
                                                     "frontStatus": 3, "backStatus": 3, "licenStatus": 3,
                                                     "truckInfoList": [{
                                                         "id": driver_info['data'][0]['truckInfoList'][0]['id'],
                                                         "plateNumber": driver_info['data'][0]['truckInfoList'][0]['plateNumber'],
                                                         "status": 3,
                                                         "carModelId": driver_info['data'][0]['truckInfoList'][0]['carModelId'],
                                                         "carLengthId": driver_info['data'][0]['truckInfoList'][0]['carLengthId'],
                                                         "carLengthName": driver_info['data'][0]['truckInfoList'][0]['carLengthName'],
                                                         "carModelName": driver_info['data'][0]['truckInfoList'][0]['carModelName'],
                                                         "carLicenStatus": 3, "loadLicenStatus": 3, "insurStatus": 3,
                                                         "driverTruckStatus": 3,
                                                     }],
                                                 }}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 4800:  # 企业资质审核
                                    task_info = self.service_task_detail(task_deatil['taskSn'], cookies_ua)
                                    # print(task_info)
                                    data_json = {
                                        "checkResultEnum": "CHECKING",
                                        "companyName": task_info['data'][0]['companyInfo']['companyName'],
                                        "bankDeposit": task_info['data'][0]['companyInfo']['bankDeposit'],
                                        "companyStatusDesc": "NORMAL",
                                        "checkResult": 1,
                                        "statusEnum": "CHECKING",
                                        "identityImageUrl": task_info['data'][0]['companyInfo']['identityImageUrl'],
                                        "creditCode": task_info['data'][0]['companyInfo']['creditCode'],
                                        "bankInfoStatus": 2,
                                        "roadTransportImageUrl": task_info['data'][0]['companyInfo']['roadTransportImageUrl'],
                                        "identity": task_info['data'][0]['companyInfo']['identity'],
                                        "licenceImageUrl": task_info['data'][0]['companyInfo']['licenceImageUrl'],
                                        "dropItemCount": 0,
                                        "licenceImageStatus": 3,
                                        "legalPerson": task_info['data'][0]['companyInfo']['legalPerson'],
                                        "foundingTime": time.strftime("%Y-%m-%d", time.localtime(
                                            task_info['data'][0]['companyInfo']['foundingTime'] / 1000)),
                                        "identityImageStatus": 3,
                                        "id": task_info['data'][0]['companyInfo']['id'],
                                        "businessTermEndTime": time.strftime("%Y-%m-%d",
                                                                             time.localtime(task_info['data'][0]['companyInfo']['businessTermEndTime'] / 1000)),
                                        "companyCode": task_info['data'][0]['companyInfo']['companyCode'],
                                        "bankNumber": task_info['data'][0]['companyInfo']['bankNumber'],
                                        "address": task_info['data'][0]['companyInfo']['address'],
                                        "statusDesc": "审核中",
                                        "companyStatus": 1,
                                        "updateTime": time.strftime("%Y-%m-%d", time.localtime(
                                            task_info['data'][0]['companyInfo']['updateTime'] / 1000)),
                                        "checkInfo": {"roadTransportStatus": 1,
                                                      "checkResultEnum": "CHECKING",
                                                      "bankInfoStatus": 1,
                                                      "licenceImageStatus": 1,
                                                      "identityImageStatus": 1,
                                                      "inhandImageStatus": 1,
                                                      "checkResult": 1},
                                        "foundingTimeFmt": str(task_info['data'][0]['companyInfo']['foundingTimeFmt']),
                                        "businessTermEndTimeFmt": str(
                                            task_info['data'][0]['companyInfo']['businessTermEndTimeFmt']),
                                        "roadTransportStatus": 3,
                                        "createTime": str(time.strftime("%Y-%m-%d", time.localtime(
                                            task_info['data'][0]['companyInfo']['createTime'] / 1000))),
                                        "companyStatusEnum": "NORMAL",
                                        "inhandImageStatus": 1,
                                        "status": 1
                                    }
                                    # print(self.data_json)
                                    task_json = {"content": "自动化工具处理：驳回", "checkResult": 3}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5000 or task_deatil['taskTypeId'] == 5500:  # 扣款申诉(企业运力/司机)
                                    detail = self.service_task_detail(task_deatil['taskSn'], cookies_ua)
                                    # print(detail)
                                    appeal_task_info = detail['data'][0]['appealTaskInfo'][0]
                                    type_num = len(appeal_task_info['detail'])
                                    data_json = {}
                                    if type_num == 1:
                                        old_money1 = appeal_task_info['detail'][0]['deductMoney']
                                        type1 = appeal_task_info['detail'][0]['type']
                                        data_json = {
                                            "detail": [{
                                                "newMoney": old_money1,
                                                "status": 3,  # 1审核中 2审核通过 3审核不通过
                                                "oldMoney": old_money1,
                                                "type": type1,
                                                "handleContent": "驳回"
                                            }]
                                        }
                                    else:
                                        old_money1 = appeal_task_info['detail'][0]['deductMoney']
                                        type1 = appeal_task_info['detail'][0]['type']
                                        old_money2 = appeal_task_info['detail'][1]['deductMoney']
                                        type2 = appeal_task_info['detail'][1]['type']
                                        data_json = {
                                            "detail": [{
                                                "newMoney": old_money1,
                                                "status": 3,  # 1审核中 2审核通过 3审核不通过
                                                "oldMoney": old_money1,
                                                "type": type1,
                                                "handleContent": "驳回"
                                            }, {
                                                "newMoney": old_money2,
                                                "status": 3,  # 1审核中 2审核通过 3审核不通过
                                                "oldMoney": old_money2,
                                                "type": type2,
                                                "handleContent": "驳回"
                                            }]
                                        }
                                    task_json = {"content": "自动化工具处理：确认处理（驳回）", "imgJson": []}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5100:  # 运单取消审核
                                    task_json = {"content": "自动化工具处理：驳回"}
                                    data_json = {"methodType": 2}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5200:  # 直采司机付款
                                    task_json = {"content": "自动化工具处理：手动付款"}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                # elif task_deatil['taskTypeId'] == 5300:  # 延迟发车预警
                                #     task_json = {"content": "自动化工具处理：确认处理"}
                                #     r = self.bms_order_detail(task_deatil['orderSn'], cookies_ua)
                                #     print(r['data'])
                                #     data_json = {}
                                #     deal_result =self.service_pass_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                #     if deal_result['status']['desc'] == "操作成功":
                                #         pass
                                #     else:
                                #         error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5600:  # 监控配置
                                    deal_result = self.service_handle_monitor_company(task_deatil['id'], cookies_ua)
                                    print(deal_result)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5800:  # 吸货付款确认
                                    task_json = {"content": "自动化工具处理：确认处理", "tags": ""}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 5900:  # 车速异常
                                    task_json = {"content": "自动化工具处理：确认处理"}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 6000:  # 货主申诉
                                    detail = self.service_task_detail(task_deatil['taskSn'], cookies_ua)
                                    task_json = {"content": "自动化工具处理：确认处理", "imgJson": []}
                                    data_json = {"appealId": detail['data'][0]['appealCustomerJson']['id'], "amount": 0}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 6100:  # 指派确认
                                    task_json = {"content": "自动化工具处理：取消订单", "cancelCauseType": 3, "remark": "自动化工具处理"}
                                    deal_result = self.service_reject_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                # elif task_deatil['taskTypeId'] == 6100:  # 指派确认
                                elif task_deatil['taskTypeId'] == 6200:  # 无心跳预警
                                    task_json = {"content": "自动化工具处理：确认处理"}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 6300:  # 及时派车预警
                                    task_json = {"content": "自动化工具处理：确认处理"}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, {}, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                elif task_deatil['taskTypeId'] == 6400:  # 吸货催付款
                                    task_json = {"content": "自动化工具处理：确认处理"}
                                    data_json = {"content": "自动化工具填写备注"}
                                    deal_result = self.service_pass_task(task_deatil['id'], task_json, data_json, cookies_ua)
                                    if deal_result['status']['desc'] == "操作成功":
                                        pass
                                    else:
                                        error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': deal_result})
                                else:
                                    error.append({'任务编号': task_deatil['taskSn'], '不能处理原因': '未知任务类型'})
                        elif int(method_type) == 2:
                            for task_deatil in task_list['data']:
                                # print(task_deatil)
                                task_json = {"content": "自动化工具处理：暂存处理"}
                                self.service_suspend_task(task_deatil['id'], task_json, cookies_ua)
                        else:
                            error.append("此处理类型不能应用于【任务】处理")
                        # print(error)
                        if len(error) == 0:
                            return '操作成功'
                        else:
                            return '操作成功\n特殊说明：%s' % error
                    else:
                        return '待办任务数已为0'
                else:
                    return "未知类型"
        except Exception as e:
            return e

    def task_create_data(self, order_sn, task_type_id):
        # try:
            r_ua_request_id = self.ua_generate_check_code()
            user_mobile = '16888888888'
            user_password = "Ab@123456789"
            login_info_r = self.ua_login_r(user_mobile, user_password, r_ua_request_id)
            if login_info_r.json()['status']['desc'] != '操作成功':
                return '内置后台账号登录出错，请联系相关人员排查！！！'
            else:
                cookies_ua = login_info_r.cookies.get_dict()
                order_detail = self.bms_order_detail(order_sn, cookies_ua)
                print(order_detail)
                if order_detail['status']['desc'] != '操作成功':
                    return '错误信息为:%s' % order_detail['status']['desc']
                else:
                    if order_detail['data'][0]['quote']['statusBrk'] < 11:
                        return '运单状态为:%s，不能进行此操作' % order_detail['data'][0]['quote']['statusName']
                    else:
                        driver_mobile = order_detail['data'][0]['orderDriver']['driverMobile']
                        driver_id = order_detail['data'][0]['orderDriver']['driverId']
                        receipt_need = order_detail['data'][0]['businessInfo']['needReceipt']
                        print(task_type_id)
                        if int(task_type_id) == 2300:  # 初审
                            pass
                            # self.make_quote_info()
                        elif int(task_type_id) == 3400:  # 回单审核
                            driver_info = self.driver_login(driver_mobile)
                            # print(driver_info)
                            driver_token = driver_info['data'][0]['token']
                            task_sn = None
                            # 运单系统异常修改卸货完成
                            data = {'dateline': time.strftime('%Y-%m-%d %H:%M:%S')}
                            self.bms_order_exception(order_sn, 12, modify_data=data, cookies_bms=cookies_ua)
                            # 司机上传回单
                            self.driver_order_receipt_upload(driver_token, order_sn)
                            # 获取任务编号
                            task_info = self.service_task_search(cookies_ua)
                            for task_detail in task_info['data']:
                                if task_detail['orderSn'] == order_sn and task_detail['taskTypeId'] == 3400:
                                    task_sn = task_detail['taskSn']
                                    break
                                else:
                                    continue
                            return '操作成功，任务编号为:%s' % task_sn
                        elif int(task_type_id) == 4000:  # 司机付款申请
                            task_sn = None
                            # 调度系统异常申请付款
                            dispatch_pay_apply_r = self.dispatch_pay_apply(order_sn, driver_id, cookies_ua)
                            if dispatch_pay_apply_r['status']['desc'] == '操作成功':
                                # 获取任务编号
                                task_info = self.service_task_search(cookies_ua)
                                for task_detail in task_info['data']:
                                    if task_detail['orderSn'] == order_sn and task_detail['taskTypeId'] == 4000:
                                        task_sn = task_detail['taskSn']
                                        break
                                    else:
                                        continue
                                return '操作成功，任务编号为:%s' % task_sn
                        elif int(task_type_id) == 5200:  # 直采司机付款
                            task_sn = None
                            # 运单系统异常修改卸货完成
                            data = {'dateline': time.strftime('%Y-%m-%d %H:%M:%S')}
                            bms_order_exception_r = self.bms_order_exception(order_sn, 12, modify_data=data,
                                                                             cookies_bms=cookies_ua)
                            if bms_order_exception_r['status']['desc'] == '操作成功':
                                if receipt_need == 0:
                                    pass
                                else:
                                    self.bms_order_receipt_upload(order_sn, cookies_ua)
                                # 通过修改数据库，立即生成任务
                                env_list = {'t1': 30110, 't2': 30120, 't3': 30130, 't4': 30140, 't15': 30150, 't6': 30160,
                                            't7': 30170, 't8': 30180, 't9': 30190, 't10': 30200, 't11': 30210, 'r1': 30112,
                                            'r2': 30122, 'd1': 30111, 'd2': 30121, 'd3': 30131}
                                sql = 'update monitor_alarm_task set scheduleTime=date_sub(now(), INTERVAL 3 SECOND), ' \
                                      'maxLifeTime=date_sub(now(), INTERVAL 3 SECOND)  where taskType=65 and orderSn=' \
                                      + str(order_sn)
                                remote_database(env_list[self.env], 'fykc_order_center', sql)
                                print("等待30s，直采司机付款任务生成.......")
                                time.sleep(30)
                                # 获取任务编号
                                task_info = self.service_task_search(cookies_ua)
                                for task_detail in task_info['data']:
                                    if task_detail['orderSn'] == order_sn and task_detail['taskTypeId'] == 5200:
                                        task_sn = task_detail['taskSn']
                                        break
                                    else:
                                        continue
                                return '操作成功，任务编号为:%s' % task_sn
                            else:
                                return {'出错原因': bms_order_exception_r}
                        else:
                            return '未知任务类型！！！'
        # except Exception as e:
        #     return e

    # def task_dispatch(self, task_sn):
    #     try:
    #         r_ua_request_id = self.ua_generate_check_code()
    #         user = 16888888888
    #         user_password = "Ab@123456789"
    #         login_info_r = self.ua_login_r(user, user_password, r_ua_request_id)
    #         if login_info_r.json()['status']['desc'] == '用户名或密码错误':
    #             return '用户名或密码错误,请您检查后再次输入！'
    #         elif login_info_r.json()['status']['desc'] == '用户已被冻结':
    #             return '用户已被冻结误,请您检查后再次输入！'
    #         else:
    #             cookies_ua = login_info_r.cookies.get_dict()
    #             task_detail = self.service_task_detail(task_sn, cookies_ua)
    #             task_type_id = task_detail['data'][0]['taskOrder']['taskTypeId']
    #             task_id = task_detail['data'][0]['taskOrder']['id']
    #             task_type_name = task_detail['data'][0]['taskOrder']['name']
    #             # print(task_detail)
    #             # print(task_type_id, task_type_name, task_id)
    #             user_info = self.service_select_user_list(cookies_ua, name=session.get('username'))
    #             # print(user_info)
    #             user_id = user_info['data'][0]['id']
    #             user_name = user_info['data'][0]['name']
    #             user_mobile = user_info['data'][0]['mobile']
    #             # print(user_id, user_name)
    #             r = self.service_list_group_user(task_type_id, cookies_ua)
    #             # print(r)
    #             group_map_userids = []
    #             users_json = []
    #             for i in r['data'][0]['groupMaps']:
    #                 group_map_userids.append(i['userId'])
    #                 user_json = {
    #                     "userId": i['userId'],
    #                     "userName": i['userName'],
    #                     "mobile": i['mobile']
    #                 }
    #                 users_json.append(user_json)
    #             # print(group_map_userids)
    #             # print(users_json)
    #             if user_id in group_map_userids:
    #                 pass
    #             else:
    #                 users_json.append({"userId": user_id, "userName": user_name, "mobile": user_mobile})
    #                 sys_task_group_user_update_r = self.service_sys_task_group_user_update(cookies_ua, task_type_id,
    #                                                                                        task_type_name, users_json)
    #                 # print(sys_task_group_user_update_r)
    #                 sys_task_group_user_update_r['status']['code'] = 0
    #             # 开启接单
    #             sys_update_user_status_r = self.service_sys_update_user_status(1, cookies_ua)
    #             if sys_update_user_status_r['status']['code'] == 0:
    #                 # 任务重新分配
    #                 task_dispatch_r = self.service_task_dispatch(cookies_ua, task_id=task_id, user_name=user_name,
    #                                                              user_id=user_id)
    #                 if task_dispatch_r['status']['code'] == 0:
    #                     # 关闭接单
    #                     sys_update_user_status_r2 = self.service_sys_update_user_status(0, cookies_ua)
    #                     if sys_update_user_status_r2['status']['code'] == 0:
    #                         return "操作成功"
    #                     else:
    #                         return {'出错原因': "关闭接单失败", '接口返回': sys_update_user_status_r2}
    #                 else:
    #                     return {'出错原因': "任务重新分配失败", '接口返回': task_dispatch_r}
    #             else:
    #                 return {'出错原因': "开启接单失败", '接口返回': sys_update_user_status_r}
    #     except Exception as e:
    #         return e


if __name__ == '__main__':
    sd = ServiceDeal('r1')
    # r = sd.task_not_to_allocate_check('15944584448', 1)
    # r = sd.task_or_wrkord_all_deal('16888888888', 1, 1)
    # r = sd.task_dispatch_and_deal('RW191126T2L71Q70')
    r = sd.task_create_data('229112883900', 2300)
    print(r)
