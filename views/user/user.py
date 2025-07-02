from flask import Flask,session,render_template,redirect,Blueprint,request,jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.databaseManage import query
import time
from utils.errorResponse import errorResponse
ub = Blueprint('user',__name__,url_prefix='/user',template_folder='templates')

@ub.route('/login', methods=['GET', 'POST'])
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

@ub.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    check_password = data.get('checkPassword')

    if password != check_password:
        return jsonify({'code': 400, 'msg': '两次密码不一致'}), 400

    # 检查用户名是否存在
    users = query('select username from user', [], 'select')
    print(users)
    if any(user[0] == username for user in users):
        return jsonify({'code': 400, 'msg': '该用户名已被注册'}), 400

    # 写入数据库
    create_time = time.strftime('%Y-%m-%d', time.localtime())
    query('''
        insert into user(username, password, createTime, authority)
        values (%s, %s, %s, %s)
    ''', [username, password, create_time, 'normal'])

    return jsonify({'code': 200, 'msg': '注册成功'}), 200

@ub.route('/logOut')
def logOut():
        session.clear()
        return redirect('/user/login')

@ub.route('/admin_register',methods=['GET','POST'])
def Admin_register():
    if request.method == 'GET':
        return render_template('admin_register.html')
    else:
        # 使用 JSON 数据而不是 form 数据
        data = request.get_json()
        if not data:
            return errorResponse('请求数据格式错误')
            
        password = data.get('password')
        check_password = data.get('checkPassword')
        username = data.get('username')
        verifycode = data.get('verifycode')
        
        if password != check_password:
            return errorResponse('两次密码不符合')

        if verifycode not in ['123456','654321']:
            return errorResponse('非法管理员码！')

        users = query('select username from admin_user',[],'select')
        # users 是元组列表，每个元组包含 (username,)
        if any(user[0] == username for user in users):
            return errorResponse('该用户名已被注册')
            
        else:
            time_tuple = time.localtime(time.time())
            query('''
                insert into admin_user(id,username,password,create_time,status) values(%s,%s,%s,%s,%s)
            ''',[verifycode, username, password, str(time_tuple[0]) + '-' + str(time_tuple[1]) + '-' + str(time_tuple[2]), 'active']
            )
        return jsonify({'code': 200, 'msg': '管理员注册成功'})
    

@ub.route('/admin_login', methods=['POST', 'GET'])
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

    # 如果需要校验 verifycode，可在此加逻辑

    session['username'] = username
    return jsonify({'code': 200, 'msg': '管理员登录成功'})