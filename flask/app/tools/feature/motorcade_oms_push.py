from app.tools.api.api_oms import ApiOms
from app.tools.api.api_ua import ApiUa


class MotorcadeOmsPush(ApiOms, ApiUa):
    def __init__(self, environment, admin_mobile, admin_password):
        super().__init__(environment, admin_mobile=admin_mobile, admin_password=admin_password)
        request_id = self.ua_generate_check_code()
        self.cookies_ua = self.ua_login(admin_mobile, admin_password, request_id)

    def get_message_template_id(self, app_type, msg_type, show_type, title, digest, content, img_type, img_url):
        try:
            # 查询消息模版
            r = self.oms_select_template_list(app_type, self.cookies_ua)
            print(r)
            # 如果消息模板为空进行新增
            if r['status']['desc'] == '结果为空':
                r = self.oms_create_template(self.cookies_ua, msg_type=msg_type, title=title, digest=digest,
                                             content=content,
                                             app_type=app_type, show_type=show_type, img_type=img_type,
                                             img_url=img_url)
                print(r)
            else:
                for index in range(len(r['data'])):
                    if r['data'][index]['msgType'] == msg_type and r['data'][index]['showType'] == show_type and \
                            r['data'][index]['imgType'] == img_type:
                        return r['data'][index]['id']
                    else:
                        continue
                r = self.oms_create_template(self.cookies_ua, msg_type=msg_type, title=title, digest=digest,
                                             content=content,
                                             app_type=app_type, show_type=show_type, img_type=img_type, img_url=img_url)
                print(r)
            r = self.get_message_template_id(app_type, msg_type, show_type, title, digest, content, img_type, img_url)
            return r
        except Exception as e:
            print(e)

    # 推送消息
    def push_messages(self, app_type, msg_type, show_type, img_type, scheduled_time=''):
        if msg_type == 1:
            title = '自动化测试系统消息'
            digest = '自动化测试系统消息'
        else:
            title = '自动化测试活动消息'
            digest = '自动化测试活动消息'
        # 默认封面
        if img_type == 1:
            img_url = 'https://t8oms.fuyoukache.com/default.png'
        # 无图片
        else:
            img_url = ''
        # 消息内容
        if show_type == 1:  # 链接
            content = 'https://www.baidu.com'
        else:
            content = ''
        template_id = self.get_message_template_id(app_type, msg_type, show_type, title, digest, content, img_type,
                                                   img_url)
        r = template_id
        # 暂不支持定时推送
        r = self.oms_push(scheduled_time, app_type, template_id, push_type=1, cookies_ua=self.cookies_ua)
        return r


if __name__ == '__main__':
    r_json = MotorcadeOmsPush('t7', '16888888888', 'Ab@123456789').push_messages(3211, 2, 1, 1)
    print(r_json)
