/**
 * Created by liuchunfu on 2019/11/4.
 */

$(document).ready(function () {
    let oms = new Oms();
    oms.init();
    oms.table();
    oms.init1();
    oms.table1();
});
let Oms = function () {
};
Oms.prototype = {
    init : function () {
         $('#OmsAdvertPosition').click(function () {
             let env = $('#environment_1').val();
             let app_type = $('#app_type').val();
             let type_id = $('#type_id').val();
             let title = $('#title').val();
             let link_url = $('#link_url').val();
             let pic_url = $('#pic_url').val();
             let rank = $('#rank').val();
             let rank_re = /^[1-9]\d?$/;
             if ($.trim(app_type)  === '' || $.trim(type_id) ===  ''
                 || $.trim(title) === '' || $.trim(link_url) === ''
                 || $.trim(pic_url) === '' || $.trim(rank) === '')
                {Alert.prototype.alertWarning("请将信息填写完整再提交");
                return;}
             else if (!rank_re.exec($.trim(rank)))
                {Alert.prototype.alertWarning("请输入排序1～99");
                return;}
             else
                 {
                 param = {
                     'env' : env,
                     'app_type' : app_type,
                     'type_id' : type_id,
                     'title' : title,
                     'link_url' : link_url,
                     'pic_url' : pic_url,
                     'rank' : rank
                 };
                 Alert.prototype.alertLoading(30000)
                 $.ajax({
                    type: 'post',
                    url: '/tools/createOmsPosition',
                    data: param,
                    success: function (res) {
                        $('#ome_advert_position_table').bootstrapTable('refresh');
                        $('#selectOmsAdvertPositionResult').val(res);
                    },
                 });
             }



         })
         $('#OmsIosConfig').click(function () {
             let env = $('#environment_2').val();
             let customer_type = $('#customer_type').val();
             let dev_version = $('#devVersion').val();
             let remark = $('#remark').val();
             let host = $('#host').val();
             console.log(env);
             // let admin_name = $('#admin_name').val();
             // if ($.trim(customer_type)  === '' || $.trim(dev_version) ===  ''
             //     || $.trim(remark) === '' || $.trim(admin_name) === ''
             //    )
             //    {Alert.prototype.alertWarning("请将信息填写完整再提交");
             //    return;}
             // else
             {
             param = {
                 'env' : env,
                 'customer_type' : customer_type,
                 'dev_version' : dev_version,
                 'remark' : remark,
                 'host': host
                 // 'admin_name' : admin_name
             };
             Alert.prototype.alertLoading(30000)
             $.ajax({
                type: 'post',
                url: '/tools/createIosConfig22',
                data: param,
                success: function (res) {
                    $('#oms_ios_config_table').bootstrapTable('refresh');
                    $('#selectOmsIosConfigResult').val(res);
                },
             });
         }



         })

    },
    table: function () {
            $('#ome_advert_position_table').bootstrapTable({

                url: '/tools/selectOmsPositionTable',
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
                        field: 'app_type',
                        title: '终端类型'
                    },
                    {
                        field: 'type_id',
                        title: '广告类型'
                    },
                    {
                        field: 'title',
                        title: '标题'
                    },
                    {
                        field: 'link_url',
                        title: '链接地址'
                    },
                    {
                        field: 'pic_url',
                        title: '活动图片url'
                    },
                    {
                        field: 'rank',
                        title: 'banner排名'
                    }
                ]

            });
        },
    init1 : function () {

    },
    table1: function () {
            $('#oms_ios_config_table').bootstrapTable({

                url: '/tools/selectIosConfigTable',
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
                        title: '提测环境'
                    },
                    {
                        field: 'customer_type',
                        title: '客户端类型'
                    },
                    {
                        field: 'dev_version',
                        title: '开发版本号'
                    },
                    {
                        field: 'remark',
                        title: '备注'
                    },

                ]

            });
        },
};
