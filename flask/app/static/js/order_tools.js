/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let order = new Order();
    order.init();
    order.table();
});
let Order = function () {
};
Order.prototype = {
    init: function () {
        $('#debangOrderSubmit').click(function () {
            let env = $('#environment').val();
            let order_code = $('#orderCode').val();
            let orderStauts = $('#orderStauts').val();
            let dotype = $('#dotype1').val();
            let departureName = $('#beginregion').val();
            let arrivalsName = $('#endregion').val();
            let models = $('#carlength').val();
            let boxType = $('#cartype').val();
            let productType = $('#producttype').val();
            let price = $('#price').val();
            $('#debang_order_result').val();
            if (($.trim(productType) === '10' || $.trim(productType) === '11') && $.trim(price) === '') {
                Alert.prototype.alertInfo("裸车价不能为空！");
                return;
            } else {
                param = {
                    'env': env,
                    'order_code': order_code,
                    'orderStauts': orderStauts,
                    'dotype': dotype,
                    'departureName': departureName,
                    'arrivalsName': arrivalsName,
                    'models': models,
                    'boxType': boxType,
                    'productType': productType,
                    'price': price
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/orderDebang',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#orderCode').val(res);
                        $('#third_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        $('#debangconfimSubmit').click(function () {
            let env = $('#environment').val();
            let orderCode = $('#orderCode').val();
            let orderStauts = $('#orderStauts').val();
            let dotype = $('#dotype2').val();
            $('#debang_confim_result').val();
            param = {
                'env': env,
                'orderCode': orderCode,
                'orderStauts': orderStauts,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderDebang',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#debangConfimShow').val(res);
                    $('#debang_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#debangcheckingSubmit').click(function () {
            let env = $('#environment').val();
            let orderCode = $('#orderCode').val();
            $('#debang_checking_result').val();
            param = {
                'env': env,
                'orderCode': orderCode
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderDebangChecking',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#debangCheckingShow').val(res);
                    $('#debang_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#jdOrderSubmit').click(function () {
            let env = $('#environment_jd').val();
            let order_code = $('#jdorderCode').val();
            let carlengthtype = $('#carlengthtype').val();
            let dotype = $('#dotype1').val();
            let bengin_adress = $('#jdbeginregion').val();
            let end_adress = $('#jdendregion').val();
            $('#jd_order_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'carlengthtype': carlengthtype,
                'dotype': dotype,
                'bengin_adress': bengin_adress,
                'end_adress': end_adress,
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderJd',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#jdorderCode').val(res);
                    $('#jd_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#jdconfimSubmit').click(function () {
            let env = $('#environment_jd').val();
            let order_code = $('#jdorderCode').val();
            let dotype = $('#dotype2').val();
            $('#jd_confim_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderJd',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#jdConfimShow').val(res);
                    $('#jd_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#kyOrderSubmit').click(function () {
            let env = $('#environment_ky').val();
            let order_code = $('#kyorderCode').val();
            let carlengthtype = $('#kycar').val();
            let dotype = $('#dotype1').val();
            let bengin_adress = $('#kybeginregion').val();
            let end_adress = $('#kyendregion').val();
            $('#ky_order_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'carlengthtype': carlengthtype,
                'dotype': dotype,
                'bengin_adress': bengin_adress,
                'end_adress': end_adress,
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderKy',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#kyorderCode').val(res);
                    $('#ky_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#kyconfimSubmit').click(function () {
            let env = $('#environment_ky').val();
            let order_code = $('#kyorderCode').val();
            let dotype = $('#dotype2').val();
            $('#ky_confim_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderKy',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#kyConfimShow').val(res);
                    $('#ky_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#sfOrderSubmit').click(function () {
            let env = $('#environment_sf').val();
            let order_code = $('#sforderCode').val();
            let dotype = $('#dotype1').val();
            let vehicleton = $('#vehicleton').val();
            let vehicletypecode = $('#vehicletypecode').val();
            let bengin_adress = $('#sfbeginregion').val();
            let cross_adress = $('#sfcrossregion').val();
            let end_adress = $('#sfendregion').val();
            $('#sf_order_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype,
                'vehicleton': vehicleton,
                'vehicletypecode': vehicletypecode,
                'bengin_adress': bengin_adress,
                'cross_adress': cross_adress,
                'end_adress': end_adress
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderSf',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#sforderCode').val(res);
                    $('#sf_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#sfconfimSubmit').click(function () {
            let env = $('#environment_sf').val();
            let order_code = $('#sforderCode').val();
            let dotype = $('#dotype2').val();
            $('#sf_confim_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderSf',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#sfConfimShow').val(res);
                    $('#sf_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#ytOrderSubmit').click(function () {
            let env = $('#environment_yt').val();
            let order_code = $('#ytorderCode').val();
            let dotype = $('#dotype1').val();
            let carlengthtype = $('#ytcar').val();
            let bengin_adress = $('#ytbeginregion').val();
            let end_adress = $('#ytendregion').val();
            $('#yt_order_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype,
                'carlengthtype': carlengthtype,
                'bengin_adress': bengin_adress,
                'end_adress': end_adress
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderYt',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#ytorderCode').val(res);
                    $('#yt_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#ytconfimSubmit').click(function () {
            let env = $('#environment_yt').val();
            let order_code = $('#ytorderCode').val();
            let dotype = $('#dotype2').val();
            $('#yt_confim_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderYt',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#ytConfimShow').val(res);
                    $('#yt_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#hyddOrderSubmit').click(function () {
            let env = $('#environment_hydd').val();
            let order_code = $('#hyddorderCode').val();
            let dotype = $('#dotype1').val();
            let carlengthtype = $('#hyddcar').val();
            let bengin_adress = $('#hyddbeginregion').val();
            let end_adress = $('#hyddendregion').val();
            $('#hyddt_order_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype,
                'carlengthtype': carlengthtype,
                'bengin_adress': bengin_adress,
                'end_adress': end_adress
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderHydd',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#hyddorderCode').val(res);
                    $('#hydd_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#hyddconfimSubmit').click(function () {
            let env = $('#environment_hydd').val();
            let order_code = $('#hyddorderCode').val();
            let dotype = $('#dotype2').val();
            $('#hydd_confim_result').val();
            param = {
                'env': env,
                'order_code': order_code,
                'dotype': dotype
            };
            Alert.prototype.alertLoading();
            $.ajax({
                type: 'post',
                url: '/tools/orderHydd',
                // dataType: 'json',
                data: param,
                success: function (res) {
                    $('#hyddConfimShow').val(res);
                    $('#hydd_order_list_table').bootstrapTable('refresh');
                    Alert.prototype.alertInfo(res)
                }
            });
        });
        $('#orderAbnormalModifySubmit').click(function () {
            let env = $('#env').val();
            let orderSn = $('#orderSn').val();
            let modifyReason = $('#modifyReason').val();
            let orderStatusModify = $('#orderStatusModify').val();
            if ($.trim(env) === '' || $.trim(orderSn) === '' || $.trim(modifyReason) === '' || $.trim(orderStatusModify) === '') {
                Alert.prototype.alertWarning("陛下以上均为必填项哦");
                return;
            } else {
                param = {
                    'env': env,
                    'orderSn': orderSn,
                    'modifyReason': modifyReason,
                    'orderStatusModify': orderStatusModify,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/abnormalModify',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#order_abnormal_modify_list_table').bootstrapTable('refresh');
                        $('#orderAbnormalModifyShow').val(res);
                    },
                });
            }

        });
        $('#createAutoQuery').click(function () {
            let env = $('#environment_yxd').val();
            let plandate = $('#create_time').val();
            let type = $('#auto_query_type').val();
            let lineid = $('#line_id').val();
            $('#all_auto_query_result').val();
            if (type === '1') {
                if ($.trim(plandate)=== '') {
                    Alert.prototype.alertInfo("陛下生成时间不能为空");
                    return;
                }
            }
            else if (type === '2') {
                if ($.trim(plandate) === ''|| $.trim(lineid) === '') {
                    Alert.prototype.alertInfo("陛下生成时间或线路id不能为空");
                    return;
                }
            }

                param = {
                    'env': env,
                    'type': type,
                    'lineid': lineid,
                    'plandate': plandate
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/createAllAutoQuery',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#auto_query_result').val(res);
                        $('#auto_query_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });


        });
        $('#auto_query_type').change(function () {
            let type = $('#auto_query_type').val();
            if (type === '2') {
                $('#hide_name').show();
            } else {
                $('#hide_name').hide();
            }
        });
        //孙竹叶-司机所有运单卸货完成
        $('#ordersDoneSubmit').click(function () {
            let driver_mobile = $('#driver_mobile').val();
            let env = $('#environment1').val();

            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("陛下手机号不能为空");
                return;
            } else {
                param = {
                    'env': env,
                    'driver_mobile': driver_mobile,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/driverOrdersDone',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#orderesDoneShow').val(res);
                        $('#done_order_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        //孙竹叶-运单产生时效轨迹扣款
        $('#order_less_money').click(function () {
            let order_sn = $('#order_sn').val();
            let env = $('#environment2').val();
            //获取扣款类型
            var pay_type = null;
            var obj = document.getElementsByName("pay_type");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    pay_type = obj[i].value;
                }
            }
            if ($.trim(order_sn) === '') {
                Alert.prototype.alertWarning("运单号不能为空");
                return;
            } else {
                param = {
                    'env': env,
                    'order_sn': order_sn,
                    'pay_type': pay_type,
                    'type':'时效轨迹扣款'
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/orderLessMoney',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#order_less_money_show').val(res);
                        $('#order_less_money_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        //孙竹叶-运单修改装卸货地址
        $('#order_update_address').click(function () {
            let order_sn = $('#order_sn_szy_2').val();
            let env = $('#environment_szy_2').val();
            //获取长短途
            var is_long = null;
            var obj = document.getElementsByName("is_long");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    is_long = obj[i].value;
                }
            }
            //获取经停点
            var has_stop = null;
            var obj = document.getElementsByName("has_stop");
            for (var j = 0; j < obj.length; j++) { //遍历Radio
                if (obj[j].checked) {
                    has_stop = obj[j].value;
                }
            }
            if ($.trim(order_sn) === '') {
                Alert.prototype.alertWarning("运单号不能为空");
                return;
            } else {
                param = {
                    'env': env,
                    'order_sn': order_sn,
                    'is_long': is_long,
                    'has_stop': has_stop,
                    'type':'修改装卸货地址'
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/orderUpdateAddress',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#order_update_address_show').val(res);
                        $('#order_update_address_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
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
        // 智能调度派车开关
        $('#scheduleSwitchSubmit').click(function () {
            // 获取环境
            const div = document.getElementById('order_guobaohui_1');
            const env = div.getElementsByTagName('select')[0].value;
            // 获取单选框
            var opt_type = null;
            var obj = document.getElementsByName("opt_type");
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    opt_type = obj[i].value;
                }
            }

            $('#schedule_switch_result').val();
            if ($.trim(env) === '' || $.trim(opt_type) === '') {
                Alert.prototype.alertWarning("环境和操作类型均不能为空！");
                return;
            } else {
                param = {
                    'env': env,
                    'opt_type': opt_type,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    // url: '/tools/getScheduleSwitchList',
                    url: '/tools/scheduleSwitch',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#schedule_switch_result').val(res);
                        $('#schedule_switch_table').bootstrapTable('refresh');
                    }
                });
            }

        });
        // 指定运单生成，控制 div 是否展示
        // 22-项目货订单，21-图灵订单，25-意向单，28-吸货订单，26-计划项目货订单
        $('#appoint_order_type').change(function () {
            let appoint_order_type = $('#appoint_order_type').val();
            if (appoint_order_type === '22') {
                $('#appoint_order_offline_pay_div').hide();
                $('#auto_query_create_time_div').hide();
            } else if (appoint_order_type === '21') {
                $('#appoint_order_offline_pay_div').show();
                $('#auto_query_create_time_div').hide();
            } else if (appoint_order_type === '25') {
                $('#appoint_order_offline_pay_div').hide();
                $('#auto_query_create_time_div').show();
            } else {
                $('#appoint_order_offline_pay_div').hide();
                $('#auto_query_create_time_div').hide();
            }
        });
        // 指定运单生成
        $('#appointOrderSubmit').click(function () {
            let env = $('#appoint_order_env').val();
            let appoint_order_type = $('#appoint_order_type').val();
            let appoint_order_status = $('#appoint_order_status').val();
            let appoint_transfer_type = $('#appoint_transfer_type').val();
            let auto_query_create_time = $('#auto_query_create_time').val();
            // 获取单选框
            var appoint_order_offline_pay = null;
            var obj = document.getElementsByName("appoint_order_offline_pay");  //
            for (var i = 0; i < obj.length; i++) { //遍历Radio
                if (obj[i].checked) {
                    appoint_order_offline_pay = obj[i].value;
                }
            }
            $('#appoint_order_result').val();
            if ($.trim(env) === '' || $.trim(appoint_order_type) === '' ||
                $.trim(appoint_transfer_type) === '' || $.trim(appoint_order_status) === '') {
                Alert.prototype.alertWarning("环境、运单类型、运力类型和运单状态均不能为空！");
                // return;
            } else if (($.trim(appoint_order_type) === '25') && ($.trim(auto_query_create_time) === '')) {
                Alert.prototype.alertWarning("意向单生成时间不能为空！");
            } else if (($.trim(appoint_order_type) === '21') && ($.trim(appoint_transfer_type) === '3')) {
                Alert.prototype.alertWarning("图灵订单暂不支持固定司机！");
            } else if (($.trim(appoint_order_type) === '21') && ($.trim(appoint_transfer_type) === '5')) {
                Alert.prototype.alertWarning("图灵订单暂不支持企业运力！");
            } else if (($.trim(appoint_order_type) === '22') && ($.trim(appoint_order_status) === '1')) {
                Alert.prototype.alertWarning("项目货订单自动审核！");
            } else if (($.trim(appoint_order_type) === '22') && ($.trim(appoint_order_status) === '2')) {
                Alert.prototype.alertWarning("项目货订单自动报价！");
            } else if ($.trim(appoint_order_type) === '26') {
                Alert.prototype.alertWarning("计划项目货订单暂不支持，请谅解！");
            } else {
                param = {
                    'env': env,
                    'appoint_order_type': appoint_order_type,
                    'appoint_order_status': appoint_order_status,
                    'appoint_transfer_type': appoint_transfer_type,
                    'appoint_order_offline_pay': appoint_order_offline_pay,
                    'auto_query_create_time': auto_query_create_time,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/appointOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#appoint_order_result').val(res);
                        $('#appoint_order_table').bootstrapTable('refresh');
                    }
                });
            }
        });
        // 操作指定运单 operate_appoint_order
        $('#operateAppointOrderSubmit').click(function () {
            let env = $('#operate_appoint_order_env').val();
            let operate_appoint_order_sn = $('#operate_appoint_order_sn').val();
            let operate_appoint_order_status = $('#operate_appoint_order_status').val();

            $('#operate_appoint_order_result').val();
            if ($.trim(env) === '' || $.trim(operate_appoint_order_sn) === '' || $.trim(operate_appoint_order_status) === '') {
                Alert.prototype.alertWarning("环境、运单号、和操作类型均不能为空！");
                // return;
            } else {
                param = {
                    'env': env,
                    'operate_appoint_order_sn': operate_appoint_order_sn,
                    'operate_appoint_order_status': operate_appoint_order_status,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/operateAppointOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#operate_appoint_order_result').val(res);
                        $('#operate_appoint_order_table').bootstrapTable('refresh');
                    }
                });
            }
        });

    },

    table: function () {
        $('#debang_order_list_table').bootstrapTable({
            url: '/tools/getOrderDebangList',
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
                    field: 'thirdsn',
                    title: '德邦单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },
                {
                    field: 'result',
                    title: '操作结果'
                },

                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]
        });
        $('#jd_order_list_table').bootstrapTable({
            url: '/tools/getOrderJdList',
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
                    field: 'thirdsn',
                    title: '京东单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },

                {
                    field: 'result',
                    title: '结果信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#ky_order_list_table').bootstrapTable({
            url: '/tools/getOrderKyList',
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
                    field: 'thirdsn',
                    title: '跨越单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },

                {
                    field: 'result',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]
        });
        $('#sf_order_list_table').bootstrapTable({
            url: '/tools/getOrderSfList',
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
                    field: 'thirdsn',
                    title: '顺丰单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },

                {
                    field: 'result',
                    title: '操作信息'
                },

                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]
        });
        $('#yt_order_list_table').bootstrapTable({
            url: '/tools/getOrderYtList',
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
                    field: 'thirdsn',
                    title: '圆通单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },

                {
                    field: 'result',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#hydd_order_list_table').bootstrapTable({
            url: '/tools/getOrderHyddList',
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
                    field: 'thirdsn',
                    title: '华宇嘟嘟单号'
                },
                {
                    field: 'env',
                    title: '环境'
                },

                {
                    field: 'result',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
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
        // 智能调度派车开关
        $('#schedule_switch_table').bootstrapTable({
            url: '/tools/getScheduleSwitchList',
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
            pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',

            columns: [

                {
                    field: 'operator',
                    title: '操作人'
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
        // 指定运单生成
        $('#appoint_order_table').bootstrapTable({
            url: '/tools/getAppointOrderList',
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
                    field: 'result',
                    title: '结果信息'
                },
                {
                    field: 'appoint_order_type',
                    title: '运单类型'
                },
                {
                    field: 'appoint_order_status',
                    title: '指定运单状态'
                },
                {
                    field: 'appoint_transfer_type',
                    title: '指定运力类型'
                },
                {
                    field: 'appoint_order_offline_pay',
                    title: '是否线下支付'
                },
                {
                    field: 'auto_query_create_time',
                    title: '意向单生成时间'
                },
                {
                    field: 'opt_time',
                    title: '操作时间'
                }
            ]
        });
        // 操作指定运单
        $('#operate_appoint_order_table').bootstrapTable({
            url: '/tools/getOperateAppointOrderList',
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
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'operate_appoint_order_status',
                    title: '指定运单状态'
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
        //孙竹叶-表格-司机所有运单卸货完成
        $('#done_order_list_table').bootstrapTable({

            url: '/tools/getDriverOrdersDoneList',
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
                    field: 'name',
                    title: '操作人',
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'driver_phone',
                    title: '司机手机号'
                },
                {
                    field: 'order_num',
                    title: '司机运单数'
                },
                {
                    field: 'commit',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        //孙竹叶-表格-运单产生时效轨迹扣款
        $('#order_less_money_list_table').bootstrapTable({

            url: '/tools/getOrderLessMoneyList',
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
                    field: 'name',
                    title: '操作人',
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'commit',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        //孙竹叶-表格-运单修改装卸货地址
        $('#order_update_address_list_table').bootstrapTable({

            url: '/tools/getOrderUpdateAddress',
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
                    field: 'name',
                    title: '操作人',
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'commit',
                    title: '操作信息'
                },
                {
                    field: 'create_time',
                    title: '操作时间'
                }
            ]

        });
        $('#order_abnormal_modify_list_table').bootstrapTable({
            url: '/tools/getOrderAbnormalModifyList',
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
                    field: 'orderSn',
                    title: '运单号'
                },
                {
                    field: 'env',
                    title: '注册环境'
                },
                {
                    field: 'order_status',
                    title: '运单状态'
                },
                {
                    field: 'modify_reason',
                    title: '修改原因'
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
        $('#auto_query_table').bootstrapTable({
            url: '/tools/getAutoQueryList',
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
                    title: '操作人',
                    // width: '50%',
                },
                {
                    field: 'env',
                    title: '注册环境'
                },
                {
                    field: 'lineid',
                    title: '线路id'
                },
                {
                    field: 'result',
                    title: '提交信息'
                },
                {
                    field: 'create_time',
                    title: '创建时间'
                }
            ]

        });
    },


};
