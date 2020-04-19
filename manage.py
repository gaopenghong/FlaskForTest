#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 启动脚本
# --------------------------------------
#    When         Who        What
# --------------------------------------
# 2017-9-6    liuchunfu      程序的入口，启动脚本

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from app import create_app, check_host

config_name = check_host()
print(config_name)
app = create_app(config_name)
db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化

# 创建数据库迁移
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 创建数据库
@manager.command
def create():
    db.create_all()
    return '数据库已创建'


def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    # app.run(host="192.168.2.68", port=8003, threaded=True, debug=True)
    app.run(host="localhost", port=1087, threaded=True, debug=True)
