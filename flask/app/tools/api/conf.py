import configparser
import os
project_path = os.path.dirname(os.path.dirname(__file__))


# 获取单节配置信息
def get_config_section(target_section):
    cf = configparser.ConfigParser()
    path=project_path
    cf.read(os.path.join(project_path, 'api/config/conf.ini'), encoding='utf-8')
    return cf.items(target_section)


# 获取单个配置信息
def get_config(target_section, target_option):
    cf = configparser.ConfigParser()
    cf.read(os.path.join(project_path, 'api/config/conf.ini'), encoding='utf-8')
    r = cf.get(target_section, target_option)
    return r
