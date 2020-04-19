# coding:utf-8
from app.tools.api.api_finance import *
from app.tools.api.api_ua import *


class UpdateChannelInfo(ApiUa, ApiFinance):
    """金融渠道配置"""

    def test_update_channel_info(self, value):
        request_id = self.ua_generate_check_code()
        login_r = self.ua_login('18911487112', 'Ab@123456789', request_id=request_id)
        value_old = self.get_channel_info(login_r)
        print(value_old)
        if value == value_old:
            global desc
            desc = "当前渠道已符合条件"
        else:
            response = self.update_channel_info(value, login_r)
            desc = response['status']['desc']
        return desc


if __name__ == '__main__':
    r_q = UpdateChannelInfo('r2').ua_generate_check_code()
    login_r = UpdateChannelInfo('r2').ua_login('18911487112', 'Ab@123456789', request_id=r_q)
    UpdateChannelInfo('r2').test_update_channel_info(0)
