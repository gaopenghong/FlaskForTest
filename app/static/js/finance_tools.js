/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let finance = new Finance();
    finance.init();
    finance.table();
});
let Finance = function () {
};
Finance.prototype = {
    init: function () {
        $('#paymentChannelsSubmit').click(function () {
            let env = $('#env').val();
            let operate_id = $('input[name=PaymentChannel]:checked').val();
            if ($.trim(env) === '') {
                Alert.prototype.alertWarning("陛下请选择环境哦！");
                return;
            } else {
                param = {
                    'env': env,
                    'operate_id': operate_id,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/paymentChannels',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {

                        $('#paymentChannelsShow').val(res);
                    },
                });
            }

        });
        $('#updateChannelSubmit').click(function () {
            let env = $('#env_update_channel').val();
            let value = $('input[name=updateChannel]:checked').val();
            if ($.trim(env) === '') {
                Alert.prototype.alertWarning("陛下请选择环境哦！");
                return;
            } else {
                param = {
                    'env': env,
                    'value': value,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/updateChannels',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {

                        $('#updateChannelsShow').val(res);
                    },
                });
            }

        });
        $('#financeAllowanceSubmit').click(function () {
            let environment = $('#environment_syh').val();
            let orderSn = $('#order_sn_syh').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeAgentApproval',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_syh').val(res);
                        $('#finance_agent_allowance_table').bootstrapTable('refresh');

                    },
                });
            }

        });
        $('#caiwuSubmit').click(function () {
            let caiwuOrderSn = $('#caiwuOrderSn').val();
            let environment = $('#environment').val();
            let caiwuStatus = $('#caiwuStatus').val();
            $('#add_caiwu_result').val();
            if ($.trim(caiwuOrderSn) =='') {
                Alert.prototype.alertWarning("运单号不能为空");
                return;
            } else {
                param = {
                    'environment': environment,
                    'caiwuOrderSn': caiwuOrderSn,
                    'caiwuStatus': caiwuStatus,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeCheckOnline',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result').val(res);
                        $('#finance_check_order_table').bootstrapTable('refresh');
                    },
                });
            }

        });
        $('#finance_checking_orders_submit').click(function () {
            let finance_checking_orders = $('#finance_checking_orders').val();
            let finance_checking_env = $('#finance_checking_env').val();
            $('#add_finance_checking_result').val();
            if ($.trim(finance_checking_orders) =='') {
                Alert.prototype.alertWarning("运单号不能为空");
                return;
            } else {
                param = {
                    'finance_checking_env_views': finance_checking_env,
                    'finance_checking_orders_views': finance_checking_orders,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeOrderChecking',
                    data: param,
                    success: function (res) {
                        $('#add_finance_checking_result').val(res);
                        $('#finance_order_checking_table').bootstrapTable('refresh');
                    },
                });
            }

        });
        $('#finance_modify_punish_fee_submit').click(function () {
            let finance_modify_punish_fee_env = $('#finance_modify_punish_fee_views_env').val();
            let finance_modify_punish_fee_order = $('#finance_modify_punish_fee_order').val();
            let finance_modify_punish_fee_momey = $('#finance_modify_punish_fee_momey').val();
            $('#add_finance_modify_punish_fee_result').val();
            if ($.trim(finance_modify_punish_fee_order) =='') {
                Alert.prototype.alertWarning("运单号不能为空");
                return;
            } else {
                param = {
                    'finance_modify_punish_fee_env_views': finance_modify_punish_fee_env,
                    'finance_modify_punish_fee_order_views': finance_modify_punish_fee_order,
                    'finance_modify_punish_fee_money_views': finance_modify_punish_fee_momey,
                };
                $.ajax({
                    type: 'post',
                    url: '/tools/financeModifyPunishFee',
                    data: param,
                    success: function (res) {
                        $('#add_finance_modify_punish_fee_result').val(res);
                        $('#finance_modify_punish_fee_table').bootstrapTable('refresh');
                    },
                // Alert.prototype.alertLoading();
            });
            }

        });
        $('#finance_new_fund_doc_submit').click(function () {
            let finance_new_fund_doc_views_env = $('#finance_new_fund_doc_views_env').val();
            let finance_new_fund_doc_number = $('#finance_new_fund_doc_number').val();
            $('#add_finance_new_fund_doc_result').val();
            if ($.trim(finance_new_fund_doc_number) =='') {
                Alert.prototype.alertWarning("个数不能为空");
                return;
            } else {
                param = {
                    'finance_new_fund_doc_env_views': finance_new_fund_doc_views_env,
                    'finance_new_fund_doc_number_views': finance_new_fund_doc_number,
                };
                // Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeNewDoc',
                    data: param,
                    success: function (res) {
                        $('#add_finance_new_fund_doc_result').val(res);
                        $('#finance_new_fund_doc_table').bootstrapTable('refresh');
                    },
                });
            }

        });
        $('#financeFyInternalInvoiceSubmit').click(function () {
            let environment = $('#environment_internal').val();
            let orderSn = $('#order_sn_internal').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeFyInternalInvoiceJs',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_internal').val(res);
                        $('#finance_fy_internal_table').bootstrapTable('refresh');

                    },
                });
            }

        });
        $('#FinanceAgentDefaultMoneySubmit').click(function () {
            let environment = $('#environment_default').val();
            let orderSn = $('#order_sn_default').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/FinanceAgentDefaultMoneyJS',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_default_money').val(res);
                        $('#finance_fy_default_table').bootstrapTable('refresh');

                    },
                });
            }

        });
        $('#FinanceAgentMonthMoneySubmit').click(function () {
            let environment = $('#environment_month_money').val();
            let orderSn = $('#order_sn_month_money').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/FinanceAgentMonthMoneyJS',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_month_money').val(res);
                        $('#finance_fy_month_money_table').bootstrapTable('refresh');

                    },
                });
            }

        });
        $('#FinanceAgentTaxBillSubmit').click(function () {
            let environment = $('#environment_tax_bill').val();
            let orderSn = $('#order_sn_tax').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/FinanceTaxBill',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_tax_bill').val(res);
                        $('#finance_agent_tax_bill_table').bootstrapTable('refresh');

                    },
                });
            }

        });
        $('#driverRewardsManagementSubmit').click(function () {
            let env = $('#driver_rewards_management #env').val();
            let operate_id = $('#driver_rewards_management #operate_id').val();
            let id_or_mobile = $('#id_or_mobile').val();
            let reward_type = $('#reward_type').val();
            let reward_amount = $('#reward_amount').val();
            if ($.trim(env) === '' || $.trim(id_or_mobile) === '' || $.trim(reward_type) === '') {
                Alert.prototype.alertWarning("均为必填项哦！");
                return;
            } else {
                param = {
                    'env': env,
                    'operate_id': operate_id,
                    'id_or_mobile': id_or_mobile,
                    'reward_type': reward_type,
                    'reward_amount': reward_amount,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                        type: 'post',
                        url: '/tools/driverRewardsManagement',
                        // dataType: 'json',
                        data: param,
                        success: function (res) {
                            if (operate_id == 'ProvideDriverRewards' || operate_id == 'DriverRewardsWithdraw') {
                                $('#driverRewardsManagementShow').text(res);
                            } else {
                                var resMsg = res.split(',');
                                var html = '';
                                for (var i = 0; i < resMsg.length; i++) {
                                    if (i == 0) {
                                        html += '<span class="label label-success" style="font-size: small; line-height: 2.0em" >司机端可提金额查询结果</span>'
                                    } else if (i == 1) {
                                        html += '<span class="label label-success" style="font-size: small; line-height: 2.0em">财务提现明细查询结果</span>'
                                    }
                                    html += '<p style="font-size: small; line-height: 1.0em">' + resMsg[i] + '</p>'
                                    $('#driverRewardsManagementShow2').html(html);
                                }

                            }


                        },
                    }
                );
            }

        });
        $('#driver_rewards_management #operate_id').on('change', function (e) {
            switch (e.target.value) {
                case 'ProvideDriverRewards':
                    $('#driverRewardsManagementArea1').show()
                    $('#driverRewardsManagementArea2').hide()
                    break
                case 'DriverRewardsWithdraw':
                    $('#driverRewardsManagementArea1').show()
                    $('#driverRewardsManagementArea2').hide()
                    break
                case 'DriverRewardsQuery':
                    $('#driverRewardsManagementArea1').hide()
                    $('#driverRewardsManagementArea2').show()
                    break
            }
            $('#driverRewardsManagementShow2').html('');
        });
        $('#driver_rewards_management #operate_id').on('change', function (e) {
            switch (e.target.value) {
                case '':
                    $('.select-change').hide()
                    break
                case 'ProvideDriverRewards':
                    $('.select-change').show()
                    break
                case 'DriverRewardsWithdraw':
                    $('.select-change').eq(0).show()
                    $('.select-change').eq(1).hide()
                    $('.select-change').eq(2).hide()
                    break
                case 'DriverRewardsQuery':
                    $('.select-change').eq(0).show()
                    $('.select-change').eq(1).hide()
                    $('.select-change').eq(2).hide()
                    break
            }
        });
        $('#FinanceAgentAccountPaySubmit').click(function () {
            let environment = $('#environment_account_pay').val();
            let orderSn = $('#order_sn_account').val();
            // $('#add_caiwu_result_1').val();
            if ($.trim(environment) === '') {
                Alert.prototype.alertWarning("环境不能为空");
                return;
            } else {
                param = {
                    'env': environment,
                    'orderSn': orderSn
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/financeAgentAccountPay',
                    data: param,
                    success: function (res) {
                        $('#add_caiwu_result_account').val(res);
                        $('#finance_agent_account_pay_table').bootstrapTable('refresh');

                    },
                });
            }

        });
    },
    table: function () {
        $('#payment_channels_list_table').bootstrapTable({
            url: '/tools/getPaymentChannelsList',
            method: 'get',
            // data: res,
            search: true,
            // showColumns: true,
            // checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            // pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'name',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'operate_id',
                    title: '操作类型'
                },
                {
                    field: 'commit',
                    title: '操作结果'
                },
                {
                    field: 'create_time',
                    title: '创建时间'
                }
            ]

        });
        $('#update_channels_list_table').bootstrapTable({
            url: '/tools/updateChannelsList',
            method: 'get',
            // data: res,
            search: true,
            // showColumns: true,
            // checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            // pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'name',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'value',
                    title: '司机提现渠道'
                },
                {
                    field: 'commit',
                    title: '提交信息'
                },
                {
                    field: 'create_time',
                    title: '创建时间'
                }
            ]

        });
        $('#driver_rewards_management_list_table').bootstrapTable({
            url: '/tools/getDriverRewardsManagementList',
            method: 'get',
            // data: res,
            search: true,
            // showColumns: true,
            // checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            // pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'name',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'operate_id',
                    title: '操作类型'
                },
                {
                    field: 'id_or_mobile',
                    title: '司机ID/手机号'
                },
                {
                    field: 'reward_type',
                    title: '奖励类型'
                },
                {
                    field: 'reward_amount',
                    title: '奖励金额'
                },
                {
                    field: 'commit',
                    title: '操作结果'
                },
                {
                    field: 'create_time',
                    title: '创建时间'
                }
            ]

        });
        $('#finance_check_order_table').bootstrapTable({

            url: '/tools/financeCheckOnlineList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '审核人'
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'check_result',
                    title: '审核结果'
                },
                {
                    field: 'check_time',
                    title: '审核时间'
                }
            ]

        });
        $('#finance_agent_allowance_table').bootstrapTable({
            url: '/tools/financeFyInterList4',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
        $('#finance_order_checking_table').bootstrapTable({

            url: '/tools/financeOrderCheckingList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '执行人'
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'check_result',
                    title: '对账结果'
                },
                {
                    field: 'check_time',
                    title: '对账时间'
                }
            ]

        });
        $('#finance_modify_punish_fee_table').bootstrapTable({

            url: '/tools/financeModifyPunishFeeList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '执行人'
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'check_result',
                    title: '修改结果'
                },
                {
                    field: 'check_time',
                    title: '修改时间'
                }
            ]

        });
        $('#finance_new_fund_doc_table').bootstrapTable({

            url: '/tools/financeNewDocList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '执行人'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'check_result',
                    title: '新建结果'
                },
                {
                    field: 'check_time',
                    title: '新建时间'
                }
            ]

        });
        $('#finance_fy_internal_table').bootstrapTable({
            url: '/tools/financeFyInterList1',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
        $('#finance_fy_default_table').bootstrapTable({
            url: '/tools/financeFyInterList2',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
        $('#finance_fy_month_money_table').bootstrapTable({
            url: '/tools/financeFyInterList3',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
        $('#finance_agent_tax_bill_table').bootstrapTable({
            url: '/tools/financeTaxSettlementBill',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
        $('#finance_agent_account_pay_table').bootstrapTable({
            url: '/tools/financeAgentAccountPayList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'check_result',
                    title: '操作信息'
                },
                {
                    field: 'check_time',
                    title: '操作时间'
                }
            ]

        });
    },



};
