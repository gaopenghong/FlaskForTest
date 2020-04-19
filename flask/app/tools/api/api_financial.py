# coding:utf-8
# 金融系统接口
from .base import *
import os

import requests
import xlrd
import platform
from xlutils.copy import copy

from app.tools.api.base import Base

project_path = os.path.dirname(os.path.dirname(__file__))
# 导出、下载文件目录
export_path = project_path + '/data'


class ApiFinancial(Base):
    """金融系统接口"""
    def finance_contrast_bill(self, cookies):
        url = self.mk_url('proxy', 'fykc-financeana-service/api/internal/checkBaoliOrder')
        current_month = time.strftime('%Y-%m', time.localtime())
        year = current_month.split('-')[0]
        month = int(current_month.split('-')[1]) + 1
        if month == 13:
            year = int(current_month.split('-')[0]) + 1
            month = '1'
        if month < '13':
            month = '0%s' % month
        data = {
            'date': '%s-%s-20 00:00:00' % (year, month)
        }
        r = requests.post(url, data, cookies=cookies)
        print(r.text)
        print(data)
        return r.json()

    # 金融系統还款
    def finance_pay_back(self, cookies):
        url = self.mk_url('proxy', 'fykc-caiwu-service/api/internal/financeana/batchBaoliPay')
        data = {}
        r = requests.post(url, data, cookies=cookies)
        print(r.text)
        return r.json()
