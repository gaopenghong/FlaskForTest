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


class ImBase(object):
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
    def mk_url(self, client, url_path=''):
        suffix = {
            'im': 'fykc-imadmin-wrapper'  # 在线客服
        }
        if client in suffix.keys():
            url = 'https://%sfuwu.fuyoukache.com/service/%s/%s' % (self.env, suffix[client], url_path)
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
