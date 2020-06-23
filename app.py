from flask import Flask, session, request, redirect, render_template
from config import config
from src.view import toolView,peopleView

app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
app.register_blueprint(toolView.tool_bp, url_prefix='/tool')
app.register_blueprint(peopleView.people_bp, url_prefix='/people')


# 在请求每个路由之前进行用户登录认证(类似中间件)
# @app.before_request
# def user_bp_before_request():
#     if request.path == '/login':
#         return None
#     user = session.get('username')
#     if user:
#         return None
#     return redirect('/login')

@app.route('/title', methods=['GET'])
def title():
    title = {
        'title': 'nihao'
    }
    return render_template('title.html', title=title)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# 通用登录接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        session['username'] = 'wl'
        return '登录成功'


# 通用退出接口
@app.route('/quit', methods=['GET', 'POST'])
def quit():
    session.pop('username')
    return "退出成功"


# 项目启动主程序入口
if __name__ == '__main__':
    app.run()
