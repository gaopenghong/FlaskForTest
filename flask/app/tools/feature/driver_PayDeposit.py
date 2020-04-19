from app.tools.api.api_driver import ApiDriver


class PayDeposit(ApiDriver):
    def __init__(self, env):
        self.env = env

    def driver_PayDeposit(self, driver_mobile):
        res = self.test_pay_Deposit(self.env, driver_mobile)
        try:
            return res["status"]["desc"]
        except:
            return res

    def driver_linePayDeposit(self, driver_mobile):
        res = self.test_pay_lineDeposit(self.env, driver_mobile)
        try:
            return res["status"]["desc"]
        except:
            return res


if __name__ == "__main__":
    res = PayDeposit("t4").driver_PayDeposit(16022222222)
    print(res)
