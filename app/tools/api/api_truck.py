import os

from app.tools.api.base import *


class AddDrivers(Base):
    #  添加司机
    def add_driver(self, driver_mobile, cookies):
        driver_info_list = self.driver_info_search()
        i = random.randint(0, 676)
        driver_info = driver_info_list[i]
        url = self.mk_url('user', 'api/crm/driver/create')
        driver_plate = driver_info['plateNumber']
        driver_name = driver_info['name']
        driver_id_card_number = driver_info['idCardNumber']
        driver_id_card_address = driver_info['idCardAddress']
        data_truck = [
            {
                'plateNumber': driver_plate,
                'carLengthId': 8,
                'carModelId': 1,
                'carWidth': 3,
                'carHeigh': 3,
                'carBrand': '',
                'carType': 1,
                'carFixedLoad': 50000,
                'carWeight': 60000,
                'carAxis': 4,
                'onroadTime': '2019-07-03',
                'imgLoadLicense': 'https://public.fuyoukache.com/e869d8dc-9465-4e22-9eb7-c5c3d24d3d37---3.jpg',
                'imgInsurance': 'https: /public.fuyoukache.com/aaa832b1-b676-4d8e-a0cf-4fc4d6f474b9---3.jpg',
                'imgCarLicense': 'https://public.fuyoukache.com/4df2b909-90e8-41f3-bb33-6aff6a9a6d7e---3.jpg',
                'imgDriverTruckGroup': 'https://public.fuyoukache.com/1b6e4042-a611-4bca-8d61-f86ef6b17d05---a11.png',
                'isDefault': 1,
                'isBind': 0
            }
        ]
        data = {
            'mobile': driver_mobile,
            'name': driver_name,
            'idCardNumber': driver_id_card_number,
            'idCardAddress': driver_id_card_address,
            'regSrcType': 1,
            'imgIdCardFront': 'https://public.fuyoukache.com/29f9237b-8f53-4cb9-84a7-388abb9b11aa---b2.jpg',
            'imgIdCardBack': 'https://public.fuyoukache.com/88659bf4-be5e-4e15-8012-c5ad758cdaa9---3.jpg',
            'imgDriveLicense': 'https://public.fuyoukache.com/4fbf8820-f743-44f7-b818-00a46b4443d8---4.jpg',
            'commonLineStr': '',
            'truckInfoStr': json.dumps(data_truck)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    #  添加专车前添加好运司机司机
    def add_drivers(self, driver_mobile, driver_plate, driver_name, driver_id_card_number, driver_id_card_address,
                    cookies):
        url = self.mk_url('user', 'api/crm/driver/create')
        data_truck = [
            {
                'plateNumber': driver_plate,
                'carLengthId': 8,
                'carModelId': 1,
                'carWidth': 3,
                'carHeigh': 3,
                'carBrand': '',
                'carType': 1,
                'carFixedLoad': 50000,
                'carWeight': 60000,
                'carAxis': 4,
                'onroadTime': '2019-07-03',
                'imgLoadLicense': 'https://public.fuyoukache.com/e869d8dc-9465-4e22-9eb7-c5c3d24d3d37---3.jpg',
                'imgInsurance': 'https: /public.fuyoukache.com/aaa832b1-b676-4d8e-a0cf-4fc4d6f474b9---3.jpg',
                'imgCarLicense': 'https://public.fuyoukache.com/4df2b909-90e8-41f3-bb33-6aff6a9a6d7e---3.jpg',
                'imgDriverTruckGroup': 'https://public.fuyoukache.com/1b6e4042-a611-4bca-8d61-f86ef6b17d05---a11.png',
                'isDefault': 1,
                'isBind': 0
            }
        ]
        data = {
            'mobile': driver_mobile,
            'name': driver_name,
            'idCardNumber': driver_id_card_number,
            'idCardAddress': driver_id_card_address,
            'regSrcType': 1,
            'imgIdCardFront': 'https://public.fuyoukache.com/29f9237b-8f53-4cb9-84a7-388abb9b11aa---b2.jpg',
            'imgIdCardBack': 'https://public.fuyoukache.com/88659bf4-be5e-4e15-8012-c5ad758cdaa9---3.jpg',
            'imgDriveLicense': 'https://public.fuyoukache.com/4fbf8820-f743-44f7-b818-00a46b4443d8---4.jpg',
            'commonLineStr': '',
            'truckInfoStr': json.dumps(data_truck)
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    #   通过车牌获取司机
    def get_driver_by_plate(self, driver_plate, cookies_ua):
        url = self.mk_url('truckfy', 'api/truck/getByPlate')
        data = {
            'plateNumber': driver_plate
        }
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()

    #   配置专车
    def driver_truck_add(self, driver_id, plate_number, name, mobile, cookies_ua):
        url = self.mk_url('truckfy', 'api/truck/foryou/add')
        data = {
            'plateNumber': plate_number,
            'companyName': '湖北福运现代物流有限公司',
            'contractId': 50,
            'truckType': 1,
            'managerId': 1657,
            'managerName': '东东自动化',
            'managerMobile': '14888888888',
            'autoDispatch': 1,
            'relationDriverId': driver_id,
            'relationDriverName': name,
            'relationDriverMobile': mobile,
            'startTimeLong': '1562083200000',
            'endTimeLong': '1751472000000',
            'bankCardNumber': '6225880150027531',
            'bankAccount': '李东东',
            'payCompanyId': 0,
            'dispatchType': 1,
            'truckTeam': 0,
            'workTimeType': 1
        }
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()

    #   查询司机信息
    def driver_info_search(self):
        file_name = os.path.join(os.path.dirname(__file__), '../data/truck.txt')
        fp = open(file_name, 'r+', encoding='utf-8')
        lines = fp.readlines()
        driver_info_list = []
        for line in lines:
            driver_info = line.replace('\n', '')
            driver_info_split = driver_info.split('|')
            # driver_info_split.pop(-1)
            driver_info_key_list = ['plateNumber', 'name', 'mobile', 'idCardNumber', 'idCardAddress']
            driver_info_dict = dict(zip(driver_info_key_list, driver_info_split))
            driver_info_list.append(driver_info_dict)

        fp.close()
        return driver_info_list

    def truck_createShortRentConfig(self,start_provinceid,start_cityid,end_provinceid,start_provincename,start_cityname,end_provincename,cookies):
        import  datetime
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))+" 00:00:00"
        url = self.mk_url('dd', 'api/shortRent/createShortRentConfig')
        shortRentConfig={
         "requiredDate": tomorrow,
         "number": "100",
         "startCityId": int(start_cityid),
         "startCityName": start_cityname,
         "startProvinceId": int(start_provinceid),
         "startProvinceName": start_provincename,
         "endProvinces": [{"endProvinceId": int(end_provinceid),
                           "endProvinceName": end_provincename}],
         "carLengths": [{"carLengthId": 8, "carLengthName": 9.6}],
         "carModels": [{"carModelId": 1, "carModelName": "厢式车"}]
          }
        data = {
            "shortRentConfig": json.dumps(shortRentConfig)
        }
        r = requests.post(url, data, cookies=cookies)
        res=r.json()
        if  res["success"]==False:
            return  res["status"]["desc"]
        url_1 = self.mk_url('fuwu', 'api/src/queryCarInfoRelation')
        r1 = requests.post(url_1, cookies=cookies)
        re1=r1.json()
        if re1["success"] == False:
            return re1["status"]["desc"]
        else:
            print(re1["status"]["desc"])
        url_2 = self.mk_url('dd', 'api/src/getAllRegionTree.do')
        r2 = requests.get(url_2, cookies=cookies)
        re2=r2.json()
        if re2["success"] == False:
            return re2["status"]["desc"]
        else:
            print(re2["status"]["desc"])
        url_3=self.mk_url('dd', 'api/shortRent/queryShortRentConfig')
        r3 = requests.post(url_3, cookies=cookies)
        re3=r3.json()
        if  re3["success"] == False:
           return re3["status"]["desc"]
        else:
            print(re3["status"]["desc"])
        return res

    def truck_pushDriver(self):
        """推送标的"""
        url="http://t4proxy.fuyoukache.com/fykc-truck-scheduler/api/internal/shortRent/pushDriver"
        print(url)
        r = requests.get(url)
        print(r.json())
        return r.json()

    #   新增挂箱
    def truck_add_trailer(self, trailer_number, cookies_bg, truck_number=None):
        url = self.mk_url('truckfy', 'api/trailer/add')
        data = {
            'trailerNumber': trailer_number,
            'truckNumber': truck_number
        }
        if truck_number is not None:
            data['truckNumber'] = truck_number
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()

    #   用户系统新增挂箱
    def user_add_trailer(self, cookies_bg, plate):
        url = self.mk_url('user', 'api/crm/trailer/addOrUpdate')
        data = {
            'plateNumber': plate,
            'imgLoadLicense': 'https://public.fuyoukache.com/99eb14ad-416a-44fd-b5f8-'
                              '2ecc0f9f464e---a168r070515551874.jpg',
            'imgCarLicense': 'https://public.fuyoukache.com/fa528cc5-cdae-48ab-9b1e-6479de9ee24c---09292400i0tagswcp5'
                             'ovdt.jpg'
        }
        r = requests.post(url, data, cookies=cookies_bg)
        return r.json()
