/**
 * Created by liuchunfu on 2019/8/17.
 */


$(document).ready(function () {
    let login = new Login();
    let tools = new Tools();
    tools.init();
    tools.table();
    tools.locationMenu()
    login.init();
    searchMenu();
});
let Login = function () {

};

Login.prototype = {
    init: function () {
        let c_start = document.cookie.indexOf("username=");
        if (c_start === -1) {
            $.ajax({
                type: 'get',
                url: '/cookie',
                dataType: 'json',
                success: function (res) {
                },
            });
        }
    }
};
let Tools = function () {
};
Tools.prototype = {
    init: function () {
        $('#wayBillSubmit').click(function () {
            let customer_mobile = $('#customer_mobile').val();
            let agent_mobile = $('#agent_mobile').val();
            let driver_mobile = $('#driver_mobile').val();
            if ($.trim(customer_mobile) === '' || $.trim(agent_mobile) === '' || $.trim(driver_mobile) === '') {
                Alert.prototype.alertWarning("陛下手机号不能为空");
                return;
            } else {
                param = {
                    'customer_mobile': customer_mobile,
                    'agent_mobile': agent_mobile,
                    'driver_mobile': driver_mobile
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/wayBillOrder',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#wayBillShow').val(res);
                    },
                });
            }

        });
        $('#taskNottoAllocateCheckSubmit').click(function () {
            let user_mobile = $('#user_mobile').val();
            let user_password = $('#user_password').val();
            let task_id = $('#task_id').val();
            let env = $('#environment').val();

            if ($.trim(user_mobile) === '') {
                Alert.prototype.alertWarning("陛下后台账号不能为空");
                return;
            } else if ($.trim(user_password) === '') {
                Alert.prototype.alertWarning("陛下密码不能为空");
                return;
            } else if ($.trim(task_id) === '') {
                Alert.prototype.alertWarning("陛下任务编号都不能为空");
                return;
            } else {
                param = {
                    'user_mobile': user_mobile,
                    'user_password': user_password,
                    'task_id': task_id,
                    'env': env,
                };
                Alert.prototype.alertLoading();
                $.ajax({
                    type: 'post',
                    url: '/tools/server',
                    // dataType: 'json',
                    data: param,
                    success: function (res) {
                        $('#task_chech_result').val(res);
                        $('#task_check_list_table').bootstrapTable('refresh');
                        Alert.prototype.alertInfo(res)

                    }
                });
            }

        });
        $.ajax({
            type: 'get',
            url: '/tools/getEnvList',
            dataType: 'json',
            success: function (res) {
                Tools.prototype.envSelectInit(res, $('#environment'));
                Tools.prototype.envSelectInit(res, $('#environment1'));
                Tools.prototype.envSelectInit(res, $('#environment2'));
                Tools.prototype.envSelectInit(res, $('#environment3'));
                Tools.prototype.envSelectInit(res, $('#environment4'));
                Tools.prototype.envSelectInit(res, $('#environment5'));
                Tools.prototype.envSelectInit(res, $('#environment6'));
                Tools.prototype.envSelectInit(res, $('#environment7'));
                Tools.prototype.envSelectInit(res, $('#environment8'));
                Tools.prototype.envSelectInit(res, $('#environment9'));
                Tools.prototype.envSelectInit(res, $('#environment10'));
                Tools.prototype.envSelectInit(res, $('#environment11'));
                Tools.prototype.envSelectInit(res, $('#environment12'));
                Tools.prototype.envSelectInit(res, $('#environment13'));
                Tools.prototype.envSelectInit(res, $('#environment14'));
                Tools.prototype.envSelectInit(res, $('#environment15'));
                Tools.prototype.envSelectInit(res, $('#env'));
                Tools.prototype.envSelectInit(res, $('#environment_syh'));
                Tools.prototype.envSelectInit(res, $('#finance_checking_env'));
                Tools.prototype.envSelectInit(res, $('#environment_jd'));
                Tools.prototype.envSelectInit(res, $('#environment_ky'));
                Tools.prototype.envSelectInit(res, $('#environment_sf'));
                Tools.prototype.envSelectInit(res, $('#environment_yt'));
                Tools.prototype.envSelectInit(res, $('#environment_hydd'));
                Tools.prototype.envSelectInit(res, $('#environment_sf'));
                Tools.prototype.envSelectInit(res, $('#appoint_order_env'));
                Tools.prototype.envSelectInit(res, $('#operate_appoint_order_env'));
                Tools.prototype.envSelectInit(res, $('#environment_yxd'));
                Tools.prototype.envSelectInit(res, $('#env2'));
                Tools.prototype.envSelectInit(res, $('#env3'));
                Tools.prototype.envSelectInit(res, $('#env4'));
                Tools.prototype.envSelectInit(res, $('#env5'));
                Tools.prototype.envSelectInit(res, $('#env6'));
                Tools.prototype.envSelectInit(res, $('#finance_modify_punish_fee_views_env'));
                Tools.prototype.envSelectInit(res, $('#finance_new_fund_doc_views_env'));
                Tools.prototype.envSelectInit(res, $('#environment_internal'));
                Tools.prototype.envSelectInit(res, $('#environment_1'));
                Tools.prototype.envSelectInit(res, $('#environment_fy_driver'));
                Tools.prototype.envSelectInit(res, $('#environment_2'));
                Tools.prototype.envSelectInit(res, $('#environment_default'));
                Tools.prototype.envSelectInit(res, $('#environment_month_money'));
                Tools.prototype.envSelectInit(res, $('#environment_tax_bill'));
                Tools.prototype.envSelectInit(res, $('#environment_account_pay'));
            },
        });
    },

    table: function () {
        $('#task_check_list_table').bootstrapTable({
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
                    title: '用户电话'
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
        $('#operate_list_table').bootstrapTable({

            url: '/stat/getOperateList',
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
                },
                {
                    field: 'username',
                    title: '操作人',
                },
                {
                    field: 'operate_type',
                    title: '操作接口'
                },
                {
                    field: 'operate_time',
                    title: '操作时间'
                },
                {
                    field: 'commit',
                    title: '提交信息'
                },
            ]

        });

    },
    //定位菜单
    locationMenu: function () {
        var path = window.location.pathname;
        var paths = path.replace(".do", "").split("/").reverse();
        $("#" + paths[2]).addClass("active").addClass("menu-open");
        $("#" + paths[2] + "-" + paths[1]).addClass("active");
    },
    envSelectInit: function (res, id) {
        for (var i = 0; i < res.length; i++) {
            if (res[i].env === 'r1') {
                id.append("<option value=" + res[i].env + " selected=\"selected\">" + res[i].env + "</option>");
            } else {
                id.append("<option value=" + res[i].env + ">" + res[i].env + "</option>");
            }
        }
        // 缺一不可
        id.selectpicker('refresh');
        id.selectpicker('render');
    }
};


//搜索菜单
function searchMenu() {
    var searchtext = $("input[name=search-text]").val();
    //1.上一步搜索隐藏掉的全部显示出来
    $(".treeview").show();
    $(".treeview ul li").show();
    $(".treeview").removeClass("active").removeClass("menu-open");
    //2.搜索词为空直接不筛选，直接归位
    if (searchtext == null || searchtext === "") {
        Tools.prototype.locationMenu();
        return;
    }
    //3.遍历每组菜单进行匹配
    $(".treeview").each(function () {
        var title1 = $(this).find("a span").html();
        if (title1.indexOf(searchtext) > -1) {
            $(this).addClass("active").addClass("menu-open");
            return;
        }
        var count = 0; //统计符合条件的子菜单数量
        var father = this;
        $(this).find("ul li").each(function () {
            var title2 = $(this).html();
            if (title2.indexOf(searchtext) > -1) {
                count++;
            } else {
                $(this).hide();
            }
        });
        if (count === 0) {
            $(this).hide();
        } else {
            $(father).addClass("active").addClass("menu-open");
        }
    });

}
;
let Alert = function () {
};
Alert.prototype = {
    alertError: function (title_info, text_info) {
        swal({
            title: title_info,
            text: text_info,
            type: "error",
            timer: 3000,

        })
    },
    alertSuccess: function (title_info, text_info) {
        swal({
            title: title_info,
            text: text_info,
            type: "success",
            timer: 3000,

        })
    },
    alertWarning: function (title_info, text_info) {
        swal({
            title: title_info,
            text: text_info,
            type: "warning",
            timer: 3000,

        })
    },
    alertInfo: function (title_info, text_info) {
        swal({
            title: title_info,
            text: text_info,
            type: "info",
            timer: 3000,

        })
    },
    alertLoading: function (timer) {
        swal({
            title: '陛下',
            text: '请你耐心等待一小会，很快的哦',
            imageUrl: '/static/img/loading.gif',
            // imageWidth: 400,
            // imageHeight: 200,
            imageAlt: 'Custom image',
            timer: timer || 5000,
            // animation: false
        })
    }
}

