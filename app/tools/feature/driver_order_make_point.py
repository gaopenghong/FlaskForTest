from app.tools.api.api_driver import ApiDriver
from app.tools.api.api_crm import ApiCrm
from app.tools.api.api_lbs_amap import Amap
from app.tools.api.api_ua import ApiUa
import time


# 司机App运单打点
class orderMakePointAll(ApiDriver, Amap, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_order_make_point_all(self, order_sn, driver_mobile):
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] == 0:
            token = driver_info["data"][0]["token"]
            # 获取运单详情
            r_driver_order_detail = self.driver_order_detail(token, order_sn)
            if r_driver_order_detail["status"]["code"] == 0:
                print('运单详情: %s' % r_driver_order_detail)
                order_point = r_driver_order_detail['data'][0]['transPointList']
                print('运单经停点: %s' % order_point)
                positions = []
                for i in order_point:
                    j = '%s%s%s' % (i['provinceName'], i['cityName'], i['districtName'])
                    location_amap = self.amap_input_tips(j)
                    location = location_amap['tips'][0]['location']
                    location_1 = location.split(',')
                    location_2 = [location_1[0], location_1[1]]
                    positions.append(location_2)
                # print(positions)
                # 到达装货地
                r_start_1 = self.driver_order_make_point(token, order_sn, order_point[0]['id'], 0, 7, 1,
                                                         positions[0][0],
                                                         positions[0][1])
                print('到达装货地: %s' % r_start_1)
                time.sleep(2)
                # 装货完成
                r_start_2 = self.driver_order_make_point(token, order_sn, order_point[0]['id'], 0, 8, 2,
                                                         positions[0][0],
                                                         positions[0][1])
                print('装货完成: %s' % r_start_2)
                time.sleep(2)
                # 经停点打点
                if len(order_point) == 2:
                    destination = positions[1]
                    destination_index = 1
                if len(order_point) >= 3:
                    destination = positions[2]
                    destination_index = 2
                    r_point_1_1 = self.driver_order_make_point(token, order_sn, order_point[1]['id'], 1, 9, 1,
                                                               positions[1][0],
                                                               positions[1][1])
                    print('到达经停点1: %s' % r_point_1_1)
                    time.sleep(2)
                    r_point_1_2 = self.driver_order_make_point(token, order_sn, order_point[1]['id'], 1, 9, 2,
                                                               positions[1][0],
                                                               positions[1][1])
                    print('离开经停点1: %s' % r_point_1_2)
                    time.sleep(2)
                if len(order_point) >= 4:
                    destination = positions[3]
                    destination_index = 3
                    r_point_2_1 = self.driver_order_make_point(token, order_sn, order_point[2]['id'], 2, 9, 1,
                                                               positions[2][0],
                                                               positions[2][1])
                    print('到达经停点2: %s' % r_point_2_1)
                    time.sleep(2)
                    r_point_2_2 = self.driver_order_make_point(token, order_sn, order_point[2]['id'], 2, 9, 2,
                                                               positions[2][0],
                                                               positions[2][1])
                    print('离开经停点2: %s' % r_point_2_2)
                    time.sleep(2)
                if len(order_point) >= 5:
                    destination = positions[4]
                    destination_index = 4
                    r_point_3_1 = self.driver_order_make_point(token, order_sn, order_point[3]['id'], 3, 9, 1,
                                                               positions[3][0],
                                                               positions[3][1])
                    print('到达经停点3: %s' % r_point_3_1)
                    time.sleep(2)
                    r_point_3_2 = self.driver_order_make_point(token, order_sn, order_point[3]['id'], 3, 9, 2,
                                                               positions[3][0],
                                                               positions[3][1])
                    print('离开经停点3: %s' % r_point_3_2)
                    time.sleep(2)
                # 到达卸货地
                r_end_1 = self.driver_order_make_point(token, order_sn, order_point[-1]['id'], destination_index,
                                                       9, 1, destination[0],
                                                       destination[1])
                print('到达卸货地: %s' % r_end_1)
                time.sleep(2)
                # 卸货完成
                r_end_2 = self.driver_order_make_point(token, order_sn, order_point[-1]['id'], destination_index,
                                                       10, 2, destination[0],
                                                       destination[1])
                print('卸货完成: %s' % r_end_2)
                return "打点完成"
            else:
                return r_driver_order_detail
        else:
            return driver_info


if __name__ == "__main__":
    res = orderMakePointAll("t4").driver_order_make_point_all(429112096213, 12800000479)
    print(res)
