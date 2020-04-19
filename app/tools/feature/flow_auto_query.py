# coding:utf-8
# 意向单数据生成

from app.tools.api.api_bms import *


class AllAutoQuery(ApiAutoQuery):
    """意向单相关"""

    # 批量生成意向单
    def all_auto_query(self, plandate):
        try:
            cookies = self.get_cookies()
            res = self.create_all_auto_query(plandate, cookies)
            return res
        except Exception:
            return "接口异常"

    # 按线路生成意向单
    def lineid_auto_query(self, lineid, plandate):
        try:
            cookies = self.get_cookies()
            res = self.create_bylineid_auto_query(lineid, plandate, cookies)
            return res
        except Exception:
            return "接口异常"


if __name__ == '__main__':
    AllAutoQuery().all_auto_query('t8', '1573264566000')
