# coding:utf-8
from app.tools.api.api_agent import ApiAgent
from app.tools.api.common import get_strf_time
from app.util.ssh_conf import remote_database
from .base import *


# 查询用户信息
class ApiCrm(Base):
    """用户中心"""

    def crm_admin_info(self, cookies):
        url = self.mk_url('user', 'api/u/com/getUserInfo.do')
        r = requests.get(url, cookies=cookies)
        return r.json()

    def crm_driver_drawings(self, driverId, cookies):
        url = self.mk_url('user', 'api/crm/driver/whiteList/add')
        data = {
            'driverId': driverId
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 线路列表
    def crm_customer_lineroute_selectlist(self, jsonstr_test={}, cookie=None, broker_mobile=''):
        url = self.mk_url('user', 'api/crm/customer/lineRoute/routeList')
        jsonstr = {
            'areaId': '',
            'parentCompanyName': '',
            'companyName': '',
            'businessId': '',
            'businessCode': '',
            'startProvinceId': '',
            'startCityId': '',
            'startDistrictId': '',
            'endProvinceId': '',
            'endCityId': '',
            'endDistrictId': '',
            'carLengthId': '',
            'carModelId': '',
            'id': '',
            'matchPower': '',
            'brokerName': '',
            'brokerMobile': broker_mobile,
            'matchAddress': '',
            'routeType': '',
            'carRequire': '',
            'isIntelligentScheduler': '',
            'cusPriceType': '',
            'frequencyType': ''
        }
        jsonstr.update(jsonstr_test)
        data = {
            'jsonStr': json.dumps(jsonstr, ensure_ascii=False),
            'pageIndex': 1,
            'pageSize': 30
        }
        r = requests.post(url, data=data, cookies=cookie)
        return r.json()

    # 根据ID查询子公司详情
    def customer_internal_subcompany_detail(self, subcompany_id):
        url = self.mk_url('xcustomer', 'api/internal/customer/company/subCompanyDetail')
        data = {
            'companyId': subcompany_id
        }
        r = requests.post(url, data=data)
        return r.json()

    # 发货员信息列表
    def crm_customer_customerlist(self, parentid=None, companyid=None, cookie=None):
        url = self.mk_url('user', 'api/crm/customer/user/customerList')
        data = {
            'parentCompId': parentid,
            'companyId': companyid,
            'pageSize': 100,
            'pageIndex': 1
        }
        r = requests.post(url, data=data, cookies=cookie)
        return r.json()

    # 发货员管理列表
    def crm_customer_customermanagerlist(self, areaid=None, parentcompanyname=None, companyname=None, name=None,
                                         mobile=None, startcreatetime=None, endcreatetime=None, inquiryflag=None,
                                         status=None, cookie=None):
        url = self.mk_url('user', 'api/crm/customer/user/customerManagerList')
        data = {
            'pageSize': 100,
            'pageIndex': 1,
            'areaId': areaid,
            'parentCompName': parentcompanyname,
            'companyName': companyname,
            'name': name,
            'mobile': mobile,
            'startCreateTime': startcreatetime,
            'endCreateTime': endcreatetime,
            'inquiryFlag': inquiryflag,
            'status': status
        }
        r = requests.post(url, data=data, cookies=cookie)
        return r.json()

    # 发货员详情
    def crm_customer_customerdetail(self, customerid=None, relationid=None, cookie=None):
        url = self.mk_url('user', 'api/crm/customer/user/customerDetail')

        data = {
            'customerId': customerid,
            'relationId': relationid
        }

        r = requests.post(url, data=data, cookies=cookie)

        return r.json()

    # 经纪人列表
    def agent_crm_select_list(self, page_index=1, page_size=30, company_code='', company_name='', name='',
                              company_status='',
                              broker_code='', broker_mobile='', broker_name='', transport_type='', belong_area_id='',
                              admin_id='',
                              status='', invoice_gualification='',
                              cookies_service=''):
        url = self.mk_url('user', 'api/crm/broker/selectList')
        data = {
            'pageIndex': page_index,
            'pageSize': page_size,
            'companyCode': company_code,
            'companyName': company_name,
            'legalPerson(name)': name,
            'companyStatus': company_status,
            'brokerCode': broker_code,
            'brokerMobile': broker_mobile,
            'brokerName': broker_name,
            'transportType': transport_type,
            'belongAreaId': belong_area_id,
            'adminId': admin_id,
            'status': status,
            'invoiceGualification': invoice_gualification
        }
        r = requests.post(url, data, cookies=cookies_service)
        return r.json()

    # 根据发货员手机号获取其公司和母公司名称
    def crm_get_customer_info(self, mobile, cookies_ua):
        r = self.crm_customer_customermanagerlist(mobile=mobile, inquiryflag=1, status=1, cookie=cookies_ua)
        company_name = r['data'][0]['relation']['companyName']
        parent_comp_name = r['data'][0]['relation']['parentCompName']
        return company_name, parent_comp_name

    # 根据公司名称查询可用的项目货合同
    def crm_get_business_code(self, company_name, cookies_ua):
        url = self.mk_url('user', 'api/crm/customer/business/businessList')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'companyName': company_name,
            'businessType': 3,
            'valid': 2,
            'status': 1
        }

        r = requests.post(url, data=data, cookies=cookies_ua)
        business_code = r.json()['data'][0]['businessCode']
        business_id = r.json()['data'][0]['id']
        company_id = r.json()['data'][0]['companyId']
        return company_id, business_code, business_id

    # 拼接始发地、目的地的信息
    def crm_make_line_info(self, line_info_list):
        project_line_info = {}
        stop_point_list = []
        for i in range(len(line_info_list)):
            if i == 0:
                for info in line_info_list[0].keys():
                    if '_' in info:
                        line_key = info.split("_")[0].capitalize() + info.split("_")[1].capitalize()
                    else:
                        line_key = info.capitalize()
                    project_line_info['start' + line_key] = line_info_list[0][info]
            elif i == len(line_info_list) - 1:
                for info in line_info_list[i].keys():
                    if '_' in info:
                        line_key = info.split("_")[0].capitalize() + info.split("_")[1].capitalize()
                    else:
                        line_key = info.capitalize()
                    project_line_info['end' + line_key] = line_info_list[i][info]
            else:
                stop_point = {}
                for info in line_info_list[i].keys():
                    if '_' in info:
                        line_key = info.split("_")[0] + info.split("_")[1].capitalize()
                    stop_point[line_key] = line_info_list[i][info]
                stop_point_list.append(stop_point)
        if stop_point_list:
            for i in range(len(stop_point_list)):
                stop_point_list[i]['plannedArrivalTime'] = 128460 + i * 100000
                stop_point_list[i]['plannedLeaveTime'] = 132060 + i * 100000
        return project_line_info, stop_point_list

    # 搜索项目线路
    def crm_select_route_line(self, project_line_info, company_name, cookies_ua):
        json_str = {"areaId": "", "companyName": company_name,
                    "carLengthId": "8", "carModelId": "1"}
        for i in ["startProvinceId", "startProvinceName", "startCityId", "startCityName", "startDistrictId",
                  "startDistrictName", "endProvinceId", "endProvinceName", "endCityId", "endCityName", "endDistrictId",
                  "endDistrictName"]:
            json_str[i] = project_line_info[i]
        json_str['province'] = [project_line_info['startProvinceId'], project_line_info['startCityId'],
                                project_line_info['startDistrictId']]
        json_str['endprovince'] = [project_line_info['endProvinceId'], project_line_info['endCityId'],
                                   project_line_info['endDistrictId']]

        url = self.mk_url('user', 'api/crm/customer/lineRoute/routeList')
        data = {
            'jsonStr': str(json_str),
            'pageIndex': 1,
            'pageSize': 30
        }
        r = requests.post(url, data=data, cookies=cookies_ua)
        return r

    # 创建项目线路
    def crm_create_project_line(self, line_info_list, customer_mobile, admin_id, admin_name, cookies_ua):
        company_name, parent_comp_name = self.crm_get_customer_info(customer_mobile, cookies_ua)
        company_id, business_code, business_id = self.crm_get_business_code(company_name, cookies_ua)
        make_line_info, stop_point_list = self.crm_make_line_info(line_info_list)

        r = self.crm_select_route_line(make_line_info, company_name, cookies_ua)
        if r.json()['status']['code'] == 0:
            line_route_id = r.json()['data'][0]['id']
        else:
            line_route = {"status": 1, "statusEnum": "NORMAL", "statusDesc": "正常",
                          "businessId": business_id, "businessCode": business_code, "businessName": "【G】项目货合同",
                          "companyName": company_name, "companyId": company_id,
                          "carLengthId": "8", "carLength": "9.6", "carModelId": "1", "carModel": "厢式车",
                          "cusAmountType": 1, "cusAmonutTypeEnum": "YES", "cusAmountDesc": "是",
                          "updateTime": int(round(time.time() * 1000)), "createTime": int(round(time.time() * 1000)),
                          "frequencyType": 2, "frequencyTypeEnum": "COLLECTPRICE", "frequencyTypeName": "集采价",
                          "routeTag": "1", "routeTagName": "常年线",
                          "generateVirOrder": 2, "generateVirorderEnum": "CLOSE", "generateVirOrderName": "关",
                          "carRequire": "0", "carRequireEnum": "NOTHING", "carRequireName": "无",
                          "isIntelligentScheduler": "0", "intelligentSchedulerEnum": "FALSE",
                          "isIntelligentSchedulerName": "否",
                          "cusPriceType": "1", "cusPriceTypeEnum": "CAR", "cusPriceTypeName": "按车计价", "routeType": 1,
                          "routeTypeEnum": "UNILATERAL",
                          "routeTypeName": "单边", "frequency": "100",
                          "plannedTransitTime": 496800, "plannedArrivalStartTime": 42060,
                          "plannedLeaveStartTime": 45660,
                          "plannedArrivalEndTime": 560460,
                          "spareCarModelId": "1", "spareCarModel": "厢式车", "lineRoutePrice": 1000,
                          "source": 2, "spareCarLengthId": "8", "spareCarLength": "9.6",
                          "parentCompanyName": parent_comp_name,
                          "currentCarNums": 1, "matchAddress": 3, "stopPointCount": 0,
                          "createTimeExport": "2019-11-05 11:42:31", "operId": admin_id, "operName": admin_name,
                          "stopPointList": stop_point_list,
                          "distance": "", "duration": ""}
            line_route.update(make_line_info)
            url = self.mk_url('user', 'api/crm/customer/lineRoute/createOrUpdateLineRoute')
            data = {
                'lineRoute': str([line_route]),
                'source': 2
            }
            r = requests.post(url, data=data,
                              cookies=cookies_ua)
            line_route_id = r.json()['property']['lineId']
        return line_route_id

    # 筛选线路
    def agent_crm_get_line(self, page_index=1, page_size=30, start_province_id='', start_city_id='',
                           start_district_id='',
                           end_province_id='', end_city_id='', end_district_id='', transport_type='', broker_id='',
                           cookies=''):
        url = self.mk_url('user', 'api/crm/broker/line/brokerLineList')
        data = {
            'pageIndex': page_index,
            'pageSize': page_size,
            'jsonData': str(
                {"startProvinceId": start_province_id, "startCityId": start_city_id,
                 "startDistrictId": start_district_id,
                 "endProvinceId": end_province_id,
                 "endCityId": end_city_id, "endDistrictId": end_district_id, "transportType": transport_type,
                 'brokerId': broker_id})
        }
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()

    # 拼接福佑线路的基础信息
    def crm_make_fy_line_info(self, status, source_type, line_type, has_contract, contract_code, car_length_id,
                              car_length, car_model_id, car_model, cookies_service,
                              line_address, line_route_id='', line_info_list=[]):
        stop_point_list = []
        fy_line_info = []
        base_line_info = {"status": status, "sourceType": source_type, "lineType": line_type,
                          "hasContract": has_contract, "contractCode": contract_code}
        # 根据项目货的线路id，获取线路信息
        if line_route_id != '':
            data = {
                'id': line_route_id,
                'source': 2
            }
            url = self.mk_url('user', 'api/crm/customer/lineRoute/routeDetail')
            r = requests.post(url, data=data, cookies=cookies_service)
            # 判断线路id是否正确
            if 'data' not in r.json():
                return "项目线路信息" + str(r.json()['status']['desc']) + ",请确认项目线路id是否正确"
            base_line_info['carLengthId'] = r.json()['data'][0]['carLengthId']
            base_line_info['carLength'] = r.json()['data'][0]['carLength']
            base_line_info['carModelId'] = r.json()['data'][0]['carModelId']
            base_line_info['carModel'] = r.json()['data'][0]['carModel']
            base_line_info['line_type'] = len(r.json()['data'])
            for i in range(len(r.json()['data'])):
                line_address_info = dict()
                line_address_info['startProvinceId'] = r.json()['data'][i]['startProvinceId']
                line_address_info['startCityId'] = r.json()['data'][i]['startCityId']
                line_address_info['startDistrictId'] = r.json()['data'][i]['startDistrictId']
                line_address_info['startProvinceName'] = r.json()['data'][i]['startProvinceName']
                line_address_info['startCityName'] = r.json()['data'][i]['startCityName']
                line_address_info['startDistrictName'] = r.json()['data'][i]['startDistrictName']
                line_address_info['endProvinceId'] = r.json()['data'][i]['endProvinceId']
                line_address_info['endCityId'] = r.json()['data'][i]['endCityId']
                line_address_info['endDistrictId'] = r.json()['data'][i]['endDistrictId']
                line_address_info['endProvinceName'] = r.json()['data'][i]['endProvinceName']
                line_address_info['endCityName'] = r.json()['data'][i]['endCityName']
                line_address_info['endDistrictName'] = r.json()['data'][i]['endDistrictName']
                line_address.append(line_address_info)
                # 判断经停点
                for j in range(r.json()['data'][i]['stopPointCount']):
                    stop_point_list.append(
                        {"provinceId": r.json()['data'][i]['stopPointList'][j]['provinceId'],
                         "cityId": r.json()['data'][i]['stopPointList'][j]['cityId'],
                         "districtId": r.json()['data'][i]['stopPointList'][j]['districtId'],
                         "provinceName": r.json()['data'][i]['stopPointList'][j]['provinceName'],
                         "cityName": r.json()['data'][i]['stopPointList'][j]['cityName'],
                         "districtName": r.json()['data'][i]['stopPointList'][j]['districtName']})
                base_line_info["stopPointList"] = stop_point_list
                fy_line_info.append(dict(base_line_info, **line_address[i]))
        # 判断是否自己传入线路信息
        elif line_info_list:
            line_address_info, stop_point_list = self.crm_make_line_info(line_info_list)
            base_line_info['carLengthId'] = car_length_id
            base_line_info['carLength'] = car_length
            base_line_info['carModelId'] = car_model_id
            base_line_info['carModel'] = car_model
            base_line_info["stopPointList"] = stop_point_list
            fy_line_info.append(dict(base_line_info, **line_address_info))
        return fy_line_info

    # 创建福佑线路
    def agent_crm_create_broker_line(self, cookies_service,
                                     broker_mobile_1='16499999999',
                                     broker_mobile_2='12499999999',
                                     own_broker_mobile_1='16477777777',
                                     own_broker_mobile_2='12477777777', status=1, source_type=2,
                                     line_type=1, has_contract=0, contract_code="",
                                     start_time=get_strf_time(strf='%Y-%m-%d'),
                                     end_time=get_strf_time(days=30, strf='%Y-%m-%d'), transport_type='',
                                     car_length_id=8,
                                     car_length="9.6", car_model_id=1, car_model="厢式车", base_times=7,
                                     base_times_day=7, base_times_price=1000,
                                     ensure_times_off=7, ensure_times_busy=7, bottom_times=99, bottom_times_price=2000,
                                     next_price=2000, line_route_id='', recruit_limit_num=99, remark="测试",
                                     ):
        """
         新建修改福佑线路/根据项目货线路编码创建福佑线路
         transport_type=1:专车，2企业运力，3固定司机
         line_type=1:单边 2：双边
         :return 返回线路信息
        """
        # 拼接线路信息
        line_address = []
        line_info_list = []
        fy_line_info = self.crm_make_fy_line_info(status, source_type, line_type, has_contract, contract_code,
                                                  car_length_id,
                                                  car_length, car_model_id, car_model, cookies_service,
                                                  line_address=line_address,
                                                  line_route_id=line_route_id, line_info_list=line_info_list,
                                                  )
        # 遇到异常直接return
        if 'carLengthId' not in fy_line_info[0]:
            return fy_line_info
        # 单边
        if line_type == 1:
            broker_info = {}
            # 运力是固定司机还是企业运力？
            if transport_type == '1':
                r_broker = self.agent_crm_select_list(1, 30, broker_mobile=own_broker_mobile_1,
                                                      cookies_service=cookies_service)
                print(r_broker)
                broker_info['brokerMobile'] = own_broker_mobile_1
                broker_info['brokerId'] = r_broker['data'][0]['id']
                broker_info['brokerName'] = r_broker['data'][0]['brokerName']
                fy_line_info[0]['transportType'] = transport_type
                fy_line_info[0]["baseTimes"] = base_times
                fy_line_info[0].update(broker_info)
            elif transport_type == '2':
                r_broker = self.agent_crm_select_list(broker_mobile=broker_mobile_1, cookies_service=cookies_service,
                                                      )
                print(r_broker)
                fy_line_info[0]['transportType'] = transport_type
                fy_line_info[0]["startTime"] = start_time
                fy_line_info[0]["endTime"] = end_time
                fy_line_info[0]["baseTimes"] = base_times
                fy_line_info[0]["baseTimesDay"] = base_times_day
                fy_line_info[0]['baseTimesPrice'] = base_times_price
                fy_line_info[0]["ensureTimesOff"] = ensure_times_off
                fy_line_info[0]["ensureTimesBusy"] = ensure_times_busy
                fy_line_info[0]["bottomTimes"] = bottom_times
                fy_line_info[0]["bottomTimesPrice"] = bottom_times_price

                broker_info['brokerMobile'] = broker_mobile_1
                broker_info['companyId'] = r_broker['data'][0]['companyId']
                broker_info['brokerId'] = r_broker['data'][0]['id']
                broker_info['brokerName'] = r_broker['data'][0]['brokerName']
                broker_info['companyName'] = r_broker['data'][0]['companyName']
                print(fy_line_info[0])
                fy_line_info[0].update(broker_info)
            elif transport_type == '3':
                fy_line_info[0]['transportType'] = transport_type
                fy_line_info[0]["startTime"] = start_time
                fy_line_info[0]["endTime"] = end_time
                fy_line_info[0]['baseTimesPrice'] = base_times_price
                fy_line_info[0]['nextPrice'] = next_price
                fy_line_info[0]["recruitLimitNum"] = recruit_limit_num
                fy_line_info[0]["remark"] = remark

            json_data = eval('[' + str(fy_line_info[0]) + ']')
            data = {"jsonData": str(json_data)}

        # 双边
        elif line_type == 2:
            fy_line_info[0]['lineType'] = 2
            fy_line_info[1]['lineType'] = 2
            if len(fy_line_info) == 1:
                fy_line_info.append(fy_line_info[0])
            # 运力是专车还是企业运力？
            if transport_type == '1':
                line_index = 0
                for broker_mobile in [own_broker_mobile_1, own_broker_mobile_2]:
                    broker_info = {}
                    r_broker = self.agent_crm_select_list(1, 30, broker_mobile=broker_mobile,
                                                          cookies_service=cookies_service)
                    print(r_broker)
                    broker_info['brokerMobile'] = broker_mobile
                    broker_info['brokerId'] = r_broker['data'][0]['id']
                    broker_info['brokerName'] = r_broker['data'][0]['brokerName']
                    fy_line_info[line_index]["baseTimes"] = base_times
                    fy_line_info[line_index]['transportType'] = transport_type
                    fy_line_info[line_index].update(broker_info)
                    line_index = line_index + 1
            elif transport_type == '2':
                line_index = 0
                for broker_mobile in [broker_mobile_1, broker_mobile_2]:
                    broker_info = {}
                    r_broker = self.agent_crm_select_list(1, 30, broker_mobile=broker_mobile,
                                                          cookies_service=cookies_service)
                    print(r_broker)
                    broker_info['brokerMobile'] = broker_mobile
                    broker_info['companyId'] = r_broker['data'][0]['companyId']
                    broker_info['brokerId'] = r_broker['data'][0]['id']
                    broker_info['brokerName'] = r_broker['data'][0]['brokerName']
                    broker_info['companyName'] = r_broker['data'][0]['companyName']
                    fy_line_info[line_index]['transportType'] = transport_type
                    fy_line_info[line_index]["startTime"] = start_time
                    fy_line_info[line_index]["endTime"] = end_time
                    fy_line_info[line_index]["baseTimes"] = base_times
                    fy_line_info[line_index]["baseTimesDay"] = base_times_day
                    fy_line_info[line_index]['baseTimesPrice'] = base_times_price
                    fy_line_info[line_index]["ensureTimesOff"] = ensure_times_off
                    fy_line_info[line_index]["ensureTimesBusy"] = ensure_times_busy
                    fy_line_info[line_index]["bottomTimes"] = bottom_times
                    fy_line_info[line_index]["bottomTimesPrice"] = bottom_times_price
                    fy_line_info[line_index].update(broker_info)
                    line_index = line_index + 1
                data = {"jsonData": str(fy_line_info)
                        }

        print(str(fy_line_info))
        # 搜索线路,判断是否存在
        line_r = self.agent_crm_get_line(start_province_id=fy_line_info[0]['startProvinceId'],
                                         start_city_id=fy_line_info[0]['startCityId'],
                                         start_district_id=fy_line_info[0]['startDistrictId'],
                                         end_city_id=fy_line_info[0]['endCityId'],
                                         end_province_id=fy_line_info[0]['endProvinceId'],
                                         end_district_id=fy_line_info[0]['endDistrictId'],
                                         transport_type=transport_type,
                                         cookies=cookies_service)
        # 线路已存在
        if line_r['status']['code'] == 0:
            data = {}
            if line_type == 1:
                line_id = line_r['data'][0]['id']
                fy_line_info[0]['id'] = line_id
                json_data = eval('[' + str(fy_line_info[0]) + ']')
                data = {"jsonData": str(json_data)
                        }
            elif line_type == 2:
                line_id_0 = line_r['data'][0]['id']
                line_id_1 = line_r['data'][1]['id']
                fy_line_info[0]['id'] = line_id_0
                fy_line_info[1]['id'] = line_id_1
            url = self.mk_url('user', 'api/crm/broker/line/createBrokerLine')
            requests.post(url, data=data, cookies=cookies_service)
        # 线路不存在
        elif line_r['status']['code'] == 3:
            print(data)
            url = self.mk_url('user', 'api/crm/broker/line/createBrokerLine')
            r = requests.post(url, data=data, cookies=cookies_service)
            line_r = self.agent_crm_get_line(start_province_id=fy_line_info[0]['startProvinceId'],
                                             start_city_id=fy_line_info[0]['startCityId'],
                                             start_district_id=fy_line_info[0]['startDistrictId'],
                                             end_city_id=fy_line_info[0]['endCityId'],
                                             end_province_id=fy_line_info[0]['endProvinceId'],
                                             end_district_id=fy_line_info[0]['endDistrictId'],
                                             transport_type=transport_type, cookies=cookies_service)
            print("线路信息:" + str(line_r))
            if 'data' not in line_r:
                print(r.text)
                return r.json()
            else:
                return line_r['data'][0]['id']
        return line_r['data'][0]['id']

    # 下单
    def crm_agent_delivery(self, line_info_list, customer_cookie, need_receipt=1):
        order_time = get_strf_time(days=1)
        order_time = int(time.mktime(time.strptime(order_time, "%Y-%m-%d %H:%M:%S")))
        order_time = int(round(order_time * 1000))
        for line_info in line_info_list:
            for info in list(line_info.keys()):
                if '_' in info:
                    line_key = info.split("_")[0] + info.split("_")[1].capitalize()
                else:
                    line_key = info
                line_info[line_key] = line_info[info]
                del line_info[info]
            line_info.update({"address": "丰台体育中心", "planInTime": '', "planOutTime": '', "longitude": 116.277687,
                              "latitude": 39.866858})
        json_data = {
            'goodsName': '测试',
            'goodsWeight': 100,
            'needReceipt': need_receipt,
            'goodsLoadDate': order_time,
            'carLengthId': 8,
            'carModelId': 1,
            'tags': 13,
            'stopPoints': str(line_info_list)
        }
        url = self.mk_url('hz', 'api/pc/quote/confirm')
        r = requests.post(url, data=json_data, cookies=customer_cookie)
        print("确认询价" + str(r.json()))
        order_sn = r.json()['data'][0]['orderSn']
        time.sleep(5)
        r = ApiAgent(self.env).customer_pc_order_confirm(order_sn=order_sn, cookies=customer_cookie)
        print("确认下单" + str(r))
        return order_sn

    # 企业列表
    def agent_crm_get_company_list(self, cookies_service, company_name='长安电力华中发电有限公司', status=100, page_index=1,
                                   page_size=30):
        url = self.mk_url('user', 'api/crm/company/selectCompanyList')
        data = {
            'companyName': company_name,
            'status': status,
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()

    # 获取司机信息、车辆信息
    def agent_crm_get_driver_info(self, driver_mobile, cookies):
        data = {
            'mobile': driver_mobile
        }
        url = self.mk_url('user', 'api/crm/broker/line/getDriverBaseInfoAndStatus')
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()

    # 添加运力账号
    def agent_crm_line_add_driver(self, line_id, driver_id, driver_mobile, plate_number, cookies=''):
        data = {'lineId': line_id,
                'driverId': driver_id,
                'driverMobile': driver_mobile,
                'plateNumber': plate_number}
        url = self.mk_url('user', 'api/crm/broker/line/createBrokerLineDriver')
        r = requests.post(url, data=data, cookies=cookies)
        print('添加运力账号', r.json())
        return r.json()

    # 获取固定司机线路下司机的信息
    def agent_crm_select_contract_driver(self, line_id='', cookies=''):
        data = {'id': line_id}
        url = self.mk_url('user', 'api/crm/broker/line/selectDriverContractSignList')
        r = requests.post(url, data=data, cookies=cookies)
        print('获取固定司机线路下司机的信息', r.json())
        return r.json()

    # 推送司机合同
    def agent_crm_create_driver_contract(self, fy_line_id='', current_line_driver_ids=[], cookies=''):
        data = {
            'lineId': fy_line_id,
            'currentLineDriverIds': str(current_line_driver_ids)
        }
        url = self.mk_url('user', 'api/crm/broker/line/createDriverContract')
        r = requests.post(url, data=data, cookies=cookies)
        return r.json()

    # 给司机推送合同，并签署合同
    def agent_crm_driver_contract(self, driver_mobile, fy_line_id, cookies):
        driver_info = self.agent_crm_get_driver_info(driver_mobile, cookies)
        print('driver_info-----', driver_info)
        driver_id = driver_info['data'][0]['id']
        plate_number = driver_info['data'][0]['truckInfoList'][0]['plateNumber']
        self.agent_crm_line_add_driver(fy_line_id, driver_id, driver_mobile, plate_number, cookies=cookies)
        current_line_driver_ids = []
        r_json = self.agent_crm_select_contract_driver(line_id=fy_line_id, cookies=cookies)
        for driver_index in range(len(r_json['data'])):
            print(r_json['data'][driver_index]['id'])
            if 'current' not in r_json['data'][driver_index].keys():
                current_line_driver_ids.append(r_json['data'][driver_index]['id'])
        if current_line_driver_ids:
            self.agent_crm_create_driver_contract(fy_line_id, current_line_driver_ids, cookies=cookies)
        sql = 'UPDATE line_driver_contract SET status = 3 where lineId=%s' % fy_line_id
        print(sql)
        remote_database(self.env, 'fykc_bms', sql)

    # 自动生成意向单开关
    def switch_yxd_of_line(self, switch, fy_line_id):
        switch_yxd_sql = 'UPDATE line_route SET generateVirOrder = %s where id=%s' % (switch, fy_line_id)
        print(switch_yxd_sql)
        remote_database(self.env, 'fykc_bms', switch_yxd_sql)

    # 创建合同
    def agent_crm_insert_or_update_contract(self, cookies_service, start_time, end_time, company_id, company_name,
                                            account_name='自动化测试',
                                            card_number='123456789', bank_name='北京测试银行', line_type=1,
                                            line_name='自动化测试路线',
                                            car_length_id=2, car_model_id=1, min_cube_weight=10, cost_time=10,
                                            month_numbers=10,
                                            performance_deposit=1000, first_payed_deposit=1000):
        data = {
            'startTime': start_time,
            'endTime': end_time,
            'companyId': company_id,
            'companyName': company_name,
            'accountName': account_name,
            'cardNumber': card_number,
            'bankName': bank_name,
            'lineType': line_type,
            'lineName': line_name,
            'carLengthId': car_length_id,
            'carModelId': car_model_id,
            'minCubeWeight': min_cube_weight,
            'costTime': cost_time,
            'monthNumbers': month_numbers,
            'performanceDeposit': performance_deposit,
            'firstPayedDeposit': first_payed_deposit
        }
        url = self.mk_url('user', 'api/crm/company/contract/insertOrUpdateContract')
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()

    # 查看合同工列表
    def agent_crm_select_contract_list(self, cookies_service, contract_code='', status='', company_sign_time_start='',
                                       company_sign_time_end='', broker_mobile='', company_name='', company_id=''):
        url = self.mk_url('user', 'api/crm/company/contract/selectContractList')
        data = {
            'pageIndex': 1,
            'pageSize': 30,
            'contractCode': contract_code,
            'status': status,  # 合同状态 0：待发起 1：待签署 2：已签署 3: 已确认 4：终止中 5： 已终止 6：已弃标 7：已到期 8：已撤回 ',
            'companySignTimeStart': company_sign_time_start,
            'companySignTimeEnd': company_sign_time_end,
            'brokerMobile': broker_mobile,
            'companyName': company_name,
            'companyId': company_id
        }
        r = requests.post(url, data, cookies=cookies_service)
        print(r.json())
        return r.json()

    # 查看合同详情
    def agent_crm_get_contract_info(self, contract_id, cookies_service):
        data = {
            'id': contract_id
        }
        url = self.mk_url('user', 'api/crm/company/contract/getContractInfoById')
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()

    # 发起合同签署
    def agent_crm_sign_contract(self, cookies_service, contract_id, broker_id, is_first='true', file_type='[6, 8]'):
        data = {
            'id': contract_id,
            'isFirst': is_first,
            'brokerId': broker_id,
            'fileType': file_type  # 签署的合同：6：固定项目运输合同V1 7：固定项目运输合同V2 8：廉洁协议
        }
        url = self.mk_url('user', 'api/crm/company/contract/signContract')
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()

    # 改变合同状态
    def test_update_contract_status(self, contract_id, contract_status, cookies_service):
        data = {
            'id': contract_id,
            'contractStatus': contract_status  # 8：撤回合同，4：合同终止
        }
        url = self.mk_url('user', 'api/crm/company/contract/updateStatusById')
        r = requests.post(url, data=data, cookies=cookies_service)
        return r.json()
