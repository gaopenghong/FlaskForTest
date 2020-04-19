import requests
from  app.tools.api.conf import get_config_section
from .base import *

amap_keys = get_config_section('amap')


class Amap(Base):

    def amap_input_tips(self, address):
        url = 'https://restapi.amap.com/v3/assistant/inputtips'

        def amap_1(amap_key):
            data = {
                'key': amap_key,
                'keywords': address
            }
            r = requests.get(url, data)
            return r.json()
        for index in amap_keys:
            r_1 = amap_1(index[1])
            if r_1['status'] == '1':
                return r_1

    # 逆地理编码-经纬度查找地址
    def amap_input_regeo(self, lng, lat):
        url = 'https://restapi.amap.com/v3/geocode/regeo'

        def amap_1(amap_key):
            data = {
                'key': amap_key,
                'location': str(lng) + ',' + str(lat),
            }
            r = requests.get(url, data)
            return r.json()

        for index in amap_keys:
            r_1 = amap_1(index[1])
            if r_1['status'] == '1':
                return r_1
