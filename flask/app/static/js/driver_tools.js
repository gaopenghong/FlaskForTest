/**
 * Created by guobingjie on 2019/11/4.
 */


$(document).ready(function () {
    let driver = new Driver();
    driver.init();
    driver.table();
});
let Driver = function () {
};
Driver.prototype = {
    init: function () {

        // 司机人脸识别白名单
        $('#driverWhiteListSubmit').click(function () {
            let driver_mobile = $('#driver_mobile').val();
            let env = $('#environment').val();
            // 获取单选框
            var opt_type = null;
            var obj = document.getElementsByName("opt_type");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }

            $('#driver_white_list_result').val();
            if ($.trim(env) === '' || $.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("环境和手机号均不能为空！");
                return;
            } else {
                param = {
                    'env': env,
                    'opt_type': opt_type,
                    'driver_mobile': driver_mobile,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverWhiteList',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_white_list_result').val(res);
                        $('#driver_white_list_table').bootstrapTable('refresh');
                    }
                });
            }

        });
        $('#driverPayDepositSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverPayDeposit').val();
            let env = $('#environment1').val()
            // 获取单选框
            var opt_type = null;
            var obj = document.getElementsByName("opt_type_driverPayDeposit");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }
            $('#driver_paydeposit_result').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("手机号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'opt_type':opt_type
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverPayDeposit',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_paydeposit_list').bootstrapTable('refresh');
                        $('#driver_paydeposit_result').val(res);
                    }
                });
            }

        });
        $('#driverWhiteDrawingSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverWhiteDrawing').val();
            let env = $('#environment2').val()
            $('#driver_whitedrawing_result').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("手机号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/DriverWhiteDrawing',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_whitedrawing_list').bootstrapTable('refresh');
                        $('#driver_whitedrawing_result').val(res);
                    }
                });
            }

        });
        $('#driverBankBindCardSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverBankBindCard').val();
            let env = $('#environment3').val()
            $('#driver_bank_bind_card_result').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("手机号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverBankBindCard',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_bank_bind_card_list').bootstrapTable('refresh');
                        $('#driver_bank_bind_card_result').val(res);
                    }
                });
            }

        });
        $('#driverOrderMakepointSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverOrderMakepoint').val();
            let order_sn = $('#order_sn').val();
            let env = $('#environment4').val()
            $('#driver_ordermakepoint_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === '') {
                Alert.prototype.alertWarning("手机号或订单号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'order_sn': order_sn
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverOrderMakePoint',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_ordermakepoint_list').bootstrapTable('refresh');
                        $('#driver_ordermakepoint_result').val(res);
                    }
                });
            }

        });
        $('#driverDispatchComfirmOrderSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverDispatchComfirmOrder').val();
            let dispatch_mobile = $('#dispatch_mobile').val();
            let env = $('#environment5').val()
            // 获取单选框
            var opt_type = null;
            var obj = document.getElementsByName("opt_type_driverDispatchComfirm");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }
            $('#driver_dispatchconfirmorder_result').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("手机号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'dispatch_mobile': dispatch_mobile,
                    'opt_type':opt_type
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverDispatchConfirmOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_dispatch_confirm_order_list').bootstrapTable('refresh');
                        $('#driver_dispatchconfirmorder_result').val(res);
                    }
                });
            }

        });
        $('#addDriverSubmit').click(function () {
            let number = $('#number').val();
            let start = $('#start').val();
            let env = $('#environment6').val()
            let driver_status = $('#driver_status').val()
            let truck_status = $('#truck_status').val()
            $('#add_driver_result').val();
            // 获取单选框
            var opt_type= null;
            var obj = document.getElementsByName("opt_type_addDriver");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }
            if ($.trim(number) === '' || $.trim(start) === '' ) {
                Alert.prototype.alertWarning("数量和手机号开头不能为空");
                return;
            } else {
                param = {
                    'env': env,
                    'number': number,
                    'start': start,
                    'opt_type':opt_type,
                    'driver_status':driver_status,
                    'truck_status':truck_status

                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/addDrivertest',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#add_driver_table').bootstrapTable('refresh');
                        $('#add_driver_result').val(res);
                    }
                });
            }

        });
        $('#driveruploadReceiptSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_uploadReceipt').val();
            let order_sn = $('#order_sn_uploadReceipt').val();
            let env = $('#environment7').val()
            $('#driver_uploadReceipt_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === '') {
                Alert.prototype.alertWarning("手机号或订单号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'order_sn': order_sn
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/uploadReceipt',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_uploadReceipt_list').bootstrapTable('refresh');
                        $('#driver_uploadReceipt_result').val(res);
                    }
                });
            }

        });
        $('#driveruploadExceptionSubmit').click(function () {
            let driver_mobile = $('#driver_uploadException').val();
            let order_sn = $('#order_sn_uploadException').val();
            let env = $('#environment8').val()
            $('#driver_uploadException_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === '') {
                Alert.prototype.alertWarning("手机号或订单号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'order_sn': order_sn
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/uploadException',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_uploadException_list').bootstrapTable('refresh');
                        $('#driver_uploadException_result').val(res);
                    }
                });
            }
        });
        $('#driverdispatchpreConfirmSubmit').click(function () {
            let driver_mobile = $('#driver_dispatchpreConfirm').val();
            let order_sn = $('#order_sn_dispatchpreConfirm').val();
            let dispatch_mobile = $('#dispatch_mobile_dispatchpreConfirm').val();
            let env = $('#environment9').val()
            $('#driver_dispatchpreConfirm_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === ''|| $.trim(dispatch_mobile) === '') {
                Alert.prototype.alertWarning("手机号、订单号或者调度不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'order_sn': order_sn,
                    'dispatch_mobile':dispatch_mobile
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/dispatchpreConfirm',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_dispatchpreConfirm_list').bootstrapTable('refresh');
                        $('#driver_dispatchpreConfirm_result ').val(res);
                    }
                });
            }

        });
        $('#driverWithDrawSubmit').click(function () {
            let driver_mobile = $('#driver_WithDraw').val();
            let env = $('#environment10').val()
            // 获取单选框
            var opt_type = null;
            var obj = document.getElementsByName("opt_type_driverwithdraw");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }

            $('#driver_WithDraw_result').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("手机号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'opt_type':opt_type
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driver_WithDraw',
                    data: param,
                    success: function (res) {
                        $('#driver_WithDraw_list').bootstrapTable('refresh');
                        $('#driver_WithDraw_result ').val(res);
                    }
                });
            }
        });
        $('#driverdispatcharrangeSubmit').click(function () {
            let driver_mobile = $('#driver_mobile_driverdispatcharrange').val();
            let order_sn = $('#order_sn_dispatcharrange').val();
            let env = $('#environment11').val()
            $('#driver_dispatcharrange_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === '') {
                Alert.prototype.alertWarning("手机号或订单号不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                    'order_sn': order_sn
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverDispatchArrange',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_dispatcharrange_list').bootstrapTable('refresh');
                        $('#driver_dispatcharrange_result').val(res);
                    }
                });
            }

        });
        $('#drivershortrentSubmit').click(function () {
            let start_provincename = $('#driver_shortrent_start_provincename').val();
            let start_cityname = $('#driver_shortrent_start_cityname').val();
            let end_provincename = $('#driver_shortrent_end_provincename').val();
            let end_cityname = $('#driver_shortrent_end_cityname').val();
            let env = $('#environment12').val()
            $('#driver_shortrent_result').val();
            if ($.trim(start_provincename) === ''|| $.trim(start_cityname) === '' || $.trim(end_provincename) === '' ||$.trim(end_cityname) === '' ) {
                Alert.prototype.alertWarning("始末省市都不能为空哦");
                return;
            } else {
                param = {
                    'env': env,
                    'start_provincename': start_provincename,
                    'start_cityname':start_cityname,
                    'end_provincename':end_provincename,
                    'end_cityname':end_cityname
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverShortRent',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_shortrent_list').bootstrapTable('refresh');
                        $('#driver_shortrent_result').val(res);
                    }
                });
            }

        });
        $('#drivercreateandorderSubmit').click(function () {
            let number = $('#driver_number').val();
            let start = $('#driver_start').val();
            let env = $('#environment13').val()
            let lineid=$('#driver_line_id').val()
            $('#driver_createandorder_result').val();
            if ($.trim(number) === '' || $.trim(start) === '' || $.trim(lineid) === '') {
                Alert.prototype.alertWarning("数量、手机号开头、路线id均不可为空");
                return;
            } else {
                param = {
                    'env': env,
                    'number': number,
                    'start': start,
                    'lineid':lineid
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverCreateAndOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_createandorder_list').bootstrapTable('refresh');
                        $('#driver_createandorder_result').val(res);
                    }
                });
            }

        });
        $('#driverordersnSubmit').click(function () {
            let env = $('#environment14').val()
            let order_sn=$('#driver_order_sn').val()
            $('#driver_ordersn_result').val();
            if ($.trim(order_sn) === '') {
                Alert.prototype.alertWarning("运单号不可为空");
                return;
            } else {
                param = {
                    'env': env,
                    'order_sn': order_sn
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driver_handle_all_exception',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_ordersn_list').bootstrapTable('refresh');
                        $('#driver_ordersn_result').val(res);
                    }
                });
            }

        });
        $('#driverstatusorderSubmit').click(function () {
            let start = $('#driver_status_order_start').val();
            let mobile = $('#driver_status_order').val();
            let env = $('#environment15').val()
            let type = $('#driver_is_exit').val();
            let lineid=$('#driver_status_line_id').val()
            let status=$("#driver_order_status").val()
            $('#driver_statusorder_result').val();
            if (type === '1') {
                console.log(1,start,lineid);
                if ($.trim(start) === '' || $.trim(lineid) === '') {
                    Alert.prototype.alertWarning("手机号开头、路线id不能为空");
                    return;
                }
                else {
                param = {
                    'env': env,
                    'start': start,
                    'lineid':lineid,
                    'status':status,
                    'type':type
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverStatusOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_statusorder_list').bootstrapTable('refresh');
                        $('#driver_statusorder_result').val(res);
                    }
                });
            }

        }
            if (type === '2') {
                console.log(2);
                if ($.trim(mobile) === '' || $.trim(lineid) === '') {
                    Alert.prototype.alertWarning("手机号、路线id不能为空");
                    return;
                }
                else {
                param = {
                    'env': env,
                    'mobile': mobile,
                    'lineid':lineid,
                    'status':status,
                    'type':type
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/driverStatusOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#driver_statusorder_list').bootstrapTable('refresh');
                        $('#driver_statusorder_result').val(res);
                    }
                });
            }

        };
    });
        $('#div_exits').hide();
        $('#driver_is_exit').change(function () {
                let type = $('#driver_is_exit').val();
                if (type === '1') {
                    $('#div_create').show();
                    $('#div_exits').hide()
            } else{
                    $('#div_create').hide();
                    $('#div_exits').show()
            }
        })
 },

    table: function () {
        // 司机人脸识别白名单
        $('#driver_white_list_table').bootstrapTable({

            url: '/tools/getDriverWhiteList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_phone',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'opt_type',
                    title: '操作类型'
                },
                {
                    field: 'result',
                    title: '结果信息'
                },
                {
                    field: 'opt_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_paydeposit_list').bootstrapTable({

            url: '/tools/getDriverPayDepositList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'opt_type',
                    title: '操作类型'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_whitedrawing_list').bootstrapTable({

            url: '/tools/getDriverWhiteDrawingList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_bank_bind_card_list').bootstrapTable({

            url: '/tools/driverBankBindCardList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_ordermakepoint_list').bootstrapTable({

            url: '/tools/driverOrderMakePointList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_dispatch_confirm_order_list').bootstrapTable({

            url: '/tools/driverDispatchConfirmOrderList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'opt_type',
                    title: '操作类型'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#add_driver_table').bootstrapTable({

            url: '/tools/addDrivertestlist',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'num',
                    title: '新建司机数量'
                },

                {
                    field: 'env',
                    title: '环境'
                },
                 {
                    field: 'commit',
                    title: '结果信息'
                },
                 {
                    field: 'opt_type',
                    title: '操作类型'
                },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_uploadReceipt_list').bootstrapTable({

            url: '/tools/uploadReceiptlist',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_uploadException_list').bootstrapTable({

            url: '/tools/uploadExceptionlist',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_dispatchpreConfirm_list').bootstrapTable({

            url: '/tools/dispatchpreConfirmlist',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_WithDraw_list').bootstrapTable({

            url: '/tools/driver_WithDrawlist',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                 {
                    field: 'opt_type',
                    title: '操作类型'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_dispatcharrange_list').bootstrapTable({

            url: '/tools/driverDispatchArrangeList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_shortrent_list').bootstrapTable({

            url: '/tools/driverShortRentList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'address',
                    title: '地址'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'commit',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_createandorder_list').bootstrapTable({

            url: '/tools/driverCreateAndOrderList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'num',
                    title: '新建司机数量'
                },

                {
                    field: 'env',
                    title: '环境'
                },
                 {
                    field: 'commit',
                    title: '结果'
                },
                {
                    field: 'lineid',
                    title: '线路id'
                },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_ordersn_list').bootstrapTable({

            url: '/tools/driver_handle_all_exception_list',
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
                    field: 'operator',
                    title: '操作人'
                },
                {
                    field: 'order_sn',
                    title: '订单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                 {
                    field: 'commit',
                    title: '结果'
                },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]

        });
        $('#driver_statusorder_list').bootstrapTable({

            url: '/tools/driverStatusOrderList',
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
                    field: 'operator',
                    title: '操作人'
                    // width: '50%',
                },
                {
                    field: 'env',
                    title: '环境'
                },
                 {
                    field: 'commit',
                    title: '结果'
                },
                {
                    field: 'lineid',
                    title: '线路id'
                },
                 {
                      field: 'status',
                    title: '运单状态'
                 },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]

        });

    },


};