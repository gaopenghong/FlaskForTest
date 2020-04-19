from app.tools.api.base import *
import requests


class ApiOms(Base):
    #  新建广告位
    def api_create_ad(self, cookies, app_type, type_1, title_1, link_url, pic_url, rank_1):
        url = self.mk_url('oms', 'api/ad/createAd')
        data = {
            'appType': app_type,
            'type': type_1,
            'title': title_1,
            'linkUrl': link_url,
            'startTime': '2019-11-01 11:11',
            'endTime': '2029-11-01 11:11',
            'picUrl': pic_url,
            'rank': rank_1,
            'ruleType': 2
        }
        r = requests.post(url, data, cookies=cookies)
        return r.json()

    # 新增ios提审配置
    def api_create_ios_config(self, cookies, customer_type, dev_version, host):
        url = self.mk_url('oms', 'api/upgrade/createAppHost')
        # url = 'https://t8oms.fuyoukache.com/service/fykc-oms-service/api/upgrade/createAppHost'
        print(url)
        data = {
            'customerType': customer_type,
            'devVersion': dev_version,
            'host': host,
            'remark': '测试呀',
        }
        print(data)
        r = requests.post(url, data, cookies=cookies)
        print('aaaaaa:', r.text)
        return r.json()

    # 'Request URL: https://t8oms.fuyoukache.com/service/fykc-oms-service/api/upgrade/createAppHost

    # 消息推送-查询消息模版列表
    def oms_select_template_list(self, app_type, cookies_ua, page_index=1, page_size=10):
        url = self.mk_url('oms', 'api/push/selectTemplateList')
        data = {
            'appType': app_type,
            'pageIndex': page_index,
            'pageSize': page_size
        }
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()

    # 消息推送-新建消息模版
    def oms_create_template(self, cookies_ua, msg_type=1, title='自动化测试系统消息', digest='自动化测试系统消息-默认封面，跳转百度',
                            content='https://www.baidu.com', app_type=1132, show_type=1, img_type=1,
                            img_url='https://t8oms.fuyoukache.com/default.png'):
        url = self.mk_url('oms', 'api/push/createTemplate')
        data = {
            'msgType': msg_type,  # 1:系统消息，2：活动消息
            'title': title,  # 标题
            'digest': digest,  # 摘要
            'content': content,  # 链接
            'appType': app_type,  # 1132:好运,3211:车队，2311:货主，3232:福佑专车
            'showType': show_type,  # 3:跳app首页；1：跳转指定链接
            'imgType': img_type,  # 1:默认封面，2:上传封面
            'imgUrl': img_url  # 封面url
        }
        print(data)
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()

    # 消息推送-消息推送发送
    def oms_push(self, scheduled_time, app_type, template_id, push_type, cookies_ua, id=''):
        url = self.mk_url('oms', 'api/push/push')
        push_param = {
            "scheduledTime": scheduled_time,
            'appType': app_type,
            'templateId': template_id,
            'pushType': push_type,
            'id': id
        }
        data = {
            'pushParam': json.dumps(push_param)
        }
        print(data)
        r = requests.post(url, data, cookies=cookies_ua)
        return r.json()
