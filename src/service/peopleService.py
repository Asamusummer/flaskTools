
from src.until.dbUntil import SQLManager
from src.until.pageUtils import Pagination
# 功能描述: 针对用户表根据条件进行数据的查询，并是否要分页
# 参数说明: condition(筛选条件)、request(默认请求)、page(当前页码)、 is_page(是否需要分页)
# 返回值: list(用户表表数据)
def list(condition=None, request=None, page=None, is_page=False):
    countsql = "select count(*) all_count from people a where 1=1 "
    sql = "select * from people a where 1=1 "
    # 如果有条件筛选
    if condition:
        for key in condition.keys():
            sql = sql + " and " + key + "=" + "\'" + str(condition.get(key)) + "\'"
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

# 功能说明: 根据条件回去单个用户表的信息数据
# 参数说明: condition(查询条件)
# 返回值: 单个用户表的信息
def one(condition):
    sql = 'select * from people where 1=1 '
    for key in condition.keys():
        sql = sql + " and " + key + "=" + "\'" + str(condition.get(key)) + "\'"
    obj = SQLManager.get_one(sql)
    return obj


# 功能说明: 根据条件进行用户表信息的修改或添加
# 参数说明: condition(条件)
# 注意: 根据condition是否存在pk来进行判断是更新还是创建，没有pk就是创建，有就是更新
# 返回值: "update" or "create"
def save(condition):
    if 'pk' in condition.keys():  # 更新保存操作
        sql = " update people set "
        if condition:
            for key in condition.keys():
                if key != 'pk':
                    sql = sql + key + "=" + "\'" + str(condition.get(key)) + "\'" + ","
        sql = sql[:-1]
        sql = sql + " where id=" + str(condition.get('pk'))
        result = SQLManager.moddify(sql)
        if result == 0:
            return False, "更新失败"
        if result == 1:
            return True, "更新成功"
    else:  # 创建保存操作
        sql = " insert into people("
        for key in condition.keys():
            sql = sql + key + ","
        sql = sql[:-1] + " )" + " values ("
        for key in condition.keys():
            sql = sql + "\'" + str(condition.get(key)) + "\'" + " ,"
        sql = sql[:-1] + " )"
        result = SQLManager.moddify(sql)
        if result == 0:
            return False, "创建失败"
        if result == 1:
            return True, "创建成功"


# 功能说明: 根据条件进行用户表数据的删除
# 参数说明: condition(条件)
# 返回值: 成功还是失败
def delete(condition):
    sql = ' delete from people where 1=1 '
    for key in condition.keys():
        sql = sql + " and " + key + "=" + "\'" + str(condition.get(key)) + "\'"
    SQLManager.moddify(sql)
    return True

    