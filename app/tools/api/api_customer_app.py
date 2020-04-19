# coding:utf-8
from .api_xcusotmer_app import *


class ApiCustomerApp(Base):
    """货主APP接口"""

    # 生成询价信息
    def make_quote_info(self, points=2, goodsname='技术测试', goodsweight=2.5, goodscubage=None, carlengthid=1, carmodelid=4,
                        needreceipt=1, goodsloaddate=True, plantranstime=None, comments=None, tags=None,
                        region_list=None):
        data_dic = {}
        if goodsname is not None:
            data_dic['goodsName'] = goodsname
        if goodsweight is not None:
            data_dic['goodsWeight'] = goodsweight
        if goodscubage is not None:
            data_dic['goodsCubage'] = goodscubage
        if carlengthid is not None:
            data_dic['carLengthId'] = carlengthid
        if carmodelid is not None:
            data_dic['carModelId'] = carmodelid
        if needreceipt is not None:
            data_dic['needReceipt'] = needreceipt
        if goodsloaddate is not None:
            if goodsloaddate is True:
                data_dic['goodsLoadDate'] = (int(time.time()) + 3600 * random.randrange(12, 24)) * 1000
            else:
                data_dic['goodsLoadDate'] = goodsloaddate
        if plantranstime is not None:
            data_dic['planTransTime'] = plantranstime
        if comments is not None:
            data_dic['comments'] = comments
        if tags is not None:
            data_dic['tags'] = tags
        # if region_list is None:
        #     region_list = []
        #     if points:
        #         if points >= 5:
        #             region_count = 5
        #         elif points >= 2:
        #             region_count = points
        #         else:
        #             return False
        #         for j in range(region_count):
        #             address_info = address_search(addresses[j])
        #             temp_region = {
        #                 'address': '技术测试%s' % j,
        #                 'provinceId': address_info['province_id'],
        #                 'provinceName': address_info['province_name'],
        #                 'cityId': address_info['city_id'],
        #                 'cityName': address_info['city_name'],
        #                 'districtId': address_info['district_id'],
        #                 'districtName': address_info['district_name'],
        #                 'latitude': address_info['latitude'],
        #                 'longitude': address_info['longitude'],
        #                 'planInTime': '',
        #                 'planOutTime': '',
        #                 'sort': j,
        #                 'contactId': '',
        #                 'contactName': '',
        #                 'contactMobile': '',
        #             }
        #             region_list.append(temp_region)
        # print('地址信息: %s' % region_list)
        data_dic['stopPoints'] = json.dumps(region_list, ensure_ascii=False)
        return data_dic

    # 确认询价
    def customer_app_quote_confirm(self, data_dic=None, token=None):
        url = self.mk_url('xcustomer', 'api/app/quote/confirm')
        if data_dic is None:
            data_dic = {}
        data_dic['token'] = token
        data_dic.update(data_dic)
        r = requests.post(url, data=data_dic)
        return r.json()

    # 确认下单页面信息
    def customer_app_confirmorder_info(self, ordersn=None, token=None):
        url = self.mk_url('xcustomer', 'api/app/quote/confirmOrderInfo')
        data_dic = {
            'token': token,
            'orderSn': ordersn
        }
        data_dic.update(data_mobile)
        r = requests.post(url, data=data_dic)
        return r.json()

    # 确认下单
    def customer_app_order_confirm(self, token=None, ordersn=None, stoppoints=True, goodsworth=10000):
        url = self.mk_url('xcustomer', 'api/app/quote/confirmOrder')
        data_dic = {
            'token': token,
            'orderSn': ordersn,
            # 'goodsWorth': goodsworth
        }
        if stoppoints is not None:
            time.sleep(0.2)
            d = self.customer_app_confirmorder_info(ordersn=ordersn, token=token)
            print(d)
            stoppointlist = d['data'][0]['stopPointList']
            keys = ['id', 'contactName', 'contactMobile']
            contact = {
                'contactName': '测试',
                'contactMobile': '18000000001'
            }
            stoppoints = \
                list({key: value for key, value in stoppoint.items() if key in keys} for stoppoint in stoppointlist)
            stoppoints2 = []
            for stoppoint in stoppoints:
                stoppoint.update(contact)
                stoppoints2.append(stoppoint)
            data_dic['stopPoints'] = json.dumps(stoppoints2, ensure_ascii=False)
            # print('%s' % data_dic)
        data_dic.update(data_mobile)
        print(url)
        r = requests.post(url, data=data_dic)
        return r.json()

    # 运单产生压车费
    def time_out_money(self, env, order_sn, detain_time, operator_id=1, operator_name='操作人', operator_type=1):
        url = "http://%sproxy.fuyoukache.com/fykc-order-core/api/custom/foryou/detainTime" % env
        data = {
           'orderSn': order_sn,
           'operatorId': operator_id,
           'operatorName': operator_name,
           'operatorType': operator_type,
           'detainTime': detain_time
        }
        print(url)
        r = requests.post(url, data)
        return r.json()

    # 发放优惠卷
    def customer_grant_coupon(self, env, mobile, cookies_bms, number=1, coupon_id=113):
        url = "http://%soms.fuyoukache.com/service/fykc-oms-service/api/coupon/queryBeforGrantCoupon" % env
        data = {
           'id': coupon_id,
           'mobiles': mobile,
           'token': cookies_bms,
           'everyoneNumber': number
        }
        print(url)
        r = requests.post(url, data, cookies=cookies_bms)
        return r.json()