/**
 * Created by liuchunfu on 2019/8/17.
 */

$(document).ready(function () {
    let fchatrecord = new Fchatrecord();
    fchatrecord.init();
    fchatrecord.table();
    fchatrecord.tableIndex();
    fchatrecord.tableDetail();
    fchatrecord.tableExactIndex();
});
let Fchatrecord = function () {
};
//获取当前url的参数.比如?id= 后面的参数
function getQueryString(variable)
{
var query = window.location.search.substring(1);
var vars = query.split("&");
for (var i=0;i<vars.length;i++) {
   var pair = vars[i].split("=");
   if(pair[0] == variable){return pair[1];}
}
return(false);
}
Fchatrecord.prototype = {
    init: function () {
        $('#run_fchat').click(function () {

            $.ajax({
                type: 'post',
                url: '/algorithm/runFchat',
                data: '',
                success: function (res) {
                    $('#record_list_table').bootstrapTable('refresh');
                },
            });
        });
    },

    table: function () {
        $('#record_list_table').bootstrapTable({

            url: '/algorithm/getRunHistory',
            method: 'get',
            // data: res,
            search: true,
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
                    title: '序号'
                },
                {
                    field: 'operator',
                    title: '操作人',
                },
                {
                    field: 'run_time',
                    title: '执行时间'
                },
                {
                    field: 'run_result',
                    title: '结果',
                    formatter: function (value) {
                        console.log(value);
                        switch (value) {
                            case 'true':
                                return '正确';
                            case 'false':
                                return '错误';
                        }
                    }
                },
                {
                    field: 'operate',
                    title: '操作',

                    formatter: function (value,row,index) {
                        // let v = $.map($("#record_list_table").bootstrapTable('getSelections'), function (row) {
                        //     return row.id
                        // });
                        return '<a id="indicator" href="/algorithm/getStaticIndex?id='+row.id+'" +title="index" target="_blank">指标</a>' +' '+
                        //return '<a href="/algorithm/getStaticIndex'+'" +title="index" target="_blank">指标</a>' +' '+
                            '<a href="/algorithm/getDetailIndex"title="detail" target="_blank">详情</a>'
                    }
                }
            ]

        });
    },

    tableIndex: function () {
        id = getQueryString('id')
        console.log(id)
        $('#static_list_table').bootstrapTable({
            url: '/algorithm/getStaticHistory?id=' +id+ '',
            method: 'get',
            // data: res,
            search: true,
            showColumns: true,
            // checkboxHeader: true,
            //queryParams: 'queryParams',
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
                    field: 'record_id',
                    title: '执行记录',
                },
                {
                    field: 'coverage',
                    title: '覆盖率',
                },
                {
                    field: 'accuracy',
                    title: '准确率'
                },
                {
                    field: 'precision',
                    title: '精确率'
                },
                {
                    field: 'recall',
                    title: '召回率'
                }
                ,
                {
                    field: 'f_measure',
                    title: '综合指标'
                }
            ]

        });
    },

        tableExactIndex: function () {
        id = getQueryString('id')
        console.log(id)
        $('#exactstatic_list_table').bootstrapTable({

            url: '/algorithm/getExactStatic?id=' +id+ '',
            method: 'get',
            // data: res,
            search: true,
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
                    field: 'record_id',
                    title: '执行记录',
                },
                {
                    field: 'intention_exact',
                    title: '预期意图',
                },
                {
                    field: 'coverage_exact',
                    title: '覆盖率',
                },
                {
                    field: 'accuracy_exact',
                    title: '准确率'
                },
                {
                    field: 'precision_exact',
                    title: '精确率'
                },
                {
                    field: 'recall_exact',
                    title: '召回率'
                }
                ,
                {
                    field: 'f_measure_exact',
                    title: '综合指标'
                }
            ]

        });
    },

    tableDetail: function () {
        $('#get_fchatdetail_list').bootstrapTable({

            url: '/algorithm/getFChatDetail',
            method: 'get',
            // data: res,
            search: true,
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
                    field: 'test_corpus',
                    title: '测试语料',
                },
                {
                    field: 'match_corpus',
                    title: '相似语料',
                },
                {
                    field: 'exact_intention',
                    title: '正确意图'
                },
                {
                    field: 'hit_intention',
                    title: '命中意图'
                },
                {
                    field: 'result',
                    title: '结果',
                    formatter: function (value) {
                        console.log(value);
                        switch (value) {
                            case 0:
                                return '正确';
                            case 1:
                                return '错误';
                            case 2:
                                return '未知';
                        }
                    }
                }
            ]

        });
    },


};
