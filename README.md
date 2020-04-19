#环境安装

##1、安装python3.6
git clone https://gitlab.fuyoukache.com/qa/ftest.git

cd ftest

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

##2、启动
本地可以直接通过manage.py启动服务

python manage.py

##3、uwsgi启动
uwsgi config.ini

##4、uwsgi停止
uwsgi --stop uwsgi.pid

##5、查看状态
uwsgi --connect-and-read uwsgi.status

##6、查看log
uwsgi.log


# 框架简介
- main
- oauth: 权限、登录等
- stat
- static
   - bower_components
   - css: CSS
   - dist: 预编译Bootstrap包内的所有文件
   - fonts: 字体
   - img
   - js: JavaScript
- templates: 页面模板
   - tools: 各测试工具对应页（页面在此编写）
   - 404.html: 404页面
   - 500.html: 500页面
   - base.html: 页面基础框架
   - index.html: 首页
   - login.html: 登录页面
- tools
   - api: 接口列表（接口在此定义）
   - feature: 业务场景/测试工具（工具在此编写）
- util
- .gitignore: 代码提交时忽略文件
- config.py: 配置
- manage.py: 本地启动文件
- READEME.md:
- requirements.txt: 框架必备库



