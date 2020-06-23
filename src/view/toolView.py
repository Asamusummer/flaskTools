#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/18 17:01
# @Author  : WangLei
# @FileName: toolView.py
# @Software: PyCharm


from flask import Blueprint, jsonify

from src.service import toolServece

tool_bp = Blueprint('tool', __name__)


@tool_bp.route('/set', methods=['GET', 'POST'])
def set():
    table_name = 'people'
    result = toolServece.get_table_comment(table_name)
    if result:
        return jsonify({"code": 200, 'message': "文件初始化成功!"})
