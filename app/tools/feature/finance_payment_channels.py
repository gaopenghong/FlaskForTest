# coding:utf-8
from app.tools.api.api_finance import *
from app.tools.api.api_ua import *


class PaymentChannelsSet(ApiFinance, ApiUa):
    def test_finance_payment_channels(self, env, operate_id):
        request_id_r = self.ua_generate_check_code()
        login_r = self.ua_login('18911487112', 'Ab@123456789', request_id=request_id_r)
        print("登录" + str(login_r))
        if operate_id == '开启支付通道':
            payment_channels_r = self.payment_channels('true', login_r)
        else:
            payment_channels_r = self.payment_channels('false', login_r)
        print("支付" + str(payment_channels_r))
        desc = payment_channels_r['status']['desc']
        if desc == '操作成功':
            desc == str(env) + '环境支付通道开启成功'
        return desc
