#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuchunfu'
__time__ = 2019 / 11 / 5

from flask import render_template, request, session

# models位置
from app.algorithm.models.fchat_model import *
from app.algorithm.models.config_model import *

# feature

from app.algorithm.feature.fchat_algorithm import *

# 导入蓝本 main
from app.algorithm import algorithm_blue
from app.stat.models import stat


# 算法相关
@algorithm_blue.route('/algorithm/fchatIndex')
def algorithm_index():
    return render_template('algorithm/fchat.html', name=session.get('username'))


@algorithm_blue.route('/algorithm/getRunHistory')
def get_record_list():

    return Fchatrecord.get_fchatrecord_list()


@algorithm_blue.route('/algorithm/runFchat', methods=['POST'])
def create_fchat_record():
    operator = session.get('username')
    run_time = datetime.now()
    type = '1'
    res = Fchatest().test_fchat()
    record_id = Fchatrecord.create(operator, type,run_time, res[0])
    coverage =res[1][0]
    accuracy=res[1][1]
    precision=res[1][2]
    recall=res[1][3]
    f_measure=res[1][4]
    Fchatstatic.create_static(record_id,coverage,accuracy,precision,recall,f_measure)
    mysql_cn = pymysql.connect(host='rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com', port=3306, user='fykctest',
                               passwd='fykctest_88', db='ftest')
    df1 = pd.read_sql('select DISTINCT exact_intention from algorithm_test_case_im', con=mysql_cn)
    df2 = df1.values.tolist()
    dfs = []
    for n in df2:
        dfs.append(n[0])
    for i in dfs:
        df = pd.read_sql('select * from algorithm_test_case_im where exact_intention="%s";' % i, con=mysql_cn)
        intention_exact = i
        coverage_exact = len(df[df['result'] != 2]) / len(df)
        accuracy_exact = len(df[df['result'] == 0]) / len(df['id'])
        recall_exact = len(df[df['result'] == 0]) / len(df['id'])
        if len(df[df['result'] != 2]) == 0:
            precision_exact = 0
        else:
            precision_exact = len(df[df['result'] == 0]) / len(df[df['result'] != 2])
        if precision_exact + recall_exact == 0:
            f_measure_exact = 0
        else:
            f_measure_exact = (2 * precision_exact * recall_exact) / (precision_exact + recall_exact)
        Fchatexactstatic.create_exactstatic(record_id, intention_exact,coverage_exact, accuracy_exact, precision_exact, recall_exact, f_measure_exact)
    mysql_cn.close()
    stat.Operate.create(session.get('username'), '/algorithm/runFchat', datetime.now(), '智能客服算法测试')
    return "执行成功"


@algorithm_blue.route('/algorithm/getStaticIndex')
def algorithm_fchatstatic():

    return render_template('algorithm/fchat_static.html',name=session.get('username'))


@algorithm_blue.route('/algorithm/getStaticHistory')
def get_static_list():
    ida = request.args.get('id')
    return Fchatstatic.get_fchatstatic_list(ida)



@algorithm_blue.route('/algorithm/getDetailIndex')
def algorithm_fchatdetail():
    return render_template('algorithm/fchat_detail.html', name=session.get('username'))


@algorithm_blue.route('/algorithm/getFChatDetail')
def get_detail_list():

    return Fchatdetail.get_fchatdetail_list()

@algorithm_blue.route('/algorithm/getExactStatic')
def get_fchatexact_list():
    ida = request.args.get('id')
    return Fchatexactstatic.get_fchatexact_list(ida)

# 配置相关
@algorithm_blue.route('/algorithm/config')
def algorithm_config():
    return render_template('algorithm/config.html', name=session.get('username'))


@algorithm_blue.route('/algorithm/configList')
def get_config_list():

    return Indexconf.get_conf_list()


@algorithm_blue.route('/ConfigList/Edit', methods=['POST'])
def update_config_list():
    data = request.values.to_dict()
    key = data.get("value")
    ids = data.get("id")
    return Indexconf.update_conf_list(ids=ids,values=key)


if __name__ == '__main__':
    create_fchat_record()