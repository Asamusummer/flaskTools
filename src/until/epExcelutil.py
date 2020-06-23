#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/28 11:12
# @Author  : WangLei
# @FileName: epExcelutil.py
# @Software: PyCharm
from io import BytesIO
import xlwt as xlwt
from xlwt import Workbook
from flask import make_response

"""
封装导出excel的模板，传入三个参数
:param filename 导出的文件名称
:param data_list 数据格式 [{},{},{},{},……] [{'name': 'wanglei', 'age': 19, 'addr': '上海'},……]
:param thead 表头数据 {'name': '姓名', 'age': '年龄', 'addr': '地址'}
:import: 重要说明 :表头的key值必须要和数据格式的每个对象的key值对应！！！

:methods init_style() 定义表格样式方法
:methods handle_Data() 处理表头数据格式
:methods set_width() 处理单元格的宽度
:methods get_Excel_load() 导出数据表格至当前工作目录下
:methods get_Excel_response() 导出数据表格可供前端进行下载
"""


class ExpExcel:
    __slots__ = ("file_name", "data_list", "thead")

    def __init__(self, filename, datalist, thead):
        self.file_name = filename
        self.data_list = datalist
        self.thead = thead
        self.handler_thead()

    def init_style(self, name, height, blod=False):
        """
        定义excel的样式
        :return:
        """
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = blod
        font.color_index = 4
        font.height = height
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al
        style.font = font
        style.borders = borders
        return style

    def handler_thead(self):
        """
        处理需要导出的数据字段,根据定制的表头导出对应的数据字段
        :return:
        """
        # 取出定制表格的所有的key
        keys = [i for i in self.thead.keys()]
        new_data = []
        # 根据取到的key,重新定义需要导出的data_list
        for obj in self.data_list:
            data = {}
            for k in keys:
                if k in obj.keys():
                    data[k] = obj.get(k)
            new_data.append(data)
        return new_data

    # 获取字符串长度，一个中文的长度为2
    def len_byte(self, value):
        length = len(value)
        utf8_length = len(value.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        return int(length)

    def set_width(self):
        """
        获取数据项中最大的宽度，作为写入的宽度
        :return:
        """
        col_width = []
        for i in range(len(self.handler_thead())):
            for k, v in enumerate(self.handler_thead()[i]):
                col_width.append(self.len_byte(str(self.handler_thead()[i].get(v))))
        return max(col_width)

    def get_Excel_load(self):
        """
        导出excel到当前目录
        :return:
        """
        # 先创建工作簿
        wx = Workbook(encoding='utf-8')
        w = wx.add_sheet(self.file_name)
        # 初始化表头数据
        for key, value in enumerate(self.thead):
            w.write(0, key, self.thead.get(value), self.init_style('Times New Roman', 250, True))
            w.col(key).width = 300 * (self.set_width() + 2)

        tall_style = xlwt.easyxf('font:height 400')
        w.row(0).set_style(tall_style)
        excel_row = 1
        # 进行数据填充
        if self.handler_thead():
            for obj in self.handler_thead():
                for k, v in enumerate(obj):
                    w.write(excel_row, k, obj.get(v), self.init_style('Times New Roman', 250, False))
                    tall_style = xlwt.easyxf('font:height 300')
                    w.row(excel_row).set_style(tall_style)
                excel_row += 1
            wx.save(f'./{self.file_name}.xls')
        else:
            wx.save(f'./{self.file_name}.xls')

    def get_Excel_response(self):
        """
        导出数据excel到前端可下载
        :return:
        """
        wx = Workbook(encoding='utf-8')
        w = wx.add_sheet(self.file_name)
        # 初始化表头数据
        for key, value in enumerate(self.thead):
            w.write(0, key, self.thead.get(value), self.init_style('Times New Roman', 250, True))
            w.col(key).width = 300 * (self.set_width() + 2)

        tall_style = xlwt.easyxf('font:height 400')
        w.row(0).set_style(tall_style)
        excel_row = 1
        # 进行数据填充
        if self.handler_thead():  # 如果有数据
            for obj in self.handler_thead():
                for k, v in enumerate(obj):
                    w.write(excel_row, k, obj.get(v), self.init_style('Times New Roman', 250, False))
                    tall_style = xlwt.easyxf('font:height 300')
                    w.row(excel_row).set_style(tall_style)
                excel_row += 1
            output = BytesIO()
            wx.save(output)
            output.seek(0)
            response = make_response(output.getvalue())
            output.close()
            response.headers["Content-Disposition"] = f"attachment;filename={self.file_name}.xls"
            response.headers["Content-Type"] = 'application/x-xls'
            return response
        else:
            output = BytesIO()
            wx.save(output)
            output.seek(0)
            response = make_response(output.getvalue())
            output.close()
            response.headers["Content-Disposition"] = f"attachment;filename={self.file_name}.xls"
            response.headers["Content-Type"] = 'application/x-xls'
            return response
