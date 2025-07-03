from flask import Flask,session,render_template,redirect,Blueprint,request,jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.databaseManage import query
import time
from utils.errorResponse import errorResponse

template_folder_path = os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'user', 'templates')

# 创建登录相关的路由函数
def create_login_routes(blueprint):
    @blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        def filter_fn(user):
            return username == user[0] and password == user[1]  # 假设用户名在索引0，密码在索引1

        users = query('select username, password from user', [], 'select')
        login_success = list(filter(filter_fn, users))

        if not login_success:
            return jsonify({'code': 400, 'msg': '账号或密码错误'}), 400

        session['username'] = username
        return jsonify({'code': 200, 'msg': '登录成功'})

    @blueprint.route('/admin_login', methods=['POST', 'GET'])
    def admin_login():
        if request.method == 'GET':
            return render_template('admin_login.html')
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        verifycode = data.get('verifycode')  # 管理员id，若你有校验逻辑也放这里

        def filter_fn(user):
            return username == user[1] and password == user[2]  # 假设用户名在索引1，密码在索引2

        users = query('select id, username, password from admin_user', [], 'select')
        login_success = list(filter(filter_fn, users))

        if not login_success:
            return jsonify({'code': 400, 'msg': '账号或密码错误'}), 400

        session['username'] = username
        return jsonify({'code': 200, 'msg': '管理员登录成功'})

    @blueprint.route('/logOut')
    def logOut():
        session.clear()
        return redirect('/user/login')



