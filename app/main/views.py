#!/usr/bin/env python
# coding=utf-8

from flask import render_template, request, redirect, url_for
from flask import request, jsonify, session
import requests
# from flask_oauth import OAuth
import sys
import json

# reload(sys)
# 导入蓝本 main
from . import main


@main.route('/')
def index():

    return render_template('index.html', name=session.get('username'))


@main.route('/login')
def login():

    return render_template('login.html')


@main.route('/start')
def start():
    return render_template('starter.html')
