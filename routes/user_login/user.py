from flask import Flask,session,render_template,redirect,Blueprint,request,jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.databaseManage import query
import time
from utils.errorResponse import errorResponse
# 导入子路由
from .login import create_login_routes
from .register import create_register_routes

template_folder_path = os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'user', 'templates')
user = Blueprint('user',__name__,url_prefix='/user',template_folder=template_folder_path)

# 注册登录相关路由
create_login_routes(user)

# 注册注册相关路由
create_register_routes(user)

# 主用户路由的其他功能
@user.route('/')
def user_index():
    return redirect('/user/login')

@user.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect('/user/login')
    return render_template('dashboard.html')
