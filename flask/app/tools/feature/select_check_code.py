from app.tools.api.api_bms import get_port
from app.tools.api.base import Base
from app.util.ssh_conf import remote_database


class SelectCheckCode(Base):
    def __init__(self, environment):
        self.env = environment

    # 查询验证码
    def select_check_code(self, database_name, mobile):
        port = get_port(self.env)
        env = self.env
        if database_name == 'gold_apple':
            sql = "select code from checkcode where requestId='" + str(mobile) + "'"
        else:
            sql = "select code from check_code where requestId='" + str(mobile) + "'"
        r = remote_database(env, database_name, sql)
        if r == '连接数据库失败':
            return "请检查数据库名称是否正确"
        else:
            try:
                code = r[0][0]
                return code
            except Exception as e:
                print(e)
                return "手机号对应的验证码不存在"
