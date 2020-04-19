/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let motorcade = new Motorcade();
    motorcade.init();
    motorcade.table();
});
let Motorcade = function () {
};
Motorcade.prototype = {
    init: function () {
        $('#createMotorcadeData').click(function () {
            let env = $('#environment').val();
            let adminMobile = $('#adminMobile').val();
            let adminPassword = $('#adminPassword').val();
            let customerMobile = $('#customerMobile').val();
            let motorcadeMobile = $('#motorcadeMobile').val();
            let driverMobile = $('#driverMobile').val();
            let startPlace = $('#startPlace').val();
            let stopPlace = $('#stopPlace').val();
            let endPlace = $('#endPlace').val();
            let testData = $('#testData').val();
            let receiptCheck = $('#receiptCheck').val();
            let orderStatus = $('#order_status').val();
            let billStatus = $('#bill_status').val();
            console.log(env);
            if ($.trim(adminMobile) === '' || $.trim(adminPassword) === '' ||
                $.trim(customerMobile) === '' || $.trim(motorcadeMobile) === '' ||
                $.trim(driverMobile) === '' || $.trim(startPlace) === '' ||
                $.trim(endPlace) === '' || $.trim(testData) === '' ||
                $.trim(receiptCheck) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'adminMobile': adminMobile,
                    'adminPassword': adminPassword,
                    'customerMobile': customerMobile,
                    'motorcadeMobile': motorcadeMobile,
                    'driverMobile': driverMobile,
                    'startPlace': startPlace,
                    'stopPlace': stopPlace,
                    'endPlace': endPlace,
                    'testData': testData,
                    'receiptCheck': receiptCheck,
                    'orderStatus': orderStatus,
                    'billStatus': billStatus
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(30000)
                $.ajax({
                    type: 'post',
                    url: '/tools/createMotorcadeTestData',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#account_list_table').bootstrapTable('refresh');
                        $('#createMotorcadeDataResult').val(res);
                    },
                });
            }

        });
        $('#bill_status_div').hide();//？初始化隐藏掉账单状态
        $('#testData').change(function () {
            let testData = $('#testData').val();
            if (testData === '运单') {
                $('#order_status_div').show();
                $('#bill_status_div').hide();
            } else if (testData === '月账单') {
                $('#bill_status_div').show();
                $('#order_status_div').hide();
            }
        });
        $('#selectCheckCode').click(function () {
            let env = $('#environment1').val();
            let mobile = $('#mobile').val();
            let database_name = $('#databaseName').val();
            console.log(env);
            if ($.trim(mobile) === '' || $.trim(database_name) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'mobile': mobile,
                    'databaseName': database_name
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(2000)
                $.ajax({
                    type: 'post',
                    url: '/tools/selectCheckCode',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#select_check_code_list_table').bootstrapTable('refresh');
                        $('#selectCheckCodeResult').val(res);
                    },
                });
            }

        });
        $('#createFyLine').click(function () {
            let env = $('#environment2').val();
            let admin_mobile = $('#fyLineAdminMobile').val();
            let admin_password = $('#fyLineAdminPassword').val();
            let line_route_id = $('#lineRouteId').val();
            let transport_type = $('#transportType').val();
            let mobile = $('#fy_mobile').val();
            console.log(env);
            if ($.trim(mobile) === '' || $.trim(admin_mobile) === '' || $.trim(admin_password) === '' || $.trim(line_route_id) === '' || $.trim(transport_type) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'admin_mobile': admin_mobile,
                    'admin_password': admin_password,
                    'line_route_id': line_route_id,
                    'transport_type': transport_type,
                    'mobile': mobile
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(2000)
                $.ajax({
                    type: 'post',
                    url: '/tools/createFyLine',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#create_fy_line_list_table').bootstrapTable('refresh');
                        $('#createFyLineResult').val(res);
                    },
                });
            }

        });
        $('#transportType').change(function () {
            let transportType = $('#transportType').val();
            if (transportType === 3) {
                $('#mobile').hide();
            } else {
                $('#mobile').show();
            }
        });
        $('#driverFyLine').click(function () {
            let env = $('#environment3').val();
            let adminMobile = $('#fyDriveradminMobile').val();
            let adminPassword = $('#fyDriverAdminPassword').val();
            let customerMobile = $('#fyDriverCustomerMobile').val();
            let startPlace = $('#fyDriverStartPlace').val();
            let stopPlace = $('#fyDriverStopPlace').val();
            let endPlace = $('#fyDriverEndPlace').val();
            let lineDriverStatus = $('#lineDriverStatus').val();
            let driverMobiles = $('#fyDriverMobile').val();
            console.log(env);
            if ($.trim(driverMobiles) === '' || $.trim(adminMobile) === '' || $.trim(adminPassword) === '' || $.trim(lineDriverStatus) === '' || $.trim(customerMobile) === '' || $.trim(startPlace) === '' || $.trim(stopPlace) === '' || $.trim(endPlace) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'adminMobile': adminMobile,
                    'adminPassword': adminPassword,
                    'customerMobile': customerMobile,
                    'startPlace': startPlace,
                    'stopPlace': stopPlace,
                    'endPlace': endPlace,
                    'lineDriverStatus': lineDriverStatus,
                    'driverMobiles': driverMobiles
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(10000)
                $.ajax({
                    type: 'post',
                    url: '/tools/createFyDriverTestData',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_fy_line_list_table').bootstrapTable('refresh');
                        $('#driverFyLineResult').val(res);
                    },
                });
            }

        });
        $('#pushMessages').click(function () {
            let env = $('#environment4').val();
            let adminMobile = $('#messagesAdminMobile').val();
            let adminPassword = $('#messagesAdminPassword').val();
            let appType = $("input[name='appType']:checked").val();
            let msgType = $("input[name='msgType']:checked").val();
            let showType = $("input[name='showType']:checked").val();
            let imgType = $("input[name='imgType']:checked").val();
            console.log(env);
            if ($.trim(appType) === '' || $.trim(msgType) === '' || $.trim(showType) === '' || $.trim(lineDriverStatus) === '' || $.trim(imgType) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'adminMobile': adminMobile,
                    'adminPassword': adminPassword,
                    'appType': appType,
                    'msgType': msgType,
                    'showType': showType,
                    'imgType': imgType
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(2000)
                $.ajax({
                    type: 'post',
                    url: '/tools/pushMessages',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#select_push_messages_list_table').bootstrapTable('refresh');
                        $('#pushMessagesResult').val(res);
                    },
                });
            }

        });
        $('#motorcadeContract').click(function () {
            let env = $('#environment5').val();
            let adminMobile = $('#contractAdminMobile').val();
            let adminPassword = $('#contractAdminPassword').val();
            let motorcadeMobile = $('#contractMotorcadeMobile').val();
            let contractStatus = $("#contractStatus").val();
            console.log(env);
            if ($.trim(adminMobile) === '' || $.trim(adminPassword) === '' || $.trim(contractMotorcadeMobile) === '' || $.trim(contractStatus) === '') {
                Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;
            } else {
                param = {
                    'env': env,
                    'adminMobile': adminMobile,
                    'adminPassword': adminPassword,
                    'motorcadeMobile': motorcadeMobile,
                    'contractStatus': contractStatus
                };
                // Alert.prototype.alertLoading()
                Alert.prototype.alertLoading(5000)
                $.ajax({
                    type: 'post',
                    url: '/tools/motorcadeContract',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#select_motorcade_contract_list_table').bootstrapTable('refresh');
                        $('#motorcadeContractResult').val(res);
                    },
                });
            }

        });


    },

    table: function () {
        $('#motorcade_test_data_list_table').bootstrapTable({

            url: '/tools/getMotorcadeTestDataList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'customerMobile',
                    title: '货主账号'
                },
                {
                    field: 'adminMobile',
                    title: '后台账号'
                },
                {
                    field: 'motorcadeMobile',
                    title: '经纪人账号'
                },
                {
                    field: 'driverMobile',
                    title: '司机账号'
                },
                {
                    field: 'startPlace',
                    title: '始发地'
                },
                {
                    field: 'stopPlace',
                    title: '经停点'
                },
                {
                    field: 'endPlace',
                    title: '目的地'
                },
                {
                    field: 'orderSn',
                    title: '运单号'
                },
                {
                    field: 'billNo',
                    title: '结算批次号'
                },
                {
                    field: 'testData',
                    title: '数据类型'
                },
                {
                    field: 'status',
                    title: '状态'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                }
            ]

        });
        $('#select_check_code_list_table').bootstrapTable({
            url: '/tools/selectCheckCodeList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'databaseName',
                    title: '数据库'
                },
                {
                    field: 'code',
                    title: '验证码'
                },
                {
                    field: 'mobile',
                    title: '手机号'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                }
            ]

        });
        $('#create_fy_line_list_table').bootstrapTable({
            url: '/tools/createFyLineList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'adminMobile',
                    title: '后台账号'
                },
                {
                    field: 'transportType',
                    title: '运力类型'
                },
                {
                    field: 'lineRouteId',
                    title: '项目线路id'
                },
                {
                    field: 'lineId',
                    title: '福佑线路id'
                },
                {
                    field: 'mobile',
                    title: '手机号'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_fy_line_list_table').bootstrapTable({
            url: '/tools/fyDriverTestDataList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'adminMobile',
                    title: '后台账号'
                },
                {
                    field: 'customerMobile',
                    title: '货主账号'
                },
                {
                    field: 'driverMobile',
                    title: '司机账号'
                },
                {
                    field: 'startPlace',
                    title: '始发地'
                },
                {
                    field: 'stopPlace',
                    title: '经停点'
                },
                {
                    field: 'endPlace',
                    title: '目的地'
                },
                {
                    field: 'status',
                    title: '状态'
                },
                {
                    field: 'result',
                    title: '操作结果'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                },
            ]

        });

        $('#select_push_messages_list_table').bootstrapTable({
            url: '/tools/pushMessagesList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'adminMobile',
                    title: '后台账号'
                },
                {
                    field: 'appType',
                    title: '推送终端'
                },
                {
                    field: 'msgType',
                    title: '消息类型'
                },
                {
                    field: 'showType',
                    title: '展示方式'
                },
                {
                    field: 'imgType',
                    title: '图片类型'
                },
                {
                    field: 'result',
                    title: '操作结果'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                },
            ]

        });
        $('#select_motorcade_contract_list_table').bootstrapTable({
            url: '/tools/motorcadeContractList',
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
                    field: 'id',
                    title: '序号',
                    // width: '50%',
                },
                {
                    field: 'operator',
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '环境'
                },
                {
                    field: 'adminMobile',
                    title: '后台账号'
                },
                {
                    field: 'motorcadeMobile',
                    title: '车队账号'
                },
                {
                    field: 'status',
                    title: '合同状态'
                },
                {
                    field: 'result',
                    title: '操作结果'
                },
                {
                    field: 'operatorTime',
                    title: '操作时间'
                },
            ]

        });

    },

};