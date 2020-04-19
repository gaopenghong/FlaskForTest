#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/9 3:26 PM 
# @Author : zhangjian
# @File : api_conf_wrapper.py

from app.tools.api.base import *
import requests


class ApiConf(Base):
    '''系统配置相关接口'''

    # 系统用户管理-查询用户信息
    def conf_user_list(self, mobile, cookies):
        url = self.mk_url('pz', 'api/internal/user/selectUserList')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'mobile': mobile
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 添加系统配置系统权限
    def add_conf_limits(self, user_id, name, mobile, cookies):
        url = self.mk_url('pz', 'api/u/com/updateRoleUser.do')
        data = {
            'roleId': 1,
            'userIds': [{'id': user_id, 'name': name, 'mobile': mobile}]
        }
        r = requests.post(url, data, cookies)
        return r.json()

    # 判断该用户所拥有的角色及所属大区
    def user_system_roles(self, user_id, cookies):
        url = self.mk_url('pz', 'api/user/getUserSystemRoles')
        data = {
            'id': user_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 更改用户信息
    def update_user_info(self, user_id, cookies):
        url = self.mk_url('pz', 'api/user/updateUserInfo')
        data_string = {
            'id': user_id,
            'area': '0,1,2,3,5,6,9,10,11,15,16,17,18,19,20,21,22,23',
            'data': str([{'sysId': 1, 'roleIds': [59]}, {'sysId': 2, 'roleIds': [1123]}, {'sysId': 3, 'roleIds': [2]},
                     {'sysId': 5, 'roleIds': [1123]}, {'sysId': 6, 'roleIds': [1123]}, {'sysId': 7, 'roleIds': [61]},
                     {'sysId': 8, 'roleIds': [59]}, {'sysId': 11, 'roleIds': [1123]}, {'sysId': 12, 'roleIds': [100]},
                     {'sysId': 14, 'roleIds': [1123]}, {'sysId': 15, 'roleIds': [12]}])
        }
        r = requests.post(url, data_string, cookies=cookies)
        return r.json()


if __name__ == '__main__':
    pass
