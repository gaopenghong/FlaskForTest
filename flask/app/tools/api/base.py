# coding:utf-8
import hashlib
import json
import random
import requests
import time


# md5加密
def md5_encrypt(text):
    m = hashlib.md5()
    text_1 = text.encode()
    m.update(text_1)
    md5value = m.hexdigest()
    return md5value


class Base(object):
    def __init__(self, environment, role='', target_status='', admin_mobile='', admin_password='', customer_mobile='',
                 agent_mobile='', driver_mobile=''):
        """
        基本参数
        :param environment: 环境, t1/t2/.../t10/r1/r2, 置空表示生产环境
        :param role: 目标角色: 1货主App, 2车队App, 3好运App, 4专车App
        :param target_status: 目标运单状态: 1待审核, 2待报价, 3待下单, 4待支付, 5转账审核中, 6待安排司机, 7已安排司机,
        :param target_status: 目标运单状态: 8待发车, 9卸货完成, 10已签收, 11询价取消, 12成单取消, 13待抢单, 14待接单
        :param admin_mobile: 管理员手机号
        :param admin_password: 管理员登录密码
        :param customer_mobile: 货主手机号
        :param agent_mobile: 经纪人手机号
        :param driver_mobile: 司机手机号
        """
        self.env = environment
        self.role = role
        self.target_status = target_status
        self.admin_mobile = admin_mobile
        self.admin_password = admin_password
        self.customer_mobile = customer_mobile
        self.customer_password = '123456'
        self.agent_mobile = agent_mobile
        self.driver_mobile = driver_mobile

    # 生成URL
    def mk_url(self, client, url_path='', sign=''):
        suffix = {
            'approval': 'fykc-approval-service',  # 审批系统
            'bms': 'fykc-bms-wrapper',  # 运单系统
            'caiwu': 'fykc-caiwu-service',  # 财务系统
            'dd': 'fykc-truck-scheduler',  # 调度系统
            'fuwu': 'fykc-house-keeper',  # 服务系统
            'jr': 'fykc-financeana-service',  # 金融系统
            'ny': 'fykc-oilassign-service',  # 能源系统
            'oms': 'fykc-oms-service',  # 运营系统
            'pz': 'fykc-conf-wrapper',  # 配置系统
            'superbrain': 'fykc-biddecision-service',  # 招投标系统
            'taxsys': 'fykc-taxsys-service',  # 税务系统
            'truckfy': 'fykc-truckforyou-service',  # 专车系统
            'turing': 'fykc-turing-service',  # 图灵系统
            'user': 'fykc-crm-wrapper',  # 用户系统
            'youka': 'fykc-oilcard',  # 油卡系统
            'yxd': 'fykc-autoquery-service',  # 意向单系统
            'order': 'fykc-order-core',  # 运单
        }
        if client in suffix.keys():
            url = 'https://%s%s.fuyoukache.com/service/%s/%s' % (self.env, client, suffix[client], url_path)
        elif client == 'nopen' and sign != '':
            suffix_third = '%s?appKey=%s&reqTimestamp=%s&signStr=%s' % (
            url_path, sign["app_key"], sign["time_stamp"], sign["sign_str"])
            url = 'https://%s%s.fuyoukache.com/%s' % (self.env, client, suffix_third)
        else:
            url = 'https://%s%s.fuyoukache.com/%s' % (self.env, client, url_path)
        return url

    # 基础数据检查-账号
    def base_check(self):
        msg = 'All data is OK!'
        # 环境检查
        if self.env not in ['r1', 'r2', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 'd1', 'd2',
                            'd3']:
            msg = '环境%s不存在, 请重新填写' % self.env
        # 客户账号检查
        # 车队账号检查
        # 司机账号检查
        return msg
