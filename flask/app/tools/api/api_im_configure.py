# coding:utf-8
from app.tools.api.im_base import *

class ImConfigure(ImBase):
    """在线客服接口"""
    # 敏感词添加
    def sensitive_word_add(self, sw_name, cookies):
        url = self.mk_url("im", "api/sensitiveWords/visitor/add")
        data = {
            'word': sw_name
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 敏感词修改
    def sensitive_word_upd(self, sw_id, sw_name_upd, cookies):
        url = self.mk_url("im", "api/sensitiveWords/visitor/update")
        data = {
            'id': sw_id,
            'word': sw_name_upd
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 敏感词查询
    def sensitive_word_list(self, page_index, page_size, cookies):
        url = self.mk_url("im", "api/sensitiveWords/visitor/list")
        data = {
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 敏感词删除
    def sensitive_word_del(self, sw_id, cookies):
        url = self.mk_url("im", "api/sensitiveWords/visitor/delete")
        data = {
            'id': sw_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 违禁词添加
    def prohibited_word_add(self, pw_name, cookies):
        url = self.mk_url("im", "api/sensitiveWords/kf/add")
        data = {
            'word': pw_name
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 违禁词查询
    def prohibited_word_list(self, page_index, page_size, cookies):
        url = self.mk_url("im", "api/sensitiveWords/kf/list")
        data = {
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 违禁词修改
    def prohibited_word_upd(self, pw_id, pw_name, cookies):
        url = self.mk_url("im", "api/sensitiveWords/kf/update")
        data = {
            'id': pw_id,
            'word': pw_name
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 违禁词删除
    def prohibited_word_del(self, pw_id, cookies):
        url = self.mk_url("im", "api/sensitiveWords/kf/delete")
        data = {
            'id': pw_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复类别新增
    def quick_reply_category_add(self, qrc_name, cookies):
        url = self.mk_url("im", "api/quickReply/category/add")
        data = {
            'name': qrc_name,
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复类别修改
    def quick_reply_category_upd(self, qrc_id, qrc_name_upd, cookies):
        url = self.mk_url("im", "api/quickReply/category/add")
        data = {
            'id': qrc_id,
            'name': qrc_name_upd,
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复类别查询
    def quick_reply_category_list(self, page_index, page_size, cookies):
        url = self.mk_url("im", "api/quickReply/category/list")
        data = {
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复类别删除
    def quick_reply_category_del(self, qrc_id, cookies):
        url = self.mk_url("im", "api/quickReply/category/delete")
        data = {
            'id': qrc_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复新增
    def quick_reply_add(self, role, qrc_id, qr_name, cookies):
        url = self.mk_url("im", "api/quickReply/content/add")
        data = {
            'bizType': role,
            'cid': qrc_id,
            'content': qr_name
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复修改
    def quick_reply_upd(self, role, qrc_id, qr_name_upd, qr_id, cookies):
        url = self.mk_url("im", "api/quickReply/content/add")
        data = {
            'bizType': role,
            'cid': qrc_id,
            'content': qr_name_upd,
            'id': qr_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复查询
    def quick_reply_list(self, page_index, page_size, cookies):
        url = self.mk_url("im", "api/quickReply/content/list")
        data = {
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 快捷回复删除
    def quick_reply_del(self, qr_id, qrc_id, cookies):
        url = self.mk_url("im", "api/quickReply/content/delete")
        data = {
            'id': qr_id,
            'cid': qrc_id

        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

        # 会话标签添加
    def chat_tag_add(self, ct_name, role, cookies):
        url = self.mk_url("im", "api/chatTag/add")
        data = {
            'name': ct_name,
            'bizType': role
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

        # 会话标签删除
    def chat_tag_del(self, ct_id, cookies):
        url = self.mk_url("im", "api/chatTag/delete")
        data = {
            'id': ct_id
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

