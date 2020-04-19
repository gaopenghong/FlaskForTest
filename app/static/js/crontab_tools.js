/**
 * Created by guobaohui on 2019/11/11.
 */


$(document).ready(function () {
    let order = new Order();
    order.init();
    order.table();
});
let Order = function () {
};
// 按钮初始化
function btnFormatter(value, row, index) {
    // alert(row.job_status);
    const myArray = [];
    if (row.job_status === "close") {
        myArray.push('<button id="run_btn" type="button" class="btn btn-default">执行</button>');
        myArray.push('<button id="del_btn" type="button" class="btn btn-default">删除</button>');
    } else if (row.job_status === "open") {
        myArray.push('<button id="run_btn" disabled="disabled" type="button" class="btn btn-default">执行中</button>');
        // myArray.push('<button id="del_btn" type="button" class="btn btn-default">删除</button>');
    } else if (row.job_status === "deleted") {
        myArray.push('<button id="del_btn" disabled="disabled" type="button" class="btn btn-default">删除</button>');
    }
    return myArray.join('');
    // return [
    //     '<button id="del_btn" type="button" class="btn btn-default">删除</button>',
    //     '<button id="run_btn" type="button" class="btn btn-default">执行</button>',
    // ].join('');
}
// 按钮事件
window.btnEvents = {
    "click #del_btn": function (e, value, row, index) {
        $(this).parent().parent().remove();
        // alert(row.id);
        $('#crontab_del_result').val();
        $.ajax({
            method:"get",
            url:'/tools/delCrontab',
            data:{
                "task_id": row.id,
            },
            // dataType : "jsonp",
            // async:true,
            success:function (res) {
                $('#crontab_del_result').val(res);
                $("#crontab_table").bootstrapTable('refresh');
            }
        });
    },
    // 执行按钮点击处理
    "click #run_btn": function (e, value, row, index) {
        // 执行按钮状态控制
        let table_rows = document.getElementById("crontab_table").rows;
        for (let i=1; i<table_rows.length; i++) {
            if (String(table_rows[i].cells[1].innerText) === String(row.id)) {
                if (String(table_rows[i].cells[10].innerText) === "close") {
                    // alert(table_rows[i].cells[10].innerText);
                    $(this).attr('disabled', 'true');
                }
            }
        }
        // 执行任务
        $('#crontab_run_result').val();
        $.ajax({
            method:"get",
            url:'/tools/runCrontab',
            data:{
                "task_id": row.id,
                "run_date": row.run_date,
                "run_time": row.run_time,
                "start_week": row.start_week,
                "end_week": row.end_week,
                "robot_key": row.robot_key,
                "run_name": row.run_name,
                "job_content": row.job_content,
                "run_type": row.run_type,
            },
            // dataType : "jsonp",
            // async:true,
            success:function (res) {
                $('#crontab_run_result').val(res);
                $("#crontab_table").bootstrapTable('refresh');
            }
        });

    },
};

Order.prototype = {
    init: function () {
        // 控制 div 是否展示
        $('#run_type').change(function () {
            let run_type = $('#run_type').val();
            if (run_type === 'timer') {
                $('#run_date_div').hide();
                $('#week_div').show();
            } else if (run_type === 'onece') {
                $('#run_date_div').show();
                $('#week_div').hide();
            } else if (run_type === 'cyclic') {
                $('#run_date_div').hide();
                $('#week_div').hide();
            }
        });
        // 初始操作按钮状态控制
        let table_rows = document.getElementById("crontab_table").rows;
        for (let i=1; i<table_rows.length; i++) {
            if (String(table_rows[i].cells[10].innerText) === "open") {
                // alert(table_rows[i].cells[10].innerText);
                $("#run_btn").val('disabled', 'true');
            }
        }
        // 定时任务
        $('#crontabSubmit').click(function () {
            let run_name = $('#run_name').val();
            let run_type = $('#run_type').val();
            let start_week = $('#start_week').val();
            let end_week = $('#end_week').val();
            let job_content = $('#job_content').val();
            let robot_key = $('#robot_key').val();
            // 获取任务日期
            let year = $('#year').val();
            let month = $('#month').val();
            let day = $('#day').val();
            // 获取任务时间
            let hour = $('#hour').val();
            let mint = $('#mint').val();
            let senc = $('#senc').val();

            if ($.trim(run_name) === '' || $.trim(run_type) === '' || $.trim(hour) === '' || $.trim(mint) === '' ||
                $.trim(senc) === '' || $.trim(job_content) === '' || $.trim(robot_key) === '') {
                Alert.prototype.alertWarning("* 标记项均不能为空！");
                return;
            } else if ($.trim(run_type) === 'onece') {
                if ($.trim(year) === '' || $.trim(month) === '' || $.trim(day) === '') {
                    Alert.prototype.alertWarning("任务日期不能为空！");
                    return;
                }
            } else if ($.trim(run_type) === 'timer') {
                if ($.trim(start_week) === '' || $.trim(end_week) === '') {
                    Alert.prototype.alertWarning("任务 Week 不能为空！");
                    return;
                } else if ($.trim(start_week) > $.trim(end_week)) {
                    Alert.prototype.alertWarning("结束 Week 不能早于开始 Week！");
                    return;
                }
            } else {
                param = {
                    'run_name': run_name,
                    'run_type': run_type,
                    'run_date_year': year,
                    'run_date_month': month,
                    'run_date_day': day,
                    'run_time_hour': hour,
                    'run_time_mint': mint,
                    'run_time_senc': senc,
                    'start_week': start_week,
                    'end_week': end_week,
                    'job_content': job_content,
                    'robot_key': robot_key
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'get',
                    url: '/tools/crontab',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#crontab_result').val(res);
                        $('#crontab_table').bootstrapTable('refresh');
                    }
                });
            }

        });
    },

    table: function () {
        // 定时任务
        $('#crontab_table').bootstrapTable({
            url: '/tools/getCrontabList',
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
                    field: 'id',
                    title: '任务ID'
                },
                {
                    field: 'run_name',
                    title: '任务名称'
                },
                {
                    field: 'run_type',
                    title: '任务类型'
                },
                {
                    field: 'run_date',
                    title: '任务日期'
                },
                {
                    field: 'run_time',
                    title: '任务时间'
                },
                {
                    field: 'start_week',
                    title: '开始 Week'
                },
                {
                    field: 'end_week',
                    title: '结束 Week'
                },
                {
                    field: 'job_content',
                    title: '消息内容'
                },
                // {
                //     field: 'robot_key',
                //     title: '群机器人 Key'
                // },
                {
                    field: 'opt_time',
                    title: '创建时间'
                },
                {
                    field: 'job_status',
                    title: '任务状态'
                },
                // {
                //     field: 'update_time',
                //     title: '更新时间'
                // },
                {
                    title: '操作',
                    field: 'opt',
                    events: btnEvents,  // 给按钮注册事件
                    formatter: btnFormatter,
                },
            ]
        });
    },

};
