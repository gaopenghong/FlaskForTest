import json

from app.tools.api.api_im_configure import ImConfigure
from app.tools.api.api_ua import ApiUa


class BatchOperationSensitiveWords(ImConfigure, ApiUa):

    def __init__(self, environment):
        super().__init__(environment)
        self.r_qrc_id = None
        self.env = environment
        # 定义全局的默认导入数
        self.num = 10
        r_ua_request_id = self.ua_generate_check_code()
        user_mobile = '16888888888'
        # user_mobile = self.admin_mobile
        password = "Ab@123456789"
        print("env:" + self.env + "user_mobile:" + user_mobile + "request_id:" + r_ua_request_id)
        # 检查账号
        self.r_check = self.base_check()
        print(self.r_check)
        self.r_cookies = self.ua_login(user_mobile, password, r_ua_request_id)
        print("环境变量是:", self.env, "登录返回结果:", self.r_cookies)
        # 获取快捷回复类别id
        self.r_qrc_id = self.get_data_id()
        print("系统中快捷回复类别的id:", self.r_qrc_id)

    # 单独添加方法
    def batch_add(self, word_name, num, task_im_type_id):
        if num and task_im_type_id is not None:
            self.json = self.sensitive_word_add(word_name, self.r_cookies)
            return json.dumps(self.json)
        else:
            return "参数为空!!!"

    # 批量添加敏感词方法
    def batch_add_words(self, word_name, num, task_im_type_id):
        if int(task_im_type_id) == 0:
            print("类型为敏感词!")
            if word_name is not None:
                if int(num) <= 30:
                    print("开始输入敏感词!!!")
                    i = 0
                    for i in range(int(num)):
                        i = i + 1
                        self.json = self.sensitive_word_add(word_name + str(i), self.r_cookies)
                        # print(json.dumps(self.json))
                        print(self.json.get('status').get('desc'))
                    return str(self.json.get('status').get('desc'))
                else:
                    return "输入创建数量超过" + str(num) + '最大可支持创建30'
            else:
                return "输入参数为空"
        else:
            return "其它类型"

    # 批量添加敏感词/违禁词方法
    def batch_add_words_1(self, word_name, num, task_im_type_id):
        if self.r_cookies != {}:
            if int(task_im_type_id) == 0:
                print("类型为敏感词!")
                if word_name is not None:
                    if int(num) <= 30:
                        print("开始输入敏感词!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.sensitive_word_add(word_name + str(i), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("敏感词批量添加:" + self.json.get('status').get('desc'))
                        return str("敏感词批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            elif int(task_im_type_id) == 1:
                print("类型为违禁词")
                if word_name is not None:
                    if int(num) <= 30:
                        print("开始输入敏感词!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.prohibited_word_add(word_name + str(i), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("违禁词批量添加:" + self.json.get('status').get('desc'))
                        return str("违禁词批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            else:
                return "其它类型"
        else:
            return "登录失败,请检查!!! 请检查当前环境是否存在1688888888客服测试账号!!!"

    # 跟据不同角色批量添加标签方法
    def batch_add_words_2(self, task_im_role, tag_name, num):
        if self.r_cookies != {}:
            if task_im_role == 'driver':
                print("类型为司机!")
                if tag_name is not None:
                    if int(num) <= 30:
                        print("开始输入司机角色标签!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.chat_tag_add(tag_name + str(i), str(task_im_role), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("司机标签批量添加:" + self.json.get('status').get('desc'))
                        return str("司机标签批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            elif task_im_role == 'shipper':
                print("类型为货主")
                if tag_name is not None:
                    if int(num) <= 30:
                        print("开始输入货主角色标签!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.chat_tag_add(tag_name + str(i), str(task_im_role), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("货主标签批量添加:" + self.json.get('status').get('desc'))
                        return str("货主标签批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            else:
                return "其它类型"
        else:
            return "登录失败,请检查!!! 请检查当前环境是否存在1688888888客服测试账号!!!"

    def batch_add_words_3(self, task_im_role, qr_name, num):
        if self.r_cookies != {}:
            if task_im_role == 'driver':
                print("类型为司机!")
                if qr_name is not None:
                    if int(num) <= 30:
                        print("开始输入司机快捷回复!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.quick_reply_add("driver", self.r_qrc_id, qr_name + str(i), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("司机快捷回复批量添加:" + self.json.get('status').get('desc'))
                        return str("司机快捷回复批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            elif task_im_role == 'shipper':
                print("类型为货主")
                if qr_name is not None:
                    if int(num) <= 30:
                        print("开始输入货主角色快捷回复!!!")
                        i = 0
                        for i in range(int(num)):
                            i = i + 1
                            self.json = self.quick_reply_add("shipper", self.r_qrc_id, qr_name + str(i), self.r_cookies)
                            # print(json.dumps(self.json))
                            r = json.loads(json.dumps(self.json))
                            # print(r['status'])
                            if r['status'] == 404:
                                return "该环境中没有部署IM服务!!!请部署后再次尝试添加!!!"
                            else:
                                print("快捷回复批量添加:" + self.json.get('status').get('desc'))
                        return str("快捷回复批量添加:" + self.json.get('status').get('desc'))
                    else:
                        return "输入创建数量超过" + str(num) + '最大可支持创建30'
                else:
                    return "输入参数为空"
            else:
                return "其它类型"
        else:
            return "登录失败,请检查!!! 请检查当前环境是否存在1688888888客服测试账号!!!"

    #  批量添加方法
    def batch_adds(self, word_name, num, task_im_type_id):
        i = 0
        if word_name and num is not None:
            if task_im_type_id == 0:
                while i <= int(num):
                    i = i + 1
                    print("sw_name:", word_name + str(i))
                    print("添加数据:", self.json)
                    return self.json
                else:
                    print("不是敏感词参数!,参数出错!")
            else:
                print("不是敏感词类型!!!", task_im_type_id)
        else:
            print("参数名或参数为空,参数为空时值默认为10,请添加参数名和参数!!!")
            # num = 10
            return self.batch_add(word_name + str(num), self.r_cookies)

    # 根据不同角色批量创建快捷回复
    def get_data_id(self):
        pass
        self.json = self.quick_reply_category_list('1', '30', self.r_cookies)
        print(self.json.get('data'))
        json_data = self.json.get('data')
        if json_data is not None:
            for i in range(len(json_data)):
                print(json_data[i].get('name'))
                if json_data[i].get('name') == 'qrc':
                    print(json_data[i].get('id'))
                    self.r_qrc_id = json_data[i].get('id')
                    print("获取的id:", self.r_qrc_id)
                    break
                else:
                    print("没有找到名为'qrc'的快捷回复类别!!!")
                    self.quick_reply_category_add('qrc', self.r_cookies)
                    self.get_data_id()
                    break
            return self.r_qrc_id
        else:
            return '查询快捷回复类别为空!!!'


if __name__ == '__main__':
    # bosw = BatchOperationSensitiveWords("t3")
    # res = bosw.batch_add_words("aa", 4, 0)
    # print("*****", res)
    # bosw.batch_add_words_2("aaa", 3, "shipper")
    # bosw.batch_add_words_3("shipper", '测试一下', 3)
    pass
