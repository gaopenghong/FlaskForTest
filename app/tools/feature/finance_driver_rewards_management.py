# coding:utf-8
from app.tools.api.api_finance import *
from app.tools.api.api_ua import *
from app.util.ssh_conf import *


class DriverRewardsManagement(ApiUa, ApiFinance):
    """发放司机奖励"""

    def provide_driver_rewards_management(self, operate_type, driver_id_or_mobile, reward_type, amount):
        request_id = self.ua_generate_check_code()
        login_r = self.ua_login('18911487112', 'Ab@123456789', request_id=request_id)
        global desc
        if len(driver_id_or_mobile) > 10:
            sql_mobile = "SELECT id FROM driver_info WHERE mobile ='% s' " % (
                driver_id_or_mobile)
            global driver_id
            driver_id_r = remote_database(self.env, 'fykc_xdriver_service', sql_mobile)
            if not driver_id_r == []:
                driver_id = driver_id_r[0][0]
                print(driver_id)
                if operate_type == "ProvideDriverRewards":
                    # type=2 for 日包车；type=3 for 长途包车；type=4 for 里程奖励
                    global r_add_driver_reward
                    r_add_driver_reward = []
                    if reward_type == 2:
                        r_add_driver_reward = self.add_driver_reward(driver_id, 2, amount, cookies_ua=login_r)
                    elif reward_type == 3:
                        r_add_driver_reward = self.add_driver_reward(driver_id, 3, amount, cookies_ua=login_r)
                    elif reward_type == 4:
                        r_add_driver_reward = self.add_driver_reward(driver_id, 4, amount, cookies_ua=login_r)
                    print(type(r_add_driver_reward), r_add_driver_reward)
                    r_desc = r_add_driver_reward['status']['desc']
                    if r_desc == "操作成功":
                        desc = "发放奖励成功"
                        print(desc, type(desc))
                elif operate_type == "DriverRewardsWithdraw":
                    sql_token = "SELECT token FROM driver_info WHERE mobile ='% s' " % (
                        driver_id_or_mobile)
                    print(sql_token)
                    token_r = remote_database(self.env, 'fykc_xdriver_service', sql_token)

                    if not token_r == []:
                        token = token_r[0][0]
                    else:
                        sql_insert = "INSERT INTO driver_info(id, name, password, token, tokenExpire, mobile, sex, remark, brokerId, brokerMobile, brokerName, transportType, transportId, idCardNumber, idCardEndTime, idCardAddress, imgIdCardFront, frontStatus, imgIdCardBack, backStatus, imgDriveLicense, licenseEndTime, licenStatus, imgQualification, qualificationEndTime, auditName, checkRemark, status, checkDate, imgPortrait, wx, regSrcType, regSrcId, conTransSta, conInvoiceSta, taxProxyRegSta, drivingSta, createTime, updateTime, adminId, adminName, adminType, isNew, isCancel) VALUES ('', '%s', NULL, '95a5bfcc8d1ef03e506a487d9de6858d', '2020-12-08 21:56:03', '沈叶光', 1, NULL, NULL, NULL, NULL, 1, NULL, '341224198506110942', NULL, '安徽省寿县双庙集镇周岗村余元队', 'http://public.fuyoukache.com/FjjOrub7ER7Q-Pz2eIi7WuE61BHF', 2, 'https://public.fuyoukache.com/common/5c3e35a702869.jpg', 2, 'https://public.fuyoukache.com/989e7307-8696-4dc6-a88d-83e434bfab25---a00205cc1a49822bb3ed890a8d97891.jpg', NULL, 2, NULL, NULL, '程慧', '驾驶证信息有误', 2, NULL, NULL, NULL, 1, NULL, 1, 1, 1, 0, '2019-01-16 03:33:25', '2019-12-09 21:56:02', 141, '李东东', 1, 1, 0);" % driver_id_or_mobile
                        remote_database(self.env, 'fykc_xdriver_service', sql_insert)

                        sql_token = "SELECT token FROM driver_info WHERE mobile ='% s'" % (
                            driver_id_or_mobile)

                        token_r = remote_database(self.env, 'fykc_xdriver_service', sql_token)
                        token = token_r[0][0]
                    r_wallet_info = self.get_driver_wallet_info(token)
                    total_no_draw_money = r_wallet_info['data'][0]['totalNoDrawMoney']
                    print("total_no_draw_money" + str(total_no_draw_money))
                    year = random.randint(2020, 3030)
                    expire_time = str(year) + '-01-01 00:00:00'
                    print(expire_time)
                    sql_update_expired_time = "UPDATE check_code SET expiredTime ='%s' WHERE requestId = '%s'" % (
                        expire_time, driver_id_or_mobile)
                    print(sql_update_expired_time)
                    remote_database(self.env, 'fykc_xdriver_service', sql_update_expired_time)
                    code_update = random.randint(1000, 9999)
                    print(code_update)
                    sql_update_code = "UPDATE check_code SET code ='%s' WHERE requestId = '%s'" % (
                        code_update, driver_id_or_mobile)
                    remote_database(self.env, 'fykc_xdriver_service', sql_update_code)
                    print(sql_update_code)
                    sql_code = "select code  from check_code where requestId ='%s'" % driver_id_or_mobile
                    code_r = remote_database(self.env, 'fykc_xdriver_service', sql_code)
                    if not code_r == []:
                        code = code_r[0][0]
                        print("code" + str(code))
                        r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                        desc = r_driver_draw['status']['desc']
                        if desc == "输入验证码次数过多，请重新发送短信":
                            desc = "哦呜，输入验证码次数过多，请重新发送短信，只能5分钟后再次尝试喽！"
                        elif desc == "无可提金额，请刷新页面":
                            desc = "哦呜，司机端当前无可提现金额哦！"
                        elif desc == "司机未绑定银行卡，不能提款":
                            sql_insert = "INSERT INTO bank_card_info(id, driverId, accountType, bankName, bankCardNumber, bankAccount, idCardNumber, bankProvince, bankProvinceName, bankCity, bankCityName, depositBankName, bankColor, bankShort) VALUES ('', %s, 1, '招商银行', '6225880150027531', '李东东', NULL, NULL, NULL, NULL, NULL, '', '#C85656', 'CMB');" % driver_id
                            print(sql_insert)
                            remote_database(self.env, 'fykc_xdriver_service', sql_insert)
                            r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                            desc = r_driver_draw['status']['desc']
                            print(desc)
                    else:
                        sql_insert = "INSERT INTO check_code (id, requestId, code, expiredTime, codeType, codeCount) VALUES ('', '%s', '6651', '2020-12-09 20:11:35', 0, 0);" % str(
                            driver_id_or_mobile)
                        print(sql_insert)
                        remote_database(self.env, 'fykc_xdriver_service', sql_insert)
                        sql_code = "select code  from check_code where requestId ='%s'" % driver_id_or_mobile
                        code_r = remote_database(self.env, 'fykc_xdriver_service', sql_code)
                        code = code_r[0][0]
                        print("code" + str(code))
                        r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                        print("UUUUUUUU", r_driver_draw)
                        desc = r_driver_draw['status']['desc']
                        if desc == "输入验证码次数过多，请重新发送短信":
                            print("哦呜，输入验证码次数过多，请重新发送短信，只能5分钟后再次尝试喽！")
                        elif desc == "无可提金额，请刷新页面":
                            desc = "哦呜，司机端当前无可提现金额哦！"
                        elif desc == "司机未绑定银行卡，不能提款":
                            sql_insert = "INSERT INTO bank_card_info(id, driverId, accountType, bankName, bankCardNumber, bankAccount, idCardNumber, bankProvince, bankProvinceName, bankCity, bankCityName, depositBankName, bankColor, bankShort) VALUES ('', %s, 1, '招商银行', '6225880150027531', '李东东', NULL, NULL, NULL, NULL, NULL, '', '#C85656', 'CMB');" % driver_id
                            print(sql_insert)
                            remote_database(self.env, 'fykc_xdriver_service', sql_insert)
                            r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                            desc = r_driver_draw['status']['desc']
                            print(desc)
                elif operate_type == "DriverRewardsQuery":
                    # 司机端可提金额查询结果
                    sql_mobile = "SELECT id FROM driver_info WHERE mobile ='% s' " % driver_id_or_mobile
                    print(sql_mobile)
                    driver_id = remote_database(self.env, 'fykc_xdriver_service', sql_mobile)
                    sql_token = "SELECT token FROM driver_info WHERE mobile ='% s' " % driver_id_or_mobile
                    token = remote_database(self.env, 'fykc_xdriver_service', sql_token)
                    r_wallet_info = self.get_driver_wallet_info(token)
                    if r_wallet_info['status']['desc'] == "登录失效，请登录":
                        sql_update_expired_time = "UPDATE driver_info SET tokenExpire ='2030-12-12' WHERE mobile = '%s'" % driver_id_or_mobile
                        remote_database(self.env, 'fykc_xdriver_service', sql_update_expired_time)
                        r_wallet_info = self.get_driver_wallet_info(token)
                    total_no_draw_money = r_wallet_info['data'][0]['totalNoDrawMoney']
                    desc_driver = ["司机端可以金额:" + str(total_no_draw_money)]
                    # 财务奖励提现明细查询结果
                    sql_mobile = "SELECT id FROM driver_info WHERE mobile ='% s' " % driver_id_or_mobile
                    driver_id = remote_database(self.env, 'fykc_xdriver_service', sql_mobile)
                    r_get_driver_reward_payments = self.get_driver_reward_payments(driver_id, cookies_ua=login_r)
                    print(len(r_get_driver_reward_payments['data']))
                    if len(r_get_driver_reward_payments['data']) > 1:
                        desc_caiwu = []
                        for item in range(len(r_get_driver_reward_payments['data'])):
                            reward_type_enum = r_get_driver_reward_payments['data'][item]['rewardTypeEnum']
                            if reward_type_enum == "DISTANCE_OVER":
                                reward_type_enum_zn = "里程奖励"
                            elif reward_type_enum == "LONG_DAY_HIRE_CAR":
                                reward_type_enum_zn = "长途包车"
                            elif reward_type_enum == "DAY_PACKAGE_NOTICE":
                                reward_type_enum_zn = "日包车"

                            draw_money = r_get_driver_reward_payments['data'][item]['drawMoney']
                            pay_status_name = r_get_driver_reward_payments['data'][item]['payStatusName']
                            desc_temp = (
                                    "明细" + str(item + 1) + ":" + str(reward_type_enum_zn) + "-" + str(
                                draw_money) + "-" + str(pay_status_name))
                            desc_caiwu.append(desc_temp)

                        desc_sum = [desc_driver, desc_caiwu]

                        for i in range(len(desc_sum) - 1):
                            print(i, (desc_sum[0][i].split(sep=":"))[0], (desc_sum[0][i].split(sep=":"))[1])
                            desc_dict = {}
                            desc_dict_key = desc_sum[0][i].split(sep=":")[0]
                            dict_value = desc_sum[0][i].split(sep=":")[1]
                            desc_dict.setdefault(desc_dict_key, dict_value)
                            for j in range(len(desc_sum[1])):
                                desc_dict_key = desc_sum[1][j].split(sep=":")[0]
                                dict_value = desc_sum[1][j].split(sep=":")[1]
                                desc_dict.setdefault(desc_dict_key, dict_value)
                        desc = str(desc_dict)
                    elif len(r_get_driver_reward_payments['data']) == 1:
                        desc_caiwu = []
                        for item in range(len(r_get_driver_reward_payments['data'])):
                            reward_type_enum = r_get_driver_reward_payments['data'][item]['rewardTypeEnum']
                            if reward_type_enum == "DISTANCE_OVER":
                                reward_type_enum_zn = "里程奖励"
                            elif reward_type_enum == "LONG_DAY_HIRE_CAR":
                                reward_type_enum_zn = "长途包车"
                            elif reward_type_enum == "DAY_PACKAGE_NOTICE":
                                reward_type_enum_zn = "日包车"
                            draw_money = r_get_driver_reward_payments['data'][item]['drawMoney']
                            pay_status_name = r_get_driver_reward_payments['data'][item]['payStatusName']
                            desc_temp = "明细" + str(item + 1) + ":" + str(reward_type_enum_zn) + "-" + str(
                                draw_money) + "-" + str(
                                pay_status_name)
                            desc_caiwu.append(desc_temp)
                        desc_sum = [desc_driver, desc_caiwu]
                        for i in range(len(desc_sum) - 1):
                            print(i, (desc_sum[0][i].split(sep=":"))[0], (desc_sum[0][i].split(sep=":"))[1])
                            desc_dict = {}
                            desc_dict_key = desc_sum[0][i].split(sep=":")[0]
                            dict_value = desc_sum[0][i].split(sep=":")[1]
                            desc_dict.setdefault(desc_dict_key, dict_value)
                            for j in range(len(desc_sum[1])):
                                desc_dict_key = desc_sum[1][j].split(sep=":")[0]
                                dict_value = desc_sum[1][j].split(sep=":")[1]
                                desc_dict.setdefault(desc_dict_key, dict_value)
                        desc = str(desc_dict)
                    else:
                        desc = "财务奖励提现明细为空！"
            else:
                desc = (str(self.env) + "环境中司机手机号：" + str(
                    driver_id_or_mobile) + " 记录不存在，请输入正确信息！")
        else:
            sql_mobile = "SELECT id FROM driver_info WHERE id ='% s'" % (
                str(driver_id_or_mobile))
            print(sql_mobile, "********")
            driver_id_r = remote_database(self.env, 'fykc_xdriver_service', sql_mobile)
            if not driver_id_r == []:
                driver_id = driver_id_r[0][0]
                print(driver_id)
                if operate_type == "ProvideDriverRewards":
                    # type=2 for 日包车；type=3 for 长途包车；type=4 for 里程奖励
                    if reward_type == 2:
                        r_add_driver_reward = self.add_driver_reward(driver_id_or_mobile, 2, amount, cookies_ua=login_r)
                    elif reward_type == 3:
                        r_add_driver_reward = self.add_driver_reward(driver_id_or_mobile, 3, amount, cookies_ua=login_r)
                    elif reward_type == 4:
                        r_add_driver_reward = self.add_driver_reward(driver_id_or_mobile, 4, amount, cookies_ua=login_r)
                    r_desc = r_add_driver_reward['status']['desc']
                    if r_desc == "操作成功":
                        desc = "发放奖励成功"
                        print(desc)
                elif operate_type == "DriverRewardsWithdraw":
                    sql_token = "SELECT token FROM driver_info WHERE id ='% s' " % driver_id_or_mobile
                    token = remote_database(self.env, 'fykc_xdriver_service', sql_token)[0][0]
                    print(token, "*********")
                    r_wallet_info = self.get_driver_wallet_info(token)
                    total_no_draw_money = r_wallet_info['data'][0]['totalNoDrawMoney']
                    print("total_no_draw_money" + str(total_no_draw_money))
                    year = random.randint(2020, 3030)
                    expire_time = str(year) + '-01-01 00:00:00'
                    print(expire_time)
                    sql_mobile = "select mobile from driver_info where id ='%s'" % driver_id_or_mobile
                    mobile = remote_database(self.env, 'fykc_xdriver_service', sql_mobile)[0][0]
                    print("mobile" + str(mobile))
                    sql_update_expired_time = "UPDATE check_code SET expiredTime ='%s' WHERE requestId = '%s'" % (
                        expire_time, mobile)
                    print(sql_update_expired_time)
                    remote_database(self.env, 'fykc_xdriver_service', sql_update_expired_time)
                    sql_code = "select code  from check_code where requestId ='%s'" % mobile
                    print(sql_code)
                    code = remote_database(self.env, 'fykc_xdriver_service', sql_code)[0][0]
                    print("code" + str(code))
                    r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                    desc = r_driver_draw['status']['desc']
                    if desc == "输入验证码次数过多，请重新发送短信":
                        desc = "哦呜，输入验证码次数过多，请重新发送短信，只能5分钟后再次尝试喽！"
                    elif desc == "无可提金额，请刷新页面":
                        desc = "哦呜，司机端当前无可提现金额哦！"
                    elif desc == "司机未绑定银行卡，不能提款":
                        sql_insert = "INSERT INTO bank_card_info(id, driverId, accountType, bankName, bankCardNumber, bankAccount, idCardNumber, bankProvince, bankProvinceName, bankCity, bankCityName, depositBankName, bankColor, bankShort) VALUES ('', %s, 1, '招商银行', '6225880150027531', '李东东', NULL, NULL, NULL, NULL, NULL, '', '#C85656', 'CMB');" % driver_id
                        print(sql_insert)
                        remote_database(self.env, 'fykc_xdriver_service', sql_insert)
                        r_driver_draw = self.driver_draw(total_no_draw_money, code, token, login_r)
                        desc = r_driver_draw['status']['desc']
                elif operate_type == "DriverRewardsQuery":
                    # 司机端可提金额查询结果
                    sql_token = "SELECT token FROM driver_info WHERE id ='% s' " % driver_id_or_mobile
                    print(sql_token)
                    token = remote_database(self.env, 'fykc_xdriver_service', sql_token)
                    print(token, "AAAAAAAAAAA")
                    r_wallet_info = self.get_driver_wallet_info(token)
                    total_no_draw_money = r_wallet_info['data'][0]['totalNoDrawMoney']
                    desc_driver = ["司机端可以金额:" + str(total_no_draw_money)]

                    # 财务奖励提现明细查询结果
                    r_get_driver_reward_payments = self.get_driver_reward_payments(driver_id_or_mobile,
                                                                                   cookies_ua=login_r)
                    if len(r_get_driver_reward_payments['data']) > 1:
                        desc_caiwu = []
                        for item in range(len(r_get_driver_reward_payments['data'])):
                            reward_type_enum = r_get_driver_reward_payments['data'][item]['rewardTypeEnum']
                            if reward_type_enum == "DISTANCE_OVER":
                                reward_type_enum_zn = "里程奖励"
                            elif reward_type_enum == "LONG_DAY_HIRE_CAR":
                                reward_type_enum_zn = "长途包车"
                            elif reward_type_enum == "DAY_PACKAGE_NOTICE":
                                reward_type_enum_zn = "日包车"

                            draw_money = r_get_driver_reward_payments['data'][item]['drawMoney']
                            pay_status_name = r_get_driver_reward_payments['data'][item]['payStatusName']
                            desc_temp = (
                                    "明细" + str(item + 1) + ":" + str(reward_type_enum_zn) + "-" + str(
                                draw_money) + "-" + str(pay_status_name))
                            desc_caiwu.append(desc_temp)

                        desc_sum = [desc_driver, desc_caiwu]

                        for i in range(len(desc_sum) - 1):
                            print(i, (desc_sum[0][i].split(sep=":"))[0], (desc_sum[0][i].split(sep=":"))[1])
                            desc_dict = {}
                            desc_dict_key = desc_sum[0][i].split(sep=":")[0]
                            dict_value = desc_sum[0][i].split(sep=":")[1]
                            desc_dict.setdefault(desc_dict_key, dict_value)
                            for j in range(len(desc_sum[1])):
                                desc_dict_key = desc_sum[1][j].split(sep=":")[0]
                                dict_value = desc_sum[1][j].split(sep=":")[1]
                                desc_dict.setdefault(desc_dict_key, dict_value)
                        desc = str(desc_dict)
                    elif len(r_get_driver_reward_payments['data']) == 1:
                        desc_caiwu = []
                        for item in range(len(r_get_driver_reward_payments['data'])):
                            reward_type_enum = r_get_driver_reward_payments['data'][item]['rewardTypeEnum']
                            if reward_type_enum == "DISTANCE_OVER":
                                reward_type_enum_zn = "里程奖励"
                            elif reward_type_enum == "LONG_DAY_HIRE_CAR":
                                reward_type_enum_zn = "长途包车"
                            elif reward_type_enum == "DAY_PACKAGE_NOTICE":
                                reward_type_enum_zn = "日包车"
                            draw_money = r_get_driver_reward_payments['data'][item]['drawMoney']
                            pay_status_name = r_get_driver_reward_payments['data'][item]['payStatusName']
                            desc_temp = "明细" + str(item + 1) + ":" + str(reward_type_enum_zn) + "-" + str(
                                draw_money) + "-" + str(
                                pay_status_name)
                            desc_caiwu.append(desc_temp)
                        desc_sum = [desc_driver, desc_caiwu]
                        for i in range(len(desc_sum) - 1):
                            print(i, (desc_sum[0][i].split(sep=":"))[0], (desc_sum[0][i].split(sep=":"))[1])
                            desc_dict = {}
                            desc_dict_key = desc_sum[0][i].split(sep=":")[0]
                            dict_value = desc_sum[0][i].split(sep=":")[1]
                            desc_dict.setdefault(desc_dict_key, dict_value)
                            for j in range(len(desc_sum[1])):
                                desc_dict_key = desc_sum[1][j].split(sep=":")[0]
                                dict_value = desc_sum[1][j].split(sep=":")[1]
                                desc_dict.setdefault(desc_dict_key, dict_value)
                        desc = str(desc_dict)
                    else:
                        print("财务奖励提现明细为空！")
            else:
                desc = (str(self.env) + "环境中司机id：" + str(
                    driver_id_or_mobile) + " 记录不存在，请输入正确信息！")
        return desc


if __name__ == '__main__':
    # DriverRewardsManagement('r2').provide_driver_rewards_management('ProvideDriverRewards', '16011111111', 2,
    #                                                                 '129.99')
    # DriverRewardsManagement('t1').provide_driver_rewards_management('DriverRewardsWithdraw', '12011111111', 4,
    #                                                                 '846.93')
    DriverRewardsManagement('r2').provide_driver_rewards_management('DriverRewardsQuery', '16011111111', 4,
                                                                    '846.93')
