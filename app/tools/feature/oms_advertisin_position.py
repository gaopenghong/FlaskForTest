from app.tools.api.api_oms import *
from app.tools.api.api_ua import *


def teds(env, app_type, type_id, title, link_url, pic_url, rank):
    # 获取管理员cookies
    ua = ApiUa(env)
    request_id = ua.ua_generate_check_code()
    cookies_ua = ua.ua_login('16888888888', 'Ab@123456789', request_id)

    # 添加运营位
    oms = ApiOms(env)
    result = oms.api_create_ad(cookies_ua, app_type, type_id, title, link_url, pic_url, rank)
    print(result)
    return str(result)


def ios_config(env, customer_type, dev_version, host, remark):
    ua = ApiUa(env)
    request_id = ua.ua_generate_check_code()
    cookies_ua = ua.ua_login('16888888888', 'Ab@123456789', request_id)
    oms = ApiOms(env)
    result = oms.api_create_ios_config(cookies_ua, customer_type, dev_version, host)
    print(result)
    return str(result)




