#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 10:58
# @Author  : WangLei
# @FileName: config.py
# @Software: PyCharm


# bug模式
import os
from datetime import timedelta

DEBUG = True

# 数据库配置
DB = {
    "host": "192.168.10.19",
    # "host": "127.0.0.1",
    "port": 6033,
    "user": "root",
    "passwd": "root",
    "db": "ying_v3",
    "charset": "utf8mb4"
}

# session配置
SECRET_KEY = os.urandom(24)
# session过期时间为一个小时
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
