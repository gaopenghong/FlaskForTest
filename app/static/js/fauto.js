/**
 * Created by liuchunfu on 2019/5/7.
 */

$(document).ready(function () {
    let auto = new Auto();
    auto.init();
    auto.table();
});
var Auto = function () {

};
Auto.prototype = {
    init: function () {
        // 获取环境和标签
        $('#run_iauto').click(function () {
            let env = $('#environment').val();
            let label = '' + $("#auto_label").val();
            if ($.trim(label) === "") {
                Alert.prototype.alertWarning("陛下！请选择标签");
                return;
            } else if (env === "") {
                Alert.prototype.alertWarning("陛下！请选择环境");
                return;
            } else {
                var params = {
                    "env": env,
                    "label": label
                };
                $.ajax({
                    type: 'post',
                    url: '/auto/runJob1',
                    data: params,
                    // dataType: 'json',
                    success: function (res) {
                        console.log(res);
                        Alert.prototype.alertSuccess('已执行，稍等就执行完毕');

                        // var id1 = setInterval(function () {
                        //     Alert.prototype.alertLoading(10000);
                        //     $.ajax({
                        //         type: 'get',
                        //         url: '/auto/getJobNum?uuid=' + res,
                        //         // data: params,
                        //         // dataType: 'json',
                        //         success: function (res) {
                        //             $('#auto_list_table').bootstrapTable('refresh');
                        //             if (res !== '0') {
                        //                 Alert.prototype.alertSuccess('已创建job，执行中');
                        //
                        //                 var id2 = setInterval(function () {
                        //                     $.ajax({
                        //                         type: 'get',
                        //                         url: '/auto/getJobStatus?num=' + res,
                        //                         data: params,
                        //                         success: function (res) {
                        //                             Alert.prototype.alertLoading(10000);
                        //                             if (res === 'success') {
                        //                                 Alert.prototype.alertSuccess('已执行完毕');
                        //                                 $('#auto_list_table').bootstrapTable('refresh');
                        //                                 clearInterval(id2);
                        //                             }
                        //                         }
                        //                     });
                        //
                        //                 }, 10000);
                        //                 clearInterval(id1)
                        //             }
                        //         }
                        //     })
                        // }, 10000);
                    }
                })
            }

        })
        $.ajax({
            type: 'get',
            url: '/auto/getLabel',
            dataType: 'json',
            success: function (res) {
                for (var i = 0; i < res.length; i++) {
                    try {
                        if (res[i].label_name === 'base'){
                            $('#auto_label').append("<option value=" + res[i].label_name + " selected>" + res[i].label_commit + "</option>");
                        }
                    }catch (e) {
                    }
                    $('#auto_label').append("<option value=" + res[i].label_name + ">" + res[i].label_commit + "</option>");
                }
                // 缺一不可
                $('#auto_label').selectpicker('refresh');
                $('#auto_label').selectpicker('render');
            },
        });

    },
    table: function () {
        $('#auto_list_table').bootstrapTable({

            url: '/auto/getRunHistory',
            method: 'get',
            // data: res,
            search: true, /**/
            showColumns: true,
            // checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'esc',
            showRefresh: true,
            pageSize: 10, //控制每页显示个数
            toolbar: '#tableToolbar',

            columns: [
                {
                    field: 'id',
                    title: '序号',
                },
                {
                    field: 'operator',
                    title: '执行者',
                }, {
                    field: 'run_time',
                    title: '执行时间',
                    // width: '50%',
                },
                {
                    field: 'environment',
                    title: '运行的环境'
                },
                {
                    field: 'job_num',
                    title: 'job序号'
                },
                {
                    field: 'run_label',
                    title: '运行的标签'
                },
                {
                    field: 'detail',
                    title: '执行结果'
                },
                {
                    field: 'result',
                    title: '执行结果状态',
                    formatter: function (value, row, index) {
                        if (value === 'None') {
                            return '<a href="' + value + '" class="view" title="查看" target="_blank"><img src="/static/img/loading2.gif" /></a>'
                        } else {
                            return value
                        }
                    }
                },
                {
                    field: 'console',
                    title: '控制台',
                    formatter: function (value, row, index) {
                        if (value !== null) {
                            return '<a href="' + value + '" class="view" title="查看" target="_blank"><img src="/static/img/console1.ico" /></a>'
                        } else {
                            return value
                        }
                    }
                },
                {
                    field: 'report',
                    title: '报告',
                    formatter: function (value, row, index) {
                        // console.log(row.result);
                        try {
                            let result = row.result;
                            if (result === 'SUCCESS' || result === 'FAILURE') {
                                return '<a href="' + value + '" class="view" title="查看" target="_blank"><img src="/static/img/see.ico" /></a>'
                            } else {
                                return '暂无报告'
                            }
                        } catch (e) {
                            return '暂无报告'
                        }


                    }
                }
            ]

        })
    }
};



