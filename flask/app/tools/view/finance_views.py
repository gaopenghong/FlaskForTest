#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session

# models位置
from app.tools.models.finance_model import *

# feature
from app.tools.feature.finance_payment_channels import *
from app.tools.feature.finance_agent_allowance import *
from app.tools.feature.finance_online_check import *
from app.tools.feature.finance_under_the_line_check import *
from app.tools.feature.finance_modify_punish_fee import *
from app.tools.feature.finance_new_fund_doc import *
from app.tools.feature.finance_fy_internal_invoice import *
from app.tools.feature.finance_jinrong_channel_set import *
from app.tools.feature.finance_driver_rewards_management import *
from app.tools.feature.finance_agent_default_money import *
from app.tools.feature.finance_agent_month_bill_able import *
from app.tools.feature.finance_tax_bill_for_agent_month_settlement import *
from app.tools.feature.finance_agent_account_period_pay import *
# 导入蓝本 main
from .. import tools_blue
from app.stat.models import stat


# 财务系统相关
@tools_blue.route('/tools/financeIndex')
def finance_index():
    return render_template('tools/finance.html', name=session.get('username'))


@tools_blue.route('/tools/paymentChannels', methods=['GET', 'POST'])
def payment_channels():
    env = request.values.get('env')
    operate_id = request.values.get('operate_id')
    res = PaymentChannelsSet(env).test_finance_payment_channels(env, operate_id)
    PaymentChannels.create(session.get('username'), env, '-', operate_id, '-', '-', '-', 1, res,
                           datetime.now())  # 记录测试支付通道开启记录
    stat.Operate.create(session.get('username'), '/tools/paymentChannels', datetime.now(), '开启/关闭测试支付通道')
    return res


# 开启支付通道操作列表
@tools_blue.route('/tools/getPaymentChannelsList', methods=['GET', 'POST'])
def get_payment_channels_list():
    res = PaymentChannels.payment_channels(1)
    return res


# 沈玉会 经纪人补贴
@tools_blue.route('/tools/financeAgentApproval', methods=['GET', 'POST'])
def finance_agent_red_package():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    res = TestAgentAllowance(environment=env).test_flow_allowance(order_sn)
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 4)
    stat.Operate.create(session.get('username'), '/tools/financeAgentApproval', datetime.now(),
                        '经纪人补贴插入一条数据')
    return res


@tools_blue.route('/tools/financeFyInterList4', methods=['GET', 'POST'])
def get_finance_agent_approval_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(4)
    print(res)
    return res


# 单欣欣-线下支付审核
@tools_blue.route('/tools/financeCheckOnline', methods=['GET', 'POST'])
def finance_check_online():
    env = request.values.get('environment')
    orderSn = request.values.get('caiwuOrderSn')
    check_status = request.values.get('caiwuStatus')
    if check_status == '审核通过':
        check_status = 2
    elif check_status == '审核拒绝':
        check_status = 3
    res = FinanceFlow(environment=env).test_online_check(orderSn, check_status)
    FyInvoiceInternal.create(session.get('username'), orderSn, env, res, datetime.now(), 5)
    stat.Operate.create(session.get('username'), '/tools/financeCheckOnline', datetime.now(),
                        '在线支付运单审核通过与否')
    return res


@tools_blue.route('/tools/financeCheckOnlineList', methods=['GET', 'POST'])
def finance_check_online_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(5)

    return res


# 单欣欣-批量运单对账
@tools_blue.route('/tools/financeOrderChecking', methods=['GET', 'POST'])
def finance_orders_checking():
    env = request.values.get('finance_checking_env_views')
    order_sns = request.values.get('finance_checking_orders_views')
    res = FinanceFlowUnderLineCheck(environment=env).under_the_line_checking(order_sns)
    FyInvoiceInternal.create(session.get('username'), order_sns, env, res, datetime.now(), 6)
    stat.Operate.create(session.get('username'), '/tools/financeOrderChecking', datetime.now(),
                        '批量运单对账')
    return res


@tools_blue.route('/tools/financeOrderCheckingList', methods=['GET', 'POST'])
def finance_orders_checking_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(6)
    return res


# 单欣欣-批量修改放空费
@tools_blue.route('/tools/financeModifyPunishFee', methods=['GET', 'POST'])
def finance_modify_punish_fee():
    env = request.values.get('finance_modify_punish_fee_env_views')
    order_sns = request.values.get('finance_modify_punish_fee_order_views')
    money_list = request.values.get('finance_modify_punish_fee_money_views')
    res = FinanceModifyPunishFee(environment=env).modify_punish_fee(order_sns, money_list)
    FyInvoiceInternal.create(session.get('username'), order_sns, env, res, datetime.now(), 7)
    stat.Operate.create(session.get('username'), '/tools/financeModifyPunishFee', datetime.now(),
                        '批量修改放空费')
    return res


@tools_blue.route('/tools/financeModifyPunishFeeList', methods=['GET', 'POST'])
def finance_modify_punish_fee_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(7)
    return res


# 单欣欣-生成资金单
@tools_blue.route('/tools/financeNewDoc', methods=['GET', 'POST'])
def finance_new_fund_doc():
    env = request.values.get('finance_new_fund_doc_env_views')
    number = request.values.get('finance_new_fund_doc_number_views')
    res = FinanceNewFundDoc(environment=env).new_fund_list(number)
    FyInvoiceInternal.create(session.get('username'), '', env, res, datetime.now(), 8)
    stat.Operate.create(session.get('username'), '/tools/financeNewDoc', datetime.now(),
                        '生成资金单')
    return res


@tools_blue.route('/tools/financeNewDocList', methods=['GET', 'POST'])
def finance_new_fund_doc_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(8)
    return res


# 沈玉会 内部关联开票数据来源
@tools_blue.route('/tools/financeFyInternalInvoiceJs', methods=['GET', 'POST'])
def finance_fy_internal_data():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    res = TestFyInvoiceInternal(environment=env).test_finance_invoice_internal(order_sn)
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 1)
    stat.Operate.create(session.get('username'), '/tools/financeFyInternalInvoiceJs', datetime.now(),
                        '内部关联开票插入一条数据')
    return res


@tools_blue.route('/tools/financeFyInterList1', methods=['GET', 'POST'])
def get_finance_fy_inter_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(1)
    print(res)
    return res


# 沈玉会 企业运力违约金数据来源
@tools_blue.route('/tools/FinanceAgentDefaultMoneyJS', methods=['GET', 'POST'])
def finance_agent_default_money_data():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    res = TestAgentDefaultMoney(environment=env).test_agent_default_money(order_sn)
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 2)
    stat.Operate.create(session.get('username'), '/tools/FinanceAgentDefaultMoneyJS', datetime.now(),
                        '企业运力收款单插入一条数据')
    return res


@tools_blue.route('/tools/financeFyInterList2', methods=['GET', 'POST'])
def get_finance_agent_money_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(2)
    print(res)
    return res


# 沈玉会 企业运力账期内提款
@tools_blue.route('/tools/FinanceAgentMonthMoneyJS', methods=['GET', 'POST'])
def finance_agent_month_money_data():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    res = TestAgentMonthMoney(env,order_sn).test_agent_month_money()
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 3)
    stat.Operate.create(session.get('username'), '/tools/FinanceAgentMonthMoneyJS', datetime.now(),
                        '企业运力账期内提款')
    return res


@tools_blue.route('/tools/financeFyInterList3', methods=['GET', 'POST'])
def get_finance_agent_month_money_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(3)
    return res


# 沈玉会 企业运力符合的销项税发票
@tools_blue.route('/tools/FinanceTaxBill', methods=['GET', 'POST'])
def finance_agent_tax_bill_data():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    res = TestAgentTaxBill(env, agent_mobile=16499999999).test_tax_bill(order_sn)
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 9)
    stat.Operate.create(session.get('username'), '/tools/FinanceTaxBill', datetime.now(),
                        '企业运力销项税发票')
    return res


@tools_blue.route('/tools/financeTaxSettlementBill', methods=['GET', 'POST'])
def get_finance_tax_bill():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(9)
    return res


# 金融渠道配置
@tools_blue.route('/tools/updateChannels', methods=['GET', 'POST'])
def update_channels():
    env = request.values.get('env')
    value = request.values.get('value')
    res = UpdateChannelInfo(env).test_update_channel_info(int(value))
    if int(value) == 0:
        value_message = "云信"
    else:
        value_message = "平安银行"
    PaymentChannels.create(session.get('username'), env, value_message, '-', '-', "-", '-', 3, res,
                           datetime.now())
    stat.Operate.create(session.get('username'), '/tools/updateChannels', datetime.now(), '司机提现渠道')
    return res


# 金融渠道操作列表
@tools_blue.route('/tools/updateChannelsList', methods=['GET', 'POST'])
def update_channels_list():
    res = PaymentChannels.payment_channels(3)
    return res


# 司机奖励管理
@tools_blue.route('/tools/driverRewardsManagement', methods=['GET', 'POST'])
def driver_rewards_management():
    env = request.values.get('env')
    operate_id_br = request.values.get('operate_id')
    id_or_mobile = request.values.get('id_or_mobile')
    reward_type_br = request.values.get('reward_type')
    reward_amount = request.values.get('reward_amount')
    if reward_amount == '':
        reward_amount = 200
    if reward_type_br == str(2):
        reward_type = "日包车奖励"
    elif reward_type_br == str(3):
        reward_type = "长途包车奖励"
    else:
        reward_type = "里程奖励"
    if operate_id_br == "ProvideDriverRewards":
        operate_id = "发放奖励"
    elif operate_id_br == "DriverRewardsWithdraw":
        operate_id = "奖励提现"
    else:
        operate_id = "奖励查询"

    print(env, operate_id, id_or_mobile, reward_type, reward_amount, type(operate_id), type(id_or_mobile),
          type(reward_type), type(reward_amount))
    res = DriverRewardsManagement(env).provide_driver_rewards_management(str(operate_id_br), str(id_or_mobile),
                                                                         int(reward_type_br),
                                                                         float(reward_amount))

    if operate_id == "奖励提现":
        PaymentChannels.create(session.get('username'), env, '-', operate_id, id_or_mobile, "-", reward_amount, 2, res,
                               datetime.now())
    elif operate_id == "奖励查询":
        PaymentChannels.create(session.get('username'), env, '-', operate_id, id_or_mobile, "-", "-", 2, res,
                               datetime.now())
    else:
        PaymentChannels.create(session.get('username'), env, '-', operate_id, id_or_mobile, reward_type, reward_amount,
                               2,
                               res,
                               datetime.now())
    stat.Operate.create(session.get('username'), '/tools/driverRewardsManagement', datetime.now(), '司机奖励管理')
    return res


# 司机奖励管理操作列表
@tools_blue.route('/tools/getDriverRewardsManagementList', methods=['GET', 'POST'])
def get_driver_rewards_management_list():
    res = PaymentChannels.payment_channels(2)
    return res


# 沈玉会 企业运力账期日（账期外）提款
@tools_blue.route('/tools/financeAgentAccountPay', methods=['GET', 'POST'])
def finance_agent_account_pay():
    env = request.values.get('env')
    order_sn = request.values.get('orderSn')
    # res = TestAgentMonthMoney(env, order_sn).test_agent_month_money()
    res = TestAgentAccountPay(environment=env, order_sn=order_sn).test_order_detail()
    FyInvoiceInternal.create(session.get('username'), order_sn, env, res, datetime.now(), 10)
    stat.Operate.create(session.get('username'), '/tools/financeAgentAccountPay', datetime.now(),
                        '企业运力账期外提款')
    return res


@tools_blue.route('/tools/financeAgentAccountPayList', methods=['GET', 'POST'])
def get_finance_agent_account_pay_list():
    res = FyInvoiceInternal.get_finance_fy_inter_by_type(10)
    print(res)
    return res
