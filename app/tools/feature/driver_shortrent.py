from app.tools.api.api_turing import ApiTuring
from app.tools.api.api_truck import AddDrivers
import datetime
from app.tools.api.api_ua import ApiUa
from app.util.ssh_conf import *
from app.tools.api.api_xcusotmer_app import *
import datetime


class ShortRent(ApiTuring, AddDrivers, ApiUa):
    def __init__(self, env):
        self.env = env

    def driver_ShortRent(self, start_provincename, start_cityname, end_provincename, end_cityname):
        # port = dbconfig[env]
        start_provinceid = address_search(start_provincename)["province_id"]
        start_cityid = address_search(start_cityname)["city_id"]
        end_provinceid = address_search(end_provincename)["province_id"]
        end_cityid = address_search(end_cityname)["city_id"]
        # 新增图灵日包车价格管理数据
        # api_obj = ApiUa(env)
        r_ua_request_id = self.ua_generate_check_code()
        cookies = self.ua_login(18334704870, "Ab@123456789", r_ua_request_id)
        r1 = self.turing_addOrUpdateShortRentPrice(start_provinceid, start_cityid, start_provincename,
                                                   start_cityname, cookies)
        if r1["status"]["code"] != 0:
            if r1["status"]["desc"] == '该配置已经存在，请勿重复提交':
                print(r1["status"]["desc"])
        # 调度新增日包车标的
        r2 = self.truck_createShortRentConfig(start_provinceid, start_cityid, end_provinceid, start_provincename,
                                              start_cityname, end_provincename, cookies)
        print(r2)
        # 数据库修改标的生效时间为今天
        try:
            self.modify_time()
        except:
            return "修改标的生效时间失败"
        # 推送标的
        r4 = self.truck_pushDriver()
        return r4["status"]["desc"]

    def modify_time(self):
        now = datetime.datetime.now()
        zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                             microseconds=now.microsecond)
        lastToday = zeroToday + datetime.timedelta(hours=0, minutes=0, seconds=0)
        sql = "UPDATE  `short_rent_truck_config` SET`requiredDate` ='%s' WHERE `status` = 0;" % lastToday
        remote_database(self.env, 'fykc_truck_scheduler', sql)


if __name__ == "__main__":
    res = ShortRent("t4").driver_ShortRent("天津", "天津", "云南", "昆明")
    print(res)
