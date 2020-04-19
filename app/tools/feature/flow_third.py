# coding:utf-8
# 三方运单数据生成


from app.tools.api.api_third import *
from app.util.ssh_conf import *


class DeBangFlow(ApiDebang):
    """德邦数据生成"""
    def __init__(self, environment):
        super().__init__(environment)
        self.environment = environment

    # 模拟德邦询价
    def debangorder(self, departureName, arrivalsName, models, boxType, productType, price):
        try:
            if productType == '5':
                thirdSn = self.random_order_zc()
            else:
                thirdSn = self.random_order_gx()
            res = self.create_db_order(thirdSn, departureName, arrivalsName, models, boxType, productType, price=price)
            return res, thirdSn
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟德邦确认下单
    def debangconfim(self, orderCode, orderStauts):
        try:
            res = self.comfirm_db_order(orderCode, orderStauts)
            print(res)
            if res['status'] == 500:
                database = 'fykc_xcustomer_service'
                sql = 'update business_info set receCycleType = 1 where receCycleType is null or receCycleType = 0;'
                remote_database(self.environment, database, sql)
                res = self.comfirm_db_order(orderCode, orderStauts)
                return res
            return res
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟德邦发起对账
    def debang_checking(self, thirdsn):
        try:
            res = self.push_fy_checking(thirdsn)
            return res
        except Exception:
            return '对账异常！'


class JDFlow(ApiJd):
    """京东数据生成"""

    # 模拟京东询价
    def jdorder(self, carlengthtype, bengin_adress, end_adress):
        try:
            thirdsn = self.random_out_numbers_jd()
            if bengin_adress == 'bengin1' and end_adress == 'end1':
                bengin_adress = eval(get_config('adress_jd', 'bengin1'))
                end_adress = eval(get_config('adress_jd', 'end1'))
                res = self.jd_xun_jia_out_point(carlengthtype, thirdsn, bengin_adress, end_adress)
                return res, thirdsn
            elif bengin_adress == 'bengin2' and end_adress == 'end2':
                bengin_adress = eval(get_config('adress_jd', 'bengin2'))
                end_adress = eval(get_config('adress_jd', 'end2'))
                res = self.jd_xun_jia_out_point(carlengthtype, thirdsn, bengin_adress, end_adress)
                return res, thirdsn
            else:
                return '输入地址有误！'
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟京东中标
    def jdconfirm(self, thirdsn):
        try:
            res = self.jd_out_xia_dan(thirdsn)
            return res
        except Exception:
            return '系统异常，请联系管理员'


class KYFlow(ApiKy):
    """跨越数据生成"""

    # 模拟跨越询价
    def kyorder(self, carlengthtype, bengin_adress, end_adress):
        try:
            thirdsn = self.random_numbers_ky()
            if bengin_adress == 'bengin1' and end_adress == 'end1':
                bengin_adress = eval(get_config('adress_ky', 'bengin1'))
                end_adress = eval(get_config('adress_ky', 'end1'))
                res = self.ky_create_order(carlengthtype, thirdsn, bengin_adress, end_adress)
                return res, thirdsn
            elif bengin_adress == 'bengin2' and end_adress == 'end2':
                bengin_adress = eval(get_config('adress_ky', 'bengin2'))
                end_adress = eval(get_config('adress_ky', 'end2'))
                res = self.ky_create_order(carlengthtype, thirdsn, bengin_adress, end_adress)
                return res, thirdsn
            else:
                return '输入地址有误！'

        except Exception:
            return '系统异常，请联系管理员'

    # 模拟跨越中标
    def kyconfirm(self, thirdsn):
        try:
            res = self.ky_query_confirm(thirdsn)
            return res
        except Exception:
            return '系统异常，请联系管理员'


class SfFlow(ApiSf):
    """顺丰数据生成"""

    # 模拟顺丰询价
    def sforder(self, vehicleton, vehicletypecode, bengin_adress, cross_adress, end_adress):
        try:
            if bengin_adress == 'bengin1' and cross_adress == 'cross1' or cross_adress == 'cross2' and end_adress == 'end1':
                bengin_adress = eval(get_config('adress_sf', 'bengin1'))
                if cross_adress == 'cross2':
                    cross_adress = eval(get_config('adress_sf', 'cross2'))
                else:
                    cross_adress = eval(get_config('adress_sf', 'cross1'))
                end_adress = eval(get_config('adress_sf', 'end1'))
                res = self.make_sf_order_create(vehicleton, vehicletypecode, bengin_adress, cross_adress,
                                                end_adress)
                return res
            elif bengin_adress == 'bengin2' and cross_adress == 'cross2' or cross_adress == 'cross1' and end_adress == 'end2':
                bengin_adress = eval(get_config('adress_sf', 'bengin2'))
                if cross_adress == 'cross1':
                    cross_adress = eval(get_config('adress_sf', 'cross1'))
                else:
                    cross_adress = eval(get_config('adress_sf', 'cross2'))
                end_adress = eval(get_config('adress_sf', 'end2'))
                res = self.make_sf_order_create(vehicleton, vehicletypecode, bengin_adress, cross_adress,
                                                end_adress)
                return res
            elif bengin_adress == 'bengin1' or bengin_adress == 'bengin2' and cross_adress == 'null' and end_adress == 'end1' or end_adress == 'end2':
                if bengin_adress == 'bengin1':
                    bengin_adress = eval(get_config('adress_sf', 'bengin1'))
                elif bengin_adress == 'bengin2':
                    bengin_adress = eval(get_config('adress_sf', 'bengin2'))
                if end_adress == 'end1':
                    end_adress = eval(get_config('adress_sf', 'end1'))
                elif end_adress == 'end2':
                    end_adress = eval(get_config('adress_sf', 'end2'))
                res = self.make_sf_order_create(vehicleton, vehicletypecode, bengin_adress, cross_adress,
                                                end_adress)
                return res
            else:
                pass
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟顺丰中标
    def sfconfirm(self, thirdsn):
        try:
            res = self.get_sf_confirm_order(thirdsn)
            return res
        except Exception:
            return '系统异常，请联系管理员'


class YtFlow(ApiYt):
    """圆通数据生成"""

    # 模拟圆通询价
    def ytorder(self, carlengthtype, bengin_adress, end_adress):
        try:
            thirdsn = self.random_order_yt()
            if bengin_adress == 'bengin1' and end_adress == 'end1':
                bengin_adress = eval(get_config('adress_yt', 'bengin1'))
                end_adress = eval(get_config('adress_yt', 'end1'))
                res = self.yt_create_order(thirdsn, carlengthtype, bengin_adress, end_adress)
                return res, thirdsn
            elif bengin_adress == 'bengin2' and end_adress == 'end2':
                bengin_adress = eval(get_config('adress_yt', 'bengin2'))
                end_adress = eval(get_config('adress_yt', 'end2'))
                res = self.res = self.yt_create_order(thirdsn, carlengthtype, bengin_adress, end_adress)
                return res, thirdsn
            else:
                return '输入地址有误！'
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟圆通中标
    def ytconfirm(self, thirdsn):
        try:
            res = self.yt_confirm_order(thirdsn)
            return res
        except Exception:
            return '系统异常，请联系管理员'


class HyddFlow(ApiHydd):
    """华宇嘟嘟数据生成"""

    # 模拟华宇嘟嘟询价
    def hyddorder(self, carlengthtype, bengin_adress, end_adress):
        try:
            thirdsn = self.random_order_hydd()
            if bengin_adress == 'bengin1' and end_adress == 'end1':
                bengin_adress = eval(get_config('adress_hydd', 'bengin1'))
                end_adress = eval(get_config('adress_hydd', 'end1'))
                res = self.hydd_create_order(thirdsn, carlengthtype, bengin_adress, end_adress)
                return res, thirdsn
            elif bengin_adress == 'bengin2' and end_adress == 'end2':
                bengin_adress = eval(get_config('adress_hydd', 'bengin2'))
                end_adress = eval(get_config('adress_hydd', 'end2'))
                res = self.hydd_create_order(thirdsn, carlengthtype, bengin_adress, end_adress)
                return res, thirdsn
            else:
                return '输入地址有误！'
        except Exception:
            return '系统异常，请联系管理员'

    # 模拟华宇嘟嘟中标
    def hyddconfirm(self, thirdsn):
        try:
            res = self.hydd_confirm_order(thirdsn)
            return res
        except Exception:
            return '系统异常，请联系管理员'


if __name__ == '__main__':
    # JDFlow().jdorder('t7','bengin1','end1')
    SfFlow().sforder('r1', 1, '冷藏车-单温', 'bengin1', 'null', 'end1')
