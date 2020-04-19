# coding:utf-8
from .base import *


class ApiTuring(Base):
    """图灵系统接口"""
    # 报价管理-报价接口
    def turing_offer_price(self, order_sn, bidding_price, cookies_turing):
        url = self.mk_url('turing', 'api/order/biddingOrder.do')
        data = {
            'orderSn': order_sn,
            'biddingPrice': bidding_price,
            'cusLoadAmount': 0,
            'cusUnloadAmount': 0,
            'cusStorageAmount': 0,
        }
        r = requests.post(url, data, cookies=cookies_turing)
        return r.json()

    # 吸货报价管理-基础价格查询接口
    def turing_customer_price_list(self, data_select={}, cookies_turing=None):
        url = self.mk_url('turing', 'api/district/queryDistrictBasePriceList')
        data = {
            'pageIndex': 1,
            'pageSize': 200,
            'carModelId': 1,
            'carLengthId': 8,
            'status': 1
        }
        data.update(data_select)
        r = requests.post(url, data, cookies=cookies_turing)
        return r.json()
    def turing_addOrUpdateShortRentPrice(self,start_provinceid,start_cityid,start_provincename,start_cityname,cookies):
        url = self.mk_url('turing', 'api/rent/addOrUpdateShortRentPrice')
        data = {
            "name": "自动化新建"+str(random.randint(1,1000)),
            "carLengthId": 8,
            "carLengthName": 9.6,
            "carModelId": 1,
            "carModelName": "厢式车",
            "basePrice": 1000,
            "shortRentInfoListStr": str(
                [{"startValue": 0, "endValue": 10, "rule": 2, "param": 5},
                 {"startValue": 10, "endValue": 20, "rule": 2, "param": 5},
                 {"startValue": 20, "endValue": 999999, "rule": 2, "param": 5}]
            ),
            "extraPrice": 1000,
            "regionConfListStr": str([{"parentType": 4, "provinceId": start_provinceid,
                                       "provinceName": start_provincename,
                                       "cityId":start_cityid,
                                       "cityName": start_cityname}]),
            "overtimePrice": 100,
            "status": 1
        }
        r = requests.post(url, data, cookies=cookies)
        # print(r.json())
        return r.json()

