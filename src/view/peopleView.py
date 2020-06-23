
from flask import Blueprint, render_template, request, jsonify, session, redirect,url_for
from src.service import peopleService
from src.until.epExcelutil import ExpExcel

people_bp = Blueprint('people', __name__)


@people_bp.route('/list', methods=['GET', 'POST'])
def list():
    curr_page = request.args.get('page', 1)
    condition = {}
    for key in request.args.to_dict():
        if key.startswith('select_') and request.args.to_dict()[key] != '':
            condition.setdefault(key.split('_', 1)[1], request.args.to_dict()[key])
    # 按条件区且分页
    people_list, html = peopleService.list(condition, request, curr_page, is_page=True)
    # 定义回传数据字典
    backdict = {'entityList': people_list, 'html': html, 'condition': request.args.to_dict() }
    return render_template('people/list.html', **backdict)


@people_bp.route('/edit/', methods=['GET', 'POST'])
def edit():
    condition = {'id': request.args.to_dict().get('Id')}
    people = peopleService.one(condition)
    backdict = {'data': people}
    return render_template('people/edit.html', **backdict)


@people_bp.route('/save', methods=['GET', 'POST'])
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
    result, status = peopleService.save(condition)
    if result:
        return redirect(url_for('people.list'))
    return redirect(url_for('people.list'))
    
@people_bp.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('people/view.html')



@people_bp.route('/delete', methods=['GET', 'POST'])
def delete():
    condition = request.form.to_dict()
    result = peopleService.delete(condition)
    if result:
        return jsonify({'code': 200, 'message': "删除成功!"})


@people_bp.route('/excelload', methods=['GET', 'POST'])
def excelload():
    datalist = [{'checkdate': 'e232'}]
    thead = {'checkdate': '考勤时间'}
    response = ExpExcel('aa', datalist, thead).get_Excel_response()
    return response