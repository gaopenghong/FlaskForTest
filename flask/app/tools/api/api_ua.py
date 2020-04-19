# coding:utf-8
from .base import *


class ApiUa(Base):
    """统一登录"""

    # 生成登录验证码
    def ua_generate_check_code(self):
        url = self.mk_url('ua', 'api/uc/src/image/genCheckCodeRequest')
        print(url)
        r = requests.post(url)
        # print(123)
        print("test::%s" % r.text)
        return r.text

    # 登录
    def ua_login(self, mobile, password, request_id):
        url = self.mk_url('ua', 'api/uc/auth/login')
        data = {
            'userName': mobile,
            'userPassword': password,
            'srcType': '',
            'redirectUrl': '',
            'checkCode': '1123',
            'requestId': request_id
        }
        r = requests.post(url, data)
        return r.cookies.get_dict()

    # 登录
    def ua_login_r(self, mobile, password, request_id):
        url = self.mk_url('ua', 'api/uc/auth/login')
        data = {
            'userName': mobile,
            'userPassword': password,
            'srcType': '',
            'redirectUrl': '',
            'checkCode': '1123',
            'requestId': request_id
        }
        r = requests.post(url, data)
        return r

    # 获取管理员信息
    def bms_admin_info(self, cookies_ua):
        url = self.mk_url('bms', 'api/u/com/getUserInfo.do')
        r = requests.post(url, cookies=cookies_ua)
        return r.json()
