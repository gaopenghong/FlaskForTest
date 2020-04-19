/**
 * Created by liuchunfu on 2019/8/17.
 */
var curRow = {};
$(document).ready(function () {
    let config = new Config();
    config.table();

});
let Config = function () {
};

Config.prototype = {

    table: function () {
        $('#config_list_table').bootstrapTable({

            url: '/algorithm/configList',
            method: 'get',
            search: false,
            showColumns: true,
            checkboxHeader: true,
            sortStable: true,
            striped: true,
            pagination: true,
            onlyInfoPagination: false,
            sortOrder: 'esc',
            showRefresh: true,
            pageSize: 20,
            toolbar: '#tableToolbar',
            checkbox:true,
            singleSelect:true,
            queryParams: function (param) {
                return {};
            },

            columns: [
                {
                    field: 'id',
                    title: 'ID',
                    formatter: function (value, row, index) {
                    return "<div id='indicator' >" + value + "</div>";
                }
                },
                {
                    field: 'type',
                    title: '算法类型',
                    formatter: function (value) {
                        switch (value) {
                            case 1:
                                return '智能客服';
                            case 2:
                                return '智能报价';
                            case 3:
                                return '智能调度';
                            case 4:
                                return '货量预算';
                        }
                    }
                },
                {
                    field: 'key',
                    title: '指标',
                    formatter: function (value) {
                        switch (value) {
                            case '1':
                                return '覆盖率';
                            case '2':
                                return '正确率';
                            case '3':
                                return '精确率';
                            case '4':
                                return '召回率';
                            case '5':
                                return '综合指标';
                        }
                    }
                },
                {
                    field: 'value',
                    title: '值',
                    formatter: function (value, row, index) {
                    return "<a href=\"#\" name=\"value\" data-type=\"text\" data-pk=\""+row.id+"\" data-title=\"值\">" + value + "</a>";
                }
                },
            ],
            onClickRow: function (row, $element) {
                curRow = row;
            },
            onLoadSuccess: function (aa, bb, cc) {
                $("#config_list_table a").editable({

                    url: function (params) {
                        var sName = $(this).attr("name");
                        curRow[sName] = params.value;
                        console.log(curRow);
                        $.ajax({
                            type: 'POST',
                            url: "/ConfigList/Edit",
                            // data: JSON.stringify(curRow),
                            data: curRow,
                            dataType: 'json',
                            success: function (data, textStatus, jqXHR) {
                                alert('保存成功！');
                            },
                            error: function () { alert("error");}
                        });
                    },
                    type: 'text'
                });
            },
        });
    },

};