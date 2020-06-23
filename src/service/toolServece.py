#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/18 16:47
# @Author  : WangLei
# @FileName: toolServece.py
# @Software: PyCharm
# 功能说明: 获取数据库的字段说明
from src.until.dbUntil import SQLManager
import os


# 获取对应表的所有的字段
def get_all_titless(t_name):
    sql = f"""
        select column_name, column_comment from information_schema.columns where table_schema ='ying_v3' 
        and table_name = '{t_name}' 
    """
    titles = SQLManager.get_list(sql)
    return titles

# 获取数据的字段标题名称
def get_title(condition, t_name):
    sql = f"""
        select * from (
        select column_name, column_comment from information_schema.columns where table_schema ='ying_v3' 
        and table_name = '{t_name}' ) aa where
    """
    condit_list = condition.split(',')
    for values in condit_list:
        sql = f"{sql} aa.column_name='{values}' or"
    sql = sql[:-3]
    titles = SQLManager.get_list(sql)
    titles.append({'column_name': 'done', 'column_comment': '操作'})
    return titles


# 获取数据的字段标题名称
def get_done_title(condition, t_name):
    sql = f"""
        select * from (
        select column_name, column_comment from information_schema.columns where table_schema ='ying_v3' 
        and table_name = '{t_name}' ) aa where
    """
    condit_list = condition.split(',')
    for values in condit_list:
        sql = f"{sql} aa.column_name='{values}' or"
    sql = sql[:-3]
    search_titles = SQLManager.get_list(sql)
    return search_titles


# 获取数据库表名和comment描述,并根据描述去除需要渲染的数据
def get_table_comment(t_name):
    sql = f"""
        SELECT table_name name,TABLE_COMMENT value FROM INFORMATION_SCHEMA.TABLES WHERE table_type='base table'
        and table_schema = 'ying_v3'  and table_name="{t_name}"
    """
    table_commemts = SQLManager.get_one(sql)
    # 获取数据库表的coment，操作dic
    table_comment, done_dic = table_commemts.get('value').split(':', 1)
    # 根据数据库表名
    create_template(table_commemts.get('name'), table_comment, eval(done_dic))
    return True


# 获取项目的根目录的文件路径
def get_root_path():
    # 首先获取当前文件的路径
    current_file_path = os.path.dirname(__file__)
    # 获取项目的根目录
    root_path = os.path.dirname(os.path.dirname(current_file_path))
    return root_path


# 根据表名生成模板下模块目录文件
def create_template(table_name, table_comment, done_dic):
    root_path = get_root_path()
    # 模板存放目录
    template_folder = os.path.join(root_path, 'templates')
    # 操作的生成的数据表目录
    table_folder = os.path.join(template_folder, table_name)
    # 判断该目录下是否存在这个文件
    if not os.path.exists(table_folder):
        os.mkdir(table_folder)
    # 如果存在那么接下来创建三个文件, list.html、edit.html、view.html
    # 创建list.html文件
    # 获取对应的list页面显示的字段和搜索的条件
    list_title = done_dic.get('list')
    search_condit = done_dic.get('search')
    edit_condit = done_dic.get('edit')
    # 如果没有list_title，就渲染出了id以外的其他字段显示
    if list_title == '':
        titles = get_all_titless(table_name)
        all_list = filter(lambda x: not x.startswith("id"), [obj.get('column_name') for obj in titles])
        list_title = ','.join(list(all_list))
    if search_condit == '':
        titles = get_all_titless(table_name)
        all_list = filter(lambda x: not x.startswith("id"), [obj.get('column_name') for obj in titles])
        search_condit = ','.join(list(all_list))
    if edit_condit == '':
        titles = get_all_titless(table_name)
        all_list = filter(lambda x: not x.startswith("id"), [obj.get('column_name') for obj in titles])
        edit_condit = ','.join(list(all_list))
    create_list_html_file(table_folder, list_title, search_condit, table_name, table_comment)
    # 创建edit.html文件
    create_edit_html_file(table_folder, edit_condit, table_name)
    # 创建view.html文件
    create_view_html_file(table_folder, edit_condit, table_name)
    # 创建service.py文件
    create_service_file(root_path, table_name, table_comment)
    # 创建view.py文件
    create_view_file(root_path, table_name)
    return True


# 创建lisl.html文件
def create_list_html_file(path, list_title, search_condit, table_name, table_comment):
    titles = get_title(list_title, table_name)
    search = get_done_title(search_condit, table_name)
    ttile_value = get_done_title(list_title, table_name)
    # 写入内容的路径
    content = f"""
!% include "include/header.html" %*
<div class="list_top col-xs-12" style="padding-left: 1px;">
    <label>{table_comment}管理</label>
</div>
<hr class="col-xs-12"/>
<div class="searchback col-xs-12">
    <form class="searchform col-xs-12" autocomplete="off" id="af" action="" method="get">
    """
    content = content.replace('!', "{")
    content = content.replace('*', "}")
    for search_o in search:
        content = f"""{content}
        <div class="form-style">
        <p style="text-align: center">{search_o.get("column_comment")}:</p>
        <input class="col-xs-10" type="text" name="select_{search_o.get('column_name')}" value="!condition.select_{search_o.get('column_name')}*"/>
        </div>
        """
    content = content.replace('!', "{{")
    content = content.replace('*', "}}")
    thrid_content = f"""
        <div class="form-style" style="margin-right: 0px;">
        <button type="submit">查询</button>
        <button type="button" style="margin-left: 10px;" onclick="showModalDialog('/{table_name}/view', 'modal-lg')">添加</button>
        </div>
    </form>
</div>
<hr class="col-xs-12"/>
<div class="table-responsive listheight col-xs-12" style="padding-bottom: 50px;">
<table class="table" style="table-layout:fixed; text-align: center">
  <thead>
   <tr>
  """
    content = f"{content} {thrid_content}"
    for title in titles:
        content = f"{content} <th style='width:200px;'>{title.get('column_comment')}</th> \n"
    second_content = """
  </tr>
  </thead>
  <tbody>
  {% for data in entityList %}
    <tr>"""
    content = f"{content}{second_content}"
    for title in ttile_value:
        content = f"""{content}
            <td style='width:200px'>!data.{title.get('column_name')}*</td>"""
    content = content.replace('!', "{{")
    content = content.replace('*', "}}")
    four_content = f"""
      <td>
        <div class="btn-group">
          <button class="btn btn-primary" onclick="showModalDialog('/{table_name}/edit?Id=' + !!data.id **,'modal-lg')">编辑
          </button>
          <button class="btn btn-danger" onclick="deleteObj('!! data.id **', '/{table_name}/delete')">删除</button>
        </div>
      </td>
    </tr>
  !% endfor %*
  </tbody>
</table>
<div class="row">
  <div class="col-sm-12 col-md-7 col-md-offset-5" style="margin: 0 36%">
    !! html |safe **
  </div>
</div>
</div>
<script type="text/javascript">
</script>
!% include "include/footer.html" %*
        """
    content = f"{content}{four_content}"
    content = content.replace('!', '{')
    content = content.replace('*', '}')
    content = content.replace('!!', '{{')
    content = content.replace('**', '}}')
    with open(os.path.join(path, 'list.html'), 'w', encoding='utf-8') as f:
        f.write(content)


# 创建edit.html文件
def create_edit_html_file(path, edit_condit, table_name):
    edit_con = get_done_title(edit_condit, table_name)
    # 写入文件内容
    content = f"""
    <div class="modal-header">
  <h4 class="modal-title" style="line-height: 1.2;font-size: 1.2rem;"><i class="fa fa-tags"></i>编辑信息</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
    <span aria-hidden="true">×</span>
  </button>
</div>
<div class="modal-body">
  <form id="editInfoForm" class="searchform col-xs-12" autocomplete="off" action="/{table_name}/save" method="POST"
        enctype="multipart/form-data">
    <table class="table-bordered table table-hover table-striped table-dialog">
    <tr>
        <input hidden name="pk" id="pk" value="!data.id*">
    """
    content = content.replace('!', "{{")
    content = content.replace('*', "}}")
    for edit in edit_con:
        content = f"""{content}
           <td style="text-align: center">{edit.get('column_comment')}</td>
           <td><input class="form-control" type="text" name="edit_{edit.get('column_name')}" value="!data.{edit.get('column_name')}*"/></td>
        """
    content = content.replace('!', "{{")
    content = content.replace('*', "}}")
    second_content = """
    </tr>
    </table>
  </form>
</div>
<div class="row">
  <div class="col-md-6 col-md-offset-6" style="margin: 10px 45%;">
    <button class="btn btn-primary" id="saveInfo">&nbsp;&nbsp;&nbsp;&nbsp;保存&nbsp;&nbsp;&nbsp;&nbsp;</button>
  </div>
</div>
<script src="/static/js/validator.js"></script>
<script type="text/javascript">
  var f = document.getElementById("editInfoForm");
  $('#saveInfo').click(function () {"""
    content = f"{content}{second_content}"
    for edit in edit_con:
        content = f"""{content}
        $('input[name="edit_{edit.get('column_name')}"]').attr("datatype", "Require").attr("msg", "{edit.get('column_comment')}不能为空");\n
        """
    third_content = """
    if (Validator.Validate(f, 1)){
      $("#saveInfo").attr("disabled", true);
      f.submit();
    }
    return false;
  })
</script>

    """
    content = f"{content}{third_content}"
    with open(os.path.join(path, 'edit.html'), 'w', encoding='utf-8') as f:
        f.write(content)


# 创建View.html文件
def create_view_html_file(path, edit_condit, table_name):
    edit_con = get_done_title(edit_condit, table_name)
    # 写入文件的内容
    content = f"""
        <div class="modal-header">
      <h4 class="modal-title" style="line-height: 1.2;font-size: 1.2rem;"><i class="fa fa-tags"></i>添加信息</h4>
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">×</span>
      </button>
    </div>
    <div class="modal-body">
      <form id="editInfoForm" class="searchform col-xs-12" autocomplete="off" action="/{table_name}/save" method="POST"
            enctype="multipart/form-data">
        <table class="table-bordered table table-hover table-striped table-dialog">
        <tr>
        """
    for edit in edit_con:
        content = f"""{content}
               <td style="text-align: center">{edit.get('column_comment')}</td>
               <td><input class="form-control" type="text" name="edit_{edit.get('column_name')}" value=""/></td>
            """
    second_content = """
        </tr>
        </table>
      </form>
    </div>
    <div class="row">
      <div class="col-md-6 col-md-offset-6" style="margin: 10px 45%;">
        <button class="btn btn-primary" id="saveInfo">&nbsp;&nbsp;&nbsp;&nbsp;保存&nbsp;&nbsp;&nbsp;&nbsp;</button>
      </div>
    </div>
    <script src="/static/js/validator.js"></script>
    <script type="text/javascript">
      var f = document.getElementById("editInfoForm");
      $('#saveInfo').click(function () {"""
    content = f"{content}{second_content}"
    for edit in edit_con:
        content = f"""{content}
            $('input[name="edit_{edit.get('column_name')}"]').attr("datatype", "Require").attr("msg", "{edit.get('column_comment')}不能为空");\n
            """
    third_content = """
        if (Validator.Validate(f, 1)){
          $("#saveInfo").attr("disabled", true);
          f.submit();
        }
        return false;
      })
    </script>

        """
    content = f"{content}{third_content}"
    with open(os.path.join(path, 'view.html'), 'w', encoding='utf-8') as f:
        f.write(content)


# 创建单表的service和view文件
def create_service_file(root_path, table_name, table_comment):
    # 找到service文件的目录
    service_path = os.path.join(os.path.join(root_path, 'src'), 'service')
    # 写入的文件内容
    content = f"""
from src.until.dbUntil import SQLManager
from src.until.pageUtils import Pagination
# 功能描述: 针对{table_comment}根据条件进行数据的查询，并是否要分页
# 参数说明: condition(筛选条件)、request(默认请求)、page(当前页码)、 is_page(是否需要分页)
# 返回值: list({table_comment}表数据)
def list(condition=None, request=None, page=None, is_page=False):
    countsql = "select count(*) all_count from {table_name} a where 1=1 "
    sql = "select * from {table_name} a where 1=1 "
    # 如果有条件筛选
    if condition:
        for key in condition.keys():
            sql = sql + " and " + key + "=" + "\\'" + str(condition.get(key)) + "\\'"
    # 如果需要分页
    if is_page:
        all_count = SQLManager.get_one(countsql).get('all_count')
        page_obj = Pagination(page, all_count, request.path, request.args)
        sql = sql + " limit " + str(page_obj.start) + "," + str(page_obj.per_page_count)
        list = SQLManager.get_list(sql)
        return list, page_obj.page_html()
    # 如果不需要分页就查询所有
    list = SQLManager.get_list(sql)
    return list

# 功能说明: 根据条件回去单个{table_comment}的信息数据
# 参数说明: condition(查询条件)
# 返回值: 单个{table_comment}的信息
def one(condition):
    sql = 'select * from {table_name} where 1=1 '
    for key in condition.keys():
        sql = sql + " and " + key + "=" + "\\'" + str(condition.get(key)) + "\\'"
    obj = SQLManager.get_one(sql)
    return obj


# 功能说明: 根据条件进行{table_comment}信息的修改或添加
# 参数说明: condition(条件)
# 注意: 根据condition是否存在pk来进行判断是更新还是创建，没有pk就是创建，有就是更新
# 返回值: "update" or "create"
def save(condition):
    if 'pk' in condition.keys():  # 更新保存操作
        sql = " update {table_name} set "
        if condition:
            for key in condition.keys():
                if key != 'pk':
                    sql = sql + key + "=" + "\\'" + str(condition.get(key)) + "\\'" + ","
        sql = sql[:-1]
        sql = sql + " where id=" + str(condition.get('pk'))
        result = SQLManager.moddify(sql)
        if result == 0:
            return False, "更新失败"
        if result == 1:
            return True, "更新成功"
    else:  # 创建保存操作
        sql = " insert into {table_name}("
        for key in condition.keys():
            sql = sql + key + ","
        sql = sql[:-1] + " )" + " values ("
        for key in condition.keys():
            sql = sql + "\\'" + str(condition.get(key)) + "\\'" + " ,"
        sql = sql[:-1] + " )"
        result = SQLManager.moddify(sql)
        if result == 0:
            return False, "创建失败"
        if result == 1:
            return True, "创建成功"


# 功能说明: 根据条件进行{table_comment}数据的删除
# 参数说明: condition(条件)
# 返回值: 成功还是失败
def delete(condition):
    sql = ' delete from {table_name} where 1=1 '
    for key in condition.keys():
        sql = sql + " and " + key + "=" + "\\'" + str(condition.get(key)) + "\\'"
    SQLManager.moddify(sql)
    return True

    """
    with open(os.path.join(service_path, f'{table_name}Service.py'), 'w', encoding='utf-8') as f:
        f.write(content)


# 创建view层模板文件
def create_view_file(root_path, table_name):
    view_path = os.path.join(os.path.join(root_path, 'src'), 'view')
    content = """
from flask import Blueprint, render_template, request, jsonify, session, redirect,url_for
from src.service import &Service

&_bp = Blueprint('&', __name__)


@&_bp.route('/list', methods=['GET', 'POST'])
def list():
    curr_page = request.args.get('page', 1)
    condition = {}
    for key in request.args.to_dict():
        if key.startswith('select_') and request.args.to_dict()[key] != '':
            condition.setdefault(key.split('_', 1)[1], request.args.to_dict()[key])
    # 按条件区且分页
    &_list, html = &Service.list(condition, request, curr_page, is_page=True)
    # 定义回传数据字典
    backdict = {'entityList': &_list, 'html': html, 'condition': request.args.to_dict() }
    return render_template('&/list.html', **backdict)


@&_bp.route('/edit/', methods=['GET', 'POST'])
def edit():
    condition = {'id': request.args.to_dict().get('Id')}
    & = &Service.one(condition)
    backdict = {'data': &}
    return render_template('&/edit.html', **backdict)


@&_bp.route('/save', methods=['GET', 'POST'])
def save():
    recv = request.form.to_dict()
    condition = {}
    for key in recv:
        if key == 'pk':
            condition.setdefault(key, recv[key])
        if key.startswith('edit_'):
            value = recv[key]
            key = key.split('_', 1)[1]
            condition.setdefault(key, value)
    result, status = &Service.save(condition)
    if result:"""
    second_content = f"""
        return redirect(url_for('{table_name}.list'))
    return redirect(url_for('{table_name}.list'))
    """
    content = f"{content}{second_content}"
    third_content = """
@&_bp.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('&/view.html')



@&_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    condition = request.form.to_dict()
    result = &Service.delete(condition)
    if result:
        return jsonify({'code': 200, 'message': "删除成功!"})

    """
    content = f"{content}{third_content}"
    content = content.replace('&', table_name)
    with open(os.path.join(view_path, f'{table_name}View.py'), 'w', encoding='utf-8') as f:
        f.write(content)
