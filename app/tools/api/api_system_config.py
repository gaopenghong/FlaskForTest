# coding:utf-8
from .base import *


class ApiSystemConfig(Base):
    """配置系统"""

    # 系统用户管理-查询用户信息
    def service_select_user_list(self, cookies, page_index=1, page_size=50, name=None, mobile=None,
                                 department=None, auth_type=None):
        url = self.mk_url('pz', 'api/user/selectUserList')
        data = {
            'pageIndex': page_index,
            'pageSize': page_size,
            'name': name,
            'mobile': mobile,
            'department': department,
            'authType': auth_type
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()