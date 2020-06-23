#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 11:26
# @Author  : WangLei
# @FileName: sqltools.py
# @Software: PyCharm
import pymysql
from config.config import DB

from DBUtils.PooledDB import PooledDB

POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    maxshared=3,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host=DB["host"],
    port=DB["port"],
    user=DB["user"],
    password=DB["passwd"],
    database=DB["db"],
    charset=DB["charset"]
)


class SQLManager:

    # 初始化实例方法
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    @classmethod
    def connect(cls):
        cls.conn = POOL.connection()
        cls.cursor = cls.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cls.cursor, cls.conn

    @classmethod
    def get_list(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        cls.close()
        return result

    # 查询单条数据
    @classmethod
    def get_one(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cls.close()
        return result

    # 执行单条SQL语句
    # 支持执行报错事务回滚操作
    @classmethod
    def moddify(cls, sql, args=None):
        cursor, coon = cls.connect()
        flag = 0    # 标识数据执行成功的状态信息
        try:
            cursor.execute(sql, args)
            flag = 1
        except Exception as e:
            print(e)
            coon.rollback()
            flag = 0
        coon.commit()
        cls.close()
        return flag

    # 执行多条SQL语句
    @classmethod
    def multi_modify(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.executemany(sql, args)
        coon.commit()
        cls.close()

    # 创建单条记录的语句
    @classmethod
    def create(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        coon.commit()
        last_id = cursor.lastrowid
        cls.close()
        return last_id

    # 关闭数据库cursor和连接
    @classmethod
    def close(cls):
        cursor, coon = cls.connect()
        cursor.close()
        coon.close()

    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
