/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let truck = new Truck();
    truck.init();
    truck.table();
});
let Truck = function () {
};
Truck.prototype = {
    init: function () {
        $('#TruckTrailerSubmit').click(function () {
            let env = $('#env').val();
            let plate_number = $('#plate_number').val();

            if ($.trim(plate_number) === '') {
                Alert.prototype.alertWarning("陛下车牌号不能为空");
                return;
            } else {
                param = {
                    'plate_number': plate_number,
                    'env': env
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/addTrailer',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#truck_trailer_result').val(res);
                        // $('#trailer_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)

                    }
                });
            }
        });
        $('#fyDriverAcceptSubmit').click(function () {
            let env = $('#environment_fy_driver').val();
            let order_sn = $('#order_sn').val();
            let driver_mobile = $('#driver_mobile').val();
            let order_status = $('#order_status').val()
            
            $('#fy_driver_accept_result').val();
            if ($.trim(driver_mobile) === ''|| $.trim(order_sn) === '') {
                Alert.prototype.alertWarning("手机号或订单号不能为空");
                return;
            } else {
                param = {
                    'env': env,
                    'order_sn': order_sn,
                    'driver_mobile': driver_mobile,
                    'order_status': order_status
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/fyDriverAccept',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#fy_driver_accept_table').bootstrapTable('refresh');
                        $('#fy_driver_accept_result').val(res);
                    }
                });
            }

        });
    },

    table: function () {
        $('#trailer_list_table').bootstrapTable({
            url: '/tools/getTrailerList',
            method: 'get',
            // data: res,
            search: true,
            showColumns: true,
            checkboxHeader: true,
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
                    field: 'plate_number',
                    title: '车牌号'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '操作信息'
                },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]
        });
        $('#fy_driver_accept_table').bootstrapTable({
            url: '/tools/getFyDriverList',
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
                    field: 'driver_mobile',
                    title: '司机手机号'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '操作信息'
                },
                {
                    field: 'add_time',
                    title: '操作时间'
                }
            ]
        });
    }

};