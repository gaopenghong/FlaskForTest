/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let customer = new Customer();
    customer.init();
    customer.table();
});
let Customer = function () {
};
Customer.prototype = {
    init: function () {
        // 吸货下单提交
        $('#customerConfirmSubmit').click(function () {
            let env = $('#environment1').val();
            let order_status = $('#order_status').val();
            let mobile = $('#customer_mobile1').val();
            let order_num = $('#order_num').val();
            let car_length = $('#car_length').val();
            let load_time = $('#load_time').val();
            let start_address = $('#start_address').val();
            let end_address = $('#end_address').val();
            let receipt_need = $('#receipt_need').val();
            let stop_need = $('#stop_need').val();
            let dispatch_ai = $('#dispatch_ai ').val();
            let comment = $('#comment ').val();
            let price = $('#order_price').val();
            let re_price = /^\d.([1-9]{1,2}|[0-9][1-9])$|^[1-9]\d?(.\d{1,2})?$|^100(.0{1,2})?$/;
            let re_mobile = /^1\d{10}$/;
            let re_number = /^[1-9]\d?$/;
            document.getElementById('customer_confirm_result').value="";
            $('#customer_confirm_result').val();
            if ($.trim(mobile) === '' || $.trim(order_num) === '') {
                Alert.prototype.alertWarning("陛下手机号或下单数量不能为空");
                return;
            }
            else if (!re_mobile.exec($.trim(mobile))) {
                Alert.prototype.alertWarning("请输入正确的手机号");
                return;
            }
            else if (!re_number.exec($.trim(order_num))) {
                Alert.prototype.alertWarning("下单数量1~99");
                return;
            }
            else if (!re_price.exec($.trim(price)) && $.trim(price) !== '') {
                Alert.prototype.alertWarning("请输入金额0.01~1000");
                return;
            }
            else {
                param = {
                    'env': env,
                    'order_status': order_status,
                    'customer_mobile': mobile,
                    'order_num': order_num,
                    'car_length': car_length,
                    'load_time': load_time,
                    'start_address': start_address,
                    'end_address': end_address,
                    'receipt_need': receipt_need,
                    'stop_need': stop_need,
                    'dispatch_ai': dispatch_ai,
                    'modify_price': price,
                    'comment': comment
                };
                Alert.prototype.alertLoading();
                document.getElementById('customer_confirm_result').value="稍等片刻，结果正在路上。。。";
                $.ajax({
                    type: 'post',
                    url: '/tools/customerNewConfirm',
                    data: param,
                    success: function (res) {
                        $('#customer_confirm_result').val(res);
                        $('#customer_confirm_list_table').bootstrapTable('refresh');
                    },
                });
            }
        });
         // 线路ID下单提交
        $('#quoteByLineIdSubmit').click(function () {
            let env = $('#environment2').val();
            let order_status = $('#order_status2').val();
            let line_id = $('#line_id').val();
            let order_num = $('#order_num2').val();
            // let load_time = $('#load_time').val();
            // let receipt_need = $('#receipt_need').val();
            // let dispatch_ai = $('#dispatch_ai ').val();
            // let comment = $('#comment ').val();
            let re_number = /^[1-9]\d?$/;
            document.getElementById('quote_line_id_result').value="";
            $('#quote_line_id_result').val();
            if ($.trim(line_id) === '' || $.trim(order_num) === '') {
                Alert.prototype.alertWarning("陛下线路id或下单数量不能为空");
                return;
            }
            else if (!re_number.exec($.trim(order_num))) {
                Alert.prototype.alertWarning("下单数量1~99");
                return;
            }
            else {
                param = {
                    'env': env,
                    'order_status': order_status,
                    'line_id': line_id,
                    'order_num': order_num,
                    // 'load_time': load_time,
                    // 'receipt_need': receipt_need,
                    // 'dispatch_ai': dispatch_ai,
                    // 'comment': comment
                };
                Alert.prototype.alertLoading();
                document.getElementById('quote_line_id_result').value="稍等片刻，结果正在路上。。。";
                $.ajax({
                    type: 'post',
                    url: '/tools/customerConfirmByLineId',
                    data: param,
                    success: function (res) {
                        $('#quote_line_id_result').val(res);
                        $('#quote_line_id_table').bootstrapTable('refresh');
                    },
                });
            }
        });
         // 运单上传司机定位提交
        $('#orderPositionSubmit').click(function () {
            let env = $('#environment3').val();
            let action_type = $('#action_type3').val();
            let order_sn = $('#order_sn3').val();
            let lng_lat = $('#lng_lat3').val();
            let lag_lat_strs =  new Array(10);
            lag_lat_strs = $.trim(lng_lat).split(",");
            let re_lng = /^(\-|\+)?(((\d|[1-9]\d|1[0-7]\d|0{1,3})\.\d{0,6})|(\d|[1-9]\d|1[0-7]\d|0{1,3})|180\.0{0,6}|180)$/;
            let re_lat = /^(\-|\+)?([0-8]?\d?\.\d{0,6}|90\.0{0,6}|[0-8]?\d?|90)$/;
            let lng = parseFloat(lag_lat_strs[0]);
            let lat = parseFloat(lag_lat_strs[1]);
            document.getElementById('order_position_heartbeat_result').value="";
            $('#order_position_heartbeat_result').val();
            if ($.trim(order_sn) === '' || $.trim(lng_lat) === '') {
                Alert.prototype.alertWarning("陛下运单号或经纬度不能为空");
                return;
            }
            else if (!re_lng.exec(lng) || !re_lat.exec(lat)) {
                Alert.prototype.alertWarning("请输入正确的经纬度");
                return;
            }
            else {
                param = {
                    'env': env,
                    'order_sn': order_sn,
                    'lng': lng,
                    'lat': lat,
                    'action_type': action_type
                };
                Alert.prototype.alertLoading();
                document.getElementById('quote_line_id_result').value="稍等片刻，结果正在路上。。。";
                $.ajax({
                    type: 'post',
                    url: '/tools/orderDriverPositionHeartbeat',
                    data: param,
                    success: function (res) {
                        $('#order_position_heartbeat_result').val(res);
                        $('#order_position_heartbeat_table').bootstrapTable('refresh');
                    },
                });
            }
        });
        // 运单压车费用提交
        $('#orderTimeOutSubmit').click(function () {
            let env = $('#environment4').val();
            let order_sn = $('#order_sn4').val();
            let time_out = $('#time_out4').val();
            document.getElementById('order_time_out_result').value="";
            $('#order_time_out_result').val();
            if ($.trim(order_sn) === '' || $.trim(time_out) === '') {
                Alert.prototype.alertWarning("陛下运单号或压车时长不能为空");
                return;
            }
            else {
                param = {
                    'env': env,
                    'order_sn': order_sn,
                    'time_out': time_out,
                };
                Alert.prototype.alertLoading();
                document.getElementById('order_time_out_result').value="稍等片刻，结果正在路上。。。";
                $.ajax({
                    type: 'post',
                    url: '/tools/orderTimeOut',
                    data: param,
                    success: function (res) {
                        $('#order_time_out_result').val(res);
                        $('#order_time_out_table').bootstrapTable('refresh');
                    },
                });
            }
        });
        // 发放优惠卷
        $('#giveCouponSubmit').click(function () {
            let env = $('#environment6').val();
            let mobile = $('#mobile6').val();
            let number = $('#number6').val();
            document.getElementById('order_time_out_result').value="";
            $('#order_time_out_result').val();
            if ($.trim(mobile) === ''|| $.trim(number) === '' ) {
                Alert.prototype.alertWarning("陛下手机号或发放优惠卷数量不能为空");
                return;
            }
            else {
                param = {
                    'env': env,
                    'mobile': mobile,
                    'number': number
                };
                Alert.prototype.alertLoading();
                document.getElementById('give_coupon_result').value="稍等片刻，结果正在路上。。。";
                $.ajax({
                    type: 'post',
                    url: '/tools/GrantCoupon',
                    data: param,
                    success: function (res) {
                        $('#give_coupon_result').val(res);
                        $('#give_coupon_table').bootstrapTable('refresh');
                    },
                });
            }
        });
    },

    table: function () {
        // 吸货下单记录
        $('#customer_confirm_list_table').bootstrapTable({
            url: '/tools/getCustomeNewConfirmList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            onlyInfoPagination: false,
            pagination: true,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'customer_mobile',
                    title: '货主手机号'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'order_info',
                    title: '下单信息'
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
         // 项目货线路id下单记录
        $('#quote_line_id_table').bootstrapTable({
            url: '/tools/customerConfirmByLineIdList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            onlyInfoPagination: false,
            pagination: true,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'line_id',
                    title: '线路ID'
                },
                {
                    field: 'env',
                    title: '操作环境'
                },
                {
                    field: 'order_num',
                    title: '下单数量'
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
        // 运单上传司机定位心跳下单记录
        $('#order_position_heartbeat_table').bootstrapTable({
            url: '/tools/orderDriverPositionHeartbeatList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            onlyInfoPagination: false,
            pagination: true,
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
                    field: 'lng_lat',
                    title: '经纬度'
                },
                {
                    field: 'action_type',
                    title: '上传类型'
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
        // 产生压车费记录
        $('#order_time_out_table').bootstrapTable({
            url: '/tools/orderTimeOutList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            onlyInfoPagination: false,
            pagination: true,
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
                    field: 'time_out',
                    title: '压车时长'
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
        // 发放优惠卷记录
        $('#give_coupon_table').bootstrapTable({
            url: '/tools/GrantCouponList',
            method: 'get',
            search: true,
            sortStable: true,
            striped: true,
            onlyInfoPagination: false,
            pagination: true,
            sortOrder: 'desc',
            showRefresh: true,
            toolbar: '#tableToolbar',
            columns: [

                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'mobile',
                    title: '手机号'
                },
                {
                    field: 'number',
                    title: '数量'
                },
                {
                    field: 'env',
                    title: '操作环境'
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
    },


};