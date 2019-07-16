import hashlib
import json

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect
from geventwebsocket.websocket import WebSocketError, WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from wtforms import Form

from DBcm import db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
# 设置加密字段
app.secret_key = "chat online"
# 创建csrf对象
# CSRFProtect(app)

# 登录配置，创建LoginManager对象
login_manager = LoginManager()
# 未登录成功，跳到指定的login路由下
login_manager.login_view = "login"
# 与app关联
login_manager.init_app(app)


@app.route('/')
def index():
    # session.clear()
    return render_template('login.html')


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return redirect(url_for('index'))

        if request.method == "POST":
            login_form = LoginForm(formdata=request.form)
            if not login_form.validate():
                for error in login_form.errors:
                    flash(login_form.errors[error][0])
                return redirect(url_for('login'))

            user = db.session.query(User).filter(User.phone == login_form.data['phone']).first()
            if not user:
                flash('用户不存在')
                return redirect(url_for('login'))

            password_hash = hashlib.md5(login_form.data['password'].encode('utf-8')).hexdigest()
            if user.password == password_hash:
                login_user(user)

            return redirect(url_for('chat_online_page'))

    except Exception as e:
        print(e)
        flash('登录失败')
        return redirect(url_for('login'))


# 登录之后，加载user（必须要有）
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 注册
@app.route('/register/', methods=["GET", "POST"])
def register():
    try:
        if request.method == "GET":
            return render_template("register.html")

        if request.method == "POST":
            register_form = RegisterForm(formdata=request.form)
            if register_form.validate():
                user = db.session.query(User).filter(User.phone == register_form.data['phone']).all()
                if user:
                    flash('手机号已存在')
                    return redirect(url_for('register'))
                else:
                    password_hash = hashlib.md5(register_form.data['password'].encode('utf-8')).hexdigest()

                    new_user = User(username=register_form.data['username'], phone=register_form.data['phone'], password=password_hash)
                    db.session.add(new_user)
                    db.session.commit()
                    db.session.close()
                    flash('注册成功')

                    return redirect(url_for('login'))
            else:
                for error in register_form.errors:
                    flash(register_form.errors[error][0])

                return redirect(url_for('register'))
    except Exception as e:
        print(e)
        flash('注册失败')
        return redirect(url_for('register'))


@app.route('/logout/')
@login_required
def logout():
    try:
        if current_user.is_authenticated:
            logout_user()

            return redirect(url_for('login'))
        else:
            flash('出错啦')
            return render_template('500.html')
    except Exception as e:
        print(e)
        flash('退出登录失败')
        return render_template('500.html')


@app.route('/chat-online-page/')
@login_required
def chat_online_page():
    try:
        return render_template('chat.html')
    except Exception as e:
        print(e)
        flash(e)
        return render_template('500.html')


user_socket_dict = dict()


@app.route('/chat-online/')
def chat_online():
    try:
        user_socket = request.environ.get("wsgi.websocket")
        if not user_socket:
            flash('请以WEBSOCKET方式连接')
            return render_template('500.html')

        user = db.session.query(User).filter(User.id == session.user_id).first()
        username = user.username
        user_socket_dict[username] = user_socket

        while True:
            try:
                user_msg = user_socket.receive()
                for user_name, u_socket in user_socket_dict.items():
                    who_send_msg = {
                        "send_user": user_name,
                        "send_msg": user_msg
                    }

                    if user_socket == u_socket:
                        continue
                    user_socket.send(json.dumps(who_send_msg))
            except Exception as e:
                print(e)
                user_socket_dict.pop(username)
    except WebSocketError as e:
        print(e)
        flash(e)
        return render_template('500.html')


if __name__ == '__main__':
    http_serve = WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()
    # app.debug = True
    # app.run()
