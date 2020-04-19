# coding:utf-8
from app.tools.api.api_ua import *
from app.tools.api.api_driver import *
from app.tools.api.api_customer_app import *

dbconfig = [
    ['t1', 30110],
    ['t2', 30120],
    ['t3', 30130],
    ['t4', 30140],
    ['t5', 30150],
    ['t6', 30160],
    ['t7', 30170],
    ['t8', 30180],
    ['t9', 30190],
    ['t10', 30200],
    ['r1', 30112],
    ['r2', 30122]
]

administrator_password_ua = 'Ab@123456789'

class ApiBms(Base):

    """获取管理员手机号"""
    def bms_admin_mobile(self, admin_mobile='16877777777'):
        admin_mobile = admin_mobile
        return admin_mobile

    """运单详情接口"""
    def bms_order_detail(self, order_sn,cookies):
        # url = self.mk_url('bms', 'api/dispatch/getOrderDetail.do')
        url = self.mk_url('bms', 'api/order/detail.do')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    """运单列表"""
    def bms_order_list(self, cookies_bms, conditions={}):
        url = self.mk_url('bms', 'api/order/list.do')
        data = {
            'pageIndex': 1,
            'pageSize': 30
        }
        data.update(conditions)
        print('data-----', data)
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 运单时效信息
    def bms_order_time(self, order_sn, cookies_bms):
        url = self.mk_url('bms', 'api/order/getGoodsTime')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 获取轨迹定位数据
    def bms_order_location_trajectory(self, order_sn, cookies_bms):
        url = self.mk_url('bms', 'api/order/orderLocationTrajectory')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 运单提款条件
    def bms_order_draw_filter(self, order_sn, cookies_bms):
        url = self.mk_url('bms', 'api/order/drawFilter')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    """运单异常修改"""
    def bms_order_exception(self, order_sn, modify_function, modify_reason='', modify_data={}, cookies_bms={}):
        """
        :param order_sn:运单号
        :param modify_function:异常修改类型
        :param modify_reason:异常修改原因
        :param modify_data:异常修改数据
        :param cookies_bms:cookies
        :return:
        """
        url = self.mk_url('bms', 'api/order/abnormal/modify')
        modify_reason_all = [
            {'type': 11, 'reason': [101, 102, 103]},  # 11:"取消运单"   101:客户原因 102:经纪人原因 103:司机原因
            {'type': 12, 'reason': [104, 105, 112]},  # 12:"司机卸货完成"    104:司机未安装好运  105:司机忘记操作  112:初审修改错误
            {'type': 13, 'reason': [107, 108, 109, 110]},
            # 13:"签收"    107:无法联系货主   108:货主拒绝签收   109:核实货主已签收   110:协助货主签收
            {'type': 14, 'reason': [104, 105, 106, 112]},
            # 14:"司机到达起始地"   104:司机未安装好运   105:司机忘记操作  106:运单地址错误   112:初审修改错误
            {'type': 21, 'reason': [111, 112, 121]},  # 21:"回单修改"   111:货主更改选择   112:初审修改错误  121:其他
            {'type': 22, 'reason': [104, 105, 106, 112, 121]},
            # 22:"装卸货地位置"   104:司机未安装好运   105:司机忘记操作  106:运单地址错误  112:初审修改错误  121:其他
            {'type': 23, 'reason': [111, 112, 121]},  # 23:"回单修改(卸货后)"  111:货主更改选择   112:初审修改错误    121:其他
            {'type': 31, 'reason': [114, 115, 121]},  # 31:"更换经纪人"  114:经纪人放鸽子   115:内部转单  121:其他
            {'type': 32, 'reason': [116, 117, 118, 119, 121]},
            # 32:"更换司机"  116:调度派车错误   117:经纪人派车错误  118:司机放鸽子   119:司机低价  121:其他
            {'type': 33, 'reason': [116, 117, 118, 119, 121]},
            # 33:"更换车辆"  116:调度派车错误   117:经纪人派车错误  118:司机放鸽子   119:司机低价  121:其他
            {'type': 41, 'reason': [122, 123, 124, 125, 121]},
            # 41:"修改装卸货地址"  122：修改装货地  123：修改卸货地  124：修改经停点  125：添加经停点  121:其他
            {'type': 42, 'reason': []},  # 42:"修改车辆信息"
            {'type': 58, 'reason': []},  # 58:"客户大区修改"
            {'type': 59, 'reason': []},  # 59:“修改货物重量体积”
            {'type': 60, 'reason': [101, 102, 103, 127], 'reason_second': [1, 2, 3, 4, 5, 6, 7, 8]}  # 60:“取消运单申请”
            # 101:客户原因 102:企业运力  103:司机原因  127：福佑调度原因
            # 1 取消发货 2 货量不足 3 重复下单 4 下错单
            # 5 未及时安排司机 6 未找到符合用车 7 司机放鸽子 8 其他
        ]
        for index in modify_reason_all:
            if modify_function == 11 or modify_function == 60:
                reason_real = modify_reason
                break
            else:
                if index['type'] == modify_function and len(index['reason']) != 0:
                    reason_real = index['reason'][random.randint(0, len(index['reason']) - 1)]
                    break
                else:
                    reason_real = 121
                    break
        if modify_function == 12 or modify_function == 13:
            data = {
                'orderSn': order_sn,
                'secondLevel': reason_real,
                'comment': '技术测试异常修改',
                'voucherImg': '',
                'type': modify_function
            }
        else:
            data = {
                'orderSn': order_sn,
                'secondLevel': reason_real,
                'comment': '技术测试异常修改',
                'voucherImg': '',
                'type': modify_function,
                'changeData': json.dumps(modify_data)
            }
        # print('请求数据: ', data)
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 管理员信息获取
    def admin_info_get(self, administrator_mobile):
        sql_search_admin_info = 'select id,name,mobile,token,tokenExpire from user_base_info ' \
                                'where mobile="%s";' % str(administrator_mobile)
        r_search_admin_info = remote_database(self.env, 'fykc_tower_babel', sql_search_admin_info)
        print('管理员信息查询结果: %s' % r_search_admin_info)
        if len(r_search_admin_info) == 0:
            return '管理员账号%s不存在, 请检查' % administrator_mobile
        else:
            admin_info = {
                'id': r_search_admin_info[0][0],
                'name': r_search_admin_info[0][1],
                'mobile': r_search_admin_info[0][2],
                'cookies_ua': ''
            }
            r_admin_cookies_expire = r_search_admin_info[0][4]
            if r_admin_cookies_expire is None:
                admin_cookies_expire = 0
            else:
                admin_cookies_expire = int(time.mktime(r_admin_cookies_expire.timetuple()))

            if admin_cookies_expire >= int(time.time()) + 200:
                m2 = hashlib.md5()
                m2.update(('http://' + str(self.env) + 'ua.fuyoukache.com/view/admin/login').encode('utf-8'))
                admin_cookies_key = 'FYKC_' + str(m2.hexdigest())
                admin_cookies = {admin_cookies_key: r_search_admin_info[0][3]}
            else:
                r_ua_request_id = ApiUa(self.env).ua_generate_check_code()
                # administrator_password_ua = 'Ab@123456789'
                admin_cookies = ApiUa(self.env).ua_login(administrator_mobile, administrator_password_ua,
                                                         r_ua_request_id)
            admin_info['cookies_ua'] = admin_cookies
        return admin_info

    # 司机信息获取
    def driver_info_get(self, driver_mobile):
        sql_search_driver_info = 'select id,name,mobile,token,tokenExpire from driver_info where mobile="%s";' % driver_mobile
        r_search_driver_info = remote_database(self.env, 'fykc_xdriver_service', sql_search_driver_info)
        print('司机信息查询结果: %s' % r_search_driver_info)
        if len(r_search_driver_info) == 0:
            return '司机账号%s不存在, 请检查' % driver_mobile
        else:
            driver_info = {
                'id': r_search_driver_info[0][0],
                'name': r_search_driver_info[0][1],
                'mobile': driver_mobile,
                'token': ''
            }
            r_driver_token_expire = r_search_driver_info[0][4]
            if r_driver_token_expire is None:
                driver_token_expire = 0
            else:
                driver_token_expire = int(time.mktime(r_driver_token_expire.timetuple()))

            if driver_token_expire >= int(time.time()) + 200:
                driver_token = r_search_driver_info[0][3]
            else:
                r_driver_login = ApiDriver(self.env).driver_login(driver_mobile, '1123')
                driver_token = r_driver_login['data'][0]['token']
            driver_info['token'] = driver_token
        return driver_info

    # 货主信息获取
    def customer_info_get(self, customer_mobile):
        sql_search_customer_info = 'select id,name,mobile,password,token,tokenExpire from customer_info ' \
                                   'where mobile="%s";' % str(customer_mobile)
        r_search_customer_info = remote_database(self.env, 'fykc_xcustomer_service', sql_search_customer_info)
        print('货主信息查询结果: %s' % r_search_customer_info)
        if len(r_search_customer_info) == 0:
            return '货主账号%s不存在, 请检查' % customer_mobile
        else:
            customer_info = {
                'id': r_search_customer_info[0][0],
                'name': r_search_customer_info[0][1],
                'mobile': r_search_customer_info[0][2],
                'token': ''
            }
            r_customer_token_expire = r_search_customer_info[0][5]
            if r_customer_token_expire is None:
                customer_token_expire = 0
            else:
                customer_token_expire = int(time.mktime(r_customer_token_expire.timetuple()))

            if customer_token_expire >= int(time.time()) + 200:
                customer_info['token'] = r_search_customer_info[0][4]
            else:
                r_customer_app_login = ApiCustomerApp(self.env).customer_app_login(customer_mobile)
                print('货主登录结果: %s' % r_customer_app_login)
                customer_info['token'] = r_customer_app_login['data'][0]['token']
        return customer_info

    # 收回单
    def bms_order_receipt_confirm(self, order_sn, cookies_bms):
        url = self.mk_url('bms', 'api/order/receipt/confirm.do')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 运单异常修改
    def modify(self, orderSn, modify_reason, order_status, loginCookies):
        """
        :param orderSn:
        :param secondLevel: 104-司机未安装好运；105-司机忘记操作好运；106-初审修改地址错误；107-无法联系货主；108-货主拒绝签收；109-核实货主已签收；110-协助货主签收
        :param type: 12-司机卸货完成（104～106）；13-签收（107～110）
        :param loginCookies:
        :return:
        """
        url = self.mk_url('bms', 'api/order/abnormal/modify')
        data = {
            'orderSn': orderSn,
            'secondLevel': modify_reason,
            'comment': '运单异常修改-运单状态修改',
            'voucherImg': '',
            'type': order_status,
        }
        print(data)
        print(url)
        r = requests.post(url, data, cookies=loginCookies)
        print(r.json())
        return r.json()

    # 上传回单
    def bms_order_receipt_upload(self, order_sn, cookies_bms):
        url = self.mk_url('bms', 'api/order/receipt/uploadInfo.do')
        data_1 = {
            'orderSn': order_sn,
            'imageUrl': 'https://public.fuyoukache.com/common/5baaffc62508f.jpg',
            'backStatus': 2
        }
        data = {
            'jsonData': json.dumps(data_1)
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 标记可付款
    def bms_order_mark_exception(self, order_sn, operation_type, cookies_bms):
        """
        :param order_sn:
        :param operation_type: 2可付款, 1不可付款
        :param cookies_bms:
        :return:
        """
        url = self.mk_url('bms', '/api/order/mark/exception.do')
        data_1 = {
            'orderSn': order_sn,
            'voucherImg': '',
            'comment': '技术测试标记是否可付款',
            'operType': operation_type
        }
        if operation_type == 1:
            data_1.update({'causeType': '13'})
        data = {
            'jsonData': json.dumps(data_1)
        }
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()

    # 图灵报价推运单系统（无需等待）
    def turing_price_to_order_core_quickly(self, order_sn, turing_price=2100.00):
        url = 'http://%sproxy.fuyoukache.com/fykc-order-core/api/pipeline/quote/fykcQuote' % self.env
        data = {
            'orderSn': order_sn,
            'cusBareTransAmount': turing_price,
            'operId': 1567,
            'operName': 'ftest',
            'operatorType': 5,
            'quoteType': 1,
            'cusLoadAmount': '',
            'cusUnloadAmount': '',
            'cusMvInStorageAmount': ''
        }
        r = requests.post(url, data)
        return r.json()


class ApiAutoQuery(ApiUa):
    """意向单系统接口"""

    # 获取cookies
    def get_cookies(self):
        request_id = self.ua_generate_check_code()
        for password in ['Fy@123456789', 'Ab@123456789']:
            cookies_ua = self.ua_login('12888888888', password, request_id)
            if cookies_ua:
                break
        if not cookies_ua:
            return '管理员账号12888888888获取cookies失败，请检查数据配置'
        return cookies_ua

    # 查询线路信息
    def get_line_detail(self, cookies, line_id):
        try:
            url = self.mk_url('yxd', 'api/virtual/getLineDetail')
            print('url', url)
            data = {
                'lineId': int(line_id)
            }
            print('data', data)
            res = requests.post(url, data=data, cookies=cookies)
            print('查询线路信息', res.json())
            return res.json()
        except Exception:
            return "接口异常！"

    # 批量生成意向单
    def create_all_auto_query(self, plandate, cookies):
        try:
            url = self.mk_url('yxd', 'api/door/create?planDate={}').format(plandate)
            res = requests.get(url, cookies=cookies)
            return res.text
        except Exception:
            return "接口异常！"

    # 按线路生成意向单
    def create_bylineid_auto_query(self, lineid, plandate, cookies):
        try:
            url = self.mk_url('yxd', 'api/door/createByLineId?lineId={}&planDate={}').format(lineid, plandate)
            res = requests.get(url, cookies=cookies)
            print('按线路生成意向单', res.text)
            return res.text
        except Exception:
            return "接口异常！"

    # 意向单待确认列表
    def auto_query_list_wait(self, cookies, line_id=''):
        url = self.mk_url('yxd', 'api/virtual/conWait/list')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'planStartTime': (int(time.time()) - 3600 * 12) * 1000,
            'planEndTime': (int(time.time()) + 3600 * 96) * 1000,
            'lineId': line_id
        }
        # print(url, data)
        r = requests.post(url, data, cookies=cookies)

        page_size = r.json()['page']['pageSize']
        total_page = r.json()['page']['totalPage']
        data_again = {
            'pageIndex': total_page,
            'pageSize': page_size,
            'planStartTime': (int(time.time()) - 3600 * 12) * 1000,
            'planEndTime': (int(time.time()) + 3600 * 96) * 1000,
            'lineId': line_id
        }
        # print(url, data)
        r = requests.post(url, data_again, cookies=cookies)
        print('意向单待确认列表', r.json())
        return r.json()

    # 意向单已确认列表
    def auto_query_list_confirm(self, cookies):
        url = self.mk_url('yxd', 'api/virtual/confirmed/list')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'planStartTime': int(time.time()),
            'planEndTime': int(time.time() + 24 * 3600),
            'carLengthId': 1,
            'carModelId': 1
        }
        data.update(data)
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 意向单确认发单
    def confirm_auto_query(self, cookies, order_id):
        url = self.mk_url('yxd', 'api/virtual/confirm')
        data = {
            'ids': '[%s]' % order_id
        }
        print('data----', data)
        r = requests.post(url, data, cookies=cookies)
        print('意向单确认发单', r.json())
        return r.json()

    # 推送智能调度或一口价
    def yxd_reset_status(self, order_sn, cookies):
        url = self.mk_url('yxd', 'api/virtual/resetStatus')
        data = {
            'orderSn': order_sn
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 图灵报价推运单系统（无需等待）
    def turing_price_to_order_core_quickly(self, order_sn, turing_price=3100.00):
        url = 'http://%sproxy.fuyoukache.com/fykc-order-core/api/pipeline/quote/fykcQuote' % self.env
        data = {
            'orderSn': order_sn,
            'cusBareTransAmount': turing_price,
            'operId': 1567,
            'operName': '李琦',
            'operatorType': 5,
            'quoteType': 1,
            'cusLoadAmount': '',
            'cusUnloadAmount': '',
            'cusMvInStorageAmount': ''
        }
        r = requests.post(url, data)
        return r.json()


# 司机或车辆未完成运单异常修改卸货完成
def order_unload_for_driver_free(env, cookies_ua, driver_mobile=None, truck_num=None):
    conditions = {
        'pageSize': 100,
        'driverMobile': driver_mobile,
        'driverPlateNumber': truck_num,
        'orderStatus': '17,18'
    }
    bms = ApiBms(env)
    orders_result = bms.bms_order_list(cookies_ua, conditions)  # 查询运单列表未完成的运单
    print('未完成运单列表查询：%s' % orders_result)
    if orders_result['status']['code'] == 0:
        for order_info in orders_result['data']:
            order_sn = order_info['orderSn']
            # 运单异常修改卸货完成
            exception_result = bms.bms_order_exception(order_sn, 12, '', {}, cookies_ua)
            print('异常修改卸货完成：%s' % exception_result)
    else:
        pass

# 获取端口
def get_port(env):
    for i in dbconfig:
        if env == i[0]:
            env_port = i[1]
            break
    return env_port


if __name__ == '__main__':
    # l = ApiBms('r1').driver_info_get('17800000005')
    # print(l['token'])

    # r_driver_login = driver_login('r1', '17800000005', '1123')
    # print(r_driver_login)

    re = ApiBms('r1').driver_info_get('16011111111')
    print(re)
    #
    # l = ApiBms('t4').admin_info_get(admin_mobile)
    # print(l['cookies_ua'])
