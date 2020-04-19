# coding:utf-8
import os
import platform
import linecache
from app.util.ssh_conf import *
from app.tools.api.api_lbs_amap import *
from app.tools.api.api_finance import *
from datetime import datetime, timedelta

data_mobile = {
    'appVersion': '3.3.6',
    'osVersion': '8.0.0',
    'osType': '1',
    'network': '4',
    'networkType': '-1',
    'imei': '862258033319303',
    'model': 'MI 5',
    'devVersion': '100',
    'phoneType': 'MEIZU'
}


class ApiXcustomerAPP(Base):
    """吸货APP接口"""

    # 货主APP验证码获取接口
    def customer_app_sendcheckcode(self, mobile=None, codetype=0, smstype=1):
        """
        :param mobile:
        :param codetype:0-短信，1-语音
        :param smstype: 1-登录，2-注册，3-重置密码
        :return: json
        """
        url = self.mk_url('xcustomer', 'api/app/u/sendCheckCode')
        data_dic = {
            'mobile': mobile,
            'codeType': codetype,
            'smsType': smstype
        }
        r = requests.post(url, data_dic)
        return r.json()

    # 获取数据库有效验证码
    def customer_get_code(self, mobile):
        self.customer_app_sendcheckcode(mobile=mobile)
        sql_select = 'select code,codeCount from check_code where requestid = %d' % int(mobile)
        code = remote_database(self.env, 'fykc_xcustomer_service', sql_select)
        if code[0][1] > 10:
            day_time_5 = datetime.now() + timedelta(seconds=300)
            sql_count = 'update check_code set codeCount=0,expiredTime="%s" where requestId = %d' \
                        % (str(day_time_5).split('.')[0], int(mobile))
            remote_database(self.env, 'fykc_xcustomer_service', sql_count)
        return code[0][0]

    # 货主APP登录获取token
    def customer_app_token(self, mobile):
        url = self.mk_url('xcustomer', 'api/app/u/login')
        code = self.customer_get_code(mobile)
        data_dic = {
            'mobile': mobile,
            'code': code,
            'customerType': 6
        }
        data_dic.update(data_mobile)
        r = requests.post(url, data_dic)
        return r.json()

    # 吸货神器-询价接口
    def customer_app_quote_ai_price(self, token, data_new=None, stop_points={}):
        url = self.mk_url('xcustomer', 'api/app/quote/aiCustomerPrice')
        data_dic = {
            'token': token,
            'stopPoints': json.dumps(stop_points, ensure_ascii=False),
            'carLengthId': 8,
            'carModelId': 1,
            'highSpeed': 1
        }
        data_dic.update(data_new)
        data_dic.update(data_mobile)
        r = requests.post(url, data=data_dic)
        return r.json()

    # 吸货神器-确认下单接口
    def customer_app_quote_confirm2pay(self, token, data_new=None, stop_points_new=None):
        url = self.mk_url('xcustomer', 'api/app/quote/confirmOrder2Pay')
        data_dic = {
            'token': token,
            'stopPoints': json.dumps(stop_points_new, ensure_ascii=False),
            'carLengthId': 8,
            'carModelId': 1,
            'highSpeed': 1,
            'customerType': 6
        }
        data_dic.update(data_new)
        data_dic.update(data_mobile)
        # print(data_dic)
        r = requests.post(url, data=data_dic)
        return r.json()

    # 修改数据库金额为空
    def customer_app_modify_price(self, price_id, price_modify=0.01):
        modify_price_sql = 'update customer_price_record set customerPrice=%s where id=%s' % (price_modify, price_id)
        remote_database(self.env, 'fykc_xcustomer_service', modify_price_sql)
        return

    # 确认转账
    def customer_app_confirm_transferaccounts(self, ordersn=None, accuntnum='123123123123', token=None):
        url = self.mk_url('xcustomer', 'api/app/pay/confirmTransferAccounts')
        data_dic = {'token': token}
        if ordersn is not None:
            data_dic['orderSn'] = ordersn
        if accuntnum is not None:
            data_dic['accountNum'] = accuntnum
        data_dic.update(data_mobile)
        r = requests.post(url, data_dic)

        return r.json()


# 时间戳生成
def time_stamp_create(days=1, times='3:00:00'):
    if days >= 0:
        time_string = str(datetime.today().date() + timedelta(days=int(days))) + ' ' + times
    else:
        time_string = str(datetime.today().date() - timedelta(days=abs(int(days)))) + ' ' + times
    print('生成时间：', time_string)
    time_array = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array) * 1000)
    return time_stamp


# 查询地址信息
def address_search(address):
    if platform.system() == 'Mac' or platform.system() == 'Windows':
        file_name = os.path.join(os.path.dirname(__file__)) + '\\..\\data\\region.txt'
    else:
        file_name = os.path.join(os.path.dirname(__file__)) + '/../data/region.txt'
    # print(file_name)
    fp = open(file_name, encoding='utf-8')
    rows = len(fp.readlines())
    j = 0
    for num in range(1, rows + 1):
        region_info = linecache.getline(file_name, num).replace('\n', '')
        region_split = region_info.split('|')
        if address in region_split[1]:
            j = 1
            break
    fp.close()
    if j == 0:
        return '未查询到当前地址信息, 请检查: %s' % address
    else:
        # print(region_split)
        region_id = region_split[0]
        region_address = region_split[1]
        # print(region_address)
        lbs = Amap('t5').amap_input_tips(region_address)
        print(lbs)
        for index in range(len(lbs['tips'])):
            if lbs['tips'][index]['location']:
                break
        result = {
            'province_id': region_id.split(',')[0],
            'city_id': region_id.split(',')[1],
            'district_id': region_id.split(',')[2],
            'province_name': region_address.split('-')[0],
            'city_name': region_address.split('-')[1],
            'district_name': region_address.split('-')[2],
            'latitude': lbs['tips'][index]['location'].split(',')[1],
            'longitude': lbs['tips'][index]['location'].split(',')[0],
            'comment': region_address
        }
        return result


# 地址匹配id
def address_match(address):
    if platform.system() == 'Mac' or platform.system() == 'Windows':
        file_name = os.path.join(os.path.dirname(__file__)) + '\\..\\data\\region.txt'
    else:
        file_name = os.path.join(os.path.dirname(__file__)) + '/../data/region.txt'
    # print(file_name)
    fp = open(file_name, encoding='utf-8')
    rows = len(fp.readlines())
    j = 0
    for num in range(1, rows + 1):
        region_info = linecache.getline(file_name, num).replace('\n', '')
        region_split = region_info.split('|')
        if address in region_split[1]:
            j = 1
            break
    fp.close()
    if j == 0:
        return None
    else:
        # print(region_split)
        region_id = region_split[0]
        region_address = region_split[1]
        result = {
            'province_id': region_id.split(',')[0],
            'city_id': region_id.split(',')[1],
            'district_id': region_id.split(',')[2],
            'province_name': region_address.split('-')[0],
            'city_name': region_address.split('-')[1],
            'district_name': region_address.split('-')[2],
            'comment': region_address
        }
        return result


# 支付审核
def fiance_pay_online_check(env, order_sn, cookies_finance):
    r_online_list = ApiFinance(env).finance_fy_online_check_list({'orderPara': order_sn}, cookies=cookies_finance)
    print("线下转账列表：%s" % r_online_list)
    if 'code' not in r_online_list['status']:
        return r_online_list
    elif r_online_list['status']['code'] != 0:
        return r_online_list
    else:
        request_id = r_online_list['data'][0]['payRequestId']
        r_online_check = ApiFinance(env).finance_fy_online_check(request_id, 2, cookies_finance)
        print('线下转账审核：%s' % r_online_check)
        return r_online_check


# 智能调度开关
def dispatch_ai_switch(env, opt_type):
        url = "http://%sproxy.fuyoukache.com/fykc-order-core/internal/shortcut/internal/aiSchSwitch" % env
        data = {
            "userName": "root-internal",
            "password": "fyhowareyou1qa2ws3ed"
        }
        if opt_type == "on":
            data["switch"] = True
        else:
            data["switch"] = False
        res = requests.get(url, data)

        return res.json()


if __name__ == '__main__':
        # r = ApiXcustomerAPP('t5').customer_app_token(18100000009)
        # print(r)
        ApiXcustomerAPP.time_stamp_create()

