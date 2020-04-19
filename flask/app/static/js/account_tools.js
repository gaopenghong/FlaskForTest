/**
 * Created by liuchunfu on 2019/8/17.
 */


$(document).ready(function () {
    let account = new Account();
    account.init();
    account.table();
});
let Account = function () {
};
Account.prototype = {
    init: function () {
        $('#addAccountSubmit').click(function () {
            let name = $('#name').val();
            let mobile = $('#mobile').val();
            $('#add_admin_result').val();
            let env = $('#environment').val();
            let type = $('#type').val();
            let is_change = $('input:radio[name="is_change"]:checked').val();

            if (type === '1') {
                console.log(123);
                if ($.trim(name) === '' || $.trim(mobile) === '') {
                    Alert.prototype.alertWarning("陛下手机号或者姓名不能为空");
                    return;
                }
            }
            if ($.trim(mobile) !== '' && $.trim(mobile).length !== 11) {
                Alert.prototype.alertWarning("陛下手机号长度要11位");
                return;
            } else {
                param = {
                    'name': name,
                    'mobile': mobile,
                    'type': type,
                    'environment': env,
                    'is_change': is_change
                };

                $.ajax({
                    type: 'post',
                    url: '/tools/createAccount',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#account_list_table').bootstrapTable('refresh');
                        $('#add_account_result').val(res);
                    },
                });
            }

        });
        $('#radio_name').hide();
        $('#type').change(function () {
            let type = $('#type').val();
            if (type === '1') {
                $('#div_name').show();
                $('#radio_name').hide()
            } else if (type === '3') {
                $('#div_name').hide();
                $('#radio_name').show()
            } else {
                $('#div_name').hide();
                $('#radio_name').hide()
            }
        });
        $('#addAdminSubmit').click(function () {
            let name = $('#name').val();
            let mobile = $('#mobile').val();
            $('#add_admin_result').val();
            if ($.trim(mobile) !== '' && $.trim(mobile).length !== 11) {
                Alert.prototype.alertWarning("陛下手机号长度要11位");
                return;
            }
            if ($.trim(name) === '' || $.trim(mobile) === '') {
                Alert.prototype.alertWarning("陛下手机号或者姓名不能为空");
                return;
            } else {
                param = {
                    'name': name,
                    'mobile': mobile,
                    'type': 1
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/createAccount',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#admin_list_table').bootstrapTable('refresh');
                        $('#add_admin_result').val(res);
                    },
                });
            }

        });
        $('#TruckDriverSubmit').click(function () {
            let driver_mobile = $('#truck_driver_mobile').val();
            let environment = $('#environment2').val();
            if ($.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("陛下手机号不能为空");
                return;
            } else {
                param = {
                    'driver_mobile': driver_mobile,
                    'environment': environment
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/AddTruckDriver',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#TruckDriverShow').val(res);
                        $('#truck_driver_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    },
                });
            }

        });
    },

    table: function () {
        $('#account_list_table').bootstrapTable({

            url: '/tools/getAccountList',
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
                    field: 'add_phone',
                    title: '注册电话'
                },
                {
                    field: 'commit',
                    title: '注册信息'
                },
                {
                    field: 'type',
                    title: '注册类型',
                    formatter: function (value, row, index) {
                        // console.log(value);
                        switch (value) {
                            case 1:
                                return '后台';
                            case 2:
                                return '好运';
                            case 3:
                                return '车队';
                            case 4:
                                return '共建车';
                        }
                    }
                },
                {
                    field: 'add_time',
                    title: '注册时间'
                }
            ]

        });
    },


};
