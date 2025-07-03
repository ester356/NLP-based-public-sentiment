from flask import Flask,session,request,redirect,render_template
import re
from flask_socketio import SocketIO, emit
from routes.user_login import user
from routes.page import page_app


app = Flask(__name__)
app.secret_key = 'this is secret_key you know ?'

socketio = SocketIO(app)


app.register_blueprint(user)
app.register_blueprint(page_app)


@app.route('/')
def hello_world():  # put application's code here
    return redirect('http://127.0.0.1:5000/user/login')

@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    elif request.path in ['/user/login', '/user/register', '/user/admin_register', '/user/admin_login']:
        return
    elif session.get('username'):
        return
    return redirect('/user/login')

@app.route('/<path:path>')
def catch_all(path):
    return f"<h1>404 - Page Not Found</h1><p>Path '{path}' not found.</p>", 404

if __name__ == '__main__':
    # app.run()
    socketio.run(app, allow_unsafe_werkzeug=True,debug=True)
