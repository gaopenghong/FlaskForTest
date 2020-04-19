# coding:utf-8
import json
from app.util.ssh_conf import dbconfig
from app.util.ssh_conf import remote_database
from app.tools.api.api_conf_wrapper import *
from app.tools.api.api_ua import *
from app.tools.api.conf import *


def add_admin(environment, name, mobile):
    # 查询fykc_tower_babel.user_base_info是否存在此用户
    port = dbconfig[environment]
    sql_search_tower_babel = 'select * from user_base_info where mobile="%s";' % mobile
    r_search_tower_babel = remote_database(environment, 'fykc_tower_babel', sql_search_tower_babel)
    # 查询fykc_conf_wrapper.user_info是否存在此用户
    sql_search_conf_wrapper = 'select * from user_info where mobile="%s";' % mobile
    r_search_conf_wrapper = remote_database(environment, 'fykc_conf_wrapper', sql_search_conf_wrapper)

    if r_search_tower_babel == "连接数据库失败":
        return "%s:数据库连接失败" % mobile
    elif len(r_search_tower_babel) > 0 and len(r_search_conf_wrapper) > 0:
        if r_search_tower_babel[0][0] == r_search_conf_wrapper[0][0]:
            # 两个表中均存在管理员数据且匹配, 直接通过
            res = u'账号已存在'
            print('账号已存在: admin_id=%s, admin_name=%s, admin_mobile=%s' % (r_search_conf_wrapper[0][0], name, mobile))
            return res
        else:
            # 两个表中均存在管理员数据但不匹配, 。。。。。。
            print('fykc_tower_babel.user_base_info与fykc_conf_wrapper.user_info中id不一致, 请手动修改')
    elif len(r_search_tower_babel) > 0:
        # 向fykc_conf_wrapper中添加数据
        sql_insert_conf_wrapper = 'INSERT INTO `user_info`(`id`, `name`, `jobNumber`, `mobile`, ' \
                                  '`department`, `area`, `authType`, `status`, `userId`, `createTime`, `updateTime`, ' \
                                  '`wxUserID`) VALUES (%s, "%s", NULL, "%s", "4d9f58e75204441c9744aa95e2b7fa85", "", ' \
                                  '1, 2, NULL, "2019-09-16 19:16:33", "2019-09-16 19:16:33", NULL);' \
                                  % (r_search_conf_wrapper[0][0], name, mobile)
        remote_database(environment, 'fykc_conf_wrapper', sql_insert_conf_wrapper)
        res = '账号已更新成功'
        print('账号已更新成功: admin_id=%s, admin_name=%s, admin_mobile=%s' % (r_search_tower_babel[0][0], name, mobile))
        return res
    elif len(r_search_conf_wrapper) > 0:
        # 向fykc_tower_babel中添加数据
        sql_insert_tower_babel = 'INSERT INTO `user_base_info`(`id`, `name`, `mobile`, `token`, `password`, ' \
                                 '`lastAccessTime`, `lastAccessIp`, `tokenExpire`, `status`) VALUES (%s, "%s", ' \
                                 '"%s", NULL, "9a4e4ba9fe6fd2b8d5054456fbaa38f1", NULL, NULL, NULL, 2);' \
                                 % (r_search_conf_wrapper[0][0], name, mobile)
        remote_database(environment, 'fykc_tower_babel', sql_insert_tower_babel)
        print('账号已更新成功: admin_id=%s, admin_name=%s, admin_mobile=%s' % (max_value + 1, name, mobile))
        res = '账号已更新成功'
        return res
    else:
        # 查询fykc_tower_babel.user_base_info最大值
        sql_search_max_1 = 'select * from user_base_info order by id desc limit 1;'
        r_search_max_1 = remote_database(environment, 'fykc_tower_babel', sql_search_max_1)
        # 查询fykc_conf_wrapper.user_info最大值
        sql_search_max_2 = 'select * from user_info order by id desc limit 1;'
        r_search_max_2 = remote_database(environment, 'fykc_conf_wrapper', sql_search_max_2)
        max_value = max(r_search_max_1[0][0], r_search_max_2[0][0])
        # 向fykc_conf_wrapper中添加数据
        sql_insert_conf_wrapper = 'INSERT INTO `user_info`(`id`, `name`, `jobNumber`, `mobile`, ' \
                                  '`department`, `area`, `authType`, `status`, `userId`, `createTime`, `updateTime`, ' \
                                  '`wxUserID`) VALUES (%s, "%s", NULL, "%s", "4d9f58e75204441c9744aa95e2b7fa85", "", ' \
                                  '1, 2, NULL, "2019-09-16 19:16:33", "2019-09-16 19:16:33", NULL);' \
                                  % (max_value + 1, name, mobile)
        remote_database(environment, 'fykc_conf_wrapper', sql_insert_conf_wrapper)
        # 向fykc_tower_babel中添加数据
        sql_insert_tower_babel = 'INSERT INTO `user_base_info`(`id`, `name`, `mobile`, `token`, `password`, ' \
                                 '`lastAccessTime`, `lastAccessIp`, `tokenExpire`, `status`) VALUES (%s, "%s", ' \
                                 '"%s", NULL, "ac78e9360c7bf2f6d7b737949ce4a6c3", NULL, NULL, NULL, 2);' \
                                 % (max_value + 1, name, mobile)
        remote_database(environment, 'fykc_tower_babel', sql_insert_tower_babel)
        print('账号已添加成功: admin_id=%s, admin_name=%s, admin_mobile=%s' % (max_value + 1, name, mobile))
        res = '账号已添加成功'
        return res


class ConfClass(ApiConf, ApiUa):

    # 获取新添加用户的user_id
    def get_conf_user_id(self, mobile):
        global user_id
        r_ua_request_id = self.ua_generate_check_code()
        password = 'Ab@123456789'
        cookies = self.ua_login(mobile, password, r_ua_request_id)
        r = self.bms_admin_info(cookies)
        user_id = r['property']['user']['id']
        return user_id

    # 把新加用户加所有权限
    def add_new_user_conf(self, user_id):
        r_ua_request_id = self.ua_generate_check_code()
        self.admin_mobile = get_config("admin_account", "admin_mobile")
        self.admin_password = get_config("admin_account", "admin_password")
        cookies_ua = self.ua_login(self.admin_mobile, self.admin_password, r_ua_request_id)
        r = self.update_user_info(user_id, cookies_ua)
        return r


if __name__ == '__main__':
    # administrators = [
    #     ['15776648230', '滕鑫'],
    #     ['13074579832', '杨术丽'],
    #     ['13120327312', '梁雨'],
    #     ['13001169637', '杨静'],
    #     ['18276709611', '林玉秀'],
    #     ['18276705311', '黎素'],
    # ]
    # for environment in dbconfig:
    #     env = environment[0]
    #     port = environment[1]
    #     print(env, port)
    #     add_admin(env, '伍瑶', '18610713791')
    # ConfClass(environment='r1').get_add_conf_limits('张狗子', '13200008888')
    user_id = ConfClass(environment='r2').get_conf_user_list('13289890000')
    # ConfClass(environment='r1').get_add_conf_limits('张狗子', '14566667777')
    r = ConfClass(environment='r2').add_new_user_conf(user_id)
    print(r)
