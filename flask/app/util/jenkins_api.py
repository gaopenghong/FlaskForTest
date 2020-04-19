#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuchunfu'
__time__ = 2018 / 5 / 30
import jenkins

import time
import requests
import threading
import json
from bs4 import BeautifulSoup

c_time = int(time.time())


class JenkinsApi(object):
    _instance_lock = threading.Lock()

    def __init__(self, server_id, job_name):
        self.server_id = server_id
        self.job_name = job_name
        self.server = jenkins.Jenkins(server_id)

    def __new__(cls, *args, **kwargs):
        if not hasattr(JenkinsApi, "_instance"):
            with JenkinsApi._instance_lock:
                if not hasattr(JenkinsApi, "_instance"):
                    JenkinsApi._instance = object.__new__(cls)
        return JenkinsApi._instance

    def get_build_result(self, number):
        """
            获取返回结果
        :return:
        """
        try:

            return self.server.get_build_info(self.job_name, int(number))

        except Exception as err:
            print(err)
        # return self.server.get_build_info(self.job_name, int(number))

    def get_build_num(self):
        """

        :return:返回最后一次build number
        """

        return self.server.get_job_info(self.job_name)['lastBuild']['number']

    def run_job(self, param=None):
        """

        :param param:
        :return:
        """
        print(param)
        print("@@@@")
        if param is None:
            return self.server.build_job(self.job_name)
        else:
            return self.server.build_job(self.job_name, parameters=param)

    def get_job_number_map(self):
        """
        获取job number 的字典
        :param job_name:
        :return:
        """
        number_map = {}
        number = None
        deploy_id = None
        print('test')
        try:
            url = self.server_id + "/job/" + self.job_name
            resp = requests.get(url=url)
            html_str = resp.text
            html = BeautifulSoup(html_str, 'html.parser')
            table_str = html.select('.pane')[0].__str__()
            table = BeautifulSoup(table_str, 'html.parser')
            tdlist = table.find_all('td')
            for td in tdlist:
                td_soup = BeautifulSoup(td.__str__(), 'html.parser')
                alist = td_soup.find_all('a')
                for a in alist:
                    if a.string.__str__().startswith('#'):
                        number = int(a.string.__str__().replace('#', ''))
                divlist = td_soup.find_all('div')
                for div in divlist:
                    if "indent-multiline" in div.__str__():
                        # print(div.string.__str__().split(':'))
                        deploy_id = div.string.__str__().split(':')[0]
                if number and deploy_id:
                    number_map[deploy_id] = number
        except Exception as e:
            err_msg = "get number map error {e}".format(e=str(e))
        return number_map


if __name__ == '__main__':
    url = "http://ftest-jenkins.fuyoukache.com/"
    job1 = JenkinsApi(url, "autotest")

    res = job1.get_build_result(83)
    print(res['actions'])

