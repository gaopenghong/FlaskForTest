from app.tools.api.api_driver import ApiDriver


class bankBindCard(ApiDriver):
    def __init__(self, env):
        self.env = env

    def driver_bankBindCard(self, driver_mobile):
        # 司机登录，获取token
        driver_info = self.driver_login(driver_mobile, check_code='1123')
        if driver_info["status"]["code"] != 0:
            return driver_info["status"]["desc"]
        else:
            driver_token = driver_info["data"][0]["token"]
            idCardNumber = '320924198801226490'
            bankAccount = '陈民龙'
            bankCardNumber = '6228481983226202212'
            res = self.driver_bank_bind_card(driver_token, idCardNumber, bankAccount, bankCardNumber)
            print(res)
            return res["status"]["desc"]


if __name__ == "__main__":
    res = bankBindCard("t4").driver_bankBindCard("12011111111")
    print(res)
