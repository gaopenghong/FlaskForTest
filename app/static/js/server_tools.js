/**
 * Created by liuchunfu on 2019/11/4.
 */


$(document).ready(function () {
    let server = new Server();
    server.init();
    server.table();
});
let Server = function () {
};
Server.prototype = {
    init: function () {
        $('#taskNottoAllocateCheckSubmit').click(function () {
            let user_mobile = $('#user_mobile').val();
            let task_id = $('#task_id').val();
            let env = $('#env').val();

            if ($.trim(user_mobile) === '') {
                Alert.prototype.alertWarning("陛下后台账号不能为空");
                return;
            } else if ($.trim(task_id) === '') {
                Alert.prototype.alertWarning("陛下任务编号都不能为空");
                return;
            } else {
                param = {
                    'user_mobile': user_mobile,
                    'task_id': task_id,
                    'env': env,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/taskcheck',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#task_check_result').val(res);
                        $('#service_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        $('#taskOrWrkordAllDealSubmit').click(function () {
            let user_mobile2 = $('#user_mobile2').val();
            let deal_type = $('#deal_type').val();
            let method_type = $('#method_type').val();
            let env2 = $('#env2').val();

            if ($.trim(user_mobile2) === '') {
                Alert.prototype.alertWarning("陛下后台账号不能为空");
                return;
            } else {
                param = {
                    'user_mobile2': user_mobile2,
                    'deal_type': deal_type,
                    'method_type': method_type,
                    'env2': env2,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/taskOrWrkordAllDeal',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#taskorwrkordalldeal_result').val(res);
                        $('#service_list2_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        $('#taskCreateDataSubmit').click(function () {
            let order_sn = $('#order_sn').val();
            let task_type_id = $('#task_type_id').val();
            let env3 = $('#env3').val();

            if ($.trim(order_sn) === '') {
                Alert.prototype.alertWarning("陛下后台账号不能为空");
                return;
            } else {
                param = {
                    'order_sn': order_sn,
                    'task_type_id': task_type_id,
                    'env3': env3,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/taskCreateData',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#taskcreatedata_result').val(res);
                        $('#service_list3_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)
                    }
                });
            }
        });
        $('#task_im_Submit').click(function () {
                    let word_name = $('#word_name').val();
                    let num = $('#num').val();
                    let task_im_type_id = $('#task_im_type_id').val();
                    let env4 = $('#env4').val();
                   if ($.trim(word_name) === '') {
                        Alert.prototype.alertWarning("陛下名称参数不能为空");
                        return;
                    } else {
                        param = {
                            'word_name': word_name,
                            'num': num,
                            'task_im_type_id': task_im_type_id,
                            'env4': env4,
                        };
                        Alert.prototype.alertLoading();
                        $.ajax({
                            type: 'post',
                            url: '/tools/taskImCreateData',
                            // dataType: 'json',
                            data: param,
                            success: function (res) {
                                $('#task_im_result').val(res);
                                $('#service_list4_table').bootstrapTable('refresh');
                                Alert.prototype.alertInfo(res)
                            }
                        });
                    }
         });
         $('#task_im_tag_Submit').click(function () {
                          let tag_name = $('#tag_name').val();
                          let num = $('#num1').val();
                          let task_im_role = $('#task_im_role').val();
                          let env5 = $('#env5').val();

                          if ($.trim(tag_name) === '') {
                              Alert.prototype.alertWarning("陛下标签名不能为空");
                              return;
                          } else {
                              param = {
                                 'tag_name': tag_name,
                                 'num': num,
                                 'task_im_role': task_im_role,
                                 'env5': env5,
                              };
                                   Alert.prototype.alertLoading();
                              $.ajax({
                                   type: 'post',
                                   url: '/tools/taskImCreateTagData',
                                  // dataType: 'json',
                                  data: param,
                                  success: function (res) {
                                   $('#task_im_tag_result').val(res);
                                    $('#service_list5_table').bootstrapTable('refresh');
                                    Alert.prototype.alertInfo(res)
                                 }
                             });
                        }
          });
         $('#task_im_qr_submit').click(function () {
                          let tag_name = $('#qr_name').val();
                          let num = $('#num2').val();
                          let task_im_role = $('#task_im_role_1').val();
                          let env6 = $('#env6').val();

                          if ($.trim(tag_name) === '') {
                              Alert.prototype.alertWarning("陛下快捷回复名不能为空");
                              return;
                          } else {
                              param = {
                                  'tag_name': tag_name,
                                  'num': num,
                                  'task_im_role': task_im_role,
                                  'env6': env6,
                              };
                                    Alert.prototype.alertLoading();
                              $.ajax({
                                    type: 'post',
                                    url: '/tools/taskImCreateQrData',
                                           // dataType: 'json',
                                    data: param,
                                    success: function (res) {
                                             $('#task_im_qr_result').val(res);
                                             $('#service_list6_table').bootstrapTable('refresh');
                                             Alert.prototype.alertInfo(res)
                                    }
                              });
                          }
        });
        $('#taskSubmit').click(function () {
            let taskId = $('#taskId').val();
            let orderId = $('#orderId').val();
            let env = $('#environment').val();
            let status = $('#checkStatus').val();
            if ($.trim(taskId) === '' || $.trim(orderId) === '') {
                Alert.prototype.alertWarning("陛下运单编号和运单编号不能为空");
                return;
            } else {
                param = {
                    'taskId': taskId,
                    'orderId': orderId,
                    'env': env,
                    'status': status,
                };
                Alert.prototype.alertLoading();

                $.ajax({
                    type: 'post',
                    url: '/tools/task',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {

                        $('#add_admin_result').val(res);
                    },
                });
            }

        });
    },

    table: function () {
        $('#service_list_table').bootstrapTable({
            url: '/tools/getServiceTaskCheckist',
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
                    field: 'user_mobile',
                    title: '后台账号'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '返回信息'
                },
                {
                    field: 'create_time',
                    title: '执行时间'
                },
                {
                    field: 'operate_name',
                    title: '工具名称'
                }
            ]
        });

        $('#service_list2_table').bootstrapTable({
            url: '/tools/getServiceTaskorWrkordDealList',
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
                    field: 'user_mobile',
                    title: '后台账号'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '返回信息'
                },
                {
                    field: 'create_time',
                    title: '执行时间'
                },
                {
                    field: 'operate_name',
                    title: '工具名称'
                }
            ]
        });

        $('#service_list3_table').bootstrapTable({
            url: '/tools/getServiceTaskCreateDtaList',
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
                    field: 'order_sn',
                    title: '运单号'
                },
                {
                    field: 'task_type_id',
                    title: '任务id'
                },
                {
                    field: 'create_time',
                    title: '执行时间'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '返回信息'
                }
            ]
        });
        $('#service_list4_table').bootstrapTable({
                    url: '/tools/getImServiceCreateWordList',
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
                            field: 'word_name',
                            title: '名称'
                        },
                        {
                            field: 'task_im_type_id',
                            title: 'type'
                        },
                        {
                            field: 'create_time',
                            title: '执行时间'
                        },
                        {
                            field: 'env',
                            title: '执行环境'
                        },
                        {
                            field: 'commit',
                            title: '返回信息'
                        }
                    ]
       });
       $('#service_list5_table').bootstrapTable({
                    url: '/tools/getImServiceCreateTagList',
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
                             field: 'tag_name',
                             title: '标签名称'
                         },
                         {
                             field: 'task_im_role',
                             title: '角色'
                         },
                         {
                             field: 'create_time',
                             title: '执行时间'
                         },
                         {
                             field: 'env',
                             title: '执行环境'
                         },
                         {
                             field: 'commit',
                             title: '返回信息'
                         }
                     ]
          });
          $('#service_list6_table').bootstrapTable({
                              url: '/tools/getImServiceCreateQrList',
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
                                       field: 'tag_name',
                                       title: '快捷回复名称'
                                   },
                                   {
                                       field: 'task_im_role',
                                       title: '角色'
                                   },
                                   {
                                       field: 'create_time',
                                       title: '执行时间'
                                   },
                                   {
                                       field: 'env',
                                       title: '执行环境'
                                   },
                                   {
                                       field: 'commit',
                                       title: '返回信息'
                                   }
                               ]
                    });
        $('#service_task_table').bootstrapTable({
            url: '/tools/getServiceTaskList',
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
                    field: 'user_mobile',
                    title: '后台账号'
                },
                {
                    field: 'env',
                    title: '执行环境'
                },
                {
                    field: 'commit',
                    title: '返回信息'
                },
                {
                    field: 'create_time',
                    title: '执行时间'
                }
            ]
        });

    },


};