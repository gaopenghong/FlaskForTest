$(function(){

	var path = window.location.pathname;
    if(path == "/statistics/pvTotal/" || path == "/statistics/"){
        var listName=["zhangdanzd","furongrosy","wangxiuzixi","shangyumei","liuyahui_i","wangkaihua","yangfang","sujinggang","guoshuaiqi", "guozhengzhong_v"];
        var username=$("#username").text();

             if(isInArray(listName,username)){
                showTotal();
                showLine();
                showBroad();
                setInterval(function () {
                    showBroad();
                },5000)

            }
        else{
	        alert("您没有权限访问，请联系管理员 张丹(zhangdanzd)");
	        window.location.href="/";

         }

    }
});
function isInArray(arr,value){
    if(arr.indexOf&&typeof(arr.indexOf)=='function'){
        var index = arr.indexOf(value);
        if(index >= 0){
            return true;
        }
    }
    return false;
}
function showTotal() {
    var myChart1 = echarts.init(document.getElementById('main-bar'));
    var myChart2 = echarts.init(document.getElementById('main-pip'));
    // var myChart3 = echarts.init(document.getElementById('mainHtml-bar'));
    // var myChart4 = echarts.init(document.getElementById('mainHtml-pip'));

    option1 = {
    title : {

        text: '功能接口访问详情',
        subtext: 'DiDi Farm',
        x:'center',
        y:'top',

    },

    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: [
        {
            type: 'category',
            data:[],
            axisPointer: {
                type: 'shadow'
            },
            axisLabel: {
                interval:0,
                 rotate:30
                 },
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '次数',
            // min: 0,
            // max: 250,
            // interval: 50,
            axisLabel: {
                formatter: '{value}'
            }
        }
    ],
    series: [
        {
            name:'访问次数',
            type:'bar',
            data:[],
            itemStyle: {
                //通常情况下：
                normal: {
                    //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                    color: function (params) {
                        var colorList = ['rgb(102,153,204)', 'rgb(204,204,153)','rgb(194,85,82)','rgb(204,255,102)', 'rgb(255,153,0)'
                        ,'rgb(102,102,153)','rgb(153,204,153)','rgb(153,51,102)','rgb(47,69,84)','rgb(51,152,219)','rgb(92,111,123)','rgb(121,123,127)','rgb(207,178,169)','rgb(159,218,191)'];
                        return colorList[params.dataIndex];
                    }
                    // color:function(d){return "#"+Math.floor(Math.random()*(256*256*256-1)).toString(16);}
                }
            },
        }
    ]
};

option3 = {
    title : {

        text: '页面接口访问详情',
        subtext: 'DiDi Farm',
        x:'center',
        y:'top',

    },

    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: [
        {
            type: 'category',
            data:[],
            axisPointer: {
                type: 'shadow'
            },
            axisLabel: {
                interval:0,
                 rotate:35
                 },
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '次数',
            // min: 0,
            // max: 250,
            // interval: 50,
            axisLabel: {
                formatter: '{value}'
            }
        }
    ],
    series: [
        {
            name:'访问次数',
            type:'bar',
            data:[],
            itemStyle: {
                //通常情况下：
                normal: {
                    //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                    color: function (params) {
                        var colorList = ['rgb(102,153,204)', 'rgb(204,204,153)','rgb(194,85,82)','rgb(204,255,102)', 'rgb(255,153,0)'
                        ,'rgb(102,102,153)','rgb(153,204,153)','rgb(153,51,102)','rgb(47,69,84)','rgb(51,152,219)','rgb(92,111,123)','rgb(121,123,127)','rgb(207,178,169)','rgb(159,218,191)'];
                        return colorList[params.dataIndex];
                    }
                    // color:function(d){return "#"+Math.floor(Math.random()*(256*256*256-1)).toString(16);}
                }
            },
        }
    ]
};
//饼状图
    option2 = {
  title : {

        text: '功能接口访问占比',
        subtext: 'DiDi Farm',
        x:'center',
        y:'top',

    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:[],
        show:false,
    },
    series : [
        {
            name: 'API',
            type: 'pie',
            radius : '55%',
            center: ['50%', '50%'],
            data:[],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                },
                 normal: {
                     //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                     color: function (params) {
                         var colorList = ['rgb(102,153,204)', 'rgb(204,204,153)','rgb(194,85,82)','rgb(204,255,102)', 'rgb(255,153,0)'
                        ,'rgb(102,102,153)','rgb(153,204,153)','rgb(153,51,102)','rgb(47,69,84)','rgb(51,152,219)','rgb(92,111,123)','rgb(121,123,127)','rgb(207,178,169)','rgb(159,218,191)'];
                         return colorList[params.dataIndex];
                     }
                     // color:function(d){return "#"+Math.floor(Math.random()*(256*256*256-1)).toString(16);}
                 }
            }
        }
    ]
};
    option4 = {
        title : {
        text: '页面接口访问占比',
        subtext: 'DiDi Farm',
        x:'center',
        y:'top',

    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data:[],
        show:false,
    },
    series : [
        {
            name: 'API',
            type: 'pie',
            radius : '55%',
            center: ['50%', '55%'],
            data:[],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                },
                 normal: {
                     //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                     color: function (params) {
                          var colorList = ['rgb(102,153,204)', 'rgb(204,204,153)','rgb(194,85,82)','rgb(204,255,102)', 'rgb(255,153,0)'
                        ,'rgb(102,102,153)','rgb(153,204,153)','rgb(153,51,102)','rgb(47,69,84)','rgb(51,152,219)','rgb(92,111,123)','rgb(121,123,127)','rgb(207,178,169)','rgb(159,218,191)']
                         return colorList[params.dataIndex];
                     }
                     // color:function(d){return "#"+Math.floor(Math.random()*(156*156*156-1)).toString(16);}
                 }
            }
        }
    ]
};

    $.ajax({
        url:"/statistics/query/",
        type:"POST",
        dataType:"json",
        success:function (data) {
            if(data.errno==0){
                var interName=[];
                for(var i=0;i<data.data.result.datas.length;i++){
                    interName.push(data.data.result.datas[i].interface_name);
                }
                var interName2=[];
                for(var i=0;i<data.data.htmlresult.datas.length;i++){
                    interName2.push(data.data.htmlresult.datas[i].interface_name);
                }
                var visitTimes=[];
                for(var i=0;i<data.data.result.datas.length;i++){
                    visitTimes.push(data.data.result.datas[i].visit_times);
                }
                var visitTimes2=[];
                for(var i=0;i<data.data.result.datas.length;i++){
                     visitTimes2.push({
                            name : data.data.result.datas[i].interface_name,
                            value : data.data.result.datas[i].visit_times
                         });
                }
                var visitTimes3=[];
                var visitTimes4=[];
                for(var i=0;i<data.data.htmlresult.datas.length;i++){
                    visitTimes3.push(data.data.htmlresult.datas[i].visit_times);
                }
                for(var i=0;i<data.data.htmlresult.datas.length;i++){
                     visitTimes4.push({
                            name : data.data.htmlresult.datas[i].interface_name,
                            value : data.data.htmlresult.datas[i].visit_times
                         });
                }
                option1.xAxis[0].data=interName;
                option1.series[0].data=visitTimes;
                option2.legend.data=interName;
                option2.series[0].data=visitTimes2;
                option3.xAxis[0].data=interName2;
                option3.series[0].data=visitTimes3;
                option4.legend.data=interName2;
                option4.series[0].data=visitTimes4;
                 myChart1.setOption(option1);
                 myChart2.setOption(option2);
                 // myChart3.setOption(option3);
                 // myChart4.setOption(option4);

            //     总的访问次数
                var func = document.getElementById("func");
                // var htm = document.getElementById("htm");
                func.innerHTML="接口总访问次数："+data.data.result.total;
            }else{
                alert(data.msg);
            }
            startmarquee();



        }
    });
}

//消息循环显示
function startmarquee() {
    //获得当前<ul>
    var $uList = $("#main-new ul");
    var timer = null;
    //触摸清空定时器
    $uList.hover(function() {
        clearInterval(timer);
    },
    function() { //离开启动定时器
        timer = setInterval(function() {
            scrollList($uList);
        },
        2000);
    }).trigger("mouseleave"); //自动触发触摸事件
    //滚动动画
    function scrollList(obj) {
        //获得当前<li>的高度
        var scrollHeight = $("#main-new ul li:first").height();
        // console.log(scrollHeight);
        //滚动出一个<li>的高度
        $uList.stop().animate({
            marginTop: -scrollHeight
        },
        600,
        function() {
            //动画结束后，将当前<ul>marginTop置为初始值0状态，再将第一个<li>拼接到末尾。
            $uList.css({
                marginTop: 0
            }).find("li:first").appendTo($uList);
        });
    }
}

//折线图的显示
function showLine() {
   var myChart5 = echarts.init(document.getElementById('main-line'));
    option5 = {
        xAxis: {
        type: 'category',
        data:[],
        axisLabel: {
            interval:0,
            rotate:15
        },
    },
    yAxis: {
        type: 'value',
        name: '次数',
        axisLabel: {
            formatter: '{value}'
        }
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
   tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow',
            crossStyle: {
                color: '#999'
            }
        }
    },
    legend: {
        data:['访问总次数']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    series: [{
        name:'访问总次数',
        data:[],
        type: 'line'
     }]
    };
    var dataType=$("#countType").val();
    var x_week = ['第一周','第二周','第三周','第四周'];
    $.ajax({
        url:"/statistics/queryData/",
        type:"POST",
        dataType:"json",
        data:{dataType:dataType},
        success:function (data) {
            if(dataType == 'MM'){
                option5.xAxis.data=x_week;
                option5.series[0].data=data.data.y_data;
            }else if(dataType == 'IW'){
                var d = new Date();
                switch (d.getDay()){
                    case 0:
                        option5.xAxis.data=['M', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                        break;
                    case 1:
                        option5.xAxis.data=['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun','M'];
                        break;
                    case 2:
                        option5.xAxis.data=['Wed', 'Thu', 'Fri', 'Sat', 'Sun','M','Tue'];
                        break;
                    case 3:
                        option5.xAxis.data=[ 'Thu', 'Fri', 'Sat', 'Sun','M','Tue','Wed'];
                        break;
                    case 4:
                        option5.xAxis.data=[ 'Fri', 'Sat', 'Sun','M','Tue','Wed','Thu'];
                        break;
                    case 5:
                        option5.xAxis.data=[ 'Sat', 'Sun','M','Tue','Wed','Thu','Fri'];
                        break;
                    case 6:
                        option5.xAxis.data=[ 'Sun','M','Tue','Wed','Thu','Fri','Sat'];
                        break;
                }
                option5.series[0].data=data.data.y_data;
            }else{
                switch (data.data.x_data){
                    case 0:
                        option5.xAxis.data=["2:00"];
                        break;
                    case 1:
                        option5.xAxis.data=["2:00","4:00"];
                        break;
                    case 2:
                        option5.xAxis.data=["2:00","4:00","6:00"];
                        break;
                    case 3:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00"];
                        break;
                    case 4:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00"];
                        break;
                    case 5:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00"];
                        break;
                    case 6:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00"];
                        break;
                    case 7:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00","16:00"];
                        break;
                    case 8:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00","16:00","18:00"];
                        break;
                    case 9:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00","16:00","18:00","20:00"];
                        break;
                    case 10:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00"];
                        break;
                    case 11:
                        option5.xAxis.data=["2:00","4:00","6:00","8:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00","24:00"];
                        break;

                }
                option5.series[0].data=data.data.y_data;
            }
             myChart5.setOption(option5);
        }
    });

}

//广播消息的显示
function showBroad() {
    $.ajax({
        url:"/statistics/queryNews/",
        type:"POST",
        dataType:"json",
        success:function (data) {
            var mainNew = document.getElementById('news');
            for(var i=0; i<data.data.length;i++){
                 mainNew.innerHTML += "<li><a href='#'>" + data.data[i] + "</a></li>";
            }
        }
    })
}
