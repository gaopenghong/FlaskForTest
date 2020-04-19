#!/usr/bin/env python
# -*- codingL utf-8 -*-
__author__ = 'guobaohui'
__time__ = 2019 / 11 / 12

import threading
import time
import json
from app.util.wechat import send_message_wechat
from app.tools.api.conf import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class TaskInfo:
    # # 调度器配置
    # job_defaults = {
    #     'coalesce': False,
    #     'max_instances': 5,
    #     'misfire_grace_time': 120
    # }
    # # 执行器  常用的就线程池和进程池两种
    # thread_pool = ThreadPoolExecutor(30)
    # process_pool = ProcessPoolExecutor(5)
    # executors = {
    #     'thread': thread_pool,
    #     'process': process_pool
    # }
    # # 存储器 默认使用内存,对定时任务丢失什么的不敏感,对定时任务执行要求低
    # sqlite_store = SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    # jobstores = {
    #     'default': sqlite_store
    # }

    def __init__(self, run_date, run_time, start_week, end_week, robot_key, run_name, job_content, run_type):
        self.run_date = run_date
        self.run_time = run_time
        self.start_week = start_week
        self.end_week = end_week
        self.robot_key = robot_key
        self.run_name = run_name
        self.job_content = job_content
        self.run_type = run_type

    def run_job(self):
        # run_date = self.job["run_date"]
        # run_time = self.job["run_time"]
        hour = int(self.run_time.split(":")[0])
        minute = int(self.run_time.split(":")[1])
        second = int(self.run_time.split(":")[-1])

        # start_week = self.job["start_week"]
        # end_week = self.job["end_week"]
        day_of_week = self.start_week + "-" + self.end_week

        # scheduler = BackgroundScheduler(jobstores=self.jobstores, executors=self.executors, job_defaults=self.job_defaults, daemonic=False)
        scheduler = BackgroundScheduler()
        webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s" % self.robot_key
        # run_job_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        msg = "【" + self.run_name + "】\n" + self.job_content
        if self.run_type == "cyclic":
            scheduler.add_job(func=send_message_wechat, args=[webhook, msg, [], ["@all"]], trigger="interval",
                              hours=hour, minutes=minute, seconds=second)
        elif self.run_type == "onece":
            scheduler.add_job(func=send_message_wechat, args=[webhook, msg, [], ["@all"]], trigger="date",
                              run_date=self.run_date+" "+self.run_time)
        elif self.run_type == "timer":
            scheduler.add_job(func=send_message_wechat, args=[webhook, msg, [], ["@all"]], trigger='cron',
                              day_of_week=day_of_week, hour=hour, minute=minute, second=second)
        else:
            print("操作异常！")

        scheduler.start()
        # time.sleep(25)
        # scheduler.shutdown()
        return "okok"


if __name__ == "__main__":
    task_list = [
        {"id": 8, "operator": "\u90ed\u5b9d\u6167", "run_name": "每周", "run_type": "weekly", "run_time": "18:30:00",
         "opt_time": "2019-11-13 17:55:51", "msg": "he"},
        {"id": 9, "operator": "11", "run_name": "循环", "run_type": "cyclic", "run_time": "00:00:07",
         "opt_time": "2019-11-13 17:55:51", "msg": "nihao"},
        {"id": 10, "operator": "22", "run_name": "一次性", "run_type": "onece", "run_time": "00:00:05",
         "opt_time": "2019-11-13 17:55:51", "msg": "一次性111"},
        # {"id": 11, "operator": "22", "run_name": "一次性", "run_type": "onece", "run_time": "00:00:07", "opt_time": "2019-11-13 17:55:51", "msg":"一次性222"}
    ]
    # task_info = TaskInfo("", "00:00:08", "", "", "2d3bd0c7-2a10-4674-8a30-dd6055606d0e", "=ceshi", "ftest测试消息ftest测试消息", "cyclic")
    # a = task_info.run_job()
    # print(a)
