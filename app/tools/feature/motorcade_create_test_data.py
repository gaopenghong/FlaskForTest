from app.tools.api.api_agent import ApiAgent
from app.tools.api.api_bms import ApiBms
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_customer_pc import ApiCustomerPC
from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_service import ApiService
from app.tools.api.api_ua import ApiUa
from app.tools.api.api_xcusotmer_app import *
from app.util.ssh_conf import remote_database


class MotorcadeCreateTestData(ApiAgent, ApiCustomerPC, ApiCrm, ApiDriver, ApiBms, ApiService, ApiUa):
    def __init__(self, environment, admin_mobile, admin_password, agent_mobile, customer_mobile, driver_mobile):
        super().__init__(environment, admin_mobile=admin_mobile, admin_password=admin_password,
                         customer_mobile=customer_mobile, agent_mobile=agent_mobile, driver_mobile=driver_mobile)

    # 创建各状态订单
    def motorcade_create_test_data(self, line_info_list, test_data, receipt_check, order_status, bill_status):
        env = self.env
        order_sn = ''
        bill_no = ''
        test_data_list = ['运单', '月账单', '补贴月账单']
        # 运单状态
        order_status_list = ['待派车', '运输中', '待签收', '已签收', '回单审核中', '回单审核不通过', '回单审核通过', '已确认运单', '账期内提款中']
        # 账单状态
        bill_status_list = ['待确认月账单', '确认月账单', '账单发票审核中', '账单发票审核通过', '付款中']
        # 补贴月账单
        # 回单状态
        receipt_check_list = ['不需回单', '需回单']
        request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, request_id)
        admin_info = self.bms_admin_info(cookies_ua)
        admin_id = admin_info['property']['user']['id']
        admin_name = admin_info['property']['user']['name']
        customer_cookie = self.customer_pc_login()
        r_agent_login = self.agent_app_login()
        agent_token = r_agent_login['data'][0]['token']
        agent_id = r_agent_login['data'][0]['id']
        r_driver_login = self.driver_login(self.driver_mobile, '1123')
        print("司机登录结果:"+str(r_driver_login))
        driver_id = r_driver_login['data'][0]['id']
        r_broker = self.agent_crm_select_list(broker_mobile=self.agent_mobile, cookies_service=cookies_ua)
        print("企业运力查询结果:"+str(r_broker))
        broker_company_name = r_broker['data'][0]['companyName']
        for line_index in range(len(line_info_list)):
            print("查询始发地、经停点、目的地信息")
            line_info_list[line_index] = address_search(line_info_list[line_index])
        # 创建项目线路
        line_route_id = self.crm_create_project_line(line_info_list, self.customer_mobile, admin_id, admin_name,
                                                     cookies_ua)
        r = line_route_id
        print("创建项目线路:" + str(r))
        # 创建福佑线路
        r = self.agent_crm_create_broker_line(line_route_id=line_route_id, broker_mobile_1=self.agent_mobile,
                                              transport_type='2', cookies_service=cookies_ua)
        print("创建福佑线路:" + str(r))
        # 发货
        time.sleep(5)
        if receipt_check_list.index(receipt_check) == 0:
            order_sn = self.crm_agent_delivery(line_info_list, customer_cookie, need_receipt=0)
            print("发货:" + str(order_sn))
        elif receipt_check_list.index(receipt_check) == 1:
            order_sn = self.crm_agent_delivery(line_info_list, customer_cookie, need_receipt=1)
            print("发货:" + str(order_sn))
        # 测试数据为运单
        if test_data_list.index(test_data) >= 0:
            if test_data_list.index(test_data) == 1:
                order_status = '已确认运单'
            # 待派车
            if order_status_list.index(order_status) >= 0:
                pass
            # 运输中
            if order_status_list.index(order_status) >= 1:
                self.agent_bind_driver_broker(agent_token, driver_id)
                driver_info = self.agent_driver_detail(agent_token, self.driver_mobile)['data'][0]
                time.sleep(2)
                r = self.agent_order_arrange_driver(agent_token, driver_info=driver_info, order_sn=order_sn)
                print(r)
                r_desc = r['status']['desc']
                if '占用' in r_desc:
                    employ_order_sn = r_desc.split('被运单')[1].split('占用')[0]
                    self.bms_order_exception(employ_order_sn, 12, cookies_bms=cookies_ua)
                    r = self.agent_order_arrange_driver(agent_token, driver_info=driver_info, order_sn=order_sn)
                    print(r)
            # 待签收
            if order_status_list.index(order_status) >= 2:
                r = self.bms_order_exception(order_sn, 12, cookies_bms=cookies_ua)
                print(r)
                r = self.bms_order_exception(order_sn, 22, modify_data={"hasLoadLocation": 1, "hasUnloadLocation": 1},
                                             cookies_bms=cookies_ua)
                print(r)
            # 已签收
            if order_status_list.index(order_status) >= 3:
                time.sleep(5)
                r = self.bms_order_exception(order_sn, 13, cookies_bms=cookies_ua)
                print(r)
            # 取消补贴
            if test_data_list.index(test_data) >= 2:
                r = self.bms_order_exception(order_sn, 11,
                                             modify_data={"cancelFirstReason": 1, "comment": "测试", "customerReason": 1,
                                                          "subsidizeTarget2": 2, "extraAmount": "0",
                                                          "subsidizeAmount": "1000", "cancelSecondReason": 1,
                                                          "subsidizeTarget": 2, "extraAmountSysCalcd": "",
                                                          "subsidizeAmountSysCalcd": ""}, modify_reason='101',
                                             cookies_bms=cookies_ua)
                print(r)
                # 触发补贴月账单
            # 需要回单，回单各状态
            if receipt_check_list.index(receipt_check) == 1:
                # 回单审核中
                if order_status_list.index(order_status) >= 4:
                    r = self.agent_upload_receipt(agent_token, order_sn)
                    print(r)
                # 回单审核未通过
                if order_status_list.index(order_status) == 5:
                    r = self.servive_select_task(cookies_ua, order_sn=order_sn)
                    task_id = r['data'][0]['id']
                    self.service_task_dispatch(cookies_ua, task_id=task_id, user_name='自动化测试', user_id=admin_id)
                    task_json = {"content": "测试驳回", "cancelCauseType": 5, "remark": "测试"}
                    r = self.service_task_check_reject(task_id, cookies=cookies_ua, task_json=task_json)
                    print(r)
                # 回单审核通过
                if order_status_list.index(order_status) >= 6:
                    r = self.servive_select_task(cookies_ua, order_sn=order_sn)
                    task_id = r['data'][0]['id']
                    print("回单审核任务id:" + str(task_id))
                    self.service_task_dispatch(cookies_ua, task_id=task_id, user_name='自动化测试', user_id=admin_id)
                    time.sleep(2)
                    r = self.service_task_check_pass(task_id, data_json="技术测试", cookies=cookies_ua)
                    print("回单审核结果:" + str(r))
                    r = self.bms_order_receipt_confirm(order_sn, cookies_ua)
                    print(r)
            else:
                print('不需回单')
            # 确认运单
            if order_status_list.index(order_status) >= 7:
                r = self.agent_update_order_account(order_sn, agent_token)
                print(r)
            # 申请提款
            if order_status_list.index(order_status) >= 8:
                r = self.agent_get_order_money(order_sn, agent_token)
                r = self.agent_wallet_drawing_batch(agent_token, broker_invoice=r['data'][0]['brokerInvoice'],
                                                    broker_period=r['data'][0]['brokerPeriod'],
                                                    broker_period_days=r['data'][0]['brokerPeriodDays'],
                                                    commission="112.06", is_new=1, order_sn=order_sn,
                                                    trans_fee=r['data'][0]['transFee'], real_available_money="6090.00")
                print(r)

            if test_data_list.index(test_data) == 1:
                # 待确认账单
                if bill_status_list.index(bill_status) >= 0:
                    r = self.agent_account_list(agent_token)
                    if r['status']['desc'] == '操作成功':
                        account_r1 = r['data'][0]['settleInfo'][len(r['data'][0]['settleInfo']) - 1]
                        r1_bill_no = account_r1['billNo']
                    elif r['status']['desc'] == '结果为空':
                        r1_bill_no = ''
                    sql = "select billNo from broker_bill_order_map where orderSn='" + order_sn + "'"
                    r = remote_database(env, 'caiwu', sql)
                    bill_no = r[0][0]
                    create_time = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')
                    sql = "UPDATE broker_bill_info SET createTime = '" + str(create_time) + "' WHERE brokerId = " + str(
                        agent_id) + " and billNo=" + bill_no
                    remote_database(env, 'caiwu', sql)
                    r = {'data': {'desc': '成功进入月账单'}}
                    print(r)
                # 确认月账单
                if bill_status_list.index(bill_status) >= 1:
                    r = self.agent_account_list(agent_token)
                    print(r)
                    if r['status']['desc'] == '操作成功':
                        account_r2 = r['data'][0]['settleInfo'][len(r['data'][0]['settleInfo']) - 1]
                        r2_bill_no = account_r2['billNo']
                    elif r['status']['desc'] == '结果为空':
                        r2_bill_no = ''

                    if r1_bill_no == r2_bill_no and r2_bill_no == bill_no:
                        pass
                    else:
                        r = self.agent_confirm_account(agent_token, bill_no)
                        print(r)
                # 账单发票审核中
                if bill_status_list.index(bill_status) >= 2:
                    # 判断是否使用了之前的结算批次号
                    if r1_bill_no == r2_bill_no and r2_bill_no == bill_no:
                        pass
                    else:
                        # 查询账单
                        r = self.agent_account_list(agent_token)
                        invoice_company = r['data'][0]['settleInfo'][-1]['invoiceCompany']
                        total_money = r['data'][0]['settleInfo'][-1]['totalMoney']
                        # 获取运力公司信息
                        r = self.agent_crm_get_company_list(cookies_ua, company_name=broker_company_name)
                        tax_no = r['data'][0]['creditCode']
                        # 数据库中插入发票
                        sql = "INSERT INTO input_tax_info(invoiceType, purchaseName, salesName, invoiceCode, invoiceNo, projectContent, totalInvoiceFee, netPrice, invoiceFee, invoicePercent, invoiceStatus, certifyStatus, invoiceTime, hasImageStatus, goPassTimeStart, goPassTimeEnd, carNo, createTime, filePath, salesTaxNo) \
                               VALUES (4, '%s','%s', '111001822011', '%s', '', '%s', 246.70, 312.30, '13%%', 0, 0, '2019-06-28 00:00:00', 1,  NULL, NULL, NULL, '2019-07-10 20:54:46', NULL, '%s');" % (
                            invoice_company, broker_company_name, random.randint(10000000, 99999999), total_money,
                            tax_no)
                        print(sql)
                        remote_database(env, 'fykc_taxsys_service', sql)
                        # 查询可用发票
                        r = self.agent_get_able_invoice_list(agent_token, invoice_company)
                        invoice_no = r['data'][0]['invoiceNo']
                        invoice_code = r['data'][0]['invoiceCode']
                        invoice_date = r['data'][0]['invoiceDate']
                        # 录入发票
                        r = self.agent_add_invoice(bill_no, total_money, invoice_date, agent_token, invoice_no,
                                                   invoice_code,
                                                   invoice_company,
                                                   broker_company_name, tax_no)
                        print(r)
                # 账单发票审核通过
                if bill_status_list.index(bill_status) >= 3:
                    # 获取发票编号
                    if r1_bill_no == r2_bill_no and r2_bill_no == bill_no:
                        pass
                    else:
                        r = self.finance_broker_list_all_broker_invoices(cookies_ua)
                        invoice_id = r['data'][0]['id']
                        r = self.finance_broker_list_check_broker_bill_invoice(invoice_id, cookies_ua)
                        print(r)
                # 账单付款中
                if bill_status_list.index(bill_status) >= 4:
                    r = self.finance_broker_list_payment_broker_bill(agent_id, bill_no, cookies_ua)
                    print(r)

        return order_sn, bill_no
