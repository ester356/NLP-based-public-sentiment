import flask




app = Flask(__name__)
app.secret_key = 'this is secret_key you know ?'



if __name__ == '__main__':
    # app.run()
    socketio.run(app, allow_unsafe_werkzeug=True,debug=True)
