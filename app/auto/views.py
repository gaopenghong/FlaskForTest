#!/usr/bin/env python
# coding=utf-8

import uuid
import time
import json
import socket
import random
from flask import render_template
from flask import request, session, redirect
from app.util import jenkins_api
from app.util import message
from app.util import core
# reload(sys)
# 导入蓝本 main
from app.auto import auto_blue
from app.stat.models import stat
from app.auto.models import auto_model
from datetime import datetime

jenkins_job = 'autotest'

autotest = [
    'autotest',
    'autotest1',
    'autotest2',
    'autotest3',
    'autotest4',
    'autotest5',

]


@auto_blue.route('/auto/index')
def auto_index():
    return render_template('auto/index.html', name=session.get('username'))


@auto_blue.route('/auto/getRunHistory')
def auto_list():
    update_status()
    return auto_model.Auto.get_auto_list()


def check_status(params):
    for index, i in enumerate(autotest):
        job = jenkins_build(i)
        print('job_name:' + i)
        try:
            num = job.get_build_num()
            res = job.get_build_result(num)
            if res['building'] is False:
                job.run_job(params)
                return i
            else:
                pass
            # return i
        except Exception as e:
            job.run_job(params)
            return i
        if index == len(autotest) - 1:
            auto = random.choice(autotest)
            j = jenkins_build(auto)
            j.run_job(params)
            return i


@auto_blue.route('/auto/runJob', methods=['POST'])
def run_job():
    env = request.values.get("env")
    label = request.values.get("label")
    id = str(uuid.uuid1())
    if request.values.get("username") == '' or request.values.get("username") != 'fops':
        return str(0)
    else:
        # operator = request.values.get("username")
        operator = session.get('username')
        print(env)
        config_name = check_host()
        params = dict()
        params.update({"env": env, "operator": operator, "uuid": id, "tags": label, "run_env": config_name})

        # job = jenkins_build("autotest")
        # print(params)
        res = check_status(params)
        print(res)
        # job.run_job(params)
        # return str(job.run_job(params))
        run_label = label
        run_time = datetime.now()
        print("$$$$$$$$$$$$")
        # create_job(operator, run_label, run_time, env, id)
        # operator, environment, run_time, result, status, report, run_label
        stat.Operate.create(operator, '/auto/runJob', run_time, "执行自动化" + run_label)
        return str(id) + ':' + res


@auto_blue.route('/auto/runJob1', methods=['POST'])
def run_job1():
    env = request.values.get("env")
    label = request.values.get("label")
    id = str(uuid.uuid1())
    if session.get('username') == '' or session.get('username') == 'None' or session.get('username') is None:
        return redirect('/login')
    else:
        operator = session.get('username')
        print(env)

        params = dict()
        config_name = check_host()
        params.update({"env": env, "operator": operator, "uuid": id, "tags": label, "run_env": config_name})

        res = check_status(params)
        # return str(job.run_job(params))
        run_label = label
        run_time = datetime.now()
        print("$$$$$$$$$$$$")
        # create_job(operator, run_label, run_time, env, id)
        # operator, environment, run_time, result, status, report, run_label
        stat.Operate.create(operator, '/auto/runJob', run_time, "执行自动化" + run_label)
        return str(id) + ':' + res


def check_host():
    hostname = socket.getfqdn(socket.gethostname())
    print(hostname)
    try:
        my_host = socket.gethostbyname(hostname)
        print(my_host)
    except:
        my_host = socket.gethostbyname("")
        print(my_host)
    if my_host != "192.168.2.68":
        name = 'test'
    else:
        name = 'online'
    return name


def jenkins_build(jenkins_job):
    """
    创建jenkins对象
    :return:
    """
    url = "http://ftest-jenkins.fuyoukache.com/"
    return jenkins_api.JenkinsApi(url, jenkins_job)


# @core.asy
# def create_job(operator, run_label, run_time, env, uid):
#     job1 = jenkins_build("autotest")
#     while 1:
#         time.sleep(3)
#         result = job1.get_job_number_map()
#         print("这是异步")
#         # print(result, type(result))
#         num = result.get(uid)
#         print("this is number", num, uid)
#         if num:
#             print("num== %s" % num)
#             report = 'http://ftest-jenkins.fuyoukache.com/job/autotest/ws/foryou/report/' + str(num) + '.html'
#             console = 'http://ftest-jenkins.fuyoukache.com/job/autotest/' + str(num) + '/console'
#             res = job1.get_build_result(num)
#             auto_model.Auto.create(operator, env, run_time, num, str(res['result']), '', report,
#                                    run_label, uid, "", console)
#             break


@auto_blue.route('/auto/getJobNum')
def get_job_num():
    uuid = request.values.get("uuid")
    print(uuid)

    job = jenkins_build("autotest")
    result = job.get_job_number_map()
    print(result)
    if uuid in result:
        num = result[str(uuid)]
        get_job_status(num)
        return str(num)
    else:
        return str(0)


def send_wechat():
    res = 'jenkins自动化执行时间太长了，我监听累了'
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=da4273ef-9e0d-4971-a9ed-1938cd932123"
    message.send_message(url, str(res))


@core.asy
@core.time_limit(360)
def get_job_status(num):
    # num = request.values.get("num")
    job = jenkins_build("autotest")
    while 1:
        time.sleep(3)
        res = job.get_build_result(num)
        print(res['result'])
        if str(res['building']) == "False":
            res1 = get_result(num)
            operator = res1['operator']
            env = res1['env']
            run_time = res1['run_time']
            result = res1['result']
            report = 'http://ftest-jenkins.fuyoukache.com/job/autotest/ws/foryou/report/' + str(num) + '.html'
            console = 'http://ftest-jenkins.fuyoukache.com/job/autotest/' + str(num) + '/console'
            run_label = res1['tags']
            uuid = res1['uuid']
            try:
                auto_model.Auto.update_job_by_num(num, operator, run_time, result, report, run_label, uuid, console)
                # auto_model.Auto.update_job_by_num(num, res['result'])

                # print(res1)
            except:

                auto_model.Auto.create(operator, env, run_time, num, result, '', report,
                                       run_label, uuid, "", console)
            # res2 = auto_model.Auto.get_info(num)
            # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=da4273ef-9e0d-4971-a9ed-1938cd932123"
            # print("%%%%%%%%%%%%%%%%")
            # print(res2)
            # message.send_message(url, str(res2))

            break


@auto_blue.route('/auto/getJobStatus')
def get_job_status1():
    num = request.values.get("num")
    job = jenkins_build("autotest")
    #
    res = job.get_build_result(num)
    print(res['result'])
    if str(res['building']) == "False":
        return 'success'
    else:
        return 'false'


@core.asy
def update_status():
    #
    res = auto_model.Auto.get_auto_list()

    for i in json.loads(res):
        print(i)
        if i['result'] == 'None' or i['result'] == '' or i['result'] is None or i['operator'] is None:
            num = i['job_num']
            res1 = get_result(i['job_num'])
            print(res1)
            operator = res1['operator']
            run_time = res1['run_time']
            result = res1['result']
            report = 'http://ftest-jenkins.fuyoukache.com/job/autotest/ws/foryou/report/' + str(num) + '.html'
            console = 'http://ftest-jenkins.fuyoukache.com/job/autotest/' + str(num) + '/console'
            run_label = res1['tags']
            uuid = res1['uuid']
            building = res1['building']

            if str(building) == "False":
                auto_model.Auto.update_job_by_num(i['job_num'], operator, run_time, result, report, run_label, uuid,
                                                  console)
                # res2 = auto_model.Auto.get_info(num)
                # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=da4273ef-9e0d-4971-a9ed-1938cd932123"
                # print("%%%%%%%%%%%%%%%%")
                # print(res2)
                # message.send_message(url, str(res2))


@auto_blue.route('/auto/getLabel')
def get_label():
    return auto_model.Label.get_label_list()


def get_result(number):
    job = jenkins_build("autotest")
    res = job.get_build_result(number)
    params = res['actions'][0]['parameters']
    result = dict()
    for p in params:
        print(p)
        result[p['name']] = p['value']
    str1 = str(res['timestamp'])[:-3]
    result['run_time'] = timestamp2string(int(str1))
    result['result'] = res['result']
    result['building'] = res['building']
    return result


def timestamp2string(timeStamp):
    try:
        # d = datetime.strptime(timeStamp)
        str1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))
        # 2015-08-28 16:43:37.283000'
        return str1
    except Exception as e:
        print(e)
        return ''


if __name__ == '__main__':
    # res1 = get_result(83)
    # print(res1)
    check_status()
    # rr = timestamp2string(1575858723)
    # str = "1575858723160"
    # print(int(str[:-3]))
    # print(timestamp2string(int(str[:-3])))
