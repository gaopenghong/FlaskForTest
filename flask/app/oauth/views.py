#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, redirect, session, make_response
from . import oauth_blue
import requests
import codecs
import sys
from . import white_list
from flask_sqlalchemy import SQLAlchemy

from app import create_app, check_host

config_name = check_host()
app = create_app(config_name)
db = SQLAlchemy(app, session_options={"autoflush": False})  # 实例化


@oauth_blue.before_app_request
def login_auth():

    """
    请求前执行登录拦截
    """
    db.session.close()
    db.session.remove()
    session['path'] = request.url
    name = request.cookies.get('username')
    if request.path in white_list.white:
        return
    for url in white_list.white:
        # print(url)
        if url in request.path:
            return
    if 'username' in session:
        resp = make_response('cookie')
        if 'username' in session:
            resp.set_cookie('username', session['username'])
        return
    elif name:
        session['username'] = request.cookies.get('username')
        return
    else:
        return redirect('/login')


@oauth_blue.route('/cookie')
def set_cookie():
    resp = make_response('cookie')
    if 'username' in session:
        resp.set_cookie('username', session['username'])
        return resp
    else:
        return '{"msg":"写入cookie失败"}'


@oauth_blue.route('/delCookie')
def del_cookie():
    name = request.cookies.get('username')
    # print(name)
    if name:
        resp = make_response('delete_cookie')
        resp.delete_cookie('username')
        return resp
    else:
        return '{"msg":"删除cookie失败"}'


@oauth_blue.route('/oauth/login', methods=['GET', 'POST'])
def login():
    phone = request.values.get('phone')
    pwd = request.values.get('pwd')
    url = "https://ua.fuyoukache.com/api/uc/src/image/genCheckCodeRequest"
    res = requests.post(url)
    url1 = "https://ua.fuyoukache.com/api/uc/auth/login"

    params = {
        'userName': phone,
        'userPassword': pwd,
        'requestId': res.text,
        'checkCode': '1123'
    }
    res1 = requests.post(url1, params)

    data = res1.json()
    if data['status']['code'] == 99:
        return redirect("/login?msg=用户名或密码错误")
    elif data['status']['code'] == 0:
        name = data['data'][0]['name']
        resp = make_response('cookie')
        resp.set_cookie('username', name)
        session['username'] = name
        session['mobile'] = data['data'][0]['mobile']
        return redirect('/')


@oauth_blue.route('/oauth/logout')
def logout():
    name = request.cookies.get('username')
    if 'username' in session:
        session.pop('username', None)
    if name:
        resp = make_response('delete_cookie')
        resp.delete_cookie('username')
    return redirect("/login")
