from app.tools.api.api_truck import *
from app.tools.api.api_ua import *


class TruckAddTrailer(ApiUa, AddDrivers):
    """新增挂箱"""

    def add_truck_trailer(self, plate):
        r_ua_request_id = self.ua_generate_check_code()
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        # return cookies_ua
        print('管理员登录结果: %s' % cookies_ua)
        trailer_list = self.truck_add_trailer(cookies_bg=cookies_ua, trailer_number=plate)
        print(trailer_list)
        if '权限不足!' in trailer_list['status']['desc']:
            return '权限不足，请去对应环境添加权限'
        # elif '挂牌号不合法' in trailer_list['status']['desc']:
        #     return '车牌号不正确，请输入正确手机号如:"苏H6992J"'
        elif '挂牌不存在，请在「用户管理-挂箱管理-挂箱列表」配置' in trailer_list['status']['desc']:
            r_add_trailer = self.user_add_trailer(cookies_bg=cookies_ua, plate=plate)
            print(r_add_trailer)
            r_trailer = self.truck_add_trailer(cookies_bg=cookies_ua, trailer_number=plate)
            if r_trailer['status']['desc'] == '操作成功':
                return '新增成功'
            else:
                return '请输入正确车牌号'
        elif trailer_list['status']['desc'] == '挂牌重复':
            return '挂箱已存在，请重新输入车牌号'


if __name__ == '__main__':
    r = TruckAddTrailer(environment='t6', admin_mobile='16888888888', admin_password='Ab@123456789')
    print(r.add_truck_trailer(plate='皖9398'))
